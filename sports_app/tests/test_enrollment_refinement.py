import base64
import io
from contextlib import nullcontext
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe
from frappe.utils import CallbackManager
from PIL import Image

from sports_app import enrollment_images as images
from sports_app import enrollment_invoices, players, players_api, registrations
from sports_app import registrations_api as api


class TestEnrollmentRefinement(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, key, value in [
			(frappe, "throw", throw),
			(images, "_", lambda s: s),
			(api, "_", lambda s: s),
		]:
			active = patch.object(target, key, value)
			active.start()
			self.addCleanup(active.stop)

	def image(self):
		output = io.BytesIO()
		Image.new("RGB", (2000, 1000), "green").save(output, format="PNG")
		return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode()

	def test_image_is_bounded_reencoded_and_stable(self):
		result = images.prepare_image(self.image())
		self.assertEqual(result["hash"], images.prepare_image(self.image())["hash"])
		with Image.open(io.BytesIO(result["content"])) as image:
			self.assertEqual(image.format, "JPEG")
			self.assertEqual(image.size, (1600, 800))
			self.assertFalse(image.getexif())
		self.assertIsNone(images.prepare_image(""))

	def test_guest_cannot_supply_urls_svg_invalid_or_large_images(self):
		for value in [
			"/private/files/other.jpg",
			"data:image/svg+xml;base64,PHN2Zz4=",
			"data:image/png;base64,invalid",
			self.image().replace("data:image/png;", "data:text/plain;"),
			"x" * (images.MAX_BYTES * 2),
		]:
			with self.subTest(value=value[:40]), self.assertRaises(frappe.ValidationError):
				images.prepare_image(value)

	def test_private_attachment_has_non_guest_owner_and_exact_provenance(self):
		doc = SimpleNamespace(name="APP", db_set=Mock())
		with patch.object(
			frappe,
			"get_doc",
			return_value=SimpleNamespace(
				insert=Mock(return_value=SimpleNamespace(file_url="/private/files/photo.jpg"))
			),
		) as create:
			images.save_registration_image(doc, {"content": b"image"})
			self.assertEqual(create.call_args.kwargs["is_private"], 1)
			self.assertEqual(create.call_args.kwargs["owner"], "Administrator")
			self.assertEqual(create.call_args.kwargs["attached_to_name"], "APP")
			doc.db_set.assert_called_once_with(
				"player_photo", "/private/files/photo.jpg", update_modified=False
			)

	def test_player_image_requires_existing_private_application_attachment(self):
		with (
			patch.object(frappe, "db", SimpleNamespace(exists=Mock(return_value=False))),
			self.assertRaises(frappe.ValidationError),
		):
			images.link_player_image(
				frappe._dict(name="APP", player_photo="/private/files/stolen.jpg"), "PLAYER"
			)

	def test_nested_transaction_uses_distinct_savepoints_and_drops_callbacks(self):
		db = SimpleNamespace(after_commit=CallbackManager(), savepoint=Mock(), rollback=Mock())
		callback = Mock()
		with patch.object(frappe, "db", db), self.assertRaises(ValueError):
			with registrations.acceptance_transaction():
				with registrations.acceptance_transaction():
					db.after_commit.add(callback)
				raise ValueError()
		self.assertEqual(len({call.args[0] for call in db.savepoint.call_args_list}), 2)
		db.after_commit.run()
		callback.assert_not_called()

	def test_accept_gates_invoice_before_player_and_retries_are_idempotent(self):
		doc = frappe._dict(
			name="APP",
			company="Academy",
			status="Pending",
			sales_invoice="INV",
			payment_customer="",
			program="PROGRAM",
			acceptance_key="KEY",
			flags=frappe._dict(),
		)
		doc.reload = Mock()
		doc.save = Mock()
		with (
			patch.object(api, "require_player_access"),
			patch.object(players, "validate_player_email"),
			patch.object(api, "registration_settings", return_value=frappe._dict(company="Academy")),
			patch.object(api, "review_record", return_value=doc),
			patch.object(api, "today", return_value="2026-11-06"),
			patch.object(api, "now_datetime"),
			patch.object(frappe, "session", SimpleNamespace(user="Administrator")),
			patch.object(api, "acceptance_transaction", return_value=nullcontext()),
			patch.object(frappe, "db", SimpleNamespace(set_value=Mock())),
			patch.object(players_api, "register_player", return_value="PLAYER") as register,
			patch.object(images, "link_player_image"),
			patch.object(
				enrollment_invoices, "complete_payment", side_effect=frappe.PermissionError
			) as complete,
		):
			with self.assertRaises(frappe.PermissionError):
				api.accept_registration.__wrapped__("APP")
			register.assert_not_called()
			self.assertEqual(doc.status, "Pending")
			complete.side_effect = None
			self.assertEqual(api.accept_registration.__wrapped__("APP"), "PLAYER")
			self.assertEqual(doc.status, "Accepted")
			self.assertEqual(api.accept_registration.__wrapped__("APP"), "PLAYER")
			register.assert_called_once()
			self.assertEqual(complete.call_count, 2)

	def test_draft_or_finance_denied_application_cannot_offer_acceptance(self):
		doc = frappe._dict(status="Pending", sales_invoice="INV", has_permission=Mock(return_value=True))
		with patch.object(enrollment_invoices, "can_complete_payment", return_value=True):
			self.assertFalse(api.can_accept(doc, frappe._dict(docstatus=0, workflow_state="Draft")))
			self.assertTrue(api.can_accept(doc, frappe._dict(docstatus=0, workflow_state="Pending Review")))
		with patch.object(enrollment_invoices, "can_complete_payment", return_value=False):
			self.assertFalse(api.can_accept(doc, frappe._dict(docstatus=0, workflow_state="Pending Review")))

	def test_invoice_projection_matches_company_and_application(self):
		with patch.object(frappe, "db", SimpleNamespace(get_value=Mock(return_value=None))) as db:
			api.enrollment_invoice(frappe._dict(name="APP", sales_invoice="INV", company="Academy"))
			self.assertEqual(
				db.get_value.call_args.args[1],
				{"name": "INV", "sports_registration": "APP", "company": "Academy"},
			)
