"""Backend-owned player identity, independent of application naming counters."""

import hashlib
import re
from datetime import datetime
from zoneinfo import ZoneInfo

import frappe
from frappe import _
from frappe.model.naming import getseries


def academy_date(settings):
	return datetime.now(ZoneInfo(settings.timezone)).date()


def starting_sequence(value):
	value = 1 if value is None or value == "" else value
	if isinstance(value, bool) or not re.fullmatch(r"[1-9]\d{0,9}", str(value)):
		frappe.throw(_("Player starting sequence must be a whole number from 1 to 9999999999."))
	return int(value)


def legacy_sequence(name, settings):
	pattern = re.compile(re.escape(settings.registration_prefix) + r"\d{2}-(?:0[1-9]|1[0-2])(\d{3,})")
	match = pattern.fullmatch(name or "")
	return int(match[1]) if match else 0


def ensure_counter(settings, minimum=0):
	"""Caller holds the settings lock; a floor can advance, never reset, this Company counter."""
	key = "sports-player-" + hashlib.sha256(settings.company.encode()).hexdigest()[:32]
	current = frappe.db.get_value("Series", key, "current", for_update=True, order_by="name")
	floor = max(starting_sequence(settings.get("player_starting_sequence")) - 1, minimum)
	if current is None:
		for row in frappe.get_all("Sports Player", filters={"company": settings.company}, fields=["name"]):
			floor = max(floor, legacy_sequence(row.name, settings))
		frappe.db.sql("INSERT INTO `tabSeries` (`name`, `current`) VALUES (%s, %s)", (key, floor))
	elif int(current) < floor:
		frappe.db.sql("UPDATE `tabSeries` SET `current`=%s WHERE `name`=%s", (floor, key))
	return key


def next_player_id(settings):
	# The key never includes month/year/prefix, so none of these restart numbering.
	key = ensure_counter(settings)
	from sports_app.player_ids import reserved

	date = academy_date(settings)
	while True:
		sequence = getseries(key, int(settings.registration_digits))
		candidate = f"{settings.registration_prefix}{date:%y}-{date:%m}{sequence}"
		if not reserved(candidate):
			return candidate


def prepare_import(doc):
	"""Native Data Import may retain its ID column; only academy managers can use it."""
	if not frappe.flags.in_import:
		return
	from sports_app.academy import require_settings_access
	from sports_app.players import registration_settings

	require_settings_access()
	settings = registration_settings(for_update=True)
	if doc.company != settings.company:
		frappe.throw(_("Player company must match the academy company."))
	return settings


def reserve_imported_sequence(doc):
	settings = prepare_import(doc)
	if settings:
		ensure_counter(settings, legacy_sequence(doc.name, settings))
