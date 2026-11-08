from frappe.model.document import Document

from sports_app.academy import validate_settings


class SportsAcademySettings(Document):
	def validate(self):
		validate_settings(self)
		self.enrollment_items_configured = 1
		if self.get("enrollment_items"):
			from sports_app.enrollment_charges import calculate

			calculated = calculate(self, check_permissions=True)
			for row, values in zip(self.enrollment_items, calculated, strict=True):
				row.item_name = values["item_name"]
				row.amount = values["amount"]

		if self.get("enrollment_payments_enabled"):
			from sports_app.enrollment_invoices import invoice_configuration

			invoice_configuration(self)

	def on_update(self):
		if self.get("enrollment_payments_enabled"):
			from sports_app.payment_setup import ensure_invoice_workflow, ensure_payment_workflow

			ensure_payment_workflow()
			ensure_invoice_workflow()
