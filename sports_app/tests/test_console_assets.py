from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch
from sports_app import console_assets as assets


class TestConsoleAssets(TestCase):
 def test_changed_source_gets_a_new_url_and_old_content_is_preserved(self):
  with TemporaryDirectory() as folder, patch.object(assets,'_root',return_value=Path(folder)):
   for filename in assets.FILES:(Path(folder)/filename).write_text('// first version')
   assets.publish_assets()
   old=assets.asset_url('players.js');old_file=Path(folder)/'releases'/old.rsplit('/',1)[-1]
   (Path(folder)/'players.js').write_text('// updated, no payer selection')
   new=assets.asset_url('players.js');self.assertNotEqual(old,new)
   assets.publish_assets()
   self.assertEqual(old_file.read_text(),'// first version')
   self.assertEqual((Path(folder)/'releases'/new.rsplit('/',1)[-1]).read_text(),'// updated, no payer selection')
   assets.publish_assets();self.assertEqual(assets.asset_url('players.js'),new)

 def test_only_known_app_assets_can_be_published(self):
  with self.assertRaises(ValueError):assets.asset_url('../private.js')
