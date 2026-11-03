from frappe.model.document import Document
from sports_app.attendance import validate_attendance, prevent_delete


class SportsAttendance(Document):
    def validate(self):
        validate_attendance(self)

    def on_trash(self):
        prevent_delete()
