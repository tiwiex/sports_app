"""Content-addressed console assets, published by install/migrate hooks."""
import hashlib
from pathlib import Path

FILES = ("console_overview.js", "players.js", "registrations.js", "academy_settings.js", "development_tools.js", "relations.js", "attendance.js")


def _root():
 return Path(__file__).resolve().parent / "public" / "js"


def _content(filename):
 if filename not in FILES: raise ValueError("Unknown Sports console asset")
 content = (_root() / filename).read_bytes()
 digest = hashlib.sha256(content).hexdigest()[:16]
 return content, filename[:-3] + "." + digest + ".js"


def asset_url(filename):
 _content_bytes, published = _content(filename)
 return "/assets/sports_app/js/releases/" + published


def publish_assets():
 """Keep older immutable files for already-open pages; never reuse a changed URL."""
 destination = _root() / "releases"
 destination.mkdir(parents=True, exist_ok=True)
 for filename in FILES:
  content, published = _content(filename)
  target = destination / published
  if not target.exists() or target.read_bytes() != content:
   target.write_bytes(content)
