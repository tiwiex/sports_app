from datetime import date
from unittest import TestCase
from unittest.mock import patch

import frappe

from sports_app.players import PLAYER_FIELDS
from sports_app.registration import get_registration_fields, validate_registration_details


class TestRegistrationDetails(TestCase):
	def setUp(self):
		def throw(message, *args, **kwargs):
			raise frappe.ValidationError(message)

		for name, value in (("throw", throw), ("_", lambda text: text)):
			active = patch.object(frappe, name, value)
			active.start()
			self.addCleanup(active.stop)
		active = patch("sports_app.registration._", lambda text: text)
		active.start()
		self.addCleanup(active.stop)

	def player(self, **changes):
		doc = frappe._dict(
			first_name=" Sample ",
			last_name="Player",
			birth_date="2014-05-06",
			gender="Girl",
			contact_email="sample@example.invalid",
			guardian_name="Guardian",
			guardian_phone="08010000000",
			guardian_email="guardian@example.invalid",
			home_address="Sample address",
		)
		doc.update(changes)
		doc.is_new = lambda: True
		doc.set = lambda key, value: doc.__setitem__(key, value)
		return doc

	def test_shared_schema_cannot_expose_server_owned_identity_fields(self):
		names = {
			field["fieldname"] for field in get_registration_fields() if field["fieldtype"] != "Section Break"
		}
		self.assertTrue(names <= set(PLAYER_FIELDS))
		self.assertFalse(
			names.intersection({"customer", "portal_user", "company", "request_key", "registration_program"})
		)

	def test_names_and_dates_normalize_without_preselected_consent(self):
		doc = self.player()
		validate_registration_details(doc)
		self.assertEqual(doc.full_name, "Sample Player")
		self.assertEqual(doc.birth_date, date(2014, 5, 6))
		self.assertEqual((doc.medical_consent, doc.media_consent, doc.terms_accepted), (0, 0, 0))
		validate_registration_details(doc)  # native Date values are accepted too

	def test_structured_registration_requires_reference_details(self):
		for name in (
			"last_name",
			"birth_date",
			"gender",
			"guardian_name",
			"guardian_phone",
			"guardian_email",
			"home_address",
		):
			with self.subTest(field=name), self.assertRaises(frappe.ValidationError):
				validate_registration_details(self.player(**{name: ""}))

	def test_bad_enums_emails_dates_consent_and_lengths_rejected(self):
		for changes in (
			{"gender": "Other value"},
			{"preferred_position": "Unknown"},
			{"guardian_email": "not-email"},
			{"birth_date": []},
			{"media_consent": 2},
			{"medical_consent": "yes"},
			{"medical_notes": "x" * 2001},
			{"first_name": "x" * 141},
		):
			with self.subTest(changes=changes), self.assertRaises((frappe.ValidationError, ValueError)):
				validate_registration_details(self.player(**changes))

	def test_emergency_contact_requires_pair(self):
		for changes in ({"emergency_contact_name": "Emergency"}, {"emergency_contact_phone": "08020000000"}):
			with self.subTest(changes=changes), self.assertRaises(frappe.ValidationError):
				validate_registration_details(self.player(**changes))
		validate_registration_details(
			self.player(emergency_contact_name="Emergency", emergency_contact_phone="08020000000")
		)

	def test_legacy_full_name_records_remain_supported(self):
		doc = self.player(
			first_name="", last_name="", full_name="Legacy Player", guardian_email="", home_address=""
		)
		validate_registration_details(doc)
		self.assertEqual(doc.full_name, "Legacy Player")
