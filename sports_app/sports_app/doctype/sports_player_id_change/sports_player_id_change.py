from frappe.model.document import Document

from sports_app.player_ids import check_audit, prevent_audit_change


class SportsPlayerIDChange(Document):
	def validate(self):
		check_audit(self)

	def on_trash(self):
		prevent_audit_change()

	def before_rename(self, old, new, merge=False):
		prevent_audit_change()
