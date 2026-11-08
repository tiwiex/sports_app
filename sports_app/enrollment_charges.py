"""Configurable enrollment invoice lines; legacy snapshots remain immutable."""

from decimal import Decimal, InvalidOperation

import frappe
from frappe import _

from sports_app.billing_policy import money


def rows(settings):
	configured = settings.get("enrollment_items") or []
	if configured or settings.get("enrollment_items_configured"):
		return configured
	# Compatibility only for sites awaiting the additive settings migration.
	return [
		frappe._dict(item_code=settings.get(item), qty=1, rate=settings.get(rate))
		for item, rate in (
			("enrollment_registration_item", "enrollment_registration_fee"),
			("enrollment_jersey_item", "enrollment_jersey_fee"),
		)
		if settings.get(item) and settings.get(rate)
	]


def calculate(settings, check_permissions=False):
	configured = rows(settings)
	if not configured or len(configured) > 30:
		frappe.throw(_("Configure between 1 and 30 enrollment charge rows."))
	result = []
	for row in configured:
		code = row.get("item_code")
		if not code:
			frappe.throw(_("Select an Item for every enrollment charge."))
		item = frappe.get_doc("Item", code)
		if check_permissions:
			item.check_permission("read")
		if item.disabled or not item.is_sales_item:
			frappe.throw(_("Enrollment charges require enabled sales Items."))
		try:
			qty = Decimal(str(row.get("qty")))
			if not qty.is_finite() or qty <= 0 or qty > 1000000 or qty.as_tuple().exponent < -4:
				raise ValueError
		except (InvalidOperation, ValueError, TypeError):
			frappe.throw(_("Charge quantities must be positive with at most four decimals."))
		rate = money(row.get("rate"))
		amount = money(qty * rate)
		result.append(
			dict(
				item_code=item.name,
				item_name=item.item_name,
				qty=float(qty),
				rate=float(rate),
				amount=float(amount),
				uom=item.stock_uom,
			)
		)
	if sum(money(row["amount"]) for row in result) <= 0:
		frappe.throw(_("Total enrollment charges must be greater than zero."))
	return result


def migrate_legacy_charges():
	"""Copy only saved legacy configuration once; never rewrite issued snapshots."""
	if not frappe.db.exists("DocType", "Sports Enrollment Charge"):
		return
	settings = frappe.get_single("Sports Academy Settings")
	if settings.get("enrollment_items_configured"):
		return
	if settings.get("enrollment_items"):
		frappe.db.set_single_value("Sports Academy Settings", "enrollment_items_configured", 1)
		return
	legacy = rows(settings)
	if not legacy:
		frappe.db.set_single_value("Sports Academy Settings", "enrollment_items_configured", 1)
		return
	for row in legacy:
		settings.append(
			"enrollment_items",
			dict(
				item_code=row.item_code,
				item_name=frappe.db.get_value("Item", row.item_code, "item_name") or row.item_code,
				qty=1,
				rate=row.rate,
				amount=row.rate,
			),
		)
	# Persist only the additive child rows, without running settings/workflow updates.
	for row in settings.enrollment_items:
		row.parent = settings.name
		row.parenttype = settings.doctype
		row.parentfield = "enrollment_items"
		row.db_insert()

	frappe.db.set_single_value("Sports Academy Settings", "enrollment_items_configured", 1)
