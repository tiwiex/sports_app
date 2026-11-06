from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

import frappe

from sports_app import player_ids as service


class TestPlayerIDCorrections(TestCase):
	def setUp(self):
		def throw(message, error=frappe.ValidationError):
			raise error(message)

		for name, value in [
			("_", lambda value: value),
			("now_datetime", lambda: "2026-11-06 12:00:00"),
			("require_settings_access", Mock()),
			("validate_company", Mock()),
			(
				"registration_settings",
				Mock(return_value=frappe._dict(company="Academy", registration_prefix="MSA")),
			),
		]:
			active = patch.object(service, name, value)
			active.start()
			self.addCleanup(active.stop)
		active = patch.object(frappe, "throw", throw)
		active.start()
		self.addCleanup(active.stop)
		self.key = str(uuid4())
		self.doc = frappe._dict(
			name="OLD",
			company="Academy",
			modified="v1",
			check_permission=Mock(),
			has_permission=Mock(return_value=True),
		)
		self.db = SimpleNamespace(
			get_value=Mock(return_value=None),
			exists=Mock(return_value=False),
			savepoint=Mock(),
			rollback=Mock(),
			after_commit=frappe.utils.CallbackManager(),
		)
		for name, value in [
			("db", self.db),
			("enqueue", Mock()),
			("get_doc", Mock(return_value=self.doc)),
			("session", frappe._dict(user="Administrator")),
		]:
			active = patch.object(frappe, name, value)
			active.start()
			self.addCleanup(active.stop)

	def invoke(self, **changes):
		values = dict(
			name="OLD",
			new_id="NEW-ID",
			reason="Legacy roster correction",
			modified="v1",
			request_key=self.key,
		)
		values.update(changes)
		return service.change_player_id.__wrapped__(**values)

	def test_role_scope_revision_and_duplicate_guards(self):
		with (
			patch.object(service, "require_settings_access", side_effect=frappe.PermissionError),
			self.assertRaises(frappe.PermissionError),
		):
			self.invoke()
		self.doc.company = "Other"
		with self.assertRaises(frappe.ValidationError):
			self.invoke()
		self.doc.company = "Academy"
		with self.assertRaises(frappe.TimestampMismatchError):
			self.invoke(modified="stale")
		self.db.exists.return_value = True
		with self.assertRaises(frappe.ValidationError):
			self.invoke()
		self.db.savepoint.assert_not_called()

	def test_invalid_ids_reason_and_request_rejected(self):
		for changes in [
			dict(new_id="../bad"),
			dict(new_id=" OLD "),
			dict(new_id="old"),
			dict(reason=" "),
			dict(reason="x" * 1001),
			dict(request_key="bad"),
		]:
			with self.subTest(changes=changes), self.assertRaises(frappe.ValidationError):
				self.invoke(**changes)
		self.db.savepoint.assert_not_called()

	def test_native_rename_and_merge_require_server_context(self):
		for merge in [False, True]:
			with self.assertRaises(frappe.PermissionError):
				service.check_rename(self.doc, "OLD", "NEW-ID", merge)
		token = service._context.set(dict(old_player_id="OLD", new_player_id="NEW-ID", company="Academy"))
		try:
			service.check_rename(self.doc, "OLD", "NEW-ID")
			with self.assertRaises(frappe.PermissionError):
				service.check_rename(self.doc, "OLD", "NEW-ID", True)
		finally:
			service._context.reset(token)

	def test_retry_is_same_actor_payload_and_current_scope(self):
		self.db.get_value.return_value = frappe._dict(
			player="CURRENT",
			request_hash=service._payload("OLD", "NEW-ID", "Legacy roster correction", "v1", self.key),
			changed_by="Administrator",
		)
		self.doc.name = "CURRENT"
		self.assertEqual(self.invoke(), "CURRENT")
		with self.assertRaises(frappe.ValidationError):
			self.invoke(reason="Changed payload")
		self.db.savepoint.assert_not_called()

	def test_failure_rolls_back_and_restores_callback_and_context(self):
		original = self.db.after_commit
		with (
			patch.object(service, "ensure_counter"),
			patch.object(service, "_lock_attendance", return_value=[]),
			patch.object(frappe, "rename_doc", side_effect=RuntimeError("failure")),
		):
			with self.assertRaises(RuntimeError):
				self.invoke()
		self.db.rollback.assert_called_once_with(save_point="sports_player_id_change")
		self.assertIs(self.db.after_commit, original)
		self.assertIsNone(service._context.get())

	def test_audit_and_retired_id_cannot_be_forged_or_reused(self):
		with self.assertRaises(frappe.PermissionError):
			service.check_audit(frappe._dict())
		with self.assertRaises(frappe.PermissionError):
			service.prevent_audit_change()
		self.db.get_value.return_value = "AUDIT"
		with self.assertRaises(frappe.ValidationError):
			service.validate_new_player_id("RETIRED")

	def test_roster_locks_precede_native_rename_and_identity_repair(self):
		events = []
		self.doc.db_set = Mock()
		self.doc.insert = Mock()
		with (
			patch.object(service, "ensure_counter"),
			patch.object(service, "_lock_attendance", side_effect=lambda old: events.append("lock") or []),
			patch.object(frappe, "rename_doc", side_effect=lambda *a, **k: events.append("rename")),
			patch.object(service, "_update_attendance", side_effect=lambda *a: events.append("repair")),
		):
			self.assertEqual(self.invoke(), "NEW-ID")
		self.assertEqual(events, ["lock", "rename", "repair"])
		self.doc.insert.assert_called_once_with(ignore_permissions=True)
