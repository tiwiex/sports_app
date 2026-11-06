"""Enrollment identity checks and bounded guardian-account provisioning."""

import frappe
from frappe import _


def normalize_email(value):
	if not isinstance(value, str) or len(value) > 140:
		frappe.throw(_("Enter one valid email address."))
	email = value.strip().lower()
	if not email or "," in email or ";" in email:
		frappe.throw(_("Enter one valid email address."))
	frappe.utils.validate_email_address(email, throw=True)
	return email


def player_email_available(email, registration=None):
	if (
		frappe.db.exists("User", email)
		or frappe.db.exists("User", {"email": email})
		or frappe.db.exists("Sports Player", {"contact_email": email})
	):
		return False
	filters = {"contact_email": email, "status": "Pending"}
	if registration:
		filters["name"] = ["!=", registration]
	return not frappe.db.exists("Sports Registration", filters)


def require_available_player_email(email, registration=None):
	if not player_email_available(email, registration):
		frappe.throw(
			_(
				"This player email is already in use or has a pending enrollment. Enter a different, unique player email."
			)
		)


def create_guardian_user(player):
	from sports_app.players import require_player_access

	require_player_access()
	if not player.get("guardian_email"):
		return None  # retain legacy staff-created profiles without structured guardian details
	email = normalize_email(player.guardian_email)
	if email == player.contact_email:
		frappe.throw(_("Player and guardian must use separate email addresses."))
	existing = frappe.db.exists("User", {"email": email}) or frappe.db.exists("User", email)
	if existing:
		# A claimed guardian email never authorizes edits, activation, roles or portal
		# data access. Reuse only the identity reference; verification is future scope.
		name = existing
	else:
		user = frappe.get_doc(
			doctype="User",
			email=email,
			first_name=player.guardian_name or "Guardian",
			user_type="Website User",
			enabled=0,
			send_welcome_email=0,
			role_profile_name=None,
			module_profile=None,
			roles=[],
		)
		user.flags.no_welcome_mail = True
		setting_role = frappe.flags.setting_role
		try:
			frappe.flags.setting_role = True
			user.insert(ignore_permissions=True)
		finally:
			frappe.flags.setting_role = setting_role
		if (
			user.enabled
			or user.user_type != "Website User"
			or {r.role for r in user.roles} - {"All", "Guest"}
		):
			frappe.throw(_("New guardian accounts must remain disabled Website Users without Desk access."))
		name = user.name
	player.db_set("guardian_user", name, update_modified=False)
	return name
