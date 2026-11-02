from frappe.model.document import Document
from sports_app.academy import validate_settings


class SportsAcademySettings(Document):
	def validate(self):
		validate_settings(self)

		if self.get("enrollment_payments_enabled"):
			from sports_app.enrollment_invoices import invoice_configuration
			invoice_configuration(self)

	def on_update(self):
		if self.get("enrollment_payments_enabled"):
			from sports_app.payment_setup import ensure_payment_workflow, ensure_invoice_workflow
			ensure_payment_workflow()
			ensure_invoice_workflow()
