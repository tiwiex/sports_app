import json
from contextlib import ExitStack
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import enrollment_invoices as invoices
from sports_app import enrollment_payments as payments
from sports_app import payment_notifications as notices


class TestPaymentNotifications(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, name, value in (
			(frappe, "throw", throw),
			(frappe, "_", lambda s: s),
			(notices, "_", lambda s: s),
			(invoices, "_", lambda s: s),
			(payments, "_", lambda s: s),
		):
			active = patch.object(target, name, value)
			active.start()
			self.addCleanup(active.stop)
		self.settings = frappe._dict(
			company="Academy", payment_review_emails="one@example.com, TWO@example.com, one@example.com"
		)
		self.app = frappe._dict(
			company="Academy",
			request_key="secret-token",
			sales_invoice="INV-1",
			payment_entry="PAY-1",
			status="Pending",
			contact_email="private@example.com",
			payment_snapshot=json.dumps(dict(currency="NGN", total=250000)),
		)

	def document(self, doctype="Sales Invoice", **changes):
		doc = frappe._dict(
			doctype=doctype,
			name="INV-1" if doctype == "Sales Invoice" else "PAY-1",
			company="Academy",
			workflow_state="Draft",
			docstatus=0,
		)
		doc.update(changes)
		doc.db_set = Mock(side_effect=lambda values: doc.update(values))
		doc.add_comment = Mock()
		return doc

	def test_list_normalization_validation_and_blank_opt_out(self):
		self.assertEqual(
			notices.review_recipients(self.settings.payment_review_emails),
			["one@example.com", "two@example.com"],
		)
		self.assertEqual(notices.review_recipients("  , "), [])
		for value in [
			"invalid",
			"a@example.com; b@example.com",
			"a@example.com\nBcc:b@example.com",
			"Name <a@example.com>",
			["a@example.com"],
			",".join(f"u{i}@example.com" for i in range(51)),
		]:
			with self.subTest(value=value), self.assertRaises(frappe.ValidationError):
				notices.review_recipients(value)

	def test_queue_is_delayed_linked_private_and_not_an_approval(self):
		doc = self.document(name="INV-<test>")
		with (
			patch.object(frappe, "sendmail") as mail,
			patch.object(
				notices, "get_url_to_form", return_value="https://academy.test/app/sales-invoice/INV-1"
			),
		):
			notices.notify_payment_review(self.app, doc, self.settings)
		values = mail.call_args.kwargs
		self.assertEqual(values["recipients"], ["one@example.com", "two@example.com"])
		self.assertTrue(values["delayed"])
		self.assertFalse(values["now"])
		self.assertEqual(values["reference_doctype"], "Sales Invoice")
		self.assertIn("Review payment", values["message"])
		self.assertIn("Verify the bank credit", values["message"])
		self.assertIn("INV-&lt;test&gt;", values["message"])
		self.assertNotIn("secret-token", values["message"])
		self.assertNotIn("private@example.com", values["message"])

	def test_blank_list_skips_mail_and_other_company_cannot_receive_details(self):
		with patch.object(frappe, "sendmail") as mail:
			notices.notify_payment_review(
				self.app, self.document(), frappe._dict(company="Academy", payment_review_emails="")
			)
			mail.assert_not_called()
			with self.assertRaises(frappe.PermissionError):
				notices.notify_payment_review(self.app, self.document(company="Other"), self.settings)
			mail.assert_not_called()

	def claim_context(self, stack, module, doc):
		stack.enter_context(patch.object(module, "now_datetime", return_value="2026-11-03 12:00:00"))
		stack.enter_context(patch.object(module, "intake_settings", return_value=self.settings))
		stack.enter_context(patch.object(module, "request_uuid", return_value="secret-token"))
		stack.enter_context(
			patch.object(
				frappe,
				"db",
				SimpleNamespace(get_value=Mock(return_value="REG"), exists=Mock(return_value=False)),
			)
		)
		stack.enter_context(
			patch.object(
				frappe,
				"get_doc",
				side_effect=lambda dt, *a, **k: self.app if dt == "Sports Registration" else doc,
			)
		)
		stack.enter_context(
			patch.object(module, "_response", side_effect=lambda app, d: dict(state=d.workflow_state))
		)
		if module is invoices:
			stack.enter_context(patch.object(module, "validate_enrollment_invoice"))
			stack.enter_context(patch.object(module, "invoice_workflow"))
		else:
			stack.enter_context(patch.object(module, "validate_sports_payment"))
			stack.enter_context(patch("frappe.model.workflow.get_workflow_name", return_value="Review"))

	def test_first_claim_notifies_once_and_retries_do_not_for_both_document_types(self):
		for module, doctype, claim in [
			(invoices, "Sales Invoice", invoices.claim_invoice),
			(payments, "Payment Entry", payments.payment_made.__wrapped__),
		]:
			with self.subTest(doctype=doctype), ExitStack() as stack:
				doc = self.document(doctype)
				self.claim_context(stack, module, doc)
				if module is payments:
					# Only the workflow lookup needs the workflow fixture.
					lookup = frappe.get_doc.side_effect
					frappe.get_doc.side_effect = (
						lambda dt, *a, **k: frappe._dict(
							workflow_state_field="workflow_state",
							states=[frappe._dict(state="Pending Review", doc_status=0)],
						)
						if dt == "Workflow"
						else lookup(dt, *a, **k)
					)
				notify = stack.enter_context(patch.object(notices, "notify_payment_review"))
				self.assertEqual(claim(doc.name, "secret-token")["state"], "Pending Review")
				claim(doc.name, "secret-token")
				notify.assert_called_once_with(self.app, doc, self.settings)
				self.assertEqual(doc.docstatus, 0)
				self.app.request_key = "wrong-token"
				with self.assertRaises(frappe.PermissionError):
					claim(doc.name, "secret-token")
				self.app.request_key = "secret-token"
				self.assertEqual(notify.call_count, 1)

	def test_queue_failure_propagates_to_transaction_instead_of_silently_dropping_email(self):
		with ExitStack() as stack:
			doc = self.document()
			self.claim_context(stack, invoices, doc)
			stack.enter_context(
				patch.object(notices, "notify_payment_review", side_effect=RuntimeError("Queue failure"))
			)
			with self.assertRaisesRegex(RuntimeError, "Queue failure"):
				invoices.claim_invoice("INV-1", "secret-token")
