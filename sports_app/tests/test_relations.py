import json
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import relations, relations_api


class Doc(SimpleNamespace):
	def get(self, key, default=None):
		return getattr(self, key, default)


class TestRelationships(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		p = patch.object(frappe, "throw", throw)
		p.start()
		self.addCleanup(p.stop)
		p = patch.object(relations, "require_settings_access")
		p.start()
		self.addCleanup(p.stop)
		p = patch.object(relations, "validate_company")
		p.start()
		self.addCleanup(p.stop)
		self.doc = Doc(
			company="Academy",
			organization_name=" Club  One ",
			country="Nigeria",
			team_category="Men",
			priority_rating="Unrated",
			seed_key="forged",
			flags=SimpleNamespace(),
			get_doc_before_save=lambda: None,
		)

	def test_identity_normalizes_spacing_case_and_separates_company_and_team(self):
		self.assertEqual(
			relations.identity("A", "Club One", "Nigeria", "Men"),
			relations.identity("a", " CLUB  ONE ", "nigeria", "men"),
		)
		self.assertNotEqual(
			relations.identity("A", "X", "NG", "Men"), relations.identity("B", "X", "NG", "Men")
		)
		self.assertNotEqual(
			relations.identity("A", "X", "NG", "Men"), relations.identity("A", "X", "NG", "Women")
		)

	def test_unrated_has_no_assessor_and_forged_seed_is_removed(self):
		relations.validate_organization(self.doc)
		self.assertEqual(self.doc.organization_name, "Club One")
		self.assertIsNone(self.doc.assessed_by)
		self.assertIsNone(self.doc.seed_key)

	def test_rating_requires_reason_and_valid_range(self):
		for value in ("0", "6", "5.0", "Excellent"):
			self.doc.priority_rating = value
			with self.assertRaises(frappe.ValidationError):
				relations.validate_organization(self.doc)
		self.doc.priority_rating = "5"
		with self.assertRaises(frappe.ValidationError):
			relations.validate_organization(self.doc)

	def test_assessor_is_current_user_and_previous_audit_is_preserved(self):
		self.doc.priority_rating = "4"
		self.doc.rating_reason = "Relevant age pathway"
		with (
			patch.object(frappe, "session", SimpleNamespace(user="assessor")),
			patch.object(relations, "today", return_value="2026-11-02"),
		):
			relations.validate_organization(self.doc)
		self.assertEqual(self.doc.assessed_by, "assessor")
		previous = Doc(
			company="Academy",
			priority_rating="4",
			rating_reason=self.doc.rating_reason,
			assessed_by="original",
			assessed_on="2026-11-01",
			seed_key="trusted",
		)
		self.doc.get_doc_before_save = lambda: previous
		relations.validate_organization(self.doc)
		self.assertEqual(self.doc.assessed_by, "original")
		self.assertEqual(self.doc.seed_key, "trusted")

	def test_only_web_urls_allowed(self):
		for value in ("javascript:alert(1)", "file:///tmp/data", "https:broken"):
			with self.assertRaises(frappe.ValidationError):
				relations.validate_url(value)
		relations.validate_url("https://club.example/contact")

	def test_cross_company_links_and_native_read_denial(self):
		linked = Doc(company="Other", check_permission=Mock())
		with patch.object(frappe, "get_doc", return_value=linked):
			with self.assertRaises(frappe.PermissionError):
				relations.related_document("Sports Organization", "ORG", "Academy")
		linked.company = "Academy"
		linked.check_permission.side_effect = frappe.PermissionError
		with patch.object(frappe, "get_doc", return_value=linked):
			with self.assertRaises(frappe.PermissionError):
				relations.related_document("Sports Organization", "ORG", "Academy")

	def test_interaction_must_match_opportunity_organization(self):
		doc = Doc(company="A", organization="ORG1", opportunity="OPP")
		with patch.object(relations, "related_document", side_effect=[Doc(), Doc(organization="ORG2")]):
			with self.assertRaises(frappe.ValidationError):
				relations.validate_related(doc)

	def test_public_dataset_has_sources_unique_keys_and_no_ratings_or_contacts(self):
		rows = json.loads((Path(relations.__file__).parent / "data/club_directory.json").read_text())
		self.assertEqual(len(rows), 171)
		self.assertEqual(len({r["seed_key"] for r in rows}), 171)
		self.assertEqual({r["country"] for r in rows}, {"Nigeria", "Spain", "Germany", "United Kingdom"})
		for row in rows:
			self.assertTrue(row["source_url"].startswith("https://"))
			self.assertFalse(set(row) & {"priority_rating", "public_email", "public_phone", "assessed_by"})

	def test_import_skips_existing_rows_and_preserves_assessments(self):
		fake = SimpleNamespace(
			db=SimpleNamespace(get_value=Mock(), exists=Mock(return_value="EXISTING")), get_doc=Mock()
		)
		with (
			patch.object(relations_api, "frappe", fake),
			patch.object(relations_api, "require_settings_access"),
			patch.object(relations_api, "validate_company"),
		):
			result = relations_api.import_club_directory.__wrapped__(company="Academy")
		self.assertEqual(result, dict(created=0, skipped=171))
		fake.get_doc.assert_not_called()

	def test_native_controllers_and_import_reject_unauthorised_calls(self):
		with patch.object(relations, "require_settings_access", side_effect=frappe.PermissionError):
			with self.assertRaises(frappe.PermissionError):
				relations.validate_organization(self.doc)
		with patch.object(relations_api, "require_settings_access", side_effect=frappe.PermissionError):
			with self.assertRaises(frappe.PermissionError):
				relations_api.import_club_directory.__wrapped__(company="Academy")
			with self.assertRaises(frappe.PermissionError):
				relations_api.list_records.__wrapped__(company="Academy")

	def test_contact_enrichment_preserves_staff_email_and_attribution(self):
		row = dict(
			public_email="published@club.example",
			email_purpose="General",
			email_source_url="https://club.example/contact",
			email_checked_on="2026-11-02",
			contact_page="https://club.example/contact",
		)
		self.assertEqual(relations_api.contact_updates({"public_email": "staff@club.example"}, row), {})
		updates = relations_api.contact_updates({}, row)
		self.assertEqual(updates["public_email"], "published@club.example")
		self.assertEqual(updates["email_source_url"], row["email_source_url"])
		self.assertEqual(relations_api.contact_updates(updates, row), {})

	def test_contact_enrichment_does_not_mix_partial_staff_provenance(self):
		row = dict(
			public_email="published@club.example",
			email_purpose="General",
			email_source_url="https://club.example/contact",
			email_checked_on="2026-11-02",
		)
		self.assertEqual(
			relations_api.contact_updates({"email_source_url": "https://staff.example"}, row), {}
		)
		for value in ["javascript:alert(1)", "mailto:person@example.com"]:
			self.doc.email_source_url = value
			with self.assertRaises(frappe.ValidationError):
				relations.validate_organization(self.doc)

	def test_contact_dataset_targets_known_clubs_and_records_provenance(self):
		root = Path(relations.__file__).parent / "data"
		keys = {r["seed_key"] for r in json.loads((root / "club_directory.json").read_text())}
		contacts = json.loads((root / "club_contacts.json").read_text())
		self.assertEqual(len(contacts), 19)
		self.assertEqual(sum(bool(r.get("public_email")) for r in contacts), 14)
		for row in contacts:
			self.assertIn(row["seed_key"], keys)
			if row.get("public_email"):
				self.assertIn("@", row["public_email"])
				self.assertTrue(row["email_source_url"].startswith("https://"))
				self.assertTrue(row["email_purpose"])
				self.assertTrue(row["email_checked_on"])

	def test_sort_and_combined_filters_apply_before_pagination(self):
		rows = [Doc(name=str(i)) for i in range(31)]
		with (
			patch.object(relations_api, "require_settings_access"),
			patch.object(relations_api, "validate_company") as scope,
			patch.object(frappe, "get_list", side_effect=[rows, [Doc(country="Nigeria")]]) as query,
		):
			result = relations_api.list_records.__wrapped__(
				company="Academy",
				country="Nigeria",
				relationship="Active",
				search="United",
				has_email=1,
				sort_by="country",
				sort_order="desc",
				start=30,
			)
		scope.assert_called_once_with("Academy")
		args = query.call_args_list[0].kwargs
		self.assertEqual(args["order_by"], "country desc, name asc")
		self.assertEqual(args["start"], 30)
		self.assertEqual(args["page_length"], 31)
		self.assertEqual(
			args["filters"],
			{
				"company": "Academy",
				"country": "Nigeria",
				"relationship_status": "Active",
				"public_email": ["is", "set"],
			},
		)
		self.assertEqual(
			args["or_filters"],
			[["organization_name", "like", "%United%"], ["public_email", "like", "%United%"]],
		)
		self.assertEqual(len(result["rows"]), 30)
		self.assertTrue(result["has_more"])

	def test_reject_unapproved_sort_columns_directions_and_relationships(self):
		with (
			patch.object(relations_api, "require_settings_access"),
			patch.object(relations_api, "validate_company"),
			patch.object(frappe, "get_list") as query,
		):
			for options in (
				{"sort_by": "country desc; select 1"},
				{"sort_by": "company"},
				{"sort_order": "DESC NULLS LAST"},
				{"relationship": "forged"},
				{"doctype": "Sports Opportunity", "sort_by": "organization_name"},
			):
				with self.assertRaises(frappe.ValidationError):
					relations_api.list_records.__wrapped__(company="Academy", **options)
			query.assert_not_called()

	def test_default_sort_and_final_page(self):
		with (
			patch.object(relations_api, "require_settings_access"),
			patch.object(relations_api, "validate_company"),
			patch.object(frappe, "get_list", return_value=[]) as query,
		):
			result = relations_api.list_records.__wrapped__(company="Academy", start=-10)
		self.assertEqual(query.call_args_list[0].kwargs["order_by"], "organization_name asc, name asc")
		self.assertEqual(query.call_args_list[0].kwargs["start"], 0)
		self.assertFalse(result["has_more"])
