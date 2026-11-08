import json
from types import ModuleType, SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import enrollment_invoices as invoices


class Invoice(SimpleNamespace):
	def get(self, key, default=None):
		return getattr(self, key, default)


class TestEnrollmentInvoiceGuards(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		active = patch.object(frappe, "throw", throw)
		active.start()
		self.addCleanup(active.stop)
		active = patch.object(invoices, "_", lambda s: s)
		active.start()
		self.addCleanup(active.stop)
		self.line = frappe._dict(
			item_code="Fee",
			income_account="Income",
			cost_center="Main",
			uom="Nos",
			qty=1,
			rate=250000,
			amount=250000,
		)
		self.app = frappe._dict(
			sales_invoice="INV",
			payment_customer="CUSTOMER",
			company="Academy",
			status="Pending",
			payment_snapshot=json.dumps(
				dict(currency="NGN", paid_from="Debtors", total=250000, items=[dict(self.line)])
			),
		)

	def test_configurable_quantity_snapshot_and_fractional_tampering(self):
		self.line.qty = 2
		self.line.rate = 125000
		self.app.payment_snapshot = json.dumps(
			dict(currency="NGN", paid_from="Debtors", total=250000, items=[dict(self.line)])
		)
		with patch.object(frappe, "get_doc", return_value=self.app):
			invoices.validate_enrollment_invoice(self.invoice())
			bad = self.invoice()
			bad.items[0].qty = 2.0001
			with self.assertRaises(frappe.ValidationError):
				invoices.validate_enrollment_invoice(bad)

	def invoice(self, **changes):
		doc = frappe._dict(
			name="INV",
			sports_registration="REG",
			customer="CUSTOMER",
			company="Academy",
			currency="NGN",
			debit_to="Debtors",
			grand_total=250000,
			conversion_rate=1,
			items=[self.line.copy()],
			taxes=[],
			advances=[],
			is_return=0,
			is_pos=0,
			update_stock=0,
			discount_amount=0,
			additional_discount_percentage=0,
			write_off_amount=0,
			flags=frappe._dict(),
		)
		doc.update(changes)
		return Invoice(**doc)

	def test_invoice_party_company_amount_currency_and_offsets_cannot_change(self):
		with patch.object(invoices.frappe, "get_doc", return_value=self.app):
			invoices.validate_enrollment_invoice(self.invoice())
			for change in [
				dict(customer="OTHER"),
				dict(company="OTHER"),
				dict(name="OTHER"),
				dict(currency="USD"),
				dict(grand_total=1),
				dict(debit_to="Other"),
				dict(conversion_rate=2),
				dict(discount_amount=1),
				dict(write_off_amount=1),
				dict(taxes=[{}]),
				dict(advances=[{}]),
				dict(is_pos=1),
				dict(is_return=1),
			]:
				with self.subTest(change=change), self.assertRaises(frappe.ValidationError):
					invoices.validate_enrollment_invoice(self.invoice(**change))

	def test_each_fee_line_is_locked_including_account_cost_center_qty_and_rate(self):
		with patch.object(invoices.frappe, "get_doc", return_value=self.app):
			for key, value in [
				("item_code", "Other"),
				("income_account", "Other"),
				("cost_center", "Other"),
				("uom", "Other"),
				("qty", 2),
				("rate", 1),
				("amount", 1),
			]:
				row = self.line.copy()
				row[key] = value
				with self.subTest(field=key), self.assertRaises(frappe.ValidationError):
					invoices.validate_enrollment_invoice(self.invoice(items=[row]))
			with self.assertRaises(frappe.ValidationError):
				invoices.validate_enrollment_invoice(self.invoice(items=[]))

	def test_boolean_flag_does_not_allow_forged_factory_and_unrelated_invoices_unchanged(self):
		with patch.object(invoices.frappe, "get_doc", return_value=self.app):
			with self.assertRaises(frappe.ValidationError):
				invoices.validate_enrollment_invoice(
					self.invoice(customer="OTHER", flags=frappe._dict(sports_invoice_service=True))
				)
		invoices.validate_enrollment_invoice(frappe._dict(sports_registration=None))

	def test_guest_and_registrar_cannot_complete_financials(self):
		self.assertFalse(invoices.can_complete_payment("Guest"))
		with (
			patch.object(frappe, "get_roles", return_value=["Sports Registrar"]),
			patch.object(frappe, "has_permission", return_value=True),
		):
			self.assertFalse(invoices.can_complete_payment("registrar@example.invalid"))

	def test_finance_role_needs_both_invoice_and_payment_permissions(self):
		with (
			patch.object(frappe, "get_roles", return_value=["Accounts Manager"]),
			patch.object(frappe, "get_installed_apps", return_value=[]),
		):
			with patch.object(
				frappe,
				"has_permission",
				side_effect=lambda dt, p, user=None: not (dt == "Payment Entry" and p == "submit"),
			):
				self.assertFalse(invoices.can_complete_payment("finance@example.invalid"))
			with patch.object(frappe, "has_permission", return_value=True):
				self.assertTrue(invoices.can_complete_payment("finance@example.invalid"))

	def test_boost_approver_configuration_is_not_bypassed_for_administrator(self):
		# Boost is optional: this contract test must also run on a Sports-only bench.
		boost_api = ModuleType("erp_boost.api")
		boost_api.is_valid_invoice_approver = Mock(return_value=False)
		boost_api.is_valid_payment_entry_approver = Mock(return_value=True)
		boost = ModuleType("erp_boost")
		boost.__path__ = []
		boost.api = boost_api
		with (
			patch.object(frappe, "get_roles", return_value=["System Manager"]),
			patch.object(frappe, "has_permission", return_value=True),
			patch.object(frappe, "get_installed_apps", return_value=["erp_boost"]),
			patch.dict("sys.modules", {"erp_boost": boost, "erp_boost.api": boost_api}),
		):
			self.assertFalse(invoices.can_complete_payment("Administrator"))

	def test_financial_provenance_cannot_be_removed(self):
		previous = frappe._dict(sports_registration="REG")
		doc = self.invoice(sports_registration=None, get_doc_before_save=lambda: previous)
		with self.assertRaises(frappe.ValidationError):
			invoices.validate_enrollment_invoice(doc)

	def test_unrelated_invoice_submission_does_not_create_sports_receipts(self):
		doc = frappe._dict(sports_registration=None)
		with patch.object(
			frappe, "get_doc", side_effect=AssertionError("Unrelated accounting must not be touched")
		):
			invoices.validate_finance_submission(doc)
			invoices.record_invoice_payment(doc)

	def test_bad_token_cannot_distinguish_existing_and_missing_invoice_references(self):
		fake = SimpleNamespace(
			db=SimpleNamespace(get_value=Mock(return_value=None)),
			get_doc=Mock(return_value=frappe._dict(request_key="different")),
			throw=frappe.throw,
			PermissionError=frappe.PermissionError,
		)
		errors = []
		with (
			patch.object(invoices, "frappe", fake),
			patch.object(invoices, "intake_settings"),
			patch.object(invoices, "request_uuid", return_value="valid-token"),
		):
			for name in (None, "REG"):
				fake.db.get_value.return_value = name
				with self.assertRaises(frappe.PermissionError) as caught:
					invoices.claim_invoice("INV", "valid-token")
				errors.append(str(caught.exception))
		self.assertEqual(errors, ["Invalid payment reference or registration token."] * 2)


class TestCompletionMenuAccess(TestCase):
	def test_only_pending_review_sports_invoice_with_finance_and_workflow_access(self):
		doc = Invoice(
			sports_registration="REG",
			docstatus=0,
			workflow_state="Pending Review",
			company="Academy",
			check_permission=Mock(),
		)
		with (
			patch.object(frappe, "get_doc", return_value=doc),
			patch.object(invoices, "validate_company"),
			patch.object(invoices, "can_complete_payment", return_value=True) as finance,
			patch.object(frappe, "db", SimpleNamespace(get_value=Mock(return_value="Pending"))) as db,
			patch(
				"frappe.model.workflow.get_transitions",
				return_value=[frappe._dict(action="Complete Payment")],
			) as transitions,
		):
			self.assertTrue(invoices.completion_access.__wrapped__("INV"))
			doc.check_permission.assert_called_with("read")
			for field, value in [
				("docstatus", 1),
				("docstatus", 2),
				("workflow_state", "Draft"),
				("sports_registration", None),
			]:
				original = getattr(doc, field)
				setattr(doc, field, value)
				self.assertFalse(invoices.completion_access.__wrapped__("INV"))
				setattr(doc, field, original)
			finance.return_value = False
			self.assertFalse(invoices.completion_access.__wrapped__("INV"))
			finance.return_value = True
			db.get_value.return_value = "Rejected"
			self.assertFalse(invoices.completion_access.__wrapped__("INV"))
			db.get_value.return_value = "Pending"
			transitions.return_value = []
			self.assertFalse(invoices.completion_access.__wrapped__("INV"))
