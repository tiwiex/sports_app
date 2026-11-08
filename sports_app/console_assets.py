"""Content-addressed console assets, published by install/migrate hooks."""

import hashlib
from pathlib import Path
from tempfile import NamedTemporaryFile

FILES = (
	"finance_documents.js",
	"console_navigation.js",
	"console_overview.js",
	"players.js",
	"billing.js",
	"subscription_console.js",
	"player_profile.js",
	"player_id_change.js",
	"registrations.js",
	"academy_settings.js",
	"development_tools.js",
	"relations.js",
	"attendance.js",
	"attendance_app_link.js",
)


def _root():
	return Path(__file__).resolve().parent / "public" / "js"


def _content(filename):
	if filename not in FILES:
		raise ValueError("Unknown Sports console asset")
	content = (_root() / filename).read_bytes()
	digest = hashlib.sha256(content).hexdigest()[:16]
	return content, filename[:-3] + "." + digest + ".js"


def _publish(filename):
	content, published = _content(filename)
	destination = _root() / "releases"
	destination.mkdir(parents=True, exist_ok=True)
	target = destination / published
	if not target.exists() or target.read_bytes() != content or target.stat().st_mode & 0o444 != 0o444:
		# Publish complete bytes atomically before advertising this versioned URL.
		with NamedTemporaryFile(dir=destination, prefix=".sports-asset-", delete=False) as handle:
			handle.flush()
			temporary = Path(handle.name)
			try:
				handle.write(content)
				handle.flush()
				# Static files must also be readable by the separate web-server user.
				temporary.chmod(0o644)
			except Exception:
				temporary.unlink(missing_ok=True)
				raise
		try:
			temporary.replace(target)
		finally:
			temporary.unlink(missing_ok=True)
	return published


def asset_url(filename):
	# Source edits must never leave a provider pointing at an unpublished hash.
	return "/assets/sports_app/js/releases/" + _publish(filename)


def publish_assets():
	"""Keep older immutable files for already-open pages; never reuse a changed URL."""
	for filename in FILES:
		_publish(filename)
