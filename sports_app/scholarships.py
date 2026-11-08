"""Restricted effective-dated decisions; no invoice mutation or payment-free admission."""

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime

from sports_app.billing_access import SCHOLARSHIP, enrollment_record, require_billing
from sports_app.billing_policy import money, overlap


def validate(doc):
	settings = require_billing(manage=True)
	if doc.is_new() and doc.docstatus != 0:
		frappe.throw(_("Save a draft decision before approval."))
	enrollment, player = enrollment_record(doc.enrollment)
	if doc.company != settings.company or doc.company != enrollment.company:
		frappe.throw(_("Select the configured academy company."))
	doc.player = player.name
	old = doc.get_doc_before_save()
	if old and (doc.enrollment != old.enrollment or doc.company != old.company):
		frappe.throw(_("Decision identity cannot change."))
	if old and old.docstatus == 1:
		keys = (
			"effective_from",
			"effective_to",
			"coverage_type",
			"coverage_value",
			"reason",
			"kit_benefit",
			"trip_benefit",
			"trial_benefit",
			"tournament_benefit",
			"approved_by",
			"approved_on",
		)
		if doc._action != "cancel" or any(str(doc.get(k) or "") != str(old.get(k) or "") for k in keys):
			frappe.throw(_("Approved decisions are immutable. Revoke and create a new decision."))
	if not doc.effective_from or (
		doc.effective_to and getdate(doc.effective_to) < getdate(doc.effective_from)
	):
		frappe.throw(_("Choose valid effective dates."))
	if not str(doc.reason or "").strip():
		frappe.throw(_("Record a confidential reason for the decision."))
	if doc.coverage_type not in ("Full", "Percentage", "Fixed amount"):
		frappe.throw(_("Choose valid fee coverage."))
	doc.coverage_value = 100 if doc.coverage_type == "Full" else money(doc.coverage_value)
	if doc.coverage_type != "Full" and (
		not doc.coverage_value or (doc.coverage_type == "Percentage" and doc.coverage_value > 100)
	):
		frappe.throw(_("Enter a positive concession; percentages cannot exceed 100."))
	if doc.docstatus == 0:
		doc.approved_by = doc.approved_on = doc.revoked_by = doc.revoked_on = None
		doc.revocation_reason = None


def approve(doc):
	validate(doc)
	for other in frappe.get_all(
		SCHOLARSHIP,
		filters={
			"enrollment": doc.enrollment,
			"company": doc.company,
			"docstatus": 1,
			"name": ["!=", doc.name],
		},
		fields=["effective_from", "effective_to"],
	):
		if overlap(doc.effective_from, doc.effective_to, other.effective_from, other.effective_to):
			frappe.throw(_("Approved concessions for the same enrollment cannot overlap."))
	doc.approved_by = frappe.session.user
	doc.approved_on = now_datetime()


def revoke(doc):
	validate(doc)
	require_billing(manage=True)
	if not str(doc.revocation_reason or "").strip():
		frappe.throw(_("Record a reason before revoking this decision."))
	doc.revoked_by = frappe.session.user
	doc.revoked_on = now_datetime()


@frappe.whitelist(methods=["POST"])
def create(values: str | dict):
	settings = require_billing(manage=True)
	values = frappe.parse_json(values)
	allowed = {
		"enrollment",
		"effective_from",
		"effective_to",
		"coverage_type",
		"coverage_value",
		"reason",
		"kit_benefit",
		"trip_benefit",
		"trial_benefit",
		"tournament_benefit",
	}
	if not isinstance(values, dict) or set(values) - allowed:
		frappe.throw(_("Invalid decision fields."))
	doc = frappe.get_doc(doctype=SCHOLARSHIP, company=settings.company, **values)
	doc.insert()
	return doc.name


@frappe.whitelist(methods=["POST"])
def transition(name: str, action: str, modified: str, reason: str = ""):
	require_billing(manage=True)
	doc = frappe.get_doc(SCHOLARSHIP, name, for_update=True)
	doc.check_permission("write")
	if str(doc.modified) != str(modified):
		frappe.throw(_("Decision changed. Reload before continuing."), frappe.TimestampMismatchError)
	if action == "Approve" and doc.docstatus == 0:
		doc.submit()
	elif action == "Revoke" and doc.docstatus == 1:
		doc.revocation_reason = reason
		doc.cancel()
	else:
		frappe.throw(_("This decision cannot make the requested transition."))
	return doc.name
