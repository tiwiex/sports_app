"""Private, company-scoped club and partner relationships; no outbound effects."""

import hashlib
import re
from urllib.parse import urlparse

import frappe
from frappe.utils import today

from sports_app.academy import require_settings_access, validate_company

DOCTYPES = ("Sports Organization", "Sports Opportunity", "Sports Interaction")


def identity(company, name, country, category):
	parts = [
		re.sub(r"\s+", " ", str(v or "").strip()).casefold()
		for v in (company, name, country, category or "Unspecified")
	]
	return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()


def validate_url(value):
	if value and (urlparse(value).scheme not in ("http", "https") or not urlparse(value).netloc):
		frappe.throw("Use an http or https web address.")


def validate_organization(doc):
	require_settings_access()
	validate_company(doc.company)
	doc.organization_name = re.sub(r"\s+", " ", (doc.organization_name or "").strip())
	if not doc.organization_name:
		frappe.throw("Enter an organization name.")
	for key in ("website", "source_url", "email_source_url", "contact_page"):
		validate_url(doc.get(key))
	rating = doc.get("priority_rating") or "Unrated"
	if rating not in ("Unrated", "1", "2", "3", "4", "5"):
		frappe.throw("Select Unrated or a relationship priority from 1 to 5.")
	previous = doc.get_doc_before_save()
	if previous and previous.company != doc.company:
		frappe.throw("The academy company cannot be changed after creation.", frappe.PermissionError)
	changed = (
		not previous
		or previous.get("priority_rating") != rating
		or previous.get("rating_reason") != doc.get("rating_reason")
	)
	if rating != "Unrated" and not str(doc.get("rating_reason") or "").strip():
		frappe.throw("Explain the relationship-priority assessment.")
	if rating == "Unrated":
		doc.assessed_by = None
		doc.assessed_on = None
	elif changed:
		doc.assessed_by = frappe.session.user
		doc.assessed_on = today()
	else:
		doc.assessed_by = previous.assessed_by
		doc.assessed_on = previous.assessed_on
	doc.priority_rating = rating
	doc.directory_key = identity(doc.company, doc.organization_name, doc.country, doc.get("team_category"))
	# Import provenance is server-owned and may not be forged through forms.
	doc.seed_key = previous.get("seed_key") if previous else getattr(doc.flags, "sports_seed_key", None)


def related_document(doctype, name, company):
	doc = frappe.get_doc(doctype, name)
	doc.check_permission("read")
	if doc.company != company:
		frappe.throw("Linked records must belong to the same academy company.", frappe.PermissionError)
	return doc


def validate_related(doc):
	require_settings_access()
	validate_company(doc.company)
	previous = doc.get_doc_before_save() if hasattr(doc, "get_doc_before_save") else None
	if previous and (previous.company != doc.company or previous.organization != doc.organization):
		frappe.throw(
			"Company and organization links cannot be changed after creation.", frappe.PermissionError
		)
	related_document("Sports Organization", doc.organization, doc.company)
	if doc.get("opportunity"):
		opportunity = related_document("Sports Opportunity", doc.opportunity, doc.company)
		if opportunity.organization != doc.organization:
			frappe.throw("Select an opportunity for this organization.")
	if doc.get("player"):
		related_document("Sports Player", doc.player, doc.company)
