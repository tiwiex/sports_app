"""Submit a private application; only authorized staff can read or review it."""

from uuid import uuid4

import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
from frappe.utils import cint, get_datetime, now_datetime, today

from sports_app.players import PLAYER_FIELDS, registration_settings, require_player_access
from sports_app.registration import get_registration_fields
from sports_app.registrations import (
	PUBLIC_FIELDS,
	SERVICE_CAPABILITY,
	acceptance_transaction,
	fingerprint,
	intake_settings,
	pathway_names,
	public_payload,
	request_uuid,
	review_record,
	validate_intake,
)


# Reviewed public endpoint: minimal anonymous bootstrap or rate-limited token-bound enrollment; see tests/build logs.
@frappe.whitelist(  # nosemgrep: frappe-semgrep-rules.rules.security.guest-whitelisted-method
	allow_guest=True, methods=["POST"]
)
@rate_limit(limit=15, seconds=3600, methods=["POST"])
def submit_registration(
	player: str | dict, pathway: str, request_key: str, website: str = "", image_data: str = ""
):
	return _submit_registration(player, pathway, request_key, website, image_data)


def _submit_registration(player, pathway, request_key, website="", image_data=""):
	if website:
		frappe.throw(_("Unable to submit registration."))
	from sports_app.enrollment_images import prepare_image, save_registration_image

	image = prepare_image(image_data)
	key = request_uuid(request_key)
	values = public_payload(player)
	if not isinstance(pathway, str) or pathway not in pathway_names():
		frappe.throw(_("Select a valid program pathway."))
	settings = intake_settings()  # lock order shared with acceptance/player creation
	doc = frappe.get_doc(
		{
			"doctype": "Sports Registration",
			**values,
			"company": settings.company,
			"program": settings.default_program,
			"requested_pathway": pathway,
		}
	)
	if image:
		doc.photo_hash = image["hash"]
	validate_intake(doc)
	digest = fingerprint(doc)
	existing = frappe.db.get_value(
		"Sports Registration", {"request_key": key}, ["name", "request_hash"], as_dict=True, for_update=True
	)
	if existing:
		if existing.request_hash != digest:
			frappe.throw(_("This submission has changed. Reopen the form to submit new details."))
		return {"reference": existing.name}
	doc.flags.sports_registration_service = SERVICE_CAPABILITY
	doc.update(
		{
			"request_key": key,
			"request_hash": digest,
			"acceptance_key": str(uuid4()),
			"submitted_on": now_datetime(),
			"status": "Pending",
		}
	)
	doc.insert(ignore_permissions=True)
	save_registration_image(doc, image)
	# No player/customer/user, private fields or application status in the response.
	return {"reference": doc.name}


# Reviewed: user-requested public email availability only; no account/identity data returned.
@frappe.whitelist(  # nosemgrep: frappe-semgrep-rules.rules.security.guest-whitelisted-method
	allow_guest=True, methods=["POST"]
)
@rate_limit(limit=30, seconds=3600, methods=["POST"])
def check_player_email(email: str, request_key: str):
	from sports_app.enrollment_accounts import normalize_email, player_email_available

	email = normalize_email(email)
	key = request_uuid(request_key)
	# The request token permits unchanged retries of this application only.
	own = frappe.db.exists("Sports Registration", {"request_key": key, "contact_email": email})
	return {"available": bool(own or player_email_available(email))}


@frappe.whitelist()
def list_registrations(
	status: str = "Pending", start: str | int = 0, sort_by: str = "submitted_on", sort_order: str = "desc"
):
	require_player_access()
	if status not in ("Pending", "Accepted", "Rejected"):
		frappe.throw(_("Select a valid registration status."))
	if sort_by not in (
		"name",
		"full_name",
		"requested_pathway",
		"submitted_on",
		"status",
	) or sort_order not in ("asc", "desc"):
		frappe.throw(_("Select a valid registration sort column and direction."))
	rows = frappe.get_list(
		"Sports Registration",
		filters={"status": status},
		fields=["name", "full_name", "requested_pathway", "submitted_on", "status", "player"],
		order_by=f"{sort_by} {sort_order}" + (", name asc" if sort_by != "name" else ""),
		start=max(0, cint(start)),
		page_length=20,
	)
	for row in rows:
		doc = frappe.get_doc("Sports Registration", row.name)
		invoice = enrollment_invoice(doc)
		row.update(
			sales_invoice=invoice.name if invoice else None,
			invoice_workflow=invoice.workflow_state if invoice else None,
		)
		from sports_app.receipt_delivery import can_email

		row["elapsed_seconds"] = (
			max(0, (now_datetime() - get_datetime(doc.submitted_on)).total_seconds())
			if doc.submitted_on
			else None
		)
		payment = frappe.get_doc("Payment Entry", doc.payment_entry) if doc.payment_entry else None
		row["invoice_pdf"] = (
			invoice.name
			if invoice and frappe.get_doc("Sales Invoice", invoice.name).has_permission("read")
			else None
		)
		row["receipt_pdf"] = (
			payment.name
			if payment
			and payment.docstatus == 1
			and payment.company == doc.company
			and payment.get("sports_registration") == doc.name
			and payment.has_permission("read")
			else None
		)
		row["email_receipt"] = (
			payment.name
			if (
				doc.status == "Accepted"
				and doc.player
				and payment
				and can_email(payment)
				and payment.company == doc.company
				and payment.party_type == "Customer"
				and payment.party == frappe.db.get_value("Sports Player", doc.player, "customer")
			)
			else None
		)
		row["can_accept"] = can_accept(doc, invoice)
		row["can_review"] = row.status == "Pending" and doc.has_permission("write")
	return rows


def enrollment_invoice(doc):
	"""Only expose the invoice belonging to this scoped application/company."""
	if not doc.get("sales_invoice"):
		return None
	return frappe.db.get_value(
		"Sales Invoice",
		{"name": doc.sales_invoice, "sports_registration": doc.name, "company": doc.company},
		["name", "workflow_state", "docstatus", "outstanding_amount"],
		as_dict=True,
	)


def can_accept(doc, invoice):
	if doc.status != "Pending" or not doc.has_permission("write"):
		return False
	if not doc.get("sales_invoice"):
		return True
	if not invoice:
		return False
	from sports_app.enrollment_invoices import can_complete_payment

	return bool(
		can_complete_payment()
		and (
			(invoice.docstatus == 0 and invoice.workflow_state == "Pending Review")
			or (invoice.docstatus == 1 and invoice.outstanding_amount == 0 and doc.get("payment_entry"))
		)
	)


@frappe.whitelist()
def get_registration(name: str):
	doc = review_record(name)
	invoice = enrollment_invoice(doc)
	duplicates = frappe.get_list(
		"Sports Player",
		filters={"company": doc.company},
		or_filters=[["full_name", "=", doc.full_name], ["contact_email", "=", doc.contact_email]],
		fields=["name", "full_name", "birth_date"],
		page_length=10,
	)
	return {
		"registration": {
			key: doc.get(key)
			for key in (
				*PUBLIC_FIELDS,
				"name",
				"full_name",
				"company",
				"program",
				"requested_pathway",
				"submitted_on",
				"status",
				"player",
				"rejection_reason",
				"payment_entry",
				"sales_invoice",
				"player_photo",
			)
		},
		"possible_matches": duplicates,
		"fields": get_registration_fields(),
		"can_review": doc.status == "Pending" and doc.has_permission("write"),
		"can_accept": can_accept(doc, invoice),
		"invoice": invoice,
		"payment": frappe.db.get_value(
			"Payment Entry", doc.payment_entry, ["name", "workflow_state", "docstatus"], as_dict=True
		)
		if doc.payment_entry
		else None,
	}


@frappe.whitelist(methods=["POST"])
def accept_registration(name: str, enrollment: str | dict | None = None):
	require_player_access()
	settings = registration_settings(for_update=True)
	doc = review_record(name, write=True)
	if doc.company != settings.company:
		frappe.throw(_("Registration belongs to a different configured academy company."))
	if doc.status == "Accepted":
		return doc.player
	if doc.status != "Pending":
		frappe.throw(_("Only pending registrations can be accepted."))
	from sports_app.players import ENROLLMENT_FIELDS
	from sports_app.players_api import _payload, register_player

	initial = _payload(enrollment or {}, ENROLLMENT_FIELDS)
	initial.setdefault("program", doc.program)
	initial.setdefault("start_date", today())
	values = {key: doc.get(key) for key in PLAYER_FIELDS}
	if values.get("birth_date"):
		values["birth_date"] = str(values["birth_date"])
	from sports_app.registration_origin import registration_origin

	if doc.payment_customer and initial["program"] != doc.program:
		frappe.throw(
			_(
				"A payment draft already fixes the initial program. Review it with Finance before changing programs."
			)
		)
	with acceptance_transaction(), registration_origin(doc):
		from sports_app.players import validate_player_email

		validate_player_email(doc)
		if doc.get("sales_invoice"):
			from sports_app.enrollment_invoices import complete_payment

			complete_payment(doc.sales_invoice)
			doc.reload()
		player = register_player(values, initial, doc.acceptance_key)
		from sports_app.enrollment_images import link_player_image

		link_player_image(doc, player)
		frappe.db.set_value("Sports Player", player, "source_registration", doc.name, update_modified=False)
		doc.flags.sports_registration_service = SERVICE_CAPABILITY
		doc.update(
			{
				"status": "Accepted",
				"player": player,
				"reviewed_by": frappe.session.user,
				"reviewed_on": now_datetime(),
			}
		)
		doc.save()
	return player


@frappe.whitelist(methods=["POST"])
def reject_registration(name: str, reason: str):
	require_player_access()
	registration_settings(for_update=True)
	doc = review_record(name, write=True)
	if not isinstance(reason, str) or not reason.strip() or len(reason) > 1000:
		frappe.throw(_("Enter a rejection reason of up to 1000 characters."))
	if doc.status == "Rejected":
		return doc.name
	if doc.status != "Pending":
		frappe.throw(_("Only pending registrations can be rejected."))
	doc.flags.sports_registration_service = SERVICE_CAPABILITY
	doc.update(
		{
			"status": "Rejected",
			"rejection_reason": reason.strip(),
			"reviewed_by": frappe.session.user,
			"reviewed_on": now_datetime(),
		}
	)
	doc.save()
	return doc.name
