from frappe.model.document import Document

from sports_app.relations import validate_organization


class SportsOrganization(Document):
	def validate(self):
		validate_organization(self)
