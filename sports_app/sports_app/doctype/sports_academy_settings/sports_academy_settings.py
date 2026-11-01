from frappe.model.document import Document
from sports_app.academy import validate_settings


class SportsAcademySettings(Document):
	def validate(self):
		validate_settings(self)
