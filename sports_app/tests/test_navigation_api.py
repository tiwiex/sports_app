from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import navigation_api


class TestNavigationCounts(TestCase):
	def setUp(self):
		translation = patch.object(navigation_api, "_", lambda value: value)
		translation.start()
		self.addCleanup(translation.stop)
		for name, value in (
			("has_console_permission", True),
			("can_manage_players", True),
			("can_manage_settings", True),
		):
			active = patch.object(navigation_api, name, return_value=value)
			setattr(self, name, active.start())
			self.addCleanup(active.stop)
		for name, value in (
			("get_configured_settings", Mock(return_value=frappe._dict(company="Academy"))),
			("validate_company", Mock()),
		):
			active = patch.object(navigation_api, name, value)
			setattr(self, name, active.start())
			self.addCleanup(active.stop)
		self.native = SimpleNamespace(
			has_permission=Mock(return_value=True),
			get_list=Mock(return_value=[frappe._dict(total=31)]),
			PermissionError=frappe.PermissionError,
			throw=lambda message, error: self.raise_error(error, message),
		)
		active = patch.object(navigation_api, "frappe", self.native)
		active.start()
		self.addCleanup(active.stop)

	@staticmethod
	def raise_error(error, message):
		raise error(message)

	def test_counts_use_native_permissions_company_and_pending_queue(self):
		result = navigation_api.get_counts.__wrapped__()
		self.assertEqual(len(result), 4)
		self.assertEqual(result["sports_app:players"]["count"], 31)
		self.validate_company.assert_called_once_with("Academy")
		for call in self.native.get_list.call_args_list:
			self.assertEqual(call.kwargs["filters"]["company"], "Academy")
			self.assertEqual(call.kwargs["fields"], ["count(name) as total"])
			self.assertNotIn("ignore_permissions", call.kwargs)
		self.assertEqual(self.native.get_list.call_args_list[0].kwargs["filters"]["status"], "Pending")

	def test_guest_and_finance_only_cannot_query(self):
		self.has_console_permission.return_value = False
		with self.assertRaises(frappe.PermissionError):
			navigation_api.get_counts.__wrapped__()
		self.native.get_list.assert_not_called()

	def test_basic_console_does_not_read_settings_or_records(self):
		self.can_manage_players.return_value = False
		self.can_manage_settings.return_value = False
		self.assertEqual(navigation_api.get_counts.__wrapped__(), {})
		self.get_configured_settings.assert_not_called()
		self.native.get_list.assert_not_called()

	def test_registrar_has_no_management_count_and_denied_doctype_is_omitted(self):
		self.can_manage_settings.return_value = False
		self.native.has_permission.side_effect = lambda doctype, _ptype: doctype != "Sports Session"
		self.assertEqual(
			set(navigation_api.get_counts.__wrapped__()), {"sports_app:registrations", "sports_app:players"}
		)

	def test_company_denial_prevents_all_counts_and_zero_is_valid(self):
		self.validate_company.side_effect = frappe.PermissionError
		with self.assertRaises(frappe.PermissionError):
			navigation_api.get_counts.__wrapped__()
		self.native.get_list.assert_not_called()
		self.validate_company.side_effect = None
		self.native.get_list.return_value = [frappe._dict(total=0)]
		self.assertEqual(navigation_api.get_counts.__wrapped__()["sports_app:players"]["count"], 0)
