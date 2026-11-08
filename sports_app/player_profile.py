"""Bounded, read-only linked player histories and controlled profile observations."""

import hashlib
import json
import math
from uuid import UUID

import frappe
from frappe import _
from frappe.model import get_permitted_fields
from frappe.utils import get_datetime, getdate, now_datetime

from sports_app.academy import (
	can_manage_settings,
	get_configured_settings,
	require_settings_access,
	validate_company,
)
from sports_app.player_numbering import academy_date
from sports_app.players import require_player_access

PAGE_SIZE = 20
CAPABILITY = object()
MEASUREMENT = "Sports Player Measurement"
DOCUMENT = "Sports Player Document"
FOOT = ("", "Left", "Right", "Both", "Not specified")
SECTIONS = {
	"invoices": (
		"Sales Invoice",
		[
			"name",
			"posting_date",
			"creation",
			"due_date",
			"currency",
			"grand_total",
			"outstanding_amount",
			"status",
			"docstatus",
		],
	),
	"receipts": (
		"Payment Entry",
		[
			"name",
			"posting_date",
			"creation",
			"payment_type",
			"paid_amount",
			"paid_from_account_currency",
			"received_amount",
			"paid_to_account_currency",
			"reference_no",
			"docstatus",
		],
	),
	"attendance": ("Sports Attendance", ["name", "session", "status", "source", "marked_on"]),
	"biometrics": (
		"Sports Biometric Enrollment",
		["name", "status", "finger", "prepared_on", "demo_reference"],
	),
	"measurements": (MEASUREMENT, ["name", "assessed_on", "height_cm", "weight_kg", "recorded_by"]),
	"documents": (DOCUMENT, ["name", "title", "document_type", "document_date", "recorded_on"]),
}


def player_record(name, write=False):
	require_player_access()
	if write:
		# Serialize new linked records with admission, import and ID correction.
		get_configured_settings(for_update=True)
	doc = frappe.get_doc("Sports Player", name, for_update=write)
	doc.check_permission("write" if write else "read")
	validate_company(doc.company)
	return doc


def today():
	settings = get_configured_settings()
	return academy_date(frappe._dict(timezone=settings.timezone or "UTC"))


def available(player, section):
	doctype, fields = SECTIONS[section]
	if section in ("documents", "biometrics") and not can_manage_settings():
		return False
	if not frappe.has_permission(doctype, "read") or not set(fields) <= set(
		get_permitted_fields(doctype, permission_type="read")
	):
		return False
	if section in ("invoices", "receipts"):
		if not player.customer:
			return True  # Empty linked account is not an invented financial balance.
		return frappe.get_doc("Customer", player.customer).has_permission("read")
	if section == "attendance" and not frappe.has_permission("Sports Session", "read"):
		return False
	return True


def private_file(doctype, name, fieldname=None):
	filters = dict(attached_to_doctype=doctype, attached_to_name=name, is_private=1)
	if fieldname:
		filters["attached_to_field"] = fieldname
	file_name = frappe.db.get_value("File", filters, "name")
	if not file_name:
		return None
	doc = frappe.get_doc("File", file_name)
	if doc.has_permission("read") and str(doc.file_url or "").startswith("/private/files/"):
		return doc.file_url
	return None


@frappe.whitelist()
def overview(name: str):
	player = player_record(name)
	on = today()
	birth = getdate(player.birth_date) if player.birth_date else None
	permitted = set(get_permitted_fields("Sports Player", permission_type="read"))
	capabilities = {section: bool(available(player, section)) for section in SECTIONS}
	summary = None
	if capabilities["invoices"] and player.customer:
		summary = frappe.get_list(
			"Sales Invoice",
			filters={"company": player.company, "customer": player.customer, "docstatus": 1},
			fields=["currency", "sum(outstanding_amount) as outstanding"],
			group_by="currency",
			order_by="currency",
			page_length=0,
		)
	return dict(
		age=on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))
		if birth and "birth_date" in permitted
		else None,
		preferred_foot=player.get("preferred_foot") if "preferred_foot" in permitted else None,
		portrait=private_file("Sports Player", player.name, "player_photo")
		if "player_photo" in permitted
		else None,
		today=str(on),
		modified=str(player.modified),
		available=capabilities,
		can_edit_foot=bool(
			player.has_permission("write")
			and "preferred_foot" in get_permitted_fields("Sports Player", permission_type="write")
		),
		can_add_measurement=bool(
			player.has_permission("write") and frappe.has_permission(MEASUREMENT, "create")
		),
		can_add_document=bool(
			player.has_permission("write")
			and can_manage_settings()
			and frappe.has_permission(DOCUMENT, "create")
		),
		outstanding=summary,
	)


@frappe.whitelist()
def history(name: str, section: str, start: str | int = 0):
	player = player_record(name)
	if section not in SECTIONS:
		frappe.throw(_("Select a valid player history section."))
	if str(start) != "0" and (not str(start).isdigit() or len(str(start)) > 7):
		frappe.throw(_("Select a valid history page."))
	offset = int(start)
	if not available(player, section):
		frappe.throw(_("You do not have access to this player history."), frappe.PermissionError)
	if section in ("invoices", "receipts") and not player.customer:
		return dict(rows=[], has_more=False)
	doctype, fields = SECTIONS[section]
	filters = {"company": player.company, "player": player.name}
	if section == "invoices":
		filters = {"company": player.company, "customer": player.customer}
	elif section == "receipts":
		filters = {"company": player.company, "party_type": "Customer", "party": player.customer}
	rows = frappe.get_list(
		doctype,
		filters=filters,
		fields=fields,
		order_by="creation desc, name desc",
		start=offset,
		page_length=PAGE_SIZE + 1,
	)
	more = len(rows) > PAGE_SIZE
	rows = rows[:PAGE_SIZE]
	if section in ("invoices", "receipts"):
		from sports_app.receipt_delivery import can_email

		for row in rows:
			row["elapsed_seconds"] = (
				max(0, (now_datetime() - get_datetime(row.creation)).total_seconds())
				if row.creation
				else None
			)
			if section == "receipts":
				row["can_email_receipt"] = can_email(frappe.get_doc("Payment Entry", row.name))
	if section == "attendance":
		sessions = (
			{
				r.name: r
				for r in frappe.get_list(
					"Sports Session",
					filters={"company": player.company, "name": ["in", list({r.session for r in rows})]},
					fields=["name", "title", "session_date", "status"],
					page_length=PAGE_SIZE,
				)
			}
			if rows
			else {}
		)
		for row in rows:
			session = sessions.get(row.session)
			row.update(
				session=session.name if session else None,
				session_title=session.title if session else None,
				session_date=session.session_date if session else None,
				session_status=session.status if session else None,
			)
	if section == "documents":
		for row in rows:
			row["file_url"] = private_file(DOCUMENT, row.name)
	return dict(rows=rows, has_more=more)


@frappe.whitelist(methods=["POST"])
def save_preferred_foot(name: str, preferred_foot: str, modified: str):
	player = player_record(name, write=True)
	if preferred_foot not in FOOT:
		frappe.throw(_("Select Left, Right, Both or Not specified."))
	if str(player.modified) != str(modified):
		frappe.throw(_("Player changed. Refresh before saving."), frappe.TimestampMismatchError)
	if "preferred_foot" not in get_permitted_fields("Sports Player", permission_type="write"):
		frappe.throw(_("You cannot edit the preferred foot."), frappe.PermissionError)
	player.preferred_foot = preferred_foot
	player.save()
	return str(player.modified)


def request_identity(key, payload):
	try:
		if str(UUID(key, version=4)) != key:
			raise ValueError
	except (ValueError, TypeError, AttributeError):
		frappe.throw(_("Invalid profile request. Refresh and retry."))
	return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def positive_number(value):
	if value in (None, ""):
		return None
	try:
		number = float(value)
	except (ValueError, TypeError):
		frappe.throw(_("Measurements must be positive numbers."))
	if isinstance(value, bool) or not math.isfinite(number) or number <= 0 or number >= 1e10:
		frappe.throw(_("Measurements must be positive finite numbers below 10000000000."))
	rounded = round(number, 2)
	if rounded <= 0:
		frappe.throw(_("Measurements must be at least 0.01 cm or kg."))
	return rounded


def check_record(doc):
	if doc.doctype == DOCUMENT:
		require_settings_access()
	parent = player_record(doc.player, write=True)
	if (
		doc.company != parent.company
		or doc.flags.player_profile_service is not CAPABILITY
		or not (doc.is_new() or (doc.doctype == DOCUMENT and doc.docstatus == 1 and doc._action == "submit"))
	):
		frappe.throw(
			_(
				"Use the player profile to add a new historical record. Existing records cannot be overwritten."
			),
			frappe.PermissionError,
		)
	if doc.doctype == MEASUREMENT:
		on = getdate(doc.assessed_on)
		if not doc.assessed_on or on > today() or (parent.birth_date and on < getdate(parent.birth_date)):
			frappe.throw(_("Choose a measurement date between the player's birth and today."))
		doc.height_cm = positive_number(doc.height_cm)
		doc.weight_kg = positive_number(doc.weight_kg)
		if doc.height_cm is None and doc.weight_kg is None:
			frappe.throw(_("Enter a height or weight measurement."))
	else:
		if doc.docstatus == 1 and not doc.file_url:
			frappe.throw(_("A private supporting file is required before archiving the document."))
		if (
			doc.document_type not in ("Birth certificate", "Medical report", "Other")
			or not str(doc.title or "").strip()
			or len(doc.title) > 140
		):
			frappe.throw(_("Enter a document title and valid document type."))
		if doc.document_date and getdate(doc.document_date) > today():
			frappe.throw(_("Document date cannot be in the future."))


def prevent_delete(*args, **kwargs):
	frappe.throw(
		_("Player history records are retained for audit and cannot be deleted or renamed."),
		frappe.PermissionError,
	)


@frappe.whitelist(methods=["POST"])
def add_measurement(
	name: str,
	assessed_on: str,
	request_key: str,
	height_cm: str | float | None = None,
	weight_kg: str | float | None = None,
):
	player = player_record(name, write=True)
	values = dict(
		player=player.name,
		assessed_on=str(getdate(assessed_on)) if assessed_on else None,
		height_cm=positive_number(height_cm),
		weight_kg=positive_number(weight_kg),
	)
	digest = request_identity(request_key, values)
	old = frappe.db.get_value(
		MEASUREMENT,
		{"request_key": request_key},
		["name", "request_hash", "player"],
		as_dict=True,
		for_update=True,
	)
	if old:
		frappe.get_doc(MEASUREMENT, old.name).check_permission("read")
		if old.player != name or old.request_hash != digest:
			frappe.throw(_("This measurement request already contains different details."))
		return old.name
	doc = frappe.get_doc(
		doctype=MEASUREMENT,
		**values,
		company=player.company,
		recorded_by=frappe.session.user,
		request_key=request_key,
		request_hash=digest,
	)
	doc.flags.player_profile_service = CAPABILITY
	doc.insert()
	return doc.name
