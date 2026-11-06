"""Retired prototype link returns visitors to the original HTML academy site."""

import frappe

no_cache = 1
sitemap = 0


def get_context(context):
	frappe.flags.redirect_location = "/academy"
	raise frappe.Redirect(302)
