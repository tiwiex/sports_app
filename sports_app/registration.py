"""Shared public-demo/private-registration field definitions and input policy."""

import json
from datetime import date
from pathlib import Path

import frappe
from frappe import _


def get_registration_fields():
	return json.loads(Path(__file__).with_name("registration_fields.json").read_text())


def validate_registration_details(player):
	fields = get_registration_fields()
	# Preserve existing records and legacy full-name integrations. New structured
	# registrations supply both names and the required reference-form details.
	structured = bool(player.get("first_name") or player.get("last_name"))
	for field in fields:
		name = field["fieldname"]
		if field["fieldtype"] == "Section Break":
			continue
		value = player.get(name)
		if structured and player.is_new() and field.get("reqd") and not str(value or "").strip():
			frappe.throw(_("{0} is required.").format(field["label"]))
		if field["fieldtype"] == "Check":
			if value not in (None, "", 0, 1, "0", "1"):
				frappe.throw(_("Invalid consent choice."))
			player.set(name, int(value or 0))
		elif value and field["fieldtype"] == "Date":
			if not isinstance(value, str | date):
				frappe.throw(_("Enter a valid date of birth."))
			player.set(name, frappe.utils.getdate(value))
		elif value:
			if not isinstance(value, str):
				frappe.throw(_("Invalid value for {0}.").format(field["label"]))
			value = value.strip()
			limit = 2000 if field["fieldtype"] == "Small Text" else 140
			if len(value) > limit:
				frappe.throw(_("{0} is too long.").format(field["label"]))
			if field["fieldtype"] == "Select" and value not in field["options"].splitlines():
				frappe.throw(_("Select a valid {0}.").format(field["label"]))
			if field.get("options") == "Email":
				frappe.utils.validate_email_address(value, throw=True)
			player.set(name, value)
	if structured:
		if not player.get("first_name") or not player.get("last_name"):
			frappe.throw(_("Enter both the player's first and last names."))
		player.full_name = f"{player.first_name} {player.last_name}"
		if len(player.full_name) > 140:
			frappe.throw(_("Player name is too long."))
	if bool(player.get("emergency_contact_name")) != bool(player.get("emergency_contact_phone")):
		frappe.throw(_("Enter both the emergency contact name and phone, or leave both blank."))


def validate_application_age(birth_date, on_date):
	"""Public intake admits ages 4 through 18 inclusive, using calendar birthdays."""
	birth = frappe.utils.getdate(birth_date)
	age = on_date.year - birth.year - ((on_date.month, on_date.day) < (birth.month, birth.day))
	if age < 4 or age > 18:
		frappe.throw(_("Players must be between 4 and 18 years old."))
	return age
