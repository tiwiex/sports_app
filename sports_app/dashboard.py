"""Read-only, permission-scoped academy landing dashboard."""

from datetime import timedelta

import frappe
from frappe import _

from sports_app.academy import can_manage_settings, get_configured_settings, validate_company
from sports_app.billing_access import can_read
from sports_app.console import has_console_permission
from sports_app.player_numbering import academy_date
from sports_app.players import can_manage_players
from sports_app.subscription_payments import overview, selected_year


def count(doctype, company, **filters):
	rows = frappe.get_list(
		doctype,
		filters={"company": company, **filters},
		fields=["count(name) as total"],
		order_by="",
		page_length=1,
	)
	return int(rows[0].total if rows else 0)


@frappe.whitelist()
def get_dashboard(year: str | int | None = None):
	if not has_console_permission():
		frappe.throw(_("Sports console access is required."), frappe.PermissionError)
	players_access = can_manage_players()
	billing_access = can_read()
	settings_access = can_manage_settings()
	if not (players_access or billing_access or settings_access):
		return {"restricted": True}
	settings = get_configured_settings()
	validate_company(settings.company)
	today = academy_date(settings)
	year = selected_year(today.year if year is None else year)
	company = settings.company
	counts = {"players": None, "active": None, "pending": None, "sessions": None}
	upcoming = None
	if players_access:
		visible_players = None
		if frappe.has_permission("Sports Player", "read"):
			visible_players = frappe.get_list(
				"Sports Player", filters={"company": company}, pluck="name", page_length=0
			)
			counts["players"] = len(visible_players)
		if visible_players is not None and frappe.has_permission("Sports Enrollment", "read"):
			counts["active"] = count(
				"Sports Enrollment", company, status="Active", player=["in", visible_players or [""]]
			)
		if frappe.has_permission("Sports Registration", "read"):
			counts["pending"] = count("Sports Registration", company, status="Pending")
		if frappe.has_permission("Sports Session", "read"):
			first = today.replace(day=1)
			last = (
				first.replace(year=first.year + 1, month=1)
				if first.month == 12
				else first.replace(month=first.month + 1)
			)
			counts["sessions"] = count(
				"Sports Session",
				company,
				session_date=["between", [str(first), str(last - timedelta(days=1))]],
				status=["!=", "Cancelled"],
			)
			upcoming = frappe.get_list(
				"Sports Session",
				filters={"company": company, "status": "Scheduled", "session_date": [">=", str(today)]},
				fields=["name", "title", "session_date", "start_time", "venue"],
				order_by="session_date asc, start_time asc, name asc",
				page_length=5,
			)
	finance = None
	if billing_access and all(
		frappe.has_permission(doctype, "read")
		for doctype in ("Sales Invoice", "Sports Billing Obligation", "Sports Enrollment", "Sports Player")
	):
		finance = overview(year)
	links = []
	for key, label, allowed in (
		("players", "Players", players_access),
		("registrations", "Enrollments", players_access),
		("attendance", "Attendance", players_access),
		("billing", "Scholarships & Billing", billing_access),
		("settings", "Academy Settings", settings_access),
	):
		if allowed:
			links.append({"view": "sports_app:" + key, "label": label})
	return dict(
		company=company,
		academy_name=settings.academy_name,
		today=str(today),
		year=year,
		counts=counts,
		upcoming=upcoming,
		finance=finance,
		links=links,
	)
