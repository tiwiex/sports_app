from frappe.model.document import Document
from sports_app.relations import validate_related


class SportsInteraction(Document):
    def validate(self):
        validate_related(self)
