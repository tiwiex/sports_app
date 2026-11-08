from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import billing_access as access
from sports_app import billing_api, fee_plans, monthly_billing, scholarships
from sports_app import billing_policy as policy


class TestSportsBilling(TestCase):
	def setUp(self):
		def fail(message, error=frappe.ValidationError):
			raise error(message)

		for module in [policy, access, fee_plans, monthly_billing, scholarships]:
			p = patch.object(module, "_", lambda text: text)
			p.start()
			self.addCleanup(p.stop)
		p = patch.object(frappe, "throw", fail)
		p.start()
		self.addCleanup(p.stop)
		self.enrollment = frappe._dict(
			name="ENR",
			player="PLAYER",
			company="Academy",
			program="PROG",
			payer_customer="CUSTOMER",
			start_date="2026-01-01",
			end_date=None,
			status="Active",
			modified="e1",
		)
		self.plan = frappe._dict(
			name="PLAN",
			company="Academy",
			program="PROG",
			monthly_amount=40000,
			currency="NGN",
			due_day=7,
			effective_from="2026-01-01",
			effective_to=None,
			joining_policy="Full fee if active at month start",
			modified="p1",
		)
		self.decision = frappe._dict(
			name="SECRET",
			modified="d1",
			effective_from="2026-01-01",
			effective_to=None,
			coverage_type="Full",
			coverage_value=100,
			reason="Secret reason",
		)

	def test_month_dates_and_invalid_month(self):
		self.assertEqual(policy.period("2028-02"), (date(2028, 2, 1), date(2028, 2, 29)))
		for value in ["2026-13", "2026-1", "2026-00", "x", None]:
			with self.assertRaises(frappe.ValidationError):
				policy.period(value)

	def test_amounts_reject_negative_nonfinite_or_huge(self):
		for value in [-1, "NaN", "Infinity", "bad", 1e20, None]:
			with self.assertRaises(frappe.ValidationError):
				policy.money(value)
		self.assertEqual(policy.money("10.005"), Decimal("10.01"))

	def test_full_fee_at_month_start_no_midmonth_join_charge(self):
		value = policy.charge(self.enrollment, self.plan, [], "2026-11")
		self.assertEqual(value["amount"], "40000.00")
		self.assertEqual(value["due_date"], "2026-11-07")
		self.enrollment.start_date = "2026-11-02"
		self.assertIsNone(policy.charge(self.enrollment, self.plan, [], "2026-11"))
		self.enrollment.start_date = "2026-11-01"
		self.enrollment.end_date = "2026-11-03"
		self.assertEqual(policy.charge(self.enrollment, self.plan, [], "2026-11")["amount"], "40000.00")

	def test_no_charge_pending_withdrawn_or_ended(self):
		for status in ["Pending", "Withdrawn", "Completed"]:
			self.enrollment.status = status
			self.assertIsNone(policy.charge(self.enrollment, self.plan, [], "2026-11"))
		self.enrollment.status = "Active"
		self.enrollment.end_date = "2026-10-31"
		self.assertIsNone(policy.charge(self.enrollment, self.plan, [], "2026-11"))

	def test_suspended_unknown_plan_and_midmonth_changes_stop(self):
		self.enrollment.status = "Suspended"
		with self.assertRaises(frappe.ValidationError):
			policy.charge(self.enrollment, self.plan, [], "2026-11")
		self.enrollment.status = "Active"
		self.plan.joining_policy = ""
		with self.assertRaises(frappe.ValidationError):
			policy.charge(self.enrollment, self.plan, [], "2026-11")
		self.plan.joining_policy = "Full fee if active at month start"
		self.plan.effective_to = "2026-11-15"
		with self.assertRaises(frappe.ValidationError):
			policy.charge(self.enrollment, self.plan, [], "2026-11")

	def test_full_partial_and_fixed_coverage(self):
		self.assertEqual(
			policy.charge(self.enrollment, self.plan, [self.decision], "2026-11")["amount"], "0.00"
		)
		self.decision.coverage_type = "Percentage"
		self.decision.coverage_value = 25
		result = policy.charge(self.enrollment, self.plan, [self.decision], "2026-11")
		self.assertEqual(result["amount"], "30000.00")
		self.assertNotIn("reason", result)
		self.assertNotIn("coverage_type", result)
		self.decision.coverage_type = "Fixed amount"
		self.decision.coverage_value = 45000
		self.assertEqual(
			policy.charge(self.enrollment, self.plan, [self.decision], "2026-11")["amount"], "0.00"
		)

	def test_overlaps_and_partial_month_decisions_are_exceptions(self):
		with self.assertRaises(frappe.ValidationError):
			policy.charge(self.enrollment, self.plan, [self.decision, self.decision], "2026-11")
		self.decision.effective_from = "2026-11-02"
		with self.assertRaises(frappe.ValidationError):
			policy.charge(self.enrollment, self.plan, [self.decision], "2026-11")
		self.decision.effective_from = "2026-12-01"
		self.assertEqual(
			policy.charge(self.enrollment, self.plan, [self.decision], "2026-11")["amount"], "40000.00"
		)

	def test_overlap_inclusive_and_open_ended(self):
		self.assertTrue(policy.overlap("2026-01-01", None, "2027-01-01", None))
		self.assertTrue(policy.overlap("2026-01-01", "2026-01-31", "2026-01-31", "2026-02-28"))
		self.assertFalse(policy.overlap("2026-01-01", "2026-01-31", "2026-02-01", None))

	def test_keys_stable_and_separate_months_enrollments_companies(self):
		key = monthly_billing.key_for("A", "E", "2026-11")
		self.assertEqual(key, monthly_billing.key_for("A", "E", "2026-11"))
		for values in [("A", "E", "2026-12"), ("A", "F", "2026-11"), ("B", "E", "2026-11")]:
			self.assertNotEqual(key, monthly_billing.key_for(*values))

	def test_scholarship_role_guard_denies_shares_to_registrar(self):
		doc = frappe._dict(doctype=access.SCHOLARSHIP)
		with patch.object(access, "can_read", return_value=False):
			self.assertFalse(access.has_permission(doc, user="coach", ptype="read"))
			self.assertEqual(access.permission_query("coach"), "1=0")
		with (
			patch.object(access, "can_read", return_value=True),
			patch.object(access, "can_manage_settings", return_value=False),
		):
			self.assertIsNone(access.has_permission(doc, user="finance", ptype="read"))
			self.assertFalse(access.has_permission(doc, user="finance", ptype="submit"))

	def test_immutable_obligation_requires_service_and_correct_identity(self):
		doc = frappe._dict(
			name=monthly_billing.key_for("A", "E", "2026-11"),
			company="A",
			enrollment="E",
			billing_month="2026-11",
			flags=frappe._dict(),
			is_new=lambda: True,
		)
		with patch.object(monthly_billing, "require_billing"):
			with self.assertRaises(frappe.PermissionError):
				monthly_billing.validate_obligation(doc)
			doc.flags.sports_billing_service = access.CAPABILITY
			monthly_billing.validate_obligation(doc)
			doc.is_new = lambda: False
			with self.assertRaises(frappe.PermissionError):
				monthly_billing.validate_obligation(doc)

	def test_ordinary_invoice_untouched_and_provenance_removal_blocked(self):
		invoice = frappe._dict(get_doc_before_save=lambda: None)
		with patch.object(monthly_billing, "require_billing") as guard:
			monthly_billing.validate_invoice(invoice)
			guard.assert_not_called()
			invoice.get_doc_before_save = lambda: frappe._dict(sports_billing_obligation="OBL")
			with self.assertRaises(frappe.ValidationError):
				monthly_billing.validate_invoice(invoice)

	def test_generation_requires_native_finance_rights(self):
		with (
			patch.object(
				monthly_billing, "require_billing", return_value=frappe._dict(monthly_fees_enabled=1)
			),
			patch.object(frappe, "has_permission", return_value=False),
		):
			with self.assertRaises(frappe.PermissionError):
				monthly_billing.generate.__wrapped__("2026-11", [])

	def test_cross_company_mapping_rejected(self):
		company = frappe._dict(default_currency="USD", check_permission=Mock())
		with patch.object(frappe, "get_doc", return_value=company):
			with self.assertRaises(frappe.ValidationError):
				fee_plans.mapping(self.plan)

	def test_new_submitted_decision_cannot_bypass_approval(self):
		doc = frappe._dict(is_new=lambda: True, docstatus=1)
		with patch.object(scholarships, "require_billing"):
			with self.assertRaises(frappe.ValidationError):
				scholarships.validate(doc)

	def test_academy_monthly_disable_switch_blocks_generation(self):
		with patch.object(
			monthly_billing, "require_billing", return_value=frappe._dict(monthly_fees_enabled=0)
		):
			with self.assertRaises(frappe.ValidationError):
				monthly_billing.generate.__wrapped__("2026-11", [])

	def test_decision_projection_honors_native_field_permissions(self):
		doc = frappe._dict(name="D", company="Academy", reason="PRIVATE", check_permission=Mock())
		with (
			patch.object(billing_api, "require_billing", return_value=frappe._dict(company="Academy")),
			patch.object(frappe, "get_doc", return_value=doc),
			patch.object(billing_api, "get_permitted_fields", return_value=["name"]),
		):
			self.assertEqual(billing_api.decision.__wrapped__("D"), {"name": "D"})
