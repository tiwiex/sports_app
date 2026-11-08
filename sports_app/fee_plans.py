"""Explicit fee mapping and policy validation; no guessed accounting defaults."""

import frappe
from frappe import _
from frappe.utils import getdate

from sports_app.billing_access import PLAN, require_billing
from sports_app.billing_policy import money, overlap


def mapping(doc):
	company = frappe.get_doc("Company", doc.company)
	company.check_permission("read")
	if doc.currency != company.default_currency:
		frappe.throw(_("Monthly billing currently requires the company accounting currency."))
	program = frappe.get_doc("Sports Program", doc.program)
	program.check_permission("read")
	if program.company != doc.company or not program.enabled:
		frappe.throw(_("Choose an enabled program in the academy company."))
	item = frappe.get_doc("Item", doc.item)
	item.check_permission("read")
	if item.disabled or item.is_stock_item or not item.is_sales_item:
		frappe.throw(_("Select an enabled non-stock sales service item."))
	account = frappe.get_doc("Account", doc.income_account)
	account.check_permission("read")
	if (
		account.company != doc.company
		or account.disabled
		or account.is_group
		or account.root_type != "Income"
		or account.account_currency != doc.currency
	):
		frappe.throw(_("Choose an active company income ledger in the plan currency."))
	center = frappe.get_doc("Cost Center", doc.cost_center)
	center.check_permission("read")
	if center.company != doc.company or center.disabled or center.is_group:
		frappe.throw(_("Choose an active company cost center."))
	return item


def validate(doc):
	settings = require_billing(manage=True)
	if doc.company != settings.company:
		frappe.throw(_("Fee plan must use the configured academy company."))
	old = doc.get_doc_before_save()
	if old and any(old.get(k) != doc.get(k) for k in ("company", "program", "currency")):
		frappe.throw(_("Create a new plan instead of changing its company, program or currency."))
	if not doc.effective_from or getdate(doc.effective_from).day != 1:
		frappe.throw(_("Fee plans must start on the first day of a month."))
	if doc.effective_to:
		from sports_app.billing_policy import period

		end = getdate(doc.effective_to)
		if end < getdate(doc.effective_from) or end != period(str(end)[:7])[1]:
			frappe.throw(_("Fee plans must end on the last day of a month."))
	if doc.joining_policy != "Full fee if active at month start" or not 1 <= int(doc.due_day or 0) <= 28:
		frappe.throw(_("Select the approved month-start policy and a due day from 1 to 28."))
	if doc.get("subscription_plan"):
		from sports_app.subscription_pricing import resolve

		pricing = resolve(doc.subscription_plan, doc.currency)
		doc.item = pricing["item"]
		doc.monthly_amount = pricing["monthly_amount"]
	doc.monthly_amount = money(doc.monthly_amount)
	if not doc.monthly_amount:
		frappe.throw(_("Monthly fee must be positive; record exemptions as separate decisions."))
	mapping(doc)
	if doc.enabled:
		for other in frappe.get_all(
			PLAN,
			filters={"company": doc.company, "program": doc.program, "enabled": 1, "name": ["!=", doc.name]},
			fields=["effective_from", "effective_to"],
		):
			if overlap(doc.effective_from, doc.effective_to, other.effective_from, other.effective_to):
				frappe.throw(_("Enabled fee plans for the same program cannot overlap."))


@frappe.whitelist(methods=["POST"])
def save(values: str | dict, name: str | None = None, modified: str | None = None):
	settings = require_billing(manage=True)
	values = frappe.parse_json(values)
	allowed = {
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
	}
	if not isinstance(values, dict) or set(values) - allowed:
		frappe.throw(_("Invalid fee plan fields."))
	if name:
		doc = frappe.get_doc(PLAN, name, for_update=True)
		doc.check_permission("write")
		if str(doc.modified) != str(modified):
			frappe.throw(_("Fee plan changed. Reload before saving."), frappe.TimestampMismatchError)
		doc.update(values)
		doc.save()
	else:
		doc = frappe.get_doc(doctype=PLAN, company=settings.company, **values)
		doc.insert()
	return doc.name
