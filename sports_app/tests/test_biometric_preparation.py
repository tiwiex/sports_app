import json
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import biometric_preparation as service


class TestBiometricPreparation(TestCase):
	def test_demo_capture_is_stable_and_does_not_change_real_capture_status(self):
		doc = frappe._dict(
			name="B",
			player="P",
			status="Pending capture",
			flags=frappe._dict(),
			check_permission=Mock(),
			save=Mock(),
			add_comment=Mock(),
		)
		with (
			patch.object(service, "require_access"),
			patch.object(service, "player_record"),
			patch.object(frappe, "get_doc", return_value=doc),
			patch.object(frappe, "session", SimpleNamespace(user="operator")),
			patch.object(service, "now_datetime", return_value="now"),
		):
			first = service.demo_capture.__wrapped__("B")
			second = service.demo_capture.__wrapped__("B")
		self.assertRegex(first["demo_reference"], r"^DEMO-\d{20}$")
		self.assertEqual(first["demo_reference"], second["demo_reference"])
		self.assertEqual(first["status"], "Pending capture")
		self.assertEqual(doc.demo_generated_by, "operator")
		doc.save.assert_called_once()
		doc.add_comment.assert_called_once()

	def test_withdrawn_request_cannot_generate_a_demo_code(self):
		doc = frappe._dict(player="P", status="Withdrawn", check_permission=Mock(), save=Mock())
		with (
			patch.object(service, "require_access"),
			patch.object(service, "player_record"),
			patch.object(frappe, "get_doc", return_value=doc),
			self.assertRaises(frappe.ValidationError),
		):
			service.demo_capture.__wrapped__("B")
		doc.save.assert_not_called()

	def test_directory_uses_latest_request_and_keeps_unprepared_players_visible(self):
		players = [
			frappe._dict(name="P1", full_name="One"),
			frappe._dict(name="P2", full_name="Two"),
			frappe._dict(name="P3", full_name="Three"),
		]
		entries = [
			frappe._dict(
				name="B3", player="P1", status="Pending capture", finger="Right thumb", prepared_on="now"
			),
			frappe._dict(name="B2", player="P1", status="Withdrawn", finger="Left thumb", prepared_on="old"),
			frappe._dict(name="B1", player="P3", status="Withdrawn", finger="Right index", prepared_on="old"),
		]
		with (
			patch.object(service, "require_access"),
			patch.object(service, "validate_company"),
			patch.object(service, "get_configured_settings", return_value=frappe._dict(company="Academy")),
			patch.object(frappe, "get_list", side_effect=[players, entries]) as query,
		):
			result = service.list_player_statuses.__wrapped__()
		self.assertEqual(
			[r["fingerprint_status"] for r in result["rows"]],
			["Pending capture", "Not prepared", "Withdrawn"],
		)
		self.assertEqual(result["rows"][0]["request_name"], "B3")
		self.assertFalse(result["has_more"])
		self.assertEqual(query.call_args_list[0].kwargs["filters"], {"company": "Academy"})
		self.assertEqual(query.call_args_list[1].kwargs["filters"]["company"], "Academy")
		self.assertNotIn("consent_by", result["rows"][0])

	def setUp(self):
		lock = patch.object(service, "lock_identity_changes")
		lock.start()
		self.addCleanup(lock.stop)

		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, name, value in [(frappe, "throw", throw), (service, "_", lambda s: s)]:
			p = patch.object(target, name, value)
			p.start()
			self.addCleanup(p.stop)
		self.values = dict(
			finger="Right thumb",
			consent_by="Sample guardian",
			relationship="Parent / Guardian",
			notice_reference="Supplied notice QA",
			consent_date="2020-01-01",
		)

	def test_guest_and_registrar_without_administrator_capability_are_denied(self):
		with (
			patch.object(service, "can_manage_settings", return_value=False),
			self.assertRaises(frappe.PermissionError),
		):
			service.require_access()

	def test_missing_consent_and_unapproved_extra_fields_cannot_be_registered(self):
		with (
			patch.object(service, "require_access"),
			patch.object(service, "player_record"),
			self.assertRaises(frappe.ValidationError),
		):
			service.prepare.__wrapped__("P", self.values, 0, "key")
		for values in [
			{**self.values, "template": "not-allowed"},
			{**self.values, "finger": "Face"},
			{**self.values, "consent_by": ""},
		]:
			with self.subTest(values=values), self.assertRaises(frappe.ValidationError):
				service.validate_values(values)

	def test_future_consent_is_denied_and_valid_date_is_normalized(self):
		with patch.object(
			service, "get_configured_settings", return_value=frappe._dict(timezone="Africa/Lagos")
		):
			self.assertEqual(service.validate_values(self.values), self.values)
			with self.assertRaises(frappe.ValidationError):
				service.validate_values({**self.values, "consent_date": "2099-01-01"})

	def test_native_document_edits_require_unforgeable_service_capability(self):
		with patch.object(service, "require_access"):
			for flag in [None, True, "CAPABILITY"]:
				with self.subTest(flag=flag), self.assertRaises(frappe.PermissionError):
					service.validate_document(
						frappe._dict(flags=frappe._dict(sports_biometric_preparation=flag))
					)

	def test_no_hardware_enrolled_state_or_template_fields_exist(self):
		schema = json.loads(
			(
				Path(service.__file__).parent
				/ "sports_app/doctype/sports_biometric_enrollment/sports_biometric_enrollment.json"
			).read_text()
		)
		fields = {f["fieldname"]: f for f in schema["fields"]}
		self.assertEqual(fields["status"]["options"], "Pending capture\nWithdrawn")
		self.assertFalse({"template", "fingerprint", "image", "device_user_id"} & set(fields))
		self.assertEqual(
			{p["role"] for p in schema["permissions"]}, {"System Manager", "Sports Academy Administrator"}
		)

	def test_public_payload_does_not_expose_internal_request_keys(self):
		record = service.public_record(
			frappe._dict(
				name="QA",
				status="Pending capture",
				request_key="secret",
				request_hash="digest",
				template="forged",
			)
		)
		self.assertNotIn("request_key", record)
		self.assertNotIn("request_hash", record)
		self.assertNotIn("template", record)

	def test_cross_company_player_rejected_after_native_player_permission(self):
		player = frappe._dict(company="Other", check_permission=Mock())
		with (
			patch.object(service, "require_access"),
			patch.object(service, "validate_company"),
			patch.object(service, "get_configured_settings", return_value=frappe._dict(company="Academy")),
			patch.object(frappe, "get_doc", return_value=player),
			self.assertRaises(frappe.PermissionError),
		):
			service.player_record("P")
		player.check_permission.assert_called_once_with("read")
