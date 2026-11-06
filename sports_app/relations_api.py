"""Read-only catalogue API; writes use native documents and controllers."""

import frappe
from frappe.utils import cint

from sports_app.academy import require_settings_access, validate_company
from sports_app.relations import DOCTYPES

FIELDS = {
	"Sports Organization": [
		"name",
		"organization_name",
		"organization_type",
		"sport",
		"country",
		"region",
		"team_category",
		"public_email",
		"email_purpose",
		"email_source_url",
		"email_checked_on",
		"contact_page",
		"contact_notes",
		"priority_rating",
		"relationship_status",
		"source_url",
		"source_checked_on",
	],
	"Sports Opportunity": ["name", "title", "organization", "opportunity_type", "status", "next_follow_up"],
	"Sports Interaction": [
		"name",
		"subject",
		"organization",
		"interaction_type",
		"occurred_on",
		"next_follow_up",
	],
}


SORT_FIELDS = {
	"Sports Organization": (
		"organization_name",
		"country",
		"sport",
		"priority_rating",
		"relationship_status",
		"public_email",
		"email_purpose",
	),
	"Sports Opportunity": ("title", "opportunity_type", "status", "next_follow_up"),
	"Sports Interaction": ("subject", "interaction_type", "occurred_on", "next_follow_up"),
}


@frappe.whitelist()
def list_records(
	doctype="Sports Organization",
	company=None,
	search="",
	rating="",
	country="",
	start=0,
	has_email=0,
	sort_by="",
	sort_order="asc",
	relationship="",
):
	require_settings_access()
	if doctype not in DOCTYPES:
		frappe.throw("Select a Sports relationship record.")
	if not company:
		from sports_app.academy import get_configured_settings

		company = get_configured_settings().company
	validate_company(company)
	sort_by = sort_by or SORT_FIELDS[doctype][0]
	if sort_by not in SORT_FIELDS[doctype] or sort_order not in ("asc", "desc"):
		frappe.throw("Select a valid sort column and direction.")
	filters = {"company": company}
	if doctype == "Sports Organization":
		if rating:
			if rating not in ("Unrated", "1", "2", "3", "4", "5"):
				frappe.throw("Invalid priority rating.")
			filters["priority_rating"] = rating
		if relationship:
			if relationship not in ("Prospect", "Contacted", "Active", "Paused", "Closed"):
				frappe.throw("Invalid relationship status.")
			filters["relationship_status"] = relationship
		if country:
			filters["country"] = str(country)[:100]
		if cint(has_email):
			filters["public_email"] = ["is", "set"]
	text = str(search or "").strip()[:100]
	title = {
		"Sports Organization": "organization_name",
		"Sports Opportunity": "title",
		"Sports Interaction": "subject",
	}[doctype]
	or_filters = [[title, "like", "%" + text + "%"]] if text else None
	if text and doctype == "Sports Organization":
		or_filters.append(["public_email", "like", "%" + text + "%"])
	rows = frappe.get_list(
		doctype,
		filters=filters,
		or_filters=or_filters,
		fields=FIELDS[doctype],
		order_by=sort_by + " " + sort_order + ", name asc",
		start=max(0, cint(start)),
		page_length=31,
	)
	has_more = len(rows) > 30
	rows = rows[:30]
	names = list({row.organization for row in rows if row.get("organization")})
	labels = (
		{
			row.name: row.organization_name
			for row in frappe.get_list(
				"Sports Organization",
				filters={"company": company, "name": ["in", names]},
				fields=["name", "organization_name"],
				page_length=30,
			)
		}
		if names
		else {}
	)
	for row in rows:
		if row.get("organization"):
			row["organization_label"] = labels.get(row.organization, row.organization)
	countries = frappe.get_list(
		"Sports Organization",
		filters={"company": company},
		fields=["country"],
		group_by="country",
		page_length=200,
	)
	return dict(
		company=company,
		rows=rows,
		has_more=has_more,
		sort_by=sort_by,
		sort_order=sort_order,
		countries=sorted(row.country for row in countries if row.country),
	)


@frappe.whitelist(methods=["POST"])
def import_club_directory(company=None):
	"""Explicit, idempotent opt-in import; never sends messages or rates clubs."""
	import json
	from pathlib import Path

	from sports_app.relations import identity

	require_settings_access()
	if not company:
		from sports_app.academy import get_configured_settings

		company = get_configured_settings().company
	validate_company(company)
	# Serialize company imports so retries cannot race the unique directory identity.
	frappe.db.get_value("Company", company, "name", for_update=True)
	rows = json.loads((Path(__file__).resolve().parent / "data/club_directory.json").read_text())
	created = skipped = 0
	for row in rows:
		key = identity(company, row["organization_name"], row["country"], row["team_category"])
		existing = frappe.db.exists(
			"Sports Organization", {"company": company, "directory_key": key}
		) or frappe.db.exists("Sports Organization", {"company": company, "seed_key": row["seed_key"]})
		if existing:
			skipped += 1
			continue
		doc = frappe.get_doc(
			{
				"doctype": "Sports Organization",
				"company": company,
				**{k: v for k, v in row.items() if k != "seed_key"},
				"priority_rating": "Unrated",
				"relationship_status": "Prospect",
			}
		)
		doc.flags.sports_seed_key = row["seed_key"]
		doc.insert()
		created += 1
	return dict(created=created, skipped=skipped)


def contact_updates(existing, row):
	"""Fill reviewed contact gaps; never replace a staff contact or its attribution."""
	email_fields = ("public_email", "email_purpose", "email_source_url", "email_checked_on")
	if existing.get("public_email"):
		return {}
	updates = {}
	if row.get("public_email") and not any(existing.get(key) for key in email_fields):
		updates.update({key: row[key] for key in email_fields})
	for key in ("contact_page", "contact_notes"):
		if row.get(key) and not existing.get(key):
			updates[key] = row[key]
	return updates


@frappe.whitelist(methods=["POST"])
def enrich_club_contacts(company=None):
	"""Apply reviewed public contact data only; no email delivery/probing occurs."""
	import json
	from pathlib import Path

	require_settings_access()
	if not company:
		from sports_app.academy import get_configured_settings

		company = get_configured_settings().company
	validate_company(company)
	frappe.db.get_value("Company", company, "name", for_update=True)
	rows = json.loads((Path(__file__).resolve().parent / "data/club_contacts.json").read_text())
	updated = skipped = 0
	for row in rows:
		name = frappe.db.get_value(
			"Sports Organization", {"company": company, "seed_key": row["seed_key"]}, "name"
		)
		if not name:
			skipped += 1
			continue
		doc = frappe.get_doc("Sports Organization", name)
		doc.check_permission("write")
		updates = contact_updates(doc, row)
		if not updates:
			skipped += 1
			continue
		doc.update(updates)
		doc.save()
		updated += 1
	return dict(updated=updated, skipped=skipped)
