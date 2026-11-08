from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import billing_policy
from sports_app import subscription_payments as subscriptions


class TestSubscriptionPayments(TestCase):
	def setUp(self):
		for target, replacement in [("_", lambda value: value)]:
			item = patch.object(subscriptions, target, replacement)
			item.start()
			self.addCleanup(item.stop)
		item = patch.object(billing_policy, "_", lambda value: value)
		item.start()
		self.addCleanup(item.stop)

		def fail(message, error=frappe.ValidationError):
			raise error(message)

		item = patch.object(frappe, "throw", fail)
		item.start()
		self.addCleanup(item.stop)
		self.row = dict(enrollment="ENR", month="2026-11", source_hash="hash", outstanding="40000")

	def test_selection_requires_unique_scalar_month_cells_and_bounded_batch(self):
		self.assertEqual(subscriptions.parse_rows([self.row]), [self.row])
		for rows in [
			[],
			[self.row] * 2,
			[self.row] * 21,
			[{**self.row, "player": "OTHER"}],
			[{**self.row, "enrollment": []}],
			[{**self.row, "month": "2026-13"}],
			[{**self.row, "outstanding": "NaN"}],
		]:
			with self.assertRaises(frappe.ValidationError):
				subscriptions.parse_rows(rows)

	def test_year_filter_rejects_invalid_or_unbounded_values(self):
		self.assertEqual(subscriptions.selected_year("2026"), 2026)
		for value in ["bad", 1999, 2100, "2026-01"]:
			with self.assertRaises(frappe.ValidationError):
				subscriptions.selected_year(value)

	def test_native_accounting_permissions_required_before_finance_queries(self):
		with (
			patch.object(subscriptions, "require_billing"),
			patch.object(frappe, "has_permission", return_value=False),
		):
			with self.assertRaises(frappe.PermissionError):
				subscriptions.require_finance(("Payment Entry", "submit"))

	def test_paid_to_rejects_cross_company_currency_disabled_and_group_accounts(self):
		settings = frappe._dict(company="Academy", currency="NGN")
		bank = frappe._dict(
			company="Academy",
			account_currency="NGN",
			account_type="Bank",
			disabled=0,
			is_group=0,
			check_permission=Mock(),
		)
		with patch.object(frappe, "get_doc", return_value=bank):
			self.assertIs(subscriptions.bank_account("BANK", settings), bank)
			for key, value in [
				("company", "Other"),
				("account_currency", "USD"),
				("account_type", "Receivable"),
				("disabled", 1),
				("is_group", 1),
			]:
				original = bank[key]
				bank[key] = value
				with self.assertRaises(frappe.ValidationError):
					subscriptions.bank_account("BANK", settings)
				bank[key] = original

	def test_month_query_uses_text_values_and_company_and_enrollment_scope(self):
		with patch.object(frappe, "get_list", side_effect=[[], []]) as query:
			subscriptions.invoices_for(frappe._dict(company="Academy"), ["E"], 2026)
			filters = query.call_args_list[0].kwargs["filters"]
			self.assertEqual(filters["company"], "Academy")
			self.assertEqual(filters["enrollment"], ["in", ["E"]])
			self.assertEqual(filters["billing_month"][0], "in")
			self.assertEqual(len(filters["billing_month"][1]), 12)

	def test_ordinary_payment_is_untouched_by_sports_hook(self):
		doc = frappe._dict(get_doc_before_save=lambda: None)
		with patch.object(subscriptions, "require_billing") as guard:
			subscriptions.validate_payment(doc)
			guard.assert_not_called()

	def test_provenance_cannot_be_removed_or_injected_on_new_native_payment(self):
		old = frappe._dict(sports_billing_obligation="OBL", sports_subscription_request="KEY")
		doc = frappe._dict(get_doc_before_save=lambda: old)
		with self.assertRaises(frappe.ValidationError):
			subscriptions.validate_payment(doc)
		doc = frappe._dict(
			sports_billing_obligation="OBL",
			get_doc_before_save=lambda: None,
			is_new=lambda: True,
			flags=frappe._dict(),
		)
		with self.assertRaises(frappe.PermissionError):
			subscriptions.validate_payment(doc)

	def test_reversal_requires_reason_and_native_cancellation(self):
		with patch.object(subscriptions, "require_finance"), patch.object(frappe, "get_doc") as get:
			with self.assertRaises(frappe.ValidationError):
				subscriptions.reverse.__wrapped__(["REC"], "")
			get.assert_not_called()
		payment = Mock()
		payment.get.return_value = None
		with (
			patch.object(subscriptions, "require_finance"),
			patch.object(frappe, "get_doc", return_value=payment),
			patch.object(subscriptions, "acceptance_transaction"),
		):
			with self.assertRaises(frappe.ValidationError):
				subscriptions.reverse.__wrapped__(["ENROLLMENT-RECEIPT"], "Correction")
			payment.check_permission.assert_any_call("cancel")

	def test_grid_preview_restores_message_flag_after_expected_exception(self):
		with (
			patch.object(frappe, "flags", frappe._dict(mute_messages=False)),
			patch.object(subscriptions, "build", side_effect=frappe.ValidationError("Missing plan")),
		):
			with self.assertRaises(frappe.ValidationError):
				subscriptions.preview_charge("ENR", "2026-11")
			self.assertFalse(frappe.flags.mute_messages)

	def test_invoice_only_action_supports_historical_month_without_receipt(self):
		from datetime import date

		with (
			patch.object(subscriptions, "require_finance", return_value=frappe._dict()),
			patch.object(subscriptions, "academy_date", return_value=date(2026, 11, 7)),
			patch.object(
				subscriptions, "generate_rows", return_value=[dict(sales_invoice="INV", state="Unpaid")]
			) as generate,
			patch.object(subscriptions, "make_payment") as payment,
		):
			row = dict(self.row, month="2026-01")
			result = subscriptions.generate_invoices.__wrapped__([row])
			self.assertEqual(result[0]["sales_invoice"], "INV")
			generate.assert_called_once_with("2026-01", [{"enrollment": "ENR", "source_hash": "hash"}])
			payment.assert_not_called()

	def test_invoice_only_action_rejects_future_before_generation(self):
		from datetime import date

		with (
			patch.object(subscriptions, "require_finance", return_value=frappe._dict()),
			patch.object(subscriptions, "academy_date", return_value=date(2026, 11, 7)),
			patch.object(subscriptions, "generate_rows") as generate,
		):
			with self.assertRaises(frappe.ValidationError):
				subscriptions.generate_invoices.__wrapped__([dict(self.row, month="2026-12")])
			generate.assert_not_called()

	def test_payment_checkbox_never_creates_a_missing_invoice(self):
		from contextlib import nullcontext
		from datetime import date

		with (
			patch.object(subscriptions, "require_finance", return_value=frappe._dict()),
			patch.object(subscriptions, "academy_date", return_value=date(2026, 11, 7)),
			patch.object(subscriptions, "bank_account", return_value=frappe._dict(name="BANK")),
			patch.object(
				subscriptions, "enrollment_record", return_value=(frappe._dict(name="ENR"), frappe._dict())
			),
			patch.object(subscriptions, "existing", return_value=None),
			patch.object(subscriptions, "acceptance_transaction", side_effect=lambda: nullcontext()),
			patch.object(frappe, "session", frappe._dict(user="Finance")),
			patch.object(frappe, "db", Mock(get_value=Mock(return_value=None))),
			patch.object(subscriptions, "generate_rows") as generate,
			patch.object(subscriptions, "make_payment") as receipt,
		):
			result = subscriptions.pay.__wrapped__(
				[dict(self.row, month="2026-10")],
				"BANK",
				"2026-11-07",
				"",
				"bce0831d-a36a-4d51-9174-749c0f42513a",
			)
			self.assertEqual(result[0]["state"], "Exception")
			generate.assert_not_called()
			receipt.assert_not_called()
