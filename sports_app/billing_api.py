"""Allowlisted console projections; scholarship details have a separate restricted path."""

import frappe
from frappe import _
from frappe.model import get_permitted_fields

from sports_app.academy import can_manage_settings
from sports_app.billing_access import OBLIGATION, PLAN, SCHOLARSHIP, require_billing


@frappe.whitelist()
def configuration():
	settings = require_billing()
	company = frappe.get_doc("Company", settings.company)
	from sports_app.player_numbering import academy_date

	return dict(
		current_month=str(academy_date(settings))[:7],
		monthly_fees_enabled=bool(settings.monthly_fees_enabled),
		automatic_monthly_billing=bool(settings.get("automatic_monthly_billing")),
		monthly_billing_start=settings.get("monthly_billing_start"),
		company=settings.company,
		currency=company.default_currency,
		default_monthly_fee=settings.enrollment_monthly_fee or settings.default_monthly_fee or 40000,
		can_manage=can_manage_settings(),
		can_read_finance=bool(frappe.has_permission("Sales Invoice", "read")),
		can_generate=bool(
			frappe.has_permission("Sales Invoice", "create")
			and frappe.has_permission("Sales Invoice", "read")
			and frappe.has_permission("Sales Invoice", "submit")
		),
	)


@frappe.whitelist()
def records(section: str, start: str | int = 0):
	settings = require_billing()
	definitions = {
		"plans": (
			PLAN,
			[
				"name",
				"title",
				"program",
				"enabled",
				"effective_from",
				"effective_to",
				"currency",
				"monthly_amount",
				"joining_policy",
				"due_day",
				"item",
				"subscription_plan",
				"income_account",
				"cost_center",
				"modified",
			],
		),
		"decisions": (
			SCHOLARSHIP,
			[
				"name",
				"enrollment",
				"player",
				"effective_from",
				"effective_to",
				"coverage_type",
				"coverage_value",
				"docstatus",
				"modified",
				"approved_by",
				"approved_on",
				"revoked_by",
				"revoked_on",
			],
		),
		"obligations": (
			OBLIGATION,
			[
				"name",
				"enrollment",
				"player",
				"billing_month",
				"currency",
				"amount",
				"due_date",
				"sales_invoice",
			],
		),
	}
	if section not in definitions or not str(start).isdigit() or len(str(start)) > 6:
		frappe.throw(_("Choose a valid billing list and page."))
	doctype, fields = definitions[section]
	rows = frappe.get_list(
		doctype,
		filters={"company": settings.company},
		fields=fields,
		order_by="creation desc, name desc",
		start=int(start),
		page_length=21,
	)
	return dict(rows=rows[:20], has_more=len(rows) > 20)


@frappe.whitelist()
def decision(name: str):
	settings = require_billing()
	doc = frappe.get_doc(SCHOLARSHIP, name)
	doc.check_permission("read")
	if doc.company != settings.company:
		frappe.throw(_("Decision is outside the configured academy."), frappe.PermissionError)
	permitted = set(get_permitted_fields(SCHOLARSHIP, permission_type="read"))
	return {
		k: doc.get(k)
		for k in (
			"name",
			"enrollment",
			"player",
			"effective_from",
			"effective_to",
			"coverage_type",
			"coverage_value",
			"reason",
			"kit_benefit",
			"trip_benefit",
			"trial_benefit",
			"tournament_benefit",
			"docstatus",
			"modified",
			"approved_by",
			"approved_on",
			"revocation_reason",
			"revoked_by",
			"revoked_on",
		)
		if k in permitted
	}
