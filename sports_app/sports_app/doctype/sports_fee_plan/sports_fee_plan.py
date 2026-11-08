from frappe.model.document import Document

from sports_app.billing_access import no_delete
from sports_app.fee_plans import validate


class SportsFeePlan(Document):
	def validate(self):
		validate(self)

	def on_trash(self):
		no_delete()

	def before_rename(self, *args):
		no_delete()
