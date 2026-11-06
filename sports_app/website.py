"""Public, app-owned prototype content; never reads operational player records."""

import hashlib
import json
from pathlib import Path


def get_website_content():
	return json.loads(Path(__file__).with_name("website_content.json").read_text())


def asset_url(path):
	content = (Path(__file__).parent / "public" / path).read_bytes()
	version = hashlib.sha256(content).hexdigest()[:12]
	return f"/assets/sports_app/{path}?v={version}"
