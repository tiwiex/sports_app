from frappe.model.document import Document
from sports_app.attendance import validate_session, prevent_delete


class SportsSession(Document):
    def validate(self):
        validate_session(self)

    def on_trash(self):
        prevent_delete()
