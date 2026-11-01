"""Minimal Sports contribution to the Boost v1 console contract."""
import frappe

CONSOLE_ROLE = "Sports Console"
SETTINGS_ROLE = "Sports Academy Administrator"


def has_console_permission(user=None):
	user = user or frappe.session.user
	return bool(user and user != "Guest" and (
		user == "Administrator" or {CONSOLE_ROLE, SETTINGS_ROLE, "System Manager"}.intersection(frappe.get_roles(user))
	))


def get_provider():
	from sports_app.academy import can_manage_settings

	views = [{
		"key": "sports_app:overview", "label": "Sports Academy", "group": "Sports",
		"assets": ["/assets/sports_app/js/console_overview.js"],
	}]
	if can_manage_settings():
		views.append({
			"key": "sports_app:settings", "label": "Academy Settings", "group": "Sports",
			"assets": ["/assets/sports_app/js/academy_settings.js"],
		})
	return {
		"version": 1,
		"id": "sports_app",
		"roles": [CONSOLE_ROLE, SETTINGS_ROLE, "System Manager"],
		"has_permission": "sports_app.console.has_console_permission",
		"views": views,
	}


def setup_roles():
	for role in (CONSOLE_ROLE, SETTINGS_ROLE):
		if not frappe.db.exists("Role", role):
			frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 1}).insert(ignore_permissions=True)


def setup_console():
	"""Create unassigned roles and sync configuration access and the optional host."""
	setup_roles()
	# Configuration users can read company and currency masters, with standard User Permission
	# restrictions; no ledger/transaction permission or accounting role is granted.
	for master in ("Company", "Currency"):
		if not frappe.db.exists("DocType", master):
			continue
		for role in (SETTINGS_ROLE, "System Manager"):
			if not frappe.db.exists("Custom DocPerm", {"parent": master, "role": role, "permlevel": 0}):
				from frappe.permissions import add_permission
				add_permission(master, role, ptype="read")
	if "erp_boost" in frappe.get_installed_apps():
		# Optional host dependency; no Boost import at module load or without installation.
		frappe.get_attr("erp_boost.console_entry_setup.ensure_page_roles")()


def set_console_login_redirect(login_manager=None):
	user = getattr(login_manager, "user", None) or frappe.session.user
	if "erp_boost" not in frappe.get_installed_apps() or not has_console_permission(user):
		return
	if frappe.form_dict.get("redirect-to") or frappe.form_dict.get("redirect_to"):
		return
	frappe.cache.hset("redirect_after_login", user, "/app/boost-console")
