from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

import frappe

from sports_app import receipt_delivery as delivery


class TestReceiptDelivery(TestCase):
	def setUp(self):
		def fail(message, error=frappe.ValidationError):
			raise error(message)

		self.player = frappe._dict(
			company="Academy",
			customer="CUSTOMER",
			guardian_email="guardian@example.invalid",
			contact_email="player@example.invalid",
		)
		self.doc = frappe._dict(
			name="RECEIPT",
			company="Academy",
			party_type="Customer",
			party="CUSTOMER",
			payment_type="Receive",
			paid_amount=100,
			docstatus=1,
			check_permission=Mock(),
			has_permission=Mock(return_value=True),
		)
		for obj, key, value in [
			(delivery, "_", lambda x: x),
			(frappe, "throw", fail),
			(delivery, "player_record", Mock(return_value=self.player)),
			(frappe, "get_doc", Mock(return_value=self.doc)),
		]:
			p = patch.object(obj, key, value)
			p.start()
			self.addCleanup(p.stop)

	def test_document_permissions_company_and_customer_are_required(self):
		self.assertEqual(delivery.receipt_record("PLAYER", "RECEIPT")[1], self.doc)
		self.assertEqual(
			[c.args[0] for c in self.doc.check_permission.call_args_list], ["read", "print", "email"]
		)
		for field, value in [
			("company", "Other"),
			("party", "Other"),
			("party_type", "Supplier"),
			("docstatus", 0),
			("docstatus", 2),
			("payment_type", "Pay"),
			("paid_amount", 0),
		]:
			old = self.doc[field]
			self.doc[field] = value
			with self.assertRaises(frappe.PermissionError):
				delivery.receipt_record("PLAYER", "RECEIPT")
			self.doc[field] = old
		self.doc.check_permission.side_effect = frappe.PermissionError
		with self.assertRaises(frappe.PermissionError):
			delivery.receipt_record("PLAYER", "RECEIPT")

	def test_contact_default_requires_player_field_permission(self):
		with patch.object(delivery, "get_permitted_fields", return_value=["guardian_email", "contact_email"]):
			self.assertEqual(
				delivery.context.__wrapped__("PLAYER", "RECEIPT")["recipient"], "guardian@example.invalid"
			)
		with patch.object(delivery, "get_permitted_fields", return_value=[]):
			self.assertEqual(delivery.context.__wrapped__("PLAYER", "RECEIPT")["recipient"], "")

	def test_unposted_or_non_email_operator_has_no_menu_action(self):
		self.assertTrue(delivery.can_email(self.doc))
		self.doc.has_permission.side_effect = lambda p: p != "email"
		self.assertFalse(delivery.can_email(self.doc))
		self.doc.docstatus = 0
		self.assertFalse(delivery.can_email(self.doc))

	def test_invalid_recipient_or_request_is_rejected_before_delivery(self):
		for recipient, key in [
			("a@example.invalid,b@example.invalid", str(uuid4())),
			("a@example.invalid\r\nBcc:x", str(uuid4())),
			("", str(uuid4())),
			("valid@example.invalid", "bad"),
		]:
			with self.assertRaises(frappe.ValidationError):
				delivery._send("PLAYER", "RECEIPT", recipient, key)

	def test_same_request_reuses_communication_without_generating_or_sending(self):
		with (
			patch.object(delivery, "receipt_record", return_value=(self.player, self.doc)),
			patch.object(delivery, "validate_email_address", side_effect=lambda s, **k: s),
			patch.object(frappe, "session", frappe._dict(user="Staff")),
			patch.object(frappe, "db", Mock()) as db,
			patch.object(frappe, "sendmail") as send,
		):
			db.get_value.return_value = frappe._dict(
				recipients="guardian@example.invalid", reference_name="RECEIPT"
			)
			result = delivery._send("PLAYER", "RECEIPT", "guardian@example.invalid", str(uuid4()))
			self.assertTrue(result["duplicate"])
			send.assert_not_called()
			db.get_value.return_value.recipients = "other@example.invalid"
			with self.assertRaises(frappe.ValidationError):
				delivery._send("PLAYER", "RECEIPT", "guardian@example.invalid", str(uuid4()))

	def test_queue_contains_only_posted_pdf_and_preserves_native_reference(self):
		comm = Mock()
		comm.name = "COMM"
		comm.sender = "Staff <staff@example.invalid>"
		comm.subject = "Receipt"
		comm.content = "Body"
		with (
			patch.object(delivery, "receipt_record", return_value=(self.player, self.doc)),
			patch.object(delivery, "validate_email_address", side_effect=lambda s, **k: s),
			patch.object(delivery, "get_formatted_email", return_value=comm.sender),
			patch.object(frappe, "session", frappe._dict(user="Staff")),
			patch.object(frappe, "db", Mock()) as db,
			patch.object(frappe, "get_doc", return_value=comm),
			patch.object(frappe, "get_meta", return_value=frappe._dict(default_print_format="")),
			patch.object(
				delivery, "receipt_pdf", return_value={"fname": "receipt.pdf", "fcontent": b"%PDF"}
			) as pdf,
			patch.object(frappe, "sendmail") as send,
		):
			db.get_value.return_value = None
			result = delivery._send("PLAYER", "RECEIPT", "guardian@example.invalid", str(uuid4()))
			self.assertFalse(result["duplicate"])
			pdf.assert_called_once_with(self.doc)
			args = send.call_args.kwargs
			self.assertEqual(args["recipients"], ["guardian@example.invalid"])
			self.assertEqual(args["reference_name"], "RECEIPT")
			self.assertFalse(args["now"])
			self.assertEqual(args["attachments"][0]["fname"], "receipt.pdf")
			send.return_value = []
			with self.assertRaises(frappe.ValidationError):
				delivery._send("PLAYER", "RECEIPT", "guardian@example.invalid", str(uuid4()))
			comm.get_outgoing_email_account.return_value = None
			with self.assertRaises(frappe.ValidationError):
				delivery._send("PLAYER", "RECEIPT", "guardian@example.invalid", str(uuid4()))
