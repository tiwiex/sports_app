"""Audited, management-only player ID corrections; no general rename/merge permission."""

import hashlib
import json
import re
from contextvars import ContextVar
from uuid import UUID

import frappe
from frappe import _
from frappe.utils import CallbackManager, now_datetime

from sports_app.academy import can_manage_settings, require_settings_access, validate_company
from sports_app.player_numbering import ensure_counter, legacy_sequence
from sports_app.players import registration_settings

AUDIT = "Sports Player ID Change"
_context = ContextVar("sports_player_id_change", default=None)


def can_change(doc):
	return bool(can_manage_settings() and doc.has_permission("write"))


def reserved(name):
	return bool(
		frappe.db.get_value(AUDIT, {"old_player_id": name}, "name", for_update=True, order_by="name")
		or frappe.db.get_value(AUDIT, {"new_player_id": name}, "name", for_update=True, order_by="name")
	)


def validate_new_player_id(name):
	if reserved(name):
		frappe.throw(_("This player ID is reserved in the ID change history. Use a new ID."))


def check_rename(doc, old, new, merge=False):
	require_settings_access()
	context = _context.get()
	if (
		merge
		or not context
		or (old, new, doc.company) != (context["old_player_id"], context["new_player_id"], context["company"])
	):
		frappe.throw(
			_("Use Change Player ID with a reason. Players cannot be merged."), frappe.PermissionError
		)
	doc.check_permission("write")
	validate_company(doc.company)


def check_audit(doc):
	context = _context.get()
	if not context or not doc.is_new() or any(doc.get(key) != value for key, value in context.items()):
		frappe.throw(
			_("Player ID change history is maintained by the correction service."), frappe.PermissionError
		)


def prevent_audit_change(*args, **kwargs):
	frappe.throw(_("Player ID change history cannot be edited, deleted or renamed."), frappe.PermissionError)


def _payload(name, new_id, reason, modified, request_key):
	if not isinstance(new_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{1,139}", new_id):
		frappe.throw(
			_(
				"Use a player ID of 2-140 letters, digits, hyphens or underscores, starting with a letter or digit."
			)
		)
	if not isinstance(reason, str) or not reason.strip() or len(reason) > 1000:
		frappe.throw(_("Enter a reason of up to 1000 characters for changing the player ID."))
	try:
		if str(UUID(request_key, version=4)) != request_key:
			raise ValueError
	except (ValueError, TypeError, AttributeError):
		frappe.throw(_("Invalid ID change request. Refresh and retry."))
	if not modified or not isinstance(name, str) or name.casefold() == new_id.casefold():
		frappe.throw(_("Enter a different player ID and refresh the current player record."))
	return hashlib.sha256(json.dumps([name, new_id, reason.strip(), str(modified)]).encode()).hexdigest()


def _lock_attendance(old):
	# Lock BEFORE native rename updates Links. Keep the
	# same order as attendance saves: session first, then individual roster rows.
	rows = frappe.get_all(
		"Sports Attendance", filters={"player": old}, fields=["name", "session"], order_by="session, name"
	)
	for session in sorted({row.session for row in rows}):
		frappe.get_doc("Sports Session", session, for_update=True)
	for row in rows:
		frappe.get_doc("Sports Attendance", row.name, for_update=True)
	return rows


def _update_attendance(new, rows):
	from sports_app.attendance import identity

	for row in rows:
		doc = frappe.get_doc("Sports Attendance", row.name)
		doc.db_set("identity", identity(doc.session, new), notify=True)


@frappe.whitelist(methods=["POST"])
def change_player_id(name: str, new_id: str, reason: str, modified: str, request_key: str):
	require_settings_access()
	digest = _payload(name, new_id, reason, modified, request_key)
	settings = registration_settings(for_update=True)
	existing = frappe.db.get_value(
		AUDIT,
		{"request_key": request_key},
		["player", "request_hash", "changed_by"],
		as_dict=True,
		for_update=True,
	)
	if existing:
		doc = frappe.get_doc("Sports Player", existing.player)
		doc.check_permission("write")
		validate_company(doc.company)
		if (
			doc.company != settings.company
			or existing.request_hash != digest
			or existing.changed_by != frappe.session.user
		):
			frappe.throw(_("This ID change request was already used with different details."))
		return doc.name
	doc = frappe.get_doc("Sports Player", name, for_update=True)
	doc.check_permission("write")
	validate_company(doc.company)
	if doc.company != settings.company:
		frappe.throw(_("Player company must match the academy company."))
	if str(doc.modified) != str(modified):
		frappe.throw(_("Player changed. Refresh before changing the ID."), frappe.TimestampMismatchError)
	if frappe.db.exists("Sports Player", new_id) or reserved(new_id):
		frappe.throw(_("This player ID is already in use or reserved. Choose a new ID."))
	context = dict(
		old_player_id=name,
		new_player_id=new_id,
		player=new_id,
		company=doc.company,
		reason=reason.strip(),
		changed_by=frappe.session.user,
		changed_on=now_datetime(),
		request_key=request_key,
		request_hash=digest,
	)
	frappe.db.savepoint("sports_player_id_change")
	original_callbacks = frappe.db.after_commit
	callbacks = CallbackManager()
	frappe.db.after_commit = callbacks
	token = _context.set(context)
	try:
		# Reserve both old and corrected references without decreasing/restarting the counter.
		ensure_counter(
			settings, max(legacy_sequence(name.upper(), settings), legacy_sequence(new_id.upper(), settings))
		)
		attendance = _lock_attendance(name)
		frappe.rename_doc(
			"Sports Player",
			name,
			new_id,
			force=True,
			merge=False,
			show_alert=False,
			rebuild_search=False,
		)
		_update_attendance(new_id, attendance)
		renamed = frappe.get_doc("Sports Player", new_id)
		renamed.db_set("modified", context["changed_on"], notify=True)
		frappe.get_doc({"doctype": AUDIT, **context}).insert(ignore_permissions=True)
		frappe.enqueue(
			"frappe.utils.global_search.rebuild_for_doctype",
			doctype="Sports Player",
			enqueue_after_commit=True,
		)
		# The native rename comment records old/new; this structured, read-only record
		# also preserves reason, operator, timestamp and idempotent request identity.
	except Exception:
		callbacks.reset()
		frappe.db.rollback(save_point="sports_player_id_change")
		raise
	else:
		original_callbacks.add(callbacks.run)
	finally:
		_context.reset(token)
		frappe.db.after_commit = original_callbacks
	return new_id
