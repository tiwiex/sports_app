"""Bounded public intake and private review rules; no guest record access."""

import hashlib
import json
from contextlib import contextmanager
from uuid import UUID

import frappe
from frappe import _
from frappe.utils import CallbackManager, getdate, today

from sports_app.academy import get_configured_settings, validate_company, validate_settings_values
from sports_app.players import require_player_access
from sports_app.registration import get_registration_fields, validate_registration_details
from sports_app.website import get_website_content

SERVICE_CAPABILITY = object()
PUBLIC_FIELDS = tuple(f["fieldname"] for f in get_registration_fields() if f["fieldtype"] != "Section Break")


def request_uuid(value):
	try:
		if str(UUID(str(value), version=4)) != str(value):
			raise ValueError
	except (ValueError, TypeError, AttributeError):
		frappe.throw(_("Refresh the registration form and try again."))
	return str(value)


def public_payload(player):
	if isinstance(player, str) and len(player) > 14000:
		frappe.throw(_("Registration details are too large."))
	values = frappe.parse_json(player)
	if not isinstance(values, dict) or set(values) - set(PUBLIC_FIELDS):
		frappe.throw(_("Invalid registration details."))
	for field in get_registration_fields():
		if field["fieldtype"] != "Section Break" and field["fieldtype"] != "Check":
			value = values.get(field["fieldname"])
			if value is not None and not isinstance(value, str):
				frappe.throw(_("Invalid registration details."))
		if field.get("reqd") and not str(values.get(field["fieldname"]) or "").strip():
			frappe.throw(_("{0} is required.").format(field["label"]))
	# Validate raw flags before Frappe normalizes Check fields.
	for field in ("medical_consent", "media_consent", "terms_accepted"):
		if values.get(field) not in (None, "", 0, 1, "0", "1"):
			frappe.throw(_("Invalid consent choice."))
	return values


def validate_intake(doc):
	for field in get_registration_fields():
		if field.get("reqd") and not str(doc.get(field["fieldname"]) or "").strip():
			frappe.throw(_("{0} is required.").format(field["label"]))
	validate_registration_details(doc)
	if not doc.first_name or not doc.last_name:
		frappe.throw(_("Enter both the player's first and last names."))
	if doc.birth_date and getdate(doc.birth_date) > getdate(today()):
		frappe.throw(_("Date of birth cannot be in the future."))
	email = (doc.contact_email or "").strip().lower()
	if not email or "," in email or ";" in email:
		frappe.throw(_("Enter one unique player email address."))
	frappe.utils.validate_email_address(email, throw=True)
	doc.contact_email = email


def intake_settings():
	# Read only explicitly configured site defaults. No guest permission bypass
	# is exposed as a general-purpose settings/master endpoint.
	settings = get_configured_settings(for_update=True)
	validate_settings_values(settings.as_dict())
	program = frappe.db.get_value(
		"Sports Program", settings.default_program, ["company", "enabled"], as_dict=True
	)
	if not program or program.company != settings.company or not program.enabled:
		frappe.throw(_("Registration is unavailable. Please contact the academy."))
	return settings


def pathway_names():
	return [p["name"] for p in get_website_content()["programs"]]


def fingerprint(doc):
	values = {key: doc.get(key) for key in PUBLIC_FIELDS}
	if values.get("birth_date"):
		values["birth_date"] = str(values["birth_date"])
	return hashlib.sha256(
		json.dumps([values, doc.requested_pathway], sort_keys=True, separators=(",", ":")).encode()
	).hexdigest()


def review_record(name, write=False):
	require_player_access()
	doc = frappe.get_doc("Sports Registration", name, for_update=write)
	doc.check_permission("write" if write else "read")
	validate_company(doc.company)
	return doc


@contextmanager
def acceptance_transaction():
	# User hooks queue work after commit. Drop only this operation's callbacks
	# along with its records if the final registration transition fails.
	frappe.db.savepoint("sports_acceptance")
	original = frappe.db.after_commit
	callbacks = CallbackManager()
	frappe.db.after_commit = callbacks
	try:
		yield
	except Exception:
		callbacks.reset()
		frappe.db.rollback(save_point="sports_acceptance")
		raise
	else:
		original.add(callbacks.run)
	finally:
		frappe.db.after_commit = original
