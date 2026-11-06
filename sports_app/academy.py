"""Academy configuration policies shared by DocTypes and console endpoints."""

import re

import frappe
import pytz
from frappe import _
from frappe.utils import cint, flt

SETTINGS_ROLE = "Sports Academy Administrator"
SETTINGS_FIELDS = (
	"academy_name",
	"company",
	"currency",
	"timezone",
	"registration_prefix",
	"registration_digits",
	"default_enrollment_status",
	"default_program",
	"default_group",
	"monthly_fees_enabled",
	"default_monthly_fee",
	"enrollment_payments_enabled",
	"enrollment_payment_currency",
	"enrollment_registration_fee",
	"enrollment_jersey_fee",
	"enrollment_monthly_fee",
	"enrollment_bank_account",
	"enrollment_receivable_account",
	"enrollment_registration_item",
	"enrollment_jersey_item",
	"payment_review_emails",
)


def can_manage_settings(user=None):
	user = user or frappe.session.user
	return bool(
		user
		and user != "Guest"
		and (
			user == "Administrator" or {SETTINGS_ROLE, "System Manager"}.intersection(frappe.get_roles(user))
		)
	)


def require_settings_access():
	if not can_manage_settings():
		frappe.throw(
			_("Academy configuration requires the Sports Academy Administrator role."), frappe.PermissionError
		)


def validate_company(company):
	if not company:
		frappe.throw(_("Select a company for the academy."))
	doc = frappe.get_doc("Company", company)
	if not frappe.has_permission("Company", "read", doc=doc):
		frappe.throw(_("You do not have access to the selected company."), frappe.PermissionError)
	return doc


def validate_settings_values(values):
	"""Validate reusable policy without selecting site- or client-specific defaults."""
	from sports_app.payment_notifications import review_recipients

	review_recipients(values.get("payment_review_emails"))
	required = {
		"academy_name": "Academy name",
		"company": "Company",
		"currency": "Fee currency",
		"timezone": "Academy timezone",
		"registration_prefix": "Registration prefix",
		"default_program": "Default program",
	}
	missing = [label for name, label in required.items() if not str(values.get(name) or "").strip()]
	if missing:
		frappe.throw(_("Complete the following settings: {0}").format(", ".join(missing)))
	if values.get("timezone") not in pytz.all_timezones:
		frappe.throw(_("Select a valid academy timezone."))
	if not re.fullmatch(r"[A-Z][A-Z0-9-]{1,19}", values.get("registration_prefix") or ""):
		frappe.throw(
			_(
				"Registration prefix must be 2-20 uppercase letters, digits or hyphens, starting with a letter."
			)
		)
	if cint(values.get("registration_digits")) not in range(4, 11):
		frappe.throw(_("Registration digits must be between 4 and 10."))
	if values.get("default_enrollment_status") not in ("Pending", "Active"):
		frappe.throw(_("Select Pending or Active as the default enrollment status."))
	if flt(values.get("default_monthly_fee")) < 0:
		frappe.throw(_("The default monthly fee cannot be negative."))
	if cint(values.get("monthly_fees_enabled")) and flt(values.get("default_monthly_fee")) <= 0:
		frappe.throw(_("Set a positive monthly fee, or explicitly disable monthly fees."))


def validate_settings(doc):
	require_settings_access()
	validate_settings_values(doc.as_dict())
	from sports_app.payment_notifications import review_recipients

	doc.payment_review_emails = ", ".join(review_recipients(doc.get("payment_review_emails")))
	validate_company(doc.company)
	if not frappe.db.exists("Currency", {"name": doc.currency, "enabled": 1}):
		frappe.throw(_("Select an enabled currency."))
	program = frappe.get_doc("Sports Program", doc.default_program)
	program.check_permission("read")
	if program.company != doc.company or not program.enabled:
		frappe.throw(_("Default program must be enabled and belong to the selected company."))
	if doc.default_group:
		group = frappe.get_doc("Sports Group", doc.default_group)
		group.check_permission("read")
		if group.program != program.name or group.company != doc.company or not group.enabled:
			frappe.throw(_("Default group must be enabled and belong to the default program."))


def get_configured_settings(for_update=False):
	"""Use explicit saved values or schema defaults, never unrelated user defaults."""
	doc = (
		frappe.get_doc("Sports Academy Settings", "Sports Academy Settings", for_update=True)
		if for_update
		else frappe.get_single("Sports Academy Settings")
	)
	stored = (
		frappe.db.get_singles_dict("Sports Academy Settings", for_update=True)
		if for_update
		else frappe.db.get_singles_dict("Sports Academy Settings")
	)
	for fieldname in SETTINGS_FIELDS:
		if fieldname not in stored:
			field = doc.meta.get_field(fieldname)
			doc.set(fieldname, field.default if field else None)
	return doc


def get_ready_settings():
	"""Future enrollment/billing callers must validate readiness in their own authorized flow."""
	doc = get_configured_settings()
	doc.check_permission("read")
	validate_settings(doc)
	return doc
