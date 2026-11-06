"""Consent/preparation only. No scanner, templates, matching or enrolled state."""

import hashlib
import json
import re
import secrets
from html import escape

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime

from sports_app.academy import can_manage_settings, get_configured_settings, validate_company
from sports_app.registrations import request_uuid

CAPABILITY = object()
DOCTYPE = "Sports Biometric Enrollment"
FINGERS = ("Right thumb", "Left thumb", "Right index", "Left index")
CONSENT_FIELDS = ("finger", "consent_by", "relationship", "notice_reference", "consent_date")


def lock_identity_changes():
	get_configured_settings(for_update=True)


def require_access():
	if not can_manage_settings():
		frappe.throw(_("Biometric preparation requires an academy administrator."), frappe.PermissionError)


def player_record(name, lock=False):
	require_access()
	settings = get_configured_settings()
	validate_company(settings.company)
	player = frappe.get_doc("Sports Player", name, for_update=lock)
	player.check_permission("read")
	if player.company != settings.company:
		frappe.throw(_("Player belongs to another academy."), frappe.PermissionError)
	return player


def validate_values(values):
	if not isinstance(values, dict) or set(values) != set(CONSENT_FIELDS):
		frappe.throw(_("Supply only the fingerprint preparation and consent fields."))
	if any(not isinstance(v, str) or not v.strip() or len(v) > 140 for v in values.values()):
		frappe.throw(_("Complete the consent details, up to 140 characters per field."))
	result = {k: v.strip() for k, v in values.items()}
	if result["finger"] not in FINGERS or result["relationship"] not in ("Player", "Parent / Guardian"):
		frappe.throw(_("Select the finger and consent relationship."))
	from datetime import datetime
	from zoneinfo import ZoneInfo

	if getdate(result["consent_date"]) > datetime.now(ZoneInfo(get_configured_settings().timezone)).date():
		frappe.throw(_("Consent date cannot be in the future."))
	result["consent_date"] = str(getdate(result["consent_date"]))
	return result


def validate_document(doc):
	require_access()
	if doc.flags.sports_biometric_preparation is not CAPABILITY:
		frappe.throw(_("Use Fingerprint registration in the attendance app."), frappe.PermissionError)
	player = player_record(doc.player)
	if doc.company != player.company or doc.status not in ("Pending capture", "Withdrawn"):
		frappe.throw(_("Only pending capture or withdrawal is supported without a scanner."))
	previous = doc.get_doc_before_save()
	if previous and any(
		str(previous.get(k) or "") != str(doc.get(k) or "")
		for k in (
			*CONSENT_FIELDS,
			"player",
			"company",
			"request_key",
			"request_hash",
			"prepared_by",
			"prepared_on",
		)
	):
		frappe.throw(
			_(
				"Preparation identity and recorded consent cannot be edited. Withdraw and prepare a new record."
			)
		)
	if doc.status == "Withdrawn" and not (doc.withdrawal_reason or "").strip():
		frappe.throw(_("A withdrawal reason is required."))
	if doc.get("demo_reference"):
		if (
			not re.fullmatch(r"DEMO-\d{20}", doc.demo_reference)
			or not doc.get("demo_generated_by")
			or not doc.get("demo_generated_on")
		):
			frappe.throw(_("Invalid simulated capture metadata."))
	if (
		previous
		and previous.get("demo_reference")
		and any(
			str(previous.get(k) or "") != str(doc.get(k) or "")
			for k in ("demo_reference", "demo_generated_by", "demo_generated_on")
		)
	):
		frappe.throw(_("The simulated reference cannot be changed or removed."))


def public_record(doc):
	return {
		k: doc.get(k)
		for k in (
			"name",
			"player",
			"status",
			"finger",
			"consent_by",
			"relationship",
			"notice_reference",
			"consent_date",
			"prepared_by",
			"prepared_on",
			"withdrawal_reason",
			"demo_reference",
			"demo_generated_by",
			"demo_generated_on",
		)
	}


@frappe.whitelist()
def search_players(search: str = ""):
	require_access()
	settings = get_configured_settings()
	validate_company(settings.company)
	if not isinstance(search, str) or len(search) > 140:
		frappe.throw(_("Invalid search."))
	return frappe.get_list(
		"Sports Player",
		filters={"company": settings.company},
		or_filters=[["name", "like", f"%{search}%"], ["full_name", "like", f"%{search}%"]]
		if search
		else None,
		fields=["name", "full_name"],
		order_by="full_name asc, name asc",
		page_length=20,
	)


@frappe.whitelist()
def list_player_statuses(search: str = "", start: str | int = 0):
	require_access()
	from frappe.utils import cint

	settings = get_configured_settings()
	validate_company(settings.company)
	if not isinstance(search, str) or len(search) > 140:
		frappe.throw(_("Invalid search."))
	players = frappe.get_list(
		"Sports Player",
		filters={"company": settings.company},
		or_filters=[["name", "like", f"%{search}%"], ["full_name", "like", f"%{search}%"]]
		if search
		else None,
		fields=["name", "full_name"],
		order_by="full_name asc, name asc",
		start=max(0, cint(start)),
		page_length=21,
	)
	page = players[:20]
	latest = {}
	if page:
		entries = frappe.get_list(
			DOCTYPE,
			filters={"company": settings.company, "player": ["in", [p.name for p in page]]},
			fields=["name", "player", "status", "finger", "prepared_on", "demo_reference"],
			order_by="creation desc, name desc",
			page_length=0,
		)
		for entry in entries:
			latest.setdefault(entry.player, entry)
	rows = []
	for player in page:
		entry = latest.get(player.name)
		rows.append(
			dict(
				name=player.name,
				full_name=player.full_name,
				fingerprint_status=entry.status if entry else "Not prepared",
				finger=entry.finger if entry else "",
				request_name=entry.name if entry else "",
				prepared_on=entry.prepared_on if entry else None,
				demo_reference=entry.get("demo_reference") if entry else None,
			)
		)
	return dict(rows=rows, has_more=len(players) > 20)


@frappe.whitelist()
def records(player: str):
	player_record(player)
	return frappe.get_list(
		DOCTYPE,
		filters={"player": player},
		fields=[
			"name",
			"status",
			"finger",
			"consent_by",
			"relationship",
			"notice_reference",
			"consent_date",
			"prepared_by",
			"prepared_on",
			"withdrawal_reason",
			"demo_reference",
			"demo_generated_by",
			"demo_generated_on",
		],
		order_by="creation desc",
		page_length=20,
	)


@frappe.whitelist(methods=["POST"])
def prepare(player: str, values: str | dict, consent_confirmed: str | int | bool, request_key: str):
	require_access()
	lock_identity_changes()
	player = player_record(player, lock=True)
	if consent_confirmed not in (1, "1", True):
		frappe.throw(_("Confirm only consent actually supplied for biometric registration."))
	values = validate_values(frappe.parse_json(values))
	key = request_uuid(request_key)
	digest = hashlib.sha256(json.dumps([player.name, values], sort_keys=True).encode()).hexdigest()
	existing = frappe.db.get_value(DOCTYPE, {"request_key": key}, "name")
	if existing:
		doc = frappe.get_doc(DOCTYPE, existing)
		doc.check_permission("read")
		if doc.player != player.name or doc.company != player.company or doc.request_hash != digest:
			frappe.throw(_("The retried preparation changed. Use the original details."))
		return public_record(doc)
	if frappe.db.exists(DOCTYPE, {"player": player.name, "status": "Pending capture"}):
		frappe.throw(_("This player already has a pending capture request. Review or withdraw it first."))
	doc = frappe.get_doc(
		doctype=DOCTYPE,
		player=player.name,
		company=player.company,
		status="Pending capture",
		**values,
		request_key=key,
		request_hash=digest,
		prepared_by=frappe.session.user,
		prepared_on=now_datetime(),
	)
	doc.flags.sports_biometric_preparation = CAPABILITY
	doc.insert()
	return public_record(doc)


@frappe.whitelist(methods=["POST"])
def demo_capture(name: str):
	require_access()
	lock_identity_changes()
	doc = frappe.get_doc(DOCTYPE, name, for_update=True)
	doc.check_permission("write")
	player_record(doc.player)
	if doc.status != "Pending capture":
		frappe.throw(_("Only a pending preparation can receive a simulated capture."))
	if doc.get("demo_reference"):
		return public_record(doc)
	doc.flags.sports_biometric_preparation = CAPABILITY
	doc.update(
		dict(
			demo_reference=f"DEMO-{secrets.randbelow(10**20):020d}",
			demo_generated_by=frappe.session.user,
			demo_generated_on=now_datetime(),
		)
	)
	doc.save()
	doc.add_comment(
		"Comment",
		_(
			"Demo capture generated a random barcode reference. No fingerprint was captured. Not an authentication or attendance credential."
		),
	)
	return public_record(doc)


@frappe.whitelist(methods=["POST"])
def withdraw(name: str, reason: str):
	require_access()
	lock_identity_changes()
	if not isinstance(reason, str) or not reason.strip() or len(reason) > 1000:
		frappe.throw(_("Supply a withdrawal reason, up to 1000 characters."))
	doc = frappe.get_doc(DOCTYPE, name, for_update=True)
	doc.check_permission("write")
	player_record(doc.player)
	if doc.status == "Withdrawn":
		return public_record(doc)
	doc.flags.sports_biometric_preparation = CAPABILITY
	doc.update(dict(status="Withdrawn", withdrawal_reason=reason.strip()))
	doc.save()
	doc.add_comment(
		"Comment", _("Pending biometric preparation withdrawn: {0}").format(escape(reason.strip()))
	)
	return public_record(doc)
