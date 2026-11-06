import frappe
from frappe import _
from frappe.model.document import Document

from sports_app.academy import validate_company
from sports_app.players import immutable, require_player_access, validate_enrollment_values


class SportsEnrollment(Document):
	def validate(self):
		require_player_access()
		immutable(self, ("player", "company"))
		player = frappe.get_doc("Sports Player", self.player)
		player.check_permission("read")
		if not player.customer:
			frappe.throw(_("The player has no linked Customer. Contact the academy administrator."))
		if self.payer_customer and self.payer_customer != player.customer:
			frappe.throw(_("Enrollment must use the player's own Customer."))
		self.payer_customer = player.customer
		self.company = player.company
		validate_company(self.company)
		program = frappe.get_doc("Sports Program", self.program)
		program.check_permission("read")
		group = frappe.get_doc("Sports Group", self.group) if self.group else None
		if group:
			group.check_permission("read")
		customer = frappe.get_doc("Customer", self.payer_customer)
		customer.check_permission("read")
		validate_enrollment_values(self, program, group, customer)
