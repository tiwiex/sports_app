import json
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

import frappe

from sports_app import attendance_api
from sports_app import attendance_mobile_api as mobile


class TestAttendanceMobile(TestCase):
	def test_guest_receives_no_private_configuration_or_token(self):
		with (
			patch.object(frappe, "session", SimpleNamespace(user="Guest")),
			patch.object(mobile, "get_configured_settings") as settings,
		):
			response = mobile.bootstrap.__wrapped__()
		self.assertEqual(json.loads(response.data), {"message": {"authenticated": False}})
		self.assertEqual(response.headers["Cache-Control"], "no-store, private")
		settings.assert_not_called()

	def test_staff_bootstrap_checks_role_company_and_has_narrow_no_store_response(self):
		settings = frappe._dict(
			company="Academy",
			academy_name="Sports Academy",
			timezone="Africa/Lagos",
			payment_review_emails="private@example.test",
		)
		with (
			patch.object(frappe, "session", SimpleNamespace(user="staff@example.test")),
			patch.object(mobile.policy, "require_access") as access,
			patch.object(mobile, "validate_company") as company,
			patch.object(mobile, "get_configured_settings", return_value=settings),
			patch.object(mobile, "get_csrf_token", return_value="session-only-token"),
			patch.object(mobile, "can_manage_settings", return_value=True),
		):
			response = mobile.bootstrap.__wrapped__()
		access.assert_called_once()
		company.assert_called_once_with("Academy")
		self.assertEqual(
			set(json.loads(response.data)["message"]),
			{
				"authenticated",
				"user",
				"academy_name",
				"company",
				"timezone",
				"today",
				"csrf_token",
				"can_prepare_biometrics",
			},
		)
		self.assertEqual(response.headers["Vary"], "Cookie")
		self.assertNotIn("private@example.test", response.get_data(as_text=True))

	def test_denied_staff_cannot_get_offline_bootstrap(self):
		with (
			patch.object(frappe, "session", SimpleNamespace(user="finance@example.test")),
			patch.object(mobile.policy, "require_access", side_effect=frappe.PermissionError),
			patch.object(mobile, "get_configured_settings") as settings,
		):
			with self.assertRaises(frappe.PermissionError):
				mobile.bootstrap.__wrapped__()
		settings.assert_not_called()

	def test_roster_marking_capability_requires_session_and_attendance_write_and_valid_date(self):
		for status, date, session_write, row_write, allowed in [
			("Scheduled", "2020-01-01", True, True, True),
			("Cancelled", "2020-01-01", True, True, False),
			("Scheduled", "2099-01-01", True, True, False),
			("Scheduled", "2020-01-01", False, True, False),
			("Scheduled", "2020-01-01", True, False, False),
		]:
			session = frappe._dict(
				name="QA",
				company="Academy",
				timezone="Africa/Lagos",
				status=status,
				session_date=date,
				has_permission=lambda permission: session_write,
			)
			with (
				self.subTest(status=status, date=date, session_write=session_write, row_write=row_write),
				patch.object(attendance_api.policy, "get_session", return_value=session),
				patch.object(frappe, "get_list", return_value=[]),
				patch.object(frappe, "has_permission", return_value=row_write),
			):
				self.assertEqual(attendance_api.roster.__wrapped__("QA")["can_mark"], allowed)
