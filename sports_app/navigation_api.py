"""Permission-scoped Sports sidebar counts, independent of the Finance host."""

import frappe
from frappe import _

from sports_app.academy import can_manage_settings, get_configured_settings, validate_company
from sports_app.console import has_console_permission
from sports_app.players import can_manage_players


@frappe.whitelist()
def get_counts():
	if not has_console_permission():
		frappe.throw(_("Sports console access is required."), frappe.PermissionError)
	players = can_manage_players()
	settings_access = can_manage_settings()
	if not players and not settings_access:
		return {}
	company = get_configured_settings().company
	validate_company(company)
	counts = {}
	for key, doctype, title, extra, allowed in (
		("registrations", "Sports Registration", "Pending enrollments", {"status": "Pending"}, players),
		("players", "Sports Player", "Players", {}, players),
		("attendance", "Sports Session", "Attendance sessions", {}, players),
		("relations", "Sports Organization", "Clubs and partners", {}, settings_access),
	):
		if not allowed or not frappe.has_permission(doctype, "read"):
			continue
		# Native list queries retain User Permissions and permission-query conditions.
		rows = frappe.get_list(
			doctype,
			filters={"company": company, **extra},
			fields=["count(name) as total"],
			order_by="",
			page_length=1,
		)
		counts["sports_app:" + key] = {
			"count": int(rows[0].total if rows else 0),
			"title": f"{title} — {company}",
		}
	return counts
