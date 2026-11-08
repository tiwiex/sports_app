from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import printing


class TestSportsPrinting(TestCase):
	def test_missing_customer_or_unread_customer_has_no_finance_references(self):
		with patch.object(frappe, "get_doc") as get, patch.object(frappe, "get_list") as query:
			self.assertIsNone(printing.latest_documents(frappe._dict(customer=None))["latest_invoice"])
			get.assert_not_called()
			get.return_value.has_permission.return_value = False
			self.assertIsNone(printing.latest_documents(frappe._dict(customer="PRIVATE"))["latest_receipt"])
			query.assert_not_called()

	def test_native_filters_enforce_company_customer_posted_receive_and_bounded_latest(self):
		player = frappe._dict(customer="CUSTOMER", company="ACADEMY")
		customer = Mock()
		customer.has_permission.return_value = True
		receipt = frappe._dict(
			name="REC",
			docstatus=1,
			payment_type="Receive",
			paid_amount=100,
			has_permission=Mock(return_value=True),
		)
		with (
			patch.object(
				frappe, "get_doc", side_effect=lambda dt, n: customer if dt == "Customer" else receipt
			),
			patch.object(frappe, "has_permission", return_value=True),
			patch.object(
				frappe, "get_list", side_effect=[[frappe._dict(name="INV")], [frappe._dict(name="REC")]]
			) as query,
		):
			result = printing.latest_documents(player)
			self.assertEqual(result, dict(latest_invoice="INV", latest_receipt="REC", can_email_receipt=True))
			invoice_args, receipt_args = [c.kwargs for c in query.call_args_list]
			self.assertEqual(invoice_args["filters"], dict(company="ACADEMY", customer="CUSTOMER"))
			self.assertEqual(
				receipt_args["filters"],
				dict(
					company="ACADEMY",
					party_type="Customer",
					party="CUSTOMER",
					payment_type="Receive",
					docstatus=1,
				),
			)
			for args in [invoice_args, receipt_args]:
				self.assertEqual(args["page_length"], 1)
				self.assertNotIn("ignore_permissions", args)

	def test_type_permission_denial_never_queries_finance(self):
		with (
			patch.object(frappe, "get_doc", return_value=Mock(has_permission=Mock(return_value=True))),
			patch.object(frappe, "has_permission", return_value=False),
			patch.object(frappe, "get_list") as query,
		):
			result = printing.latest_documents(frappe._dict(customer="CUSTOMER", company="ACADEMY"))
			self.assertEqual(result, dict(latest_invoice=None, latest_receipt=None, can_email_receipt=False))
			query.assert_not_called()
