from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import registrations_api as api


class TestRegistrationList(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, name, value in ((frappe, "throw", throw), (api, "_", lambda s: s)):
			active = patch.object(target, name, value)
			active.start()
			self.addCleanup(active.stop)

	def test_sort_allowlist_and_stable_order_are_applied_before_pagination(self):
		with (
			patch.object(api, "require_player_access"),
			patch.object(frappe, "get_list", return_value=[]) as query,
		):
			for field in ("name", "full_name", "requested_pathway", "submitted_on", "status"):
				api.list_registrations.__wrapped__("Pending", 20, field, "asc")
				kwargs = query.call_args.kwargs
				self.assertEqual(
					kwargs["order_by"], f"{field} asc" + (", name asc" if field != "name" else "")
				)
				self.assertEqual(kwargs["start"], 20)
				self.assertEqual(kwargs["page_length"], 20)
				self.assertEqual(kwargs["filters"], {"status": "Pending"})
			for field, direction in [
				("request_key", "asc"),
				("name; drop table x", "asc"),
				("name", "desc; select 1"),
			]:
				with self.subTest(field=field), self.assertRaises(frappe.ValidationError):
					api.list_registrations.__wrapped__(sort_by=field, sort_order=direction)

	def test_review_capability_is_document_write_permission_and_pending_only(self):
		for status, write, expected in [
			("Pending", True, True),
			("Pending", False, False),
			("Accepted", True, False),
			("Rejected", True, False),
		]:
			row = frappe._dict(name="REG", status=status)
			with (
				self.subTest(status=status, write=write),
				patch.object(api, "require_player_access"),
				patch.object(frappe, "get_list", return_value=[row]),
				patch.object(
					frappe, "get_doc", return_value=SimpleNamespace(has_permission=Mock(return_value=write))
				),
			):
				result = api.list_registrations.__wrapped__(status)
				self.assertEqual(result[0]["can_review"], expected)

	def test_list_role_gate_still_runs_before_any_query(self):
		with (
			patch.object(api, "require_player_access", side_effect=frappe.PermissionError),
			patch.object(frappe, "get_list") as query,
			self.assertRaises(frappe.PermissionError),
		):
			api.list_registrations.__wrapped__()
		query.assert_not_called()
