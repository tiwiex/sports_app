"""Sports-owned print formats and bounded permission-filtered list references."""

import frappe
from frappe import _

FORMATS = {"Sales Invoice": "Sports Academy Invoice", "Payment Entry": "Sports Academy Receipt"}


def setup_formats():
	for folder in ("sports_academy_invoice", "sports_academy_receipt"):
		frappe.reload_doc("sports_app", "print_format", folder)


def latest_documents(player):
	result = dict(latest_invoice=None, latest_receipt=None, can_email_receipt=False)
	customer = getattr(player, "customer", None)
	if not customer or not frappe.get_doc("Customer", customer).has_permission("read"):
		return result
	for doctype, key in (("Sales Invoice", "latest_invoice"), ("Payment Entry", "latest_receipt")):
		if not frappe.has_permission(doctype, "read"):
			continue
		filters = (
			dict(company=player.company, customer=customer)
			if doctype == "Sales Invoice"
			else dict(
				company=player.company,
				party_type="Customer",
				party=customer,
				payment_type="Receive",
				docstatus=1,
			)
		)
		rows = frappe.get_list(
			doctype, filters=filters, fields=["name"], order_by="creation desc, name desc", page_length=1
		)
		if rows:
			result[key] = rows[0].name
			if doctype == "Payment Entry":
				from sports_app.receipt_delivery import can_email

				result["can_email_receipt"] = can_email(frappe.get_doc(doctype, rows[0].name))
	return result
