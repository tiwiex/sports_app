import frappe
from frappe import _
from frappe.model.document import Document
from sports_app.academy import require_settings_access, validate_company


class SportsGroup(Document):
	def before_validate(self):
		require_settings_access()
		if self.program:
			program = frappe.get_doc("Sports Program", self.program)
			program.check_permission("read")
			validate_company(program.company)
			if not program.enabled:
				frappe.throw(_("Choose an enabled program."))
			self.company = program.company

	def validate(self):
		validate_company(self.company)
		if frappe.db.get_single_value("Sports Academy Settings", "default_group") == self.name:
			default_program = frappe.db.get_single_value("Sports Academy Settings", "default_program")
			if not self.enabled or self.program != default_program:
				frappe.throw(_("Choose another academy default group before disabling or moving this group."))
