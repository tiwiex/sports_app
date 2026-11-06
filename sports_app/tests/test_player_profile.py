import base64
import io
from datetime import date
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

import frappe
from pypdf import PdfWriter

from sports_app import player_documents as documents
from sports_app import player_profile as profile


class TestCentralPlayerProfile(TestCase):
	def setUp(self):
		def throw(message, error=frappe.ValidationError):
			raise error(message)

		for module, name, value in [
			(frappe, "throw", throw),
			(profile, "_", lambda s: s),
			(documents, "_", lambda s: s),
			(profile, "today", lambda: date(2026, 11, 6)),
		]:
			p = patch.object(module, name, value)
			p.start()
			self.addCleanup(p.stop)
		self.player = frappe._dict(
			name="PLAYER",
			company="Academy",
			customer="CUSTOMER",
			birth_date="2015-11-07",
			modified="v1",
			preferred_foot="Left",
			has_permission=Mock(return_value=True),
			save=Mock(),
		)
		for name, value in [
			("player_record", Mock(return_value=self.player)),
			("private_file", Mock(return_value=None)),
		]:
			p = patch.object(profile, name, value)
			p.start()
			self.addCleanup(p.stop)
		self.native = SimpleNamespace(
			has_permission=Mock(return_value=True),
			get_doc=Mock(return_value=self.player),
			get_list=Mock(return_value=[]),
		)
		p = patch.object(profile, "frappe", self.native)
		p.start()
		self.addCleanup(p.stop)
		self.native.PermissionError = frappe.PermissionError
		self.native.TimestampMismatchError = frappe.TimestampMismatchError
		self.native.throw = throw
		p = patch.object(
			profile,
			"get_permitted_fields",
			side_effect=lambda doctype, **k: list(
				{
					"preferred_foot",
					"birth_date",
					"player_photo",
					*next((fields for dt, fields in profile.SECTIONS.values() if dt == doctype), []),
				}
			),
		)
		p.start()
		self.addCleanup(p.stop)
		p = patch.object(profile, "can_manage_settings", return_value=True)
		self.management = p.start()
		self.addCleanup(p.stop)

	def test_permissions_and_field_restrictions_prevent_financial_reads(self):
		self.native.has_permission.return_value = False
		result = profile.overview.__wrapped__("PLAYER")
		self.assertFalse(any(result["available"].values()))
		self.assertIsNone(result["outstanding"])
		self.native.get_list.assert_not_called()
		self.native.has_permission.return_value = True
		with patch.object(profile, "get_permitted_fields", return_value=["name"]):
			self.assertFalse(profile.available(self.player, "invoices"))
		self.player.has_permission.return_value = False
		self.assertFalse(profile.available(self.player, "receipts"))

	def test_management_private_sections_hidden_even_with_native_read(self):
		self.management.return_value = False
		self.assertFalse(profile.available(self.player, "documents"))
		self.assertFalse(profile.available(self.player, "biometrics"))
		with self.assertRaises(frappe.PermissionError):
			profile.history.__wrapped__("PLAYER", "documents")
		self.native.get_list.assert_not_called()

	def test_financial_summary_is_company_customer_submitted_and_currency_grouped(self):
		self.native.get_list.return_value = [
			frappe._dict(currency="NGN", outstanding=100),
			frappe._dict(currency="USD", outstanding=20),
		]
		result = profile.overview.__wrapped__("PLAYER")
		query = self.native.get_list.call_args.kwargs
		self.assertEqual(query["filters"], dict(company="Academy", customer="CUSTOMER", docstatus=1))
		self.assertEqual(query["group_by"], "currency")
		self.assertEqual([r.currency for r in result["outstanding"]], ["NGN", "USD"])
		self.assertEqual(result["age"], 10)

	def test_missing_customer_is_empty_without_unscoped_finance_query(self):
		self.player.customer = None
		self.assertEqual(profile.history.__wrapped__("PLAYER", "receipts"), dict(rows=[], has_more=False))
		self.native.get_list.assert_not_called()

	def test_invoice_receipt_pagination_and_party_filters(self):
		self.native.get_list.return_value = [frappe._dict(name=f"ROW-{i}") for i in range(21)]
		result = profile.history.__wrapped__("PLAYER", "receipts", 20)
		self.assertEqual(len(result["rows"]), 20)
		self.assertTrue(result["has_more"])
		query = self.native.get_list.call_args.kwargs
		self.assertEqual(query["filters"], dict(company="Academy", party_type="Customer", party="CUSTOMER"))
		self.assertEqual(query["start"], 20)
		self.assertEqual(query["page_length"], 21)
		self.assertNotIn("ignore_permissions", query)

	def test_unknown_sections_and_invalid_pages_rejected(self):
		for section, start in [("User", 0), ("invoices", -1), ("attendance", "1e3")]:
			with self.assertRaises(frappe.ValidationError):
				profile.history.__wrapped__("PLAYER", section, start)
		self.native.get_list.assert_not_called()

	def test_unread_session_does_not_leak_name_title_or_date(self):
		self.native.get_list.side_effect = [
			[frappe._dict(name="ATT", session="SECRET-SESSION", status="Present")],
			[],
		]
		row = profile.history.__wrapped__("PLAYER", "attendance")["rows"][0]
		self.assertIsNone(row.session)
		self.assertIsNone(row.session_title)
		self.assertIsNone(row.session_date)

	def test_preferred_foot_revision_and_allowlist(self):
		with self.assertRaises(frappe.TimestampMismatchError):
			profile.save_preferred_foot.__wrapped__("PLAYER", "Right", "stale")
		with self.assertRaises(frappe.ValidationError):
			profile.save_preferred_foot.__wrapped__("PLAYER", "unexpected", "v1")
		self.assertEqual(profile.save_preferred_foot.__wrapped__("PLAYER", "Right", "v1"), "v1")
		self.assertEqual(self.player.preferred_foot, "Right")
		self.player.save.assert_called_once()

	def test_positive_units_reject_nonfinite_zero_and_boolean(self):
		for value in ["nan", "inf", 0, -1, True, "not-number", "0.001"]:
			with self.assertRaises(frappe.ValidationError):
				profile.positive_number(value)
		self.assertEqual(profile.positive_number("150.25"), 150.25)
		self.assertIsNone(profile.positive_number(None))

	def test_measurement_history_cannot_be_overwritten_or_dates_fabricated(self):
		doc = frappe._dict(
			doctype=profile.MEASUREMENT,
			player="PLAYER",
			company="Academy",
			flags=frappe._dict(player_profile_service=profile.CAPABILITY),
			is_new=lambda: False,
		)
		with self.assertRaises(frappe.PermissionError):
			profile.check_record(doc)
		doc.is_new = lambda: True
		doc.assessed_on = "2026-11-07"
		with self.assertRaises(frappe.ValidationError):
			profile.check_record(doc)
		doc.assessed_on = "2010-01-01"
		with self.assertRaises(frappe.ValidationError):
			profile.check_record(doc)
		doc.assessed_on = "2026-11-06"
		doc.height_cm = 140
		doc.weight_kg = 35
		profile.check_record(doc)

	def test_request_identity_is_strict_and_changed_payload_differs(self):
		key = str(uuid4())
		self.assertNotEqual(
			profile.request_identity(key, dict(height=140)), profile.request_identity(key, dict(height=141))
		)
		with self.assertRaises(frappe.ValidationError):
			profile.request_identity("not-uuid", {})

	def test_supporting_file_permissions_cannot_be_shared_to_nonmanager(self):
		with patch.object(documents, "can_manage_settings", return_value=False):
			self.assertFalse(documents.has_permission(None, user="registrar"))
			self.assertEqual(documents.permission_query("registrar"), "1=0")

	def test_pdf_validation_rejects_encrypted_active_and_malformed_files(self):
		def data(writer):
			stream = io.BytesIO()
			writer.write(stream)
			return "data:application/pdf;base64," + base64.b64encode(stream.getvalue()).decode()

		writer = PdfWriter()
		writer.add_blank_page(width=100, height=100)
		self.assertEqual(documents.prepare_file(data(writer))["extension"], "pdf")
		writer.add_js('app.alert("x")')
		with self.assertRaises(frappe.ValidationError):
			documents.prepare_file(data(writer))
		writer = PdfWriter()
		writer.add_blank_page(width=100, height=100)
		writer.encrypt("secret")
		with self.assertRaises(frappe.ValidationError):
			documents.prepare_file(data(writer))
		for value in [
			"data:application/pdf;base64,JVBERi0=",
			"https://example.invalid/file.pdf",
			"data:text/html;base64,PHNjcmlwdD4=",
		]:
			with self.assertRaises(frappe.ValidationError):
				documents.prepare_file(value)

	def test_supporting_file_must_stay_private_attached_and_owned_by_administrator(self):
		doc = frappe._dict(
			is_private=0,
			attached_to_doctype=profile.DOCUMENT,
			attached_to_name="DOC",
			get_doc_before_save=lambda: None,
		)
		with patch.object(documents, "require_settings_access"):
			with self.assertRaises(frappe.ValidationError):
				documents.protect_file(doc)

	def test_file_list_scope_uses_permitted_document_parents(self):
		native = SimpleNamespace(
			db=SimpleNamespace(exists=Mock(return_value=True), escape=lambda name: "'" + name + "'"),
			has_permission=Mock(return_value=True),
			get_list=Mock(return_value=["VISIBLE"]),
		)
		with (
			patch.object(documents, "frappe", native),
			patch.object(documents, "can_manage_settings", return_value=True),
		):
			condition = documents.file_permission_query("manager")
			self.assertIn("'VISIBLE'", condition)
			self.assertIn("attached_to_name", condition)
			native.get_list.assert_called_once_with(
				profile.DOCUMENT, pluck="name", page_length=0, user="manager"
			)
		with (
			patch.object(documents, "frappe", native),
			patch.object(documents, "can_manage_settings", return_value=False),
		):
			self.assertNotIn("'VISIBLE'", documents.file_permission_query("registrar"))

	def test_linked_history_filters_player_and_company(self):
		for section in ("attendance", "biometrics", "measurements", "documents"):
			profile.history.__wrapped__("PLAYER", section)
			self.assertEqual(
				self.native.get_list.call_args.kwargs["filters"], {"company": "Academy", "player": "PLAYER"}
			)

	def test_documents_require_controlled_archive_and_private_file(self):
		doc = frappe._dict(
			doctype=profile.DOCUMENT,
			player="PLAYER",
			company="Academy",
			docstatus=1,
			_action="submit",
			flags=frappe._dict(player_profile_service=profile.CAPABILITY),
			is_new=lambda: False,
			title="Certificate",
			document_type="Birth certificate",
			file_url=None,
		)
		with patch.object(profile, "require_settings_access"):
			with self.assertRaises(frappe.ValidationError):
				profile.check_record(doc)
			doc.file_url = "/private/files/certificate.pdf"
			profile.check_record(doc)
			doc.flags.player_profile_service = None
			with self.assertRaises(frappe.PermissionError):
				profile.check_record(doc)
