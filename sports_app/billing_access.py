"""Sports-owned billing capabilities; no automatic role assignment or ERP grants."""

import frappe
from frappe import _

from sports_app.academy import can_manage_settings, get_configured_settings, validate_company

FINANCE_ROLE = "Sports Finance"
SCHOLARSHIP = "Sports Scholarship Decision"
PLAN = "Sports Fee Plan"
OBLIGATION = "Sports Billing Obligation"
CAPABILITY = object()


def can_read(user=None):
	user = user or frappe.session.user
	return bool(
		user and user != "Guest" and (can_manage_settings(user) or FINANCE_ROLE in frappe.get_roles(user))
	)


def require_billing(manage=False):
	if not (can_manage_settings() if manage else can_read()):
		frappe.throw(_("Sports billing access is required."), frappe.PermissionError)
	settings = get_configured_settings(for_update=True)
	validate_company(settings.company)
	return settings


def has_permission(doc, user=None, ptype=None, **kwargs):
	if not can_read(user):
		return False
	if doc.get("company") and doc.company != get_configured_settings().company:
		return False
	if (
		doc.doctype == SCHOLARSHIP
		and ptype in ("create", "write", "submit", "cancel", "delete")
		and not can_manage_settings(user)
	):
		return False
	return None


def permission_query(user=None, doctype=None):
	if not can_read(user) or doctype not in (SCHOLARSHIP, PLAN, OBLIGATION):
		return "1=0"
	company = get_configured_settings().company
	return f"`tab{doctype}`.`company` = {frappe.db.escape(company)}"


def no_delete(*args, **kwargs):
	frappe.throw(_("Billing and scholarship history cannot be deleted or renamed."), frappe.PermissionError)


def enrollment_record(name):
	doc = frappe.get_doc("Sports Enrollment", name, for_update=True)
	doc.check_permission("read")
	player = frappe.get_doc("Sports Player", doc.player, for_update=True)
	player.check_permission("read")
	settings = require_billing()
	if (
		doc.company != settings.company
		or player.company != doc.company
		or player.customer != doc.payer_customer
	):
		frappe.throw(_("Enrollment, player and academy accounts must belong to the configured company."))
	validate_company(doc.company)
	return doc, player
