from frappe.model.document import Document

from sports_app.attendance import prevent_delete, validate_attendance


class SportsAttendance(Document):
	def validate(self):
		validate_attendance(self)

	def on_trash(self):
		prevent_delete()
