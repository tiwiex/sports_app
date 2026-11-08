from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from sports_app import console_assets as assets


class TestSportsConsoleAssets(TestCase):
	def test_url_publishes_new_source_before_advertising_and_retains_old_version(self):
		with TemporaryDirectory() as directory, patch.object(assets, "_root", return_value=Path(directory)):
			source = Path(directory) / "subscription_console.js"
			source.write_text("window.version = 1;")
			first = assets.asset_url(source.name)
			published = Path(directory) / "releases" / first.rsplit("/", 1)[1]
			self.assertEqual(published.read_bytes(), source.read_bytes())
			source.write_text("window.version = 2;")
			second = assets.asset_url(source.name)
			self.assertNotEqual(first, second)
			self.assertEqual(published.read_text(), "window.version = 1;")
			self.assertEqual((published.parent / second.rsplit("/", 1)[1]).read_bytes(), source.read_bytes())
			self.assertEqual(list(published.parent.glob(".sports-asset-*")), [])

	def test_missing_or_damaged_release_is_repaired_but_unknown_filename_rejected(self):
		with TemporaryDirectory() as directory, patch.object(assets, "_root", return_value=Path(directory)):
			source = Path(directory) / "billing.js"
			source.write_text("window.billing = true;")
			url = assets.asset_url(source.name)
			release = Path(directory) / "releases" / url.rsplit("/", 1)[1]
			release.write_text("incomplete")
			release.chmod(0o600)
			self.assertEqual(assets.asset_url(source.name), url)
			self.assertEqual(release.read_bytes(), source.read_bytes())
			self.assertEqual(release.stat().st_mode & 0o777, 0o644)
			with self.assertRaises(ValueError):
				assets.asset_url("../private.js")
