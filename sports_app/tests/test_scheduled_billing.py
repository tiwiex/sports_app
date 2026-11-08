from contextlib import nullcontext
from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import monthly_billing
from sports_app import scheduled_billing as scheduled


class TestScheduledBilling(TestCase):
	def setUp(self):
		self.settings = frappe._dict(
			company="Academy",
			monthly_fees_enabled=1,
			automatic_monthly_billing=1,
			monthly_billing_start="2026-11-01",
			monthly_billing_user="Finance",
		)
		self.patches = [
			patch.object(scheduled, "_", lambda value: value),
			patch.object(monthly_billing, "_", lambda value: value),
			patch.object(scheduled, "get_configured_settings", return_value=self.settings),
			patch.object(scheduled, "require_billing", return_value=self.settings),
			patch.object(scheduled, "validate_configuration"),
			patch.object(scheduled, "acceptance_transaction", side_effect=lambda: nullcontext()),
			patch.object(scheduled, "enrollment_record"),
			patch.object(frappe, "has_permission", return_value=True),
			patch.object(frappe, "set_user"),
			patch.object(frappe, "session", frappe._dict(user="Finance")),
			patch.object(scheduled, "academy_date", return_value=date(2026, 11, 7)),
		]
		for item in self.patches:
			item.start()
			self.addCleanup(item.stop)

	def test_completed_months_catch_up_from_enrollment_not_legacy_start(self):
		self.assertEqual(list(scheduled.months(self.settings, "2026-09-01")), ["2026-09", "2026-10"])
		self.assertEqual(len(list(scheduled.months(self.settings, "2026-01-01"))), 10)
		self.assertEqual(list(scheduled.months(self.settings, "2026-11-01")), [])
		self.assertEqual(list(scheduled.months(self.settings, "2026-12-01")), [])

	def test_month_end_boundary_and_year_rollover(self):
		with patch.object(scheduled, "academy_date", return_value=date(2027, 1, 1)):
			self.assertEqual(list(scheduled.months(self.settings, "2026-11-01")), ["2026-11", "2026-12"])

	def test_enrollment_change_requests_background_catchup_after_commit(self):
		with patch.object(frappe, "enqueue") as enqueue:
			scheduled.request_catchup()
			self.assertTrue(enqueue.call_args.kwargs["enqueue_after_commit"])
			self.assertTrue(enqueue.call_args.kwargs["deduplicate"])
			self.settings.automatic_monthly_billing = 0
			enqueue.reset_mock()
			scheduled.request_catchup()
			enqueue.assert_not_called()

	def test_disabled_switches_never_query_or_generate(self):
		with patch.object(frappe, "get_list") as query:
			self.settings.automatic_monthly_billing = 0
			self.assertIsNone(scheduled.run())
			self.settings.automatic_monthly_billing = 1
			self.settings.monthly_fees_enabled = 0
			self.assertIsNone(scheduled.run())
			query.assert_not_called()

	def test_existing_invoice_resumed_without_repricing_and_actor_restored(self):
		old = frappe._dict(sales_invoice="INV")
		with (
			patch.object(
				frappe, "get_list", return_value=[frappe._dict(name="ENR", start_date="2026-10-01")]
			) as query,
			patch.object(scheduled, "existing", return_value=old),
			patch.object(scheduled, "submit_obligation") as resume,
			patch.object(scheduled, "build") as build,
		):
			self.assertEqual(scheduled.run(), {"failed": 0})
			resume.assert_called_once_with(old)
			build.assert_not_called()
			self.assertEqual(query.call_args.kwargs["filters"]["status"], "Active")
			self.assertEqual(query.call_args.kwargs["filters"]["company"], "Academy")
			frappe.set_user.assert_called_with("Finance")

	def test_failed_row_logs_key_without_reason_and_next_row_continues(self):
		with (
			patch.object(
				frappe,
				"get_list",
				return_value=[
					frappe._dict(name="BAD", start_date="2026-10-01"),
					frappe._dict(name="OK", start_date="2026-10-01"),
				],
			),
			patch.object(scheduled, "existing", return_value=None),
			patch.object(
				scheduled, "build", side_effect=[ValueError("private reason"), ({"source_hash": "h"}, {})]
			),
			patch.object(scheduled, "generate_rows", return_value=[{"state": "Unpaid"}]) as generate,
			patch.object(frappe, "log_error") as log,
		):
			self.assertEqual(scheduled.run(), {"failed": 1})
			generate.assert_called_once()
			self.assertIn("BAD", log.call_args.kwargs["message"])
			self.assertNotIn("private reason", log.call_args.kwargs["message"])

	def test_ended_enrollment_skipped(self):
		with (
			patch.object(
				frappe,
				"get_list",
				return_value=[frappe._dict(name="END", start_date="2026-10-01", end_date="2026-09-30")],
			),
			patch.object(scheduled, "existing") as existing,
		):
			self.assertEqual(scheduled.run(), {"failed": 0})
			existing.assert_not_called()

	def test_native_submit_permission_required_even_for_scheduler(self):
		with (
			patch.object(frappe, "has_permission", return_value=False),
			patch.object(frappe, "throw", side_effect=frappe.PermissionError),
			patch.object(frappe, "get_list") as query,
		):
			with self.assertRaises(frappe.PermissionError):
				scheduled.run()
			query.assert_not_called()
			frappe.set_user.assert_called_with("Finance")

	def test_cancelled_obligation_never_replaced(self):
		invoice = Mock(docstatus=2)
		with (
			patch.object(frappe, "get_doc", return_value=invoice),
			patch.object(frappe, "throw", side_effect=frappe.ValidationError),
			patch.object(monthly_billing, "submit_invoice") as submit,
		):
			with self.assertRaises(frappe.ValidationError):
				monthly_billing.submit_obligation(frappe._dict(sales_invoice="CANCELLED"))
			submit.assert_not_called()

	def test_submitted_obligation_never_reposted(self):
		with (
			patch.object(frappe, "get_doc", return_value=Mock(docstatus=1)),
			patch.object(monthly_billing, "submit_invoice") as submit,
		):
			monthly_billing.submit_obligation(frappe._dict(sales_invoice="POSTED"))
			submit.assert_not_called()
