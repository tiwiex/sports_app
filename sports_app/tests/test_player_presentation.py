from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import players_api as api


class TestPlayerPresentation(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, name, value in [(frappe, "throw", throw), (api, "_", lambda s: s)]:
			active = patch.object(target, name, value)
			active.start()
			self.addCleanup(active.stop)

	def test_sort_allowlist_applied_before_bounded_pagination(self):
		with (
			patch.object(api, "require_player_access"),
			patch.object(frappe, "get_list", return_value=[]) as query,
		):
			for field in ("name", "full_name", "birth_date", "company", "registered_on"):
				api.list_players.__wrapped__("Player", 20, field, "asc")
				self.assertEqual(
					query.call_args.kwargs["order_by"],
					field + " asc" + (", name asc" if field != "name" else ""),
				)
				self.assertEqual(query.call_args.kwargs["start"], 20)
				self.assertEqual(query.call_args.kwargs["page_length"], 20)
			for field, direction in [("customer", "asc"), ("name; select 1", "asc"), ("name", "invalid")]:
				with self.subTest(field=field), self.assertRaises(frappe.ValidationError):
					api.list_players.__wrapped__(sort_by=field, sort_order=direction)

	def test_menu_requires_both_player_write_and_enrollment_create(self):
		for write, create in [(True, True), (True, False), (False, True)]:
			row = frappe._dict(name="P")
			with (
				patch.object(api, "require_player_access"),
				patch.object(frappe, "get_list", return_value=[row]),
				patch.object(
					frappe, "get_doc", return_value=SimpleNamespace(has_permission=Mock(return_value=write))
				),
				patch.object(frappe, "has_permission", return_value=create),
			):
				self.assertEqual(api.list_players.__wrapped__()[0]["can_enroll"], write and create)

	def test_profile_fields_are_allowlisted_and_read_and_company_checks_remain(self):
		doc = frappe._dict(
			name="P",
			full_name="Sample Player",
			company="Academy",
			secret_scholarship="private",
			check_permission=Mock(),
			has_permission=Mock(return_value=False),
		)
		with (
			patch.object(api, "require_player_access"),
			patch.object(frappe, "get_doc", return_value=doc),
			patch.object(api, "validate_company") as scope,
			patch.object(frappe, "get_list", return_value=[]),
		):
			result = api.get_player.__wrapped__("P")
			doc.check_permission.assert_called_once_with("read")
			scope.assert_called_once_with("Academy")
			self.assertNotIn("secret_scholarship", result["player"])
			self.assertFalse(result["can_enroll"])
			self.assertTrue(result["fields"])
