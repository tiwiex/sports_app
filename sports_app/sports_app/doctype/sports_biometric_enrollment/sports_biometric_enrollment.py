import frappe
from frappe import _
from frappe.model.document import Document

from sports_app.biometric_preparation import validate_document


class SportsBiometricEnrollment(Document):
	def validate(self):
		validate_document(self)

	def on_trash(self):
		frappe.throw(_("Withdraw the preparation instead; records are retained for audit."))
