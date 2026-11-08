from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import billing_policy
from sports_app import enrollment_charges as charges
from sports_app import subscription_pricing as pricing


class TestConfigurableCharges(TestCase):
	def setUp(self):
		def fail(message, error=frappe.ValidationError):
			raise error(message)

		for module, name, value in [
			(frappe, "throw", fail),
			(charges, "_", lambda s: s),
			(billing_policy, "_", lambda s: s),
			(pricing, "_", lambda s: s),
		]:
			p = patch.object(module, name, value)
			p.start()
			self.addCleanup(p.stop)
		self.item = frappe._dict(
			name="EXISTING",
			item_name="Academy kit",
			stock_uom="Nos",
			disabled=0,
			is_sales_item=1,
			is_stock_item=1,
			check_permission=Mock(),
		)

	def test_arbitrary_rows_quantities_totals_and_stock_billing(self):
		settings = frappe._dict(
			enrollment_items_configured=1,
			enrollment_items=[
				dict(item_code="EXISTING", qty=2, rate=100),
				dict(item_code="EXISTING", qty="1.2500", rate=40),
				dict(item_code="EXISTING", qty=1, rate=0),
			],
		)
		with patch.object(frappe, "get_doc", return_value=self.item):
			result = charges.calculate(settings, check_permissions=True)
		self.assertEqual(len(result), 3)
		self.assertEqual(sum(r["amount"] for r in result), 250)
		self.assertEqual(result[0]["item_name"], "Academy kit")
		self.assertEqual(result[0]["qty"], 2)
		self.item.check_permission.assert_called_with("read")

	def test_configured_empty_table_never_uses_legacy_fees(self):
		settings = frappe._dict(
			enrollment_items_configured=1,
			enrollment_items=[],
			enrollment_registration_item="OLD",
			enrollment_registration_fee=220000,
		)
		self.assertEqual(charges.rows(settings), [])
		with self.assertRaises(frappe.ValidationError):
			charges.calculate(settings)

	def test_legacy_configuration_is_readable_until_migrated(self):
		settings = frappe._dict(
			enrollment_registration_item="OLD",
			enrollment_registration_fee=220000,
			enrollment_jersey_item="KIT",
			enrollment_jersey_fee=30000,
		)
		with patch.object(frappe, "get_doc", return_value=self.item):
			self.assertEqual(sum(r["amount"] for r in charges.calculate(settings)), 250000)

	def test_bad_quantities_rates_disabled_items_and_size_rejected(self):
		with patch.object(frappe, "get_doc", return_value=self.item):
			for qty, rate in [(0, 1), (-1, 1), ("nan", 1), ("0.00001", 1), (1, -1), (1, "inf")]:
				with self.assertRaises(frappe.ValidationError):
					charges.calculate(
						frappe._dict(enrollment_items=[dict(item_code="EXISTING", qty=qty, rate=rate)])
					)
			self.item.disabled = 1
			with self.assertRaises(frappe.ValidationError):
				charges.calculate(frappe._dict(enrollment_items=[dict(item_code="EXISTING", qty=1, rate=1)]))
			with self.assertRaises(frappe.ValidationError):
				charges.calculate(frappe._dict(enrollment_items=[{}] * 31))

	def test_subscription_plan_requires_native_read_month_currency_and_fixed_rate(self):
		plan = frappe._dict(
			name="PLAN",
			item="SERVICE",
			currency="NGN",
			billing_interval="Month",
			billing_interval_count=1,
			price_determination="Fixed Rate",
			modified="v1",
			check_permission=Mock(),
		)
		self.item.is_stock_item = 0
		with (
			patch.object(
				frappe,
				"get_doc",
				side_effect=lambda kind, name: plan if kind == "Subscription Plan" else self.item,
			),
			patch(
				"erpnext.accounts.doctype.subscription_plan.subscription_plan.get_plan_rate",
				return_value=40000,
			),
		):
			result = pricing.resolve("PLAN", "NGN")
			self.assertEqual(result["monthly_amount"], 40000)
			self.assertEqual(result["item"], "SERVICE")
			plan.check_permission.assert_called_with("read")
			for field, value in [
				("currency", "USD"),
				("billing_interval", "Week"),
				("billing_interval_count", 2),
				("price_determination", "Based On Price List"),
			]:
				previous = plan[field]
				plan[field] = value
				with self.assertRaises(frappe.ValidationError):
					pricing.resolve("PLAN", "NGN")
				plan[field] = previous
			plan.check_permission.side_effect = frappe.PermissionError
			with self.assertRaises(frappe.PermissionError):
				pricing.resolve("PLAN", "NGN")
