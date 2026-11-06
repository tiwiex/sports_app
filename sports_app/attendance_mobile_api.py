"""Authenticated bootstrap; all writes reuse the existing attendance service."""

import json

import frappe
from frappe.sessions import get_csrf_token
from werkzeug.wrappers import Response

from sports_app import attendance as policy
from sports_app.academy import can_manage_settings, get_configured_settings, validate_company


@frappe.whitelist(allow_guest=True, methods=["GET"])
def bootstrap():
	if frappe.session.user == "Guest":
		result = {"authenticated": False}
	else:
		policy.require_access()
		settings = get_configured_settings()
		validate_company(settings.company)
		result = {
			"authenticated": True,
			"user": frappe.session.user,
			"academy_name": settings.academy_name,
			"company": settings.company,
			"timezone": settings.timezone,
			"today": str(policy.datetime.now(policy.ZoneInfo(settings.timezone)).date()),
			"csrf_token": get_csrf_token(),
			"can_prepare_biometrics": can_manage_settings(),
		}
	return Response(
		json.dumps({"message": result}),
		mimetype="application/json",
		headers={"Cache-Control": "no-store, private", "Vary": "Cookie"},
	)
