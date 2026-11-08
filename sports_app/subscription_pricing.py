"""Reuse ERPNext monthly Subscription Plan pricing without starting its scheduler."""

import frappe
from frappe import _

from sports_app.billing_access import require_billing
from sports_app.billing_policy import money


def resolve(name, currency):
	plan = frappe.get_doc("Subscription Plan", name)
	plan.check_permission("read")
	if plan.currency != currency or plan.billing_interval != "Month" or plan.billing_interval_count != 1:
		frappe.throw(_("Choose a Subscription Plan for one calendar month in the company currency."))
	if plan.price_determination != "Fixed Rate":
		frappe.throw(_("Use a Fixed Rate Subscription Plan for the manual scholarship billing prototype."))
	item = frappe.get_doc("Item", plan.item)
	item.check_permission("read")
	if item.disabled or item.is_stock_item or not item.is_sales_item:
		frappe.throw(_("Subscription Plan must use an enabled non-stock sales Item."))
	from erpnext.accounts.doctype.subscription_plan.subscription_plan import get_plan_rate

	rate = money(get_plan_rate(name, quantity=1, prorate_factor=1))
	if not rate:
		frappe.throw(_("Subscription Plan rate must be greater than zero."))
	return dict(
		item=plan.item,
		monthly_amount=float(rate),
		currency=plan.currency,
		subscription_plan=plan.name,
		subscription_revision=str(plan.modified),
	)


@frappe.whitelist()
def plan_details(name: str):
	settings = require_billing()
	company = frappe.get_doc("Company", settings.company)
	return resolve(name, company.default_currency)
