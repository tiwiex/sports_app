from frappe.model.document import Document

from sports_app.player_profile import check_record, prevent_delete


class SportsPlayerMeasurement(Document):
	def validate(self):
		check_record(self)

	def on_trash(self):
		prevent_delete()

	def before_rename(self, old, new, merge=False):
		prevent_delete()
