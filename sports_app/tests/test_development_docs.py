from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

import frappe

from sports_app import development_api as api


class TestDevelopmentDocs(TestCase):
	def setUp(self):
		self.temp = TemporaryDirectory()
		self.addCleanup(self.temp.cleanup)
		self.root = Path(self.temp.name) / "docs"
		self.root.mkdir()
		(self.root / "REQUIREMENTS.md").write_text("# Requirements\n\nCurrent rules.")

		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, name, value in (
			(api, "_root", lambda: self.root),
			(api, "require_settings_access", lambda: None),
			(api, "_", lambda s: s),
			(frappe, "throw", throw),
		):
			active = patch.object(target, name, value)
			active.start()
			self.addCleanup(active.stop)

	def test_role_required_for_every_endpoint(self):
		with patch.object(api, "require_settings_access", side_effect=frappe.PermissionError):
			for method, args in (
				(api.get_documents, ()),
				(api.get_document, ("REQUIREMENTS.md",)),
				(api.get_asset, ("x.png",)),
			):
				with self.subTest(method=method.__name__), self.assertRaises(frappe.PermissionError):
					method.__wrapped__(*args)

	def test_paths_and_symlink_escape_rejected(self):
		outside = self.root.parent / "private.md"
		outside.write_text("secret")
		(self.root / "linked.md").symlink_to(outside)
		for path in (
			"../private.md",
			str(outside),
			"a/../../private.md",
			"..\\private.md",
			"linked.md",
			"file.py",
		):
			with self.subTest(path=path), self.assertRaises(frappe.PermissionError):
				api.get_document.__wrapped__(path)
		self.assertEqual(
			[row["path"] for row in api.get_documents.__wrapped__()["documents"]], ["REQUIREMENTS.md"]
		)

	def test_index_discovers_new_build_logs_and_requirement_documents(self):
		folder = self.root / "build-logs"
		folder.mkdir()
		(folder / "2026-11-01-adjustment.md").write_text("# Adjustment evidence\nPass")
		rows = api.get_documents.__wrapped__()["documents"]
		self.assertTrue(
			any(row["title"] == "Adjustment evidence" and row["category"] == "Build Logs" for row in rows)
		)
		self.assertTrue(any(row["category"] == "Requirements" for row in rows))

	def test_rendered_document_is_sanitized(self):
		(self.root / "unsafe.md").write_text(
			'# Rules\n<script>alert(1)</script>\n<a href="javascript:alert(2)">bad</a>'
		)
		html = api.get_document.__wrapped__("unsafe.md")["html"]
		self.assertNotIn("<script", html.lower())
		self.assertNotIn("javascript:", html.lower())

	def test_images_and_size_limits(self):
		(self.root / "test.png").write_bytes(b"\x89PNG\r\n\x1a\n")
		self.assertTrue(
			api.get_asset.__wrapped__("test.png")["data_url"].startswith("data:image/png;base64,")
		)
		with self.assertRaises(frappe.PermissionError):
			api.get_asset.__wrapped__("REQUIREMENTS.md")
		(self.root / "huge.md").write_text("x" * (512 * 1024 + 1))
		with self.assertRaises(frappe.ValidationError):
			api.get_document.__wrapped__("huge.md")


class TestDocumentationRoot(TestCase):
	def test_frappe_module_path_normalization_does_not_rename_docs_folder(self):
		with TemporaryDirectory() as folder:
			base = Path(folder)
			(base / "doc-sports").mkdir()

			def module_path(app, *joins):
				return str(base.joinpath(*(part.replace("-", "_") for part in joins)))

			with patch.object(api.frappe, "get_app_path", side_effect=module_path):
				self.assertEqual(api._root(), base / "doc-sports")
				self.assertTrue(api._root().is_dir())
