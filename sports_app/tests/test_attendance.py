from contextlib import contextmanager
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import attendance as policy
from sports_app import attendance_api as api


class TestAttendance(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, key, value in [
			(frappe, "throw", throw),
			(policy, "_", lambda s: s),
			(api, "_", lambda s: s),
		]:
			active = patch.object(target, key, value)
			active.start()
			self.addCleanup(active.stop)

	def row(self, status="Unmarked"):
		row = frappe._dict(
			status=status, modified="version-1", flags=frappe._dict(), save=Mock(), add_comment=Mock()
		)
		return row

	def test_identity_is_stable_and_distinct_per_session_player(self):
		self.assertEqual(policy.identity("S", "P"), policy.identity("S", "P"))
		self.assertNotEqual(policy.identity("S", "P"), policy.identity("S2", "P"))
		self.assertNotEqual(policy.identity("S", "P"), policy.identity("S", "P2"))

	def test_roster_uses_effective_active_enrollments_and_deduplicates(self):
		rows = [
			frappe._dict(
				name="E1", player="P1", status="Active", start_date="2026-01-01", end_date="2026-11-03"
			),
			frappe._dict(name="E2", player="P1", status="Active", start_date="2026-01-01"),
			frappe._dict(
				name="E3", player="P2", status="Active", start_date="2026-01-01", end_date="2026-11-02"
			),
			frappe._dict(name="E4", player="P3", status="Pending", start_date="2026-01-01"),
			frappe._dict(name="E5", player="P4", status="Active", start_date="2026-11-04"),
		]
		session = frappe._dict(company="Academy", program="Prog", group="Group", session_date="2026-11-03")
		with patch.object(frappe, "get_list", return_value=rows) as query:
			self.assertEqual(policy.eligible_roster(session), {"P1": "E1"})
			filters = query.call_args.kwargs["filters"]
			self.assertEqual(filters["company"], "Academy")
			self.assertEqual(filters["group"], "Group")
			self.assertEqual(filters["status"], "Active")

	def test_first_mark_attributes_actor_and_source_and_retry_is_noop(self):
		row = self.row()
		with (
			patch.object(policy, "now_datetime", return_value="now"),
			patch.object(frappe, "session", SimpleNamespace(user="operator")),
		):
			self.assertTrue(policy.mark_row(row, "Present", "version-1"))
			self.assertEqual((row.status, row.source, row.marked_by), ("Present", "Manual", "operator"))
			self.assertFalse(policy.mark_row(row, "Present", "stale"))
			row.save.assert_called_once()
			row.add_comment.assert_called_once()

	def test_corrections_require_reason_and_stale_change_is_rejected(self):
		row = self.row("Absent")
		with self.assertRaises(frappe.ValidationError):
			policy.mark_row(row, "Present", "version-1")
		with self.assertRaises(frappe.TimestampMismatchError):
			policy.mark_row(row, "Present", "stale", "Coach correction")
		row.save.assert_not_called()
		with (
			patch.object(policy, "now_datetime", return_value="now"),
			patch.object(frappe, "session", SimpleNamespace(user="operator")),
		):
			policy.mark_row(row, "Excused", "version-1", "Guardian notified coach")
			self.assertEqual(row.correction_reason, "Guardian notified coach")
			self.assertIn("Absent → Excused", row.add_comment.call_args.args[1])

	def test_invalid_status_and_long_correction_cannot_save(self):
		row = self.row("Present")
		for status, reason in [("Biometric", "x"), ("Unmarked", "x"), ("Absent", "x" * 1001)]:
			with self.subTest(status=status), self.assertRaises(frappe.ValidationError):
				policy.mark_row(row, status, "version-1", reason)
		row.save.assert_not_called()

	def test_forged_flag_and_finance_only_access_cannot_write(self):
		with patch.object(policy, "require_access"):
			for flag in (None, True, "CAPABILITY"):
				with self.subTest(flag=flag), self.assertRaises(frappe.PermissionError):
					policy.require_service(frappe._dict(flags=frappe._dict(sports_attendance_service=flag)))
		with (
			patch.object(policy, "require_player_access", side_effect=frappe.PermissionError),
			self.assertRaises(frappe.PermissionError),
		):
			policy.require_access()

	def test_cancelled_and_future_sessions_cannot_be_marked(self):
		for status, date in [("Cancelled", "2020-01-01"), ("Scheduled", "2099-01-01")]:
			with self.subTest(status=status), self.assertRaises(frappe.ValidationError):
				policy.ensure_markable(
					frappe._dict(status=status, session_date=date, timezone="Africa/Lagos")
				)

	def test_session_company_scope_is_checked_after_document_permission(self):
		doc = frappe._dict(company="Restricted", check_permission=Mock())
		with (
			patch.object(policy, "require_access"),
			patch.object(frappe, "get_doc", return_value=doc),
			patch.object(policy, "validate_company", side_effect=frappe.PermissionError),
			self.assertRaises(frappe.PermissionError),
		):
			policy.get_session("S")
		doc.check_permission.assert_called_once_with("read")

	def test_batch_transaction_rolls_back_on_failure(self):
		db = SimpleNamespace(savepoint=Mock(), rollback=Mock())
		with patch.object(frappe, "db", db), self.assertRaises(ValueError):
			with policy.transaction():
				raise ValueError("second row conflict")
		db.rollback.assert_called_once_with(save_point="sports_attendance")

	def test_endpoints_require_sports_access(self):
		with patch.object(policy, "require_access", side_effect=frappe.PermissionError):
			for fn, args in [
				(api.configuration, ()),
				(api.create_session, ({}, "x")),
				(api.list_sessions, ()),
				(api.roster, ("S",)),
				(api.save_attendance, ("S", [])),
				(api.finalize_session, ("S",)),
				(api.cancel_session, ("S", "reason")),
			]:
				with self.subTest(endpoint=fn.__name__), self.assertRaises(frappe.PermissionError):
					fn.__wrapped__(*args)

	def test_session_payload_rejects_server_owned_fields(self):
		with patch.object(policy, "require_access"):
			for values in [{"company": "Other"}, {"status": "Finalized"}, {"operator": "Administrator"}, []]:
				with self.subTest(values=values), self.assertRaises(frappe.ValidationError):
					api.create_session.__wrapped__(values, "x")

	def test_finalization_only_marks_unmarked_and_repeat_is_noop(self):
		session = frappe._dict(
			name="S",
			company="Academy",
			status="Scheduled",
			flags=frappe._dict(),
			save=Mock(),
			add_comment=Mock(),
		)
		row = frappe._dict(name="A", modified="v", check_permission=Mock())

		@contextmanager
		def tx():
			yield

		with (
			patch.object(policy, "get_session", return_value=session),
			patch.object(policy, "ensure_markable"),
			patch.object(policy, "transaction", tx),
			patch.object(frappe, "get_list", return_value=[frappe._dict(name="A")]) as query,
			patch.object(frappe, "get_doc", return_value=row),
			patch.object(policy, "mark_row") as mark,
			patch.object(api, "roster", return_value={}),
			patch.object(api, "now_datetime", return_value="now"),
			patch.object(frappe, "session", SimpleNamespace(user="operator")),
		):
			api.finalize_session.__wrapped__("S")
			self.assertEqual(query.call_args.kwargs["filters"]["status"], "Unmarked")
			mark.assert_called_once_with(row, "Absent", "v", source="Finalization")
			self.assertEqual(session.status, "Finalized")
			api.finalize_session.__wrapped__("S")
			self.assertEqual(mark.call_count, 1)
