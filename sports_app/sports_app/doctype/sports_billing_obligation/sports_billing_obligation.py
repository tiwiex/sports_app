from frappe.model.document import Document

from sports_app.billing_access import no_delete
from sports_app.monthly_billing import validate_obligation


class SportsBillingObligation(Document):
	def autoname(self):
		from sports_app.monthly_billing import key_for

		self.name = key_for(self.company, self.enrollment, self.billing_month)

	def validate(self):
		validate_obligation(self)

	def on_trash(self):
		no_delete()

	def before_rename(self, *args):
		no_delete()
