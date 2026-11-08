from datetime import date
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import dashboard


class TestAcademyDashboard(TestCase):
	def setUp(self):
		for key, value in (
			("has_console_permission", True),
			("can_manage_players", True),
			("can_manage_settings", True),
			("can_read", True),
			("get_configured_settings", frappe._dict(company="Academy", academy_name="Academy")),
			("validate_company", None),
			("academy_date", date(2026, 11, 7)),
			("overview", {"billed": "40000", "outstanding": "40000"}),
		):
			active = patch.object(dashboard, key, return_value=value)
			setattr(self, key, active.start())
			self.addCleanup(active.stop)

		def fail(message, error):
			raise error(message)

		def query(doctype, **kwargs):
			if doctype == "Sports Player":
				return ["VISIBLE"]
			if kwargs.get("fields") == ["count(name) as total"]:
				return [frappe._dict(total=2)]
			return []

		self.native = SimpleNamespace(
			get_list=Mock(side_effect=query),
			has_permission=Mock(return_value=True),
			throw=fail,
			PermissionError=frappe.PermissionError,
		)
		active = patch.object(dashboard, "frappe", self.native)
		active.start()
		self.addCleanup(active.stop)
		active = patch.object(dashboard, "_", lambda s: s)
		active.start()
		self.addCleanup(active.stop)

	def test_scope_and_native_counts_with_visible_player_intersection(self):
		data = dashboard.get_dashboard.__wrapped__()
		self.assertEqual(data["counts"]["players"], 1)
		self.validate_company.assert_called_once_with("Academy")
		self.overview.assert_called_once_with(2026)
		for call in self.native.get_list.call_args_list:
			self.assertEqual(call.kwargs["filters"]["company"], "Academy")
			self.assertNotIn("ignore_permissions", call.kwargs)
		enrollment = next(c for c in self.native.get_list.call_args_list if c.args[0] == "Sports Enrollment")
		self.assertEqual(enrollment.kwargs["filters"]["player"], ["in", ["VISIBLE"]])
		self.assertEqual(enrollment.kwargs["filters"]["status"], "Active")
		session = next(c for c in self.native.get_list.call_args_list if c.args[0] == "Sports Session")
		self.assertEqual(session.kwargs["filters"]["session_date"], ["between", ["2026-11-01", "2026-11-30"]])

	def test_guest_rejected_before_settings_or_queries(self):
		self.has_console_permission.return_value = False
		with self.assertRaises(frappe.PermissionError):
			dashboard.get_dashboard.__wrapped__()
		self.get_configured_settings.assert_not_called()
		self.native.get_list.assert_not_called()

	def test_basic_console_returns_restricted_without_reading_settings(self):
		self.can_manage_players.return_value = False
		self.can_manage_settings.return_value = False
		self.can_read.return_value = False
		self.assertEqual(dashboard.get_dashboard.__wrapped__(), {"restricted": True})
		self.get_configured_settings.assert_not_called()
		self.overview.assert_not_called()

	def test_native_denials_show_restricted_not_zero(self):
		self.native.has_permission.return_value = False
		data = dashboard.get_dashboard.__wrapped__()
		self.assertTrue(all(v is None for v in data["counts"].values()))
		self.assertIsNone(data["finance"])
		self.assertIsNone(data["upcoming"])
		self.native.get_list.assert_not_called()
		self.overview.assert_not_called()

	def test_registrar_cannot_read_finance_or_settings_links(self):
		self.can_read.return_value = False
		self.can_manage_settings.return_value = False
		data = dashboard.get_dashboard.__wrapped__("2025")
		self.assertIsNone(data["finance"])
		self.overview.assert_not_called()
		self.assertNotIn("sports_app:billing", [l["view"] for l in data["links"]])
		self.assertNotIn("sports_app:settings", [l["view"] for l in data["links"]])

	def test_invalid_year_rejected_and_december_rolls_over(self):
		with self.assertRaises(Exception):
			dashboard.get_dashboard.__wrapped__("2026 OR 1=1")
		self.native.get_list.assert_not_called()
		self.academy_date.return_value = date(2026, 12, 31)
		dashboard.get_dashboard.__wrapped__()
		filters = next(
			c.kwargs["filters"] for c in self.native.get_list.call_args_list if c.args[0] == "Sports Session"
		)
		self.assertEqual(filters["session_date"], ["between", ["2026-12-01", "2026-12-31"]])
