from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

from sports_app import console


class TestSportsConsole(TestCase):
	def test_roles_and_manifest(self):
		fake = SimpleNamespace(session=SimpleNamespace(user="sports@test"), get_roles=lambda user: ["Sports Console"])
		with patch.object(console, "frappe", fake):
			self.assertTrue(console.has_console_permission())
			fake.get_roles = lambda user: ["Accounts User"]
			self.assertFalse(console.has_console_permission())
			self.assertFalse(console.has_console_permission("Guest"))
		with patch("sports_app.academy.can_manage_settings", return_value=False):
			manifest = console.get_provider()
		self.assertEqual(manifest["id"], "sports_app")
		self.assertEqual(manifest["views"][0]["key"], "sports_app:overview")

	def test_setup_without_boost_does_not_import_host(self):
		fake = SimpleNamespace(db=SimpleNamespace(exists=lambda *args: True), get_installed_apps=lambda: ["frappe", "sports_app"], get_attr=Mock())
		with patch.object(console, "frappe", fake):
			console.setup_console()
		fake.get_attr.assert_not_called()

	def test_setup_synchronizes_host_without_assigning_roles(self):
		fake = SimpleNamespace(db=SimpleNamespace(exists=lambda doctype, *args: doctype != "Role"), get_installed_apps=lambda: ["frappe", "sports_app", "erp_boost"], get_attr=Mock(), get_doc=Mock())
		with patch.object(console, "frappe", fake):
			console.setup_console()
		fake.get_doc.assert_any_call({"doctype": "Role", "role_name": "Sports Console", "desk_access": 1})
		fake.get_doc.assert_any_call({"doctype": "Role", "role_name": "Sports Academy Administrator", "desk_access": 1})
		fake.get_attr.assert_called_once_with("erp_boost.console_entry_setup.ensure_page_roles")

	def test_explicit_login_redirect_is_preserved(self):
		cache = SimpleNamespace(hset=Mock())
		fake = SimpleNamespace(session=SimpleNamespace(user="sports@test"), get_installed_apps=lambda: ["sports_app", "erp_boost"], get_roles=lambda user: ["Sports Console"], form_dict={"redirect-to": "/app/profile"}, cache=cache)
		with patch.object(console, "frappe", fake):
			console.set_console_login_redirect()
			cache.hset.assert_not_called()
			fake.form_dict = {}
			console.set_console_login_redirect()
		cache.hset.assert_called_once_with("redirect_after_login", "sports@test", "/app/boost-console")

	def test_master_read_access_covers_system_and_sports_administrators(self):
		fake = SimpleNamespace(
			db=SimpleNamespace(exists=lambda doctype, *args: doctype != "Custom DocPerm"),
			get_installed_apps=lambda: [],
		)
		with patch.object(console, "frappe", fake), patch("frappe.permissions.add_permission") as add_permission:
			console.setup_console()
		for role in ("Sports Academy Administrator", "System Manager"):
			for doctype in ("Company", "Currency"):
				add_permission.assert_any_call(doctype, role, ptype="read")
		self.assertEqual(add_permission.call_count, 4)
