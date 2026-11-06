"""Authenticated, bounded player operations; no guest listing or accounting bypass."""

import hashlib
import json
from uuid import UUID

import frappe
from frappe import _
from frappe.utils import CallbackManager, cint

from sports_app.academy import validate_company
from sports_app.player_ids import can_change
from sports_app.players import (
	ENROLLMENT_FIELDS,
	PLAYER_FIELDS,
	is_eligible,
	registration_settings,
	require_player_access,
)
from sports_app.registration import get_registration_fields


def _payload(value, fields):
	value = frappe.parse_json(value)
	if not isinstance(value, dict) or set(value) - set(fields):
		frappe.throw(_("Invalid player or enrollment fields."))
	return value


def _page(value):
	return max(0, cint(value))


@frappe.whitelist()
def get_registration_defaults():
	require_player_access()
	settings = registration_settings()
	return {
		**{
			key: settings.get(key)
			for key in ("company", "default_program", "default_group", "default_enrollment_status")
		},
		"player_fields": get_registration_fields(),
	}


@frappe.whitelist()
def list_players(
	search: str = "", start: str | int = 0, sort_by: str = "registered_on", sort_order: str = "desc"
):
	require_player_access()
	if sort_by not in ("name", "full_name", "birth_date", "company", "registered_on") or sort_order not in (
		"asc",
		"desc",
	):
		frappe.throw(_("Select a valid player sort column and direction."))
	text = str(search or "").strip()[:100]
	rows = frappe.get_list(
		"Sports Player",
		fields=["name", "full_name", "birth_date", "company", "registered_on"],
		or_filters=[["name", "like", "%" + text + "%"], ["full_name", "like", "%" + text + "%"]]
		if text
		else None,
		order_by=f"{sort_by} {sort_order}" + (", name asc" if sort_by != "name" else ""),
		start=_page(start),
		page_length=20,
	)
	for row in rows:
		can_create_enrollment = frappe.has_permission("Sports Enrollment", "create")
		row["can_change_id"] = can_change(frappe.get_doc("Sports Player", row.name))
		row["can_enroll"] = bool(
			can_create_enrollment and frappe.get_doc("Sports Player", row.name).has_permission("write")
		)
	return rows


@frappe.whitelist()
def get_player(name: str, start: str | int = 0):
	require_player_access()
	doc = frappe.get_doc("Sports Player", name)
	doc.check_permission("read")
	validate_company(doc.company)
	enrollments = frappe.get_list(
		"Sports Enrollment",
		filters={"player": name},
		fields=["name", "program", "group", "payer_customer", "start_date", "end_date", "status"],
		order_by="start_date desc, creation desc",
		start=_page(start),
		page_length=20,
	)
	for doctype, field, title in (
		("Sports Program", "program", "program_name"),
		("Sports Group", "group", "group_name"),
	):
		names = list({row[field] for row in enrollments if row[field]})
		labels = (
			{
				row.name: row[title]
				for row in frappe.get_list(
					doctype, filters={"name": ["in", names]}, fields=["name", title], page_length=20
				)
			}
			if names
			else {}
		)
		for row in enrollments:
			row[title] = labels.get(row[field], row[field])
	for row in enrollments:
		row["eligible_today"] = is_eligible(row, frappe.utils.today())
	return {
		"player": {
			key: doc.get(key)
			for key in (
				"name",
				"company",
				"registered_on",
				"modified",
				"customer",
				"portal_user",
				"guardian_user",
				*PLAYER_FIELDS,
			)
		},
		"enrollments": enrollments,
		"fields": get_registration_fields(),
		"can_change_id": can_change(doc),
		"can_enroll": bool(
			doc.has_permission("write") and frappe.has_permission("Sports Enrollment", "create")
		),
	}


@frappe.whitelist(methods=["POST"])
def register_player(player: str | dict, enrollment: str | dict, request_key: str):
	require_player_access()
	values = _payload(player, PLAYER_FIELDS)
	initial = _payload(enrollment, ENROLLMENT_FIELDS)
	try:
		if str(UUID(str(request_key), version=4)) != str(request_key):
			raise ValueError
	except (ValueError, TypeError, AttributeError):
		frappe.throw(_("Invalid registration request. Refresh and retry."))
	fingerprint = hashlib.sha256(
		json.dumps([values, initial], sort_keys=True, separators=(",", ":")).encode()
	).hexdigest()
	# Lock saved settings for the whole transaction using current reads. Concurrent
	# retries see the committed player before allocating another ID.
	settings = registration_settings(for_update=True)
	existing = frappe.db.get_value(
		"Sports Player", {"request_key": request_key}, ["name", "request_hash"], as_dict=True, for_update=True
	)
	if existing:
		doc = frappe.get_doc("Sports Player", existing.name, for_update=True)
		doc.check_permission("read")
		validate_company(doc.company)
		if existing.request_hash != fingerprint:
			frappe.throw(_("This registration request was already used with different details."))
		return existing.name
	initial.setdefault("program", settings.default_program)
	initial.setdefault(
		"group", settings.default_group if initial["program"] == settings.default_program else None
	)
	initial.setdefault("status", settings.default_enrollment_status)
	frappe.db.savepoint("sports_registration")
	original_after_commit = frappe.db.after_commit
	registration_callbacks = CallbackManager()
	frappe.db.after_commit = registration_callbacks
	try:
		doc = frappe.get_doc(
			{
				"doctype": "Sports Player",
				**values,
				"company": settings.company,
				"request_key": request_key,
				"request_hash": fingerprint,
				"registration_program": initial["program"],
			}
		).insert()
		frappe.get_doc(
			{
				"doctype": "Sports Enrollment",
				**initial,
				"player": doc.name,
				"company": settings.company,
				"payer_customer": doc.customer,
			}
		).insert()
	except Exception:
		registration_callbacks.reset()
		frappe.db.rollback(save_point="sports_registration")
		raise
	else:
		original_after_commit.add(registration_callbacks.run)
	finally:
		frappe.db.after_commit = original_after_commit
	return doc.name


@frappe.whitelist(methods=["POST"])
def save_player(name: str, player: str | dict, modified: str):
	require_player_access()
	doc = frappe.get_doc("Sports Player", name)
	doc.check_permission("write")
	if str(doc.modified) != str(modified):
		frappe.throw(_("Player changed. Refresh before saving."), frappe.TimestampMismatchError)
	doc.update(_payload(player, PLAYER_FIELDS))
	doc.save()
	return doc.name


@frappe.whitelist(methods=["POST"])
def save_enrollment(
	player: str, enrollment: str | dict, name: str | None = None, modified: str | None = None
):
	require_player_access()
	parent = frappe.get_doc("Sports Player", player)
	parent.check_permission("write")
	validate_company(parent.company)
	doc = frappe.get_doc("Sports Enrollment", name) if name else frappe.new_doc("Sports Enrollment")
	if name:
		doc.check_permission("write")
		if doc.player != player:
			frappe.throw(_("Enrollment belongs to another player."), frappe.PermissionError)
		if str(doc.modified) != str(modified):
			frappe.throw(_("Enrollment changed. Refresh before saving."), frappe.TimestampMismatchError)
	doc.update(_payload(enrollment, ENROLLMENT_FIELDS))
	doc.player = player
	doc.payer_customer = parent.customer
	doc.company = parent.company
	doc.save()
	return doc.name
