import frappe
from frappe import _
from frappe.model.document import Document
from sports_app.academy import require_settings_access, validate_company


class SportsProgram(Document):
	def validate(self):
		require_settings_access()
		validate_company(self.company)
		previous = self.get_doc_before_save()
		if previous and previous.company != self.company and frappe.db.exists("Sports Group", {"program": self.name}):
			frappe.throw(_("A program with groups cannot be moved to another company."))
		if frappe.db.get_single_value("Sports Academy Settings", "default_program") == self.name:
			if not self.enabled or (previous and previous.company != self.company):
				frappe.throw(_("Choose another academy default program before disabling or moving this program."))
