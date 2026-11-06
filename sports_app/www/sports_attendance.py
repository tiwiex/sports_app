"""Uncached content-versioned entry to the public shell; data stays authenticated."""

import hashlib
from pathlib import Path

import frappe
from frappe import _

no_cache = 1
sitemap = 0


def get_context(context):
	html = Path(__file__).resolve().parents[1] / "public" / "attendance" / "index.html"
	if not html.is_file():
		frappe.throw(_("Build and publish the attendance frontend before opening it."))
	version = hashlib.sha256(html.read_bytes()).hexdigest()[:16]
	frappe.flags.redirect_location = f"/assets/sports_app/attendance/index.html?v={version}"
	raise frappe.Redirect(302)
