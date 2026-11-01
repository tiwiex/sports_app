"""Private player identity and enrollment policy. Each player owns one automatically created ERPNext Customer."""
import frappe
from frappe import _
from frappe.utils import getdate
from sports_app.academy import get_configured_settings, validate_settings_values, validate_company

PLAYER_ROLE = "Sports Registrar"
PLAYER_FIELDS = ("full_name", "birth_date", "contact_email", "contact_phone", "guardian_name", "guardian_phone")
ENROLLMENT_FIELDS = ("program", "group", "start_date", "end_date", "status")


def can_manage_players(user=None):
 user = user or frappe.session.user
 return bool(user and user != "Guest" and (user == "Administrator" or
  {PLAYER_ROLE, "Sports Academy Administrator", "System Manager"}.intersection(frappe.get_roles(user))))


def require_player_access():
 if not can_manage_players():
  frappe.throw(_("Player management requires the Sports Registrar role."), frappe.PermissionError)


def registration_settings(for_update=False):
 require_player_access()
 settings = get_configured_settings(for_update=True) if for_update else get_configured_settings()
 validate_settings_values(settings.as_dict())
 validate_company(settings.company)
 return settings


def immutable(doc, fields):
 previous = doc.get_doc_before_save()
 if previous:
  validate_company(previous.company)
  if any(str(previous.get(key) or "") != str(doc.get(key) or "") for key in fields):
   frappe.throw(_("Identity, company and registration provenance cannot be changed."))


def validate_enrollment_values(doc, program, group, customer):
 if program.company != doc.company:
  frappe.throw(_("Program must belong to the player's company."))
 previous = doc.get_doc_before_save()
 # Retiring a master must not prevent withdrawing or correcting an existing enrollment.
 if not program.enabled and (not previous or previous.program != doc.program):
  frappe.throw(_("Select an enabled program."))
 if group and (group.company != doc.company or group.program != doc.program):
  frappe.throw(_("Group must belong to the selected program and company."))
 if group and not group.enabled and (not previous or previous.group != doc.group):
  frappe.throw(_("Select an enabled group."))
 if customer.disabled and (not previous or previous.payer_customer != doc.payer_customer):
  frappe.throw(_("The player Customer is disabled. Enable it before adding an enrollment."))
 if not doc.start_date:
  frappe.throw(_("Set the enrollment start date."))
 if doc.end_date and getdate(doc.end_date) < getdate(doc.start_date):
  frappe.throw(_("End date cannot be before start date."))
 if doc.status not in ("Pending", "Active", "Suspended", "Withdrawn", "Completed"):
  frappe.throw(_("Select a valid enrollment status."))
 if doc.status in ("Withdrawn", "Completed") and not doc.end_date:
  frappe.throw(_("Set an end date for a withdrawn or completed enrollment."))


def is_eligible(enrollment, on_date):
 day = getdate(on_date)
 return (enrollment.status == "Active" and bool(enrollment.start_date)
  and getdate(enrollment.start_date) <= day
  and (not enrollment.end_date or day <= getdate(enrollment.end_date)))


def create_player_customer(player):
 """Narrow creation capability after authorized player insertion; never link by name/email."""
 require_player_access()
 company = validate_company(player.company)
 group = ensure_program_customer_group(player)
 territory = frappe.db.get_single_value("Selling Settings", "territory")
 territory = territory or (company.country if frappe.db.exists("Territory", company.country) else None)
 if not territory:
  frappe.throw(_("Set the default Territory in ERPNext Selling Settings before registration."))
 customer = frappe.new_doc("Customer")
 customer.update({"customer_name": player.full_name, "customer_type": "Individual",
  "customer_group": group, "territory": territory,
  "email_id": player.contact_email or None, "mobile_no": None})
 # This role may register players but has no general Customer/Contact create or
 # write rights. ERPNext validation and primary Contact creation still execute.
 # Derive an app-owned key from the immutable player ID. ERPNext name-based
 # suffix lookup uses snapshot reads and can collide for concurrent same names.
 customer.insert(ignore_permissions=True, set_name="SPORTS-CUST-" + player.name)
 if player.contact_phone:
  # ERPNext 15's Contact.after_insert call-log hook commits inside its phone
  # loop. Insert the contact without phones, then append/save the phone on
  # update, so registration's surrounding transaction/savepoint remains intact.
  if customer.customer_primary_contact:
   contact = frappe.get_doc("Contact", customer.customer_primary_contact)
  else:
   from erpnext.selling.doctype.customer.customer import make_contact
   contact = make_contact(customer)
  contact.add_phone(player.contact_phone, is_primary_mobile_no=True)
  contact.save(ignore_permissions=True)
  customer.db_set({"customer_primary_contact": contact.name, "mobile_no": player.contact_phone})
 player.db_set("customer", customer.name, update_modified=False)
 return customer.name


def ensure_program_customer_group(player):
 """Create only the authorized registration program's category, inside the transaction."""
 require_player_access()
 program = frappe.get_doc("Sports Program", player.registration_program)
 program.check_permission("read")
 validate_company(program.company)
 if program.company != player.company or not program.enabled:
  frappe.throw(_("Choose an enabled registration program in the player's company."))
 name = program.program_name.strip()
 existing = frappe.db.get_value("Customer Group", name, ["name", "is_group"], as_dict=True, for_update=True)
 if existing:
  if existing.is_group:
   frappe.throw(_("Customer Group {0} is a parent category. Choose a distinct program name.").format(name))
  return existing.name
 root = frappe.db.get_value("Customer Group", {"lft": 1, "is_group": 1}, "name", for_update=True)
 if not root:
  frappe.throw(_("Configure the ERPNext Customer Group root before registration."))
 category = frappe.get_doc({"doctype": "Customer Group", "customer_group_name": name,
  "parent_customer_group": root, "is_group": 0})
 category.insert(ignore_permissions=True)
 return category.name


def validate_player_email(player):
 """New identities need their own unused email; never bind an existing account."""
 email = (player.contact_email or "").strip().lower()
 player.contact_email = email
 if not email:
  frappe.throw(_("Enter a unique email address to create the player's self-service User."))
 if "," in email or ";" in email:
  frappe.throw(_("Enter one unique email address for the player."))
 frappe.utils.validate_email_address(email, throw=True)
 if frappe.db.exists("User", email) or frappe.db.exists("Sports Player", {"contact_email": email}):
  frappe.throw(_("This email is already in use. Enter a unique player email; existing accounts require administrator review."))


def create_player_user(player):
 require_player_access()
 from erpnext.selling.doctype.customer.customer import parse_full_name
 first, middle, last = parse_full_name(player.full_name)
 user = frappe.get_doc({"doctype": "User", "email": player.contact_email,
  "first_name": first, "middle_name": middle, "last_name": last,
  "user_type": "Website User", "enabled": 0, "send_welcome_email": 0,
  "role_profile_name": None, "module_profile": None,
  "roles": [{"role": "Sports Player"}]})
 user.flags.no_welcome_mail = True
 # ERPNext's supported guard prevents contact-based Customer/Supplier role
 # inference while this bounded service provisions a future-only account.
 setting_role = frappe.flags.setting_role
 try:
  frappe.flags.setting_role = True
  user.insert(ignore_permissions=True)
 finally:
  frappe.flags.setting_role = setting_role
 if user.user_type != "Website User" or user.enabled or {row.role for row in user.roles} - {"Sports Player", "All", "Guest"}:
  frappe.throw(_("Player accounts must be Website Users without Desk access."))
 player.db_set("portal_user", user.name, update_modified=False)
 contact = frappe.db.get_value("Customer", player.customer, "customer_primary_contact")
 if contact:
  frappe.db.set_value("Contact", contact, "user", user.name, update_modified=False)
 return user.name
