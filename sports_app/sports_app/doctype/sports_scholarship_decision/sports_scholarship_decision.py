from frappe.model.document import Document

from sports_app import scholarships
from sports_app.billing_access import no_delete


class SportsScholarshipDecision(Document):
	def validate(self):
		scholarships.validate(self)

	def before_submit(self):
		scholarships.approve(self)

	def before_cancel(self):
		scholarships.revoke(self)

	def on_trash(self):
		no_delete()

	def before_rename(self, *args):
		no_delete()
