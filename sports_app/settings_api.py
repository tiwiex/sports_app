"""Permission-checked endpoints for the Sports-owned settings console."""

import frappe
import pytz
from frappe import _

from sports_app.academy import (
	SETTINGS_FIELDS,
	get_configured_settings,
	require_settings_access,
	validate_company,
)


def _values(doc):
	result = {key: doc.get(key) for key in SETTINGS_FIELDS}
	result["modified"] = str(doc.modified or "")
	return result


@frappe.whitelist()
def get_configuration():
	require_settings_access()
	doc = get_configured_settings()
	doc.check_permission("read")
	# Explicit company check also protects a Single from leaking another scope.
	if doc.company:
		validate_company(doc.company)
	return {
		"settings": _values(doc),
		"companies": frappe.get_list("Company", fields=["name", "default_currency"], limit_page_length=0),
		"timezones": pytz.all_timezones,
		"programs": frappe.get_list(
			"Sports Program",
			fields=["name", "program_name", "sport", "company", "enabled"],
			order_by="program_name",
			limit_page_length=0,
		),
		"groups": frappe.get_list(
			"Sports Group",
			fields=["name", "group_name", "program", "company", "enabled"],
			order_by="group_name",
			limit_page_length=0,
		),
	}


@frappe.whitelist()
def save_configuration(settings: str | dict):
	require_settings_access()
	values = frappe.parse_json(settings)
	if not isinstance(values, dict) or set(values) - set(SETTINGS_FIELDS) - {"modified"}:
		frappe.throw(_("Invalid academy settings fields."))
	doc = get_configured_settings()
	doc.check_permission("write")
	if str(doc.modified or "") != str(values.pop("modified", "") or ""):
		frappe.throw(
			_("Settings changed since this view was loaded. Refresh before saving."),
			frappe.TimestampMismatchError,
		)
	# Validate the submitted scope before any update, even when moving company.
	validate_company(values.get("company"))
	doc.update(values)
	doc.save()
	return _values(doc)


@frappe.whitelist()
def save_program(program: str | dict):
	require_settings_access()
	values = frappe.parse_json(program)
	allowed = {"name", "program_name", "sport", "company", "enabled"}
	if not isinstance(values, dict) or set(values) - allowed:
		frappe.throw(_("Invalid program fields."))
	name = values.pop("name", None)
	doc = frappe.get_doc("Sports Program", name) if name else frappe.new_doc("Sports Program")
	if name:
		doc.check_permission("write")
		validate_company(doc.company)
	validate_company(values.get("company"))
	doc.update(values)
	doc.save()
	return doc.name


@frappe.whitelist()
def save_group(group: str | dict):
	require_settings_access()
	values = frappe.parse_json(group)
	if not isinstance(values, dict) or set(values) - {"name", "group_name", "program", "enabled"}:
		frappe.throw(_("Invalid group fields."))
	name = values.pop("name", None)
	doc = frappe.get_doc("Sports Group", name) if name else frappe.new_doc("Sports Group")
	if name:
		doc.check_permission("write")
		validate_company(doc.company)
	doc.update(values)
	doc.save()
	return doc.name
