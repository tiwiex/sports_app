"""Submit a private application; only authorized staff can read or review it."""
from uuid import uuid4
import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
from frappe.utils import now_datetime, today, cint
from sports_app.registrations import (SERVICE_CAPABILITY, PUBLIC_FIELDS, public_payload,
    validate_intake, intake_settings, pathway_names, fingerprint, request_uuid,
    review_record, acceptance_transaction)
from sports_app.players import require_player_access, registration_settings, PLAYER_FIELDS
from sports_app.registration import get_registration_fields


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=15, seconds=3600, methods=["POST"])
def submit_registration(player, pathway, request_key, website=""):
    return _submit_registration(player, pathway, request_key, website)


def _submit_registration(player, pathway, request_key, website=""):
    if website:
        frappe.throw(_("Unable to submit registration."))
    key = request_uuid(request_key)
    values = public_payload(player)
    if not isinstance(pathway, str) or pathway not in pathway_names():
        frappe.throw(_("Select a valid program pathway."))
    settings = intake_settings()  # lock order shared with acceptance/player creation
    doc = frappe.get_doc({"doctype": "Sports Registration", **values,
        "company": settings.company, "program": settings.default_program,
        "requested_pathway": pathway})
    validate_intake(doc)
    digest = fingerprint(doc)
    existing = frappe.db.get_value("Sports Registration", {"request_key": key},
        ["name", "request_hash"], as_dict=True, for_update=True)
    if existing:
        if existing.request_hash != digest:
            frappe.throw(_("This submission has changed. Reopen the form to submit new details."))
        return {"reference": existing.name}
    doc.flags.sports_registration_service = SERVICE_CAPABILITY
    doc.update({"request_key": key, "request_hash": digest, "acceptance_key": str(uuid4()),
        "submitted_on": now_datetime(), "status": "Pending"})
    doc.insert(ignore_permissions=True)
    # No player/customer/user, private fields or application status in the response.
    return {"reference": doc.name}


@frappe.whitelist()
def list_registrations(status="Pending", start=0):
    require_player_access()
    if status not in ("Pending", "Accepted", "Rejected"):
        frappe.throw(_("Select a valid registration status."))
    return frappe.get_list("Sports Registration", filters={"status": status},
        fields=["name", "full_name", "requested_pathway", "submitted_on", "status", "player"],
        order_by="submitted_on desc", start=max(0, cint(start)), page_length=20)


@frappe.whitelist()
def get_registration(name):
    doc = review_record(name)
    duplicates = frappe.get_list("Sports Player", filters={"company": doc.company},
        or_filters=[["full_name", "=", doc.full_name], ["contact_email", "=", doc.contact_email]],
        fields=["name", "full_name", "birth_date"], page_length=10)
    return {"registration": {key: doc.get(key) for key in (*PUBLIC_FIELDS, "name", "full_name",
        "company", "program", "requested_pathway", "submitted_on", "status", "player", "rejection_reason", "payment_entry", "sales_invoice") },
        "possible_matches": duplicates, "fields": get_registration_fields(),
        "invoice": frappe.db.get_value("Sales Invoice", doc.sales_invoice, ["name", "workflow_state", "docstatus", "outstanding_amount"], as_dict=True) if doc.get("sales_invoice") else None,
        "payment": frappe.db.get_value("Payment Entry", doc.payment_entry, ["name", "workflow_state", "docstatus"], as_dict=True) if doc.payment_entry else None}


@frappe.whitelist(methods=["POST"])
def accept_registration(name, enrollment=None):
    require_player_access()
    settings = registration_settings(for_update=True)
    doc = review_record(name, write=True)
    if doc.company != settings.company:
        frappe.throw(_("Registration belongs to a different configured academy company."))
    if doc.status == "Accepted":
        return doc.player
    if doc.status != "Pending":
        frappe.throw(_("Only pending registrations can be accepted."))
    from sports_app.players_api import register_player, _payload
    from sports_app.players import ENROLLMENT_FIELDS
    initial = _payload(enrollment or {}, ENROLLMENT_FIELDS)
    initial.setdefault("program", doc.program)
    initial.setdefault("start_date", today())
    values = {key: doc.get(key) for key in PLAYER_FIELDS}
    if values.get("birth_date"):
        values["birth_date"] = str(values["birth_date"])
    from sports_app.registration_origin import registration_origin
    if doc.payment_customer and initial["program"] != doc.program:
        frappe.throw(_("A payment draft already fixes the initial program. Review it with Finance before changing programs."))
    with acceptance_transaction(), registration_origin(doc):
        player = register_player(values, initial, doc.acceptance_key)
        frappe.db.set_value("Sports Player", player, "source_registration", doc.name, update_modified=False)
        doc.flags.sports_registration_service = SERVICE_CAPABILITY
        doc.update({"status": "Accepted", "player": player, "reviewed_by": frappe.session.user,
            "reviewed_on": now_datetime()})
        doc.save()
    return player


@frappe.whitelist(methods=["POST"])
def reject_registration(name, reason):
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
    doc.update({"status": "Rejected", "rejection_reason": reason.strip(),
        "reviewed_by": frappe.session.user, "reviewed_on": now_datetime()})
    doc.save()
    return doc.name
