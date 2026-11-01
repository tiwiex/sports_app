import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import now_datetime, getdate, today
from sports_app.players import require_player_access, registration_settings, immutable, create_player_customer, create_player_user, validate_player_email
from sports_app.academy import validate_company


class SportsPlayer(Document):
 def autoname(self):
  require_player_access()
  settings = registration_settings(for_update=True)
  if self.company != settings.company:
   frappe.throw("Player company must match the academy company.")
  self.name = make_autoname(settings.registration_prefix + "-." + "#" * int(settings.registration_digits))

 def before_rename(self, old, new, merge=False):
  frappe.throw("Player registration IDs cannot be renamed or merged.")

 def after_insert(self):
  create_player_customer(self)
  create_player_user(self)

 def before_insert(self):
  require_player_access()
  if self.get("portal_user"):
   frappe.throw("The self-service User is created automatically; existing Users cannot be assigned.")
  if self.customer:
   frappe.throw("A player Customer is created automatically; existing Customers cannot be assigned.")
  if not self.registration_program:
   self.registration_program = registration_settings().default_program
  self.registered_on = now_datetime()

 def validate(self):
  require_player_access()
  validate_company(self.company)
  immutable(self, ("company", "registered_on", "request_key", "request_hash", "customer", "registration_program", "portal_user"))
  if self.registration_program:
   program = frappe.get_doc("Sports Program", self.registration_program)
   program.check_permission("read")
   if program.company != self.company or (self.is_new() and not program.enabled):
    frappe.throw("Registration program must be enabled and belong to the player's company.")
  if self.is_new():
   validate_player_email(self)
  else:
   previous = self.get_doc_before_save()
   if previous and previous.portal_user and previous.contact_email != self.contact_email:
    frappe.throw("The login email is linked to a User. Account email changes require administrator review.")
  self.full_name = (self.full_name or "").strip()
  if not self.full_name:
   frappe.throw("Enter the player's name.")
  if self.birth_date and getdate(self.birth_date) > getdate(today()):
   frappe.throw("Date of birth cannot be in the future.")
  if self.contact_email:
   frappe.utils.validate_email_address(self.contact_email, throw=True)
