from datetime import date
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import player_numbering as numbering
from sports_app import registration


class TestPlayerNumberingAndAge(TestCase):
	def setUp(self):
		reservation = patch("sports_app.player_ids.reserved", return_value=False)
		reservation.start()
		self.addCleanup(reservation.stop)

		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, name, value in [
			(frappe, "throw", throw),
			(registration, "_", lambda s: s),
			(numbering, "_", lambda s: s),
		]:
			active = patch.object(target, name, value)
			active.start()
			self.addCleanup(active.stop)
		self.settings = frappe._dict(
			company="Academy", registration_prefix="MSA", registration_digits=3, timezone="Africa/Lagos"
		)

	def test_counter_key_is_independent_of_month_year_prefix_and_application(self):
		with (
			patch.object(frappe, "db", SimpleNamespace(get_value=Mock(return_value=4))),
			patch.object(numbering, "getseries", side_effect=["005", "006", "007"]) as series,
			patch.object(
				numbering, "academy_date", side_effect=[date(2026, 8, 31), date(2026, 9, 1), date(2027, 1, 1)]
			),
		):
			self.assertEqual(numbering.next_player_id(self.settings), "MSA26-08005")
			self.assertEqual(numbering.next_player_id(self.settings), "MSA26-09006")
			self.settings.registration_prefix = "CLUB"
			self.assertEqual(numbering.next_player_id(self.settings), "CLUB27-01007")
			self.assertEqual(len({call.args[0] for call in series.call_args_list}), 1)

	def test_first_counter_starts_after_existing_matching_legacy_sequence(self):
		db = SimpleNamespace(get_value=Mock(return_value=None), sql=Mock())
		with (
			patch.object(frappe, "db", db),
			patch.object(
				frappe,
				"get_all",
				return_value=[frappe._dict(name=n) for n in ["MSA17-08005", "MSA18-01009", "MFA-00003"]],
			),
			patch.object(numbering, "getseries", return_value="010"),
			patch.object(numbering, "academy_date", return_value=date(2026, 9, 1)),
		):
			self.assertEqual(numbering.next_player_id(self.settings), "MSA26-09010")
			self.assertEqual(db.sql.call_args.args[1][1], 9)

	def test_counter_company_scope_is_separate(self):
		with (
			patch.object(frappe, "db", SimpleNamespace(get_value=Mock(return_value=1))),
			patch.object(numbering, "getseries", return_value="002") as series,
			patch.object(numbering, "academy_date", return_value=date(2026, 9, 1)),
		):
			numbering.next_player_id(self.settings)
			self.settings.company = "Other"
			numbering.next_player_id(self.settings)
			self.assertNotEqual(series.call_args_list[0].args[0], series.call_args_list[1].args[0])

	def test_starting_sequence_accepts_only_positive_whole_numbers(self):
		for value, expected in [(None, 1), ("", 1), (1, 1), ("126", 126), (9999999999, 9999999999)]:
			self.assertEqual(numbering.starting_sequence(value), expected)
		for value in [0, "0", -1, "1.5", "1e3", "001", True, 1.2, "abc", 10000000000]:
			with self.subTest(value=value), self.assertRaises(frappe.ValidationError):
				numbering.starting_sequence(value)

	def test_floor_and_import_advance_existing_counter_without_reset(self):
		db = SimpleNamespace(get_value=Mock(return_value=41), sql=Mock())
		with patch.object(frappe, "db", db):
			self.settings.player_starting_sequence = "126"
			key = numbering.ensure_counter(self.settings)
			db.sql.assert_called_once_with("UPDATE `tabSeries` SET `current`=%s WHERE `name`=%s", (125, key))
			db.sql.reset_mock()
			self.settings.player_starting_sequence = "1"
			numbering.ensure_counter(self.settings)
			db.sql.assert_not_called()
			numbering.ensure_counter(self.settings, minimum=148)
			self.assertEqual(db.sql.call_args.args[1], (148, key))

	def test_first_allocation_uses_highest_import_or_configured_floor(self):
		db = SimpleNamespace(get_value=Mock(return_value=None), sql=Mock())
		with (
			patch.object(frappe, "db", db),
			patch.object(frappe, "get_all", return_value=[frappe._dict(name="MSA17-08042")]),
		):
			self.settings.player_starting_sequence = "126"
			numbering.ensure_counter(self.settings)
			self.assertEqual(db.sql.call_args.args[1][1], 125)

	def test_import_requires_management_and_matching_company(self):
		with (
			patch.object(frappe, "flags", frappe._dict(in_import=True)),
			patch("sports_app.academy.require_settings_access", side_effect=frappe.PermissionError),
			self.assertRaises(frappe.PermissionError),
		):
			numbering.prepare_import(frappe._dict(company="Academy"))
		with (
			patch.object(frappe, "flags", frappe._dict(in_import=True)),
			patch("sports_app.academy.require_settings_access"),
			patch("sports_app.players.registration_settings", return_value=self.settings),
			self.assertRaises(frappe.ValidationError),
		):
			numbering.prepare_import(frappe._dict(company="Other"))

	def test_import_reserves_without_issuing_new_number(self):
		with (
			patch.object(numbering, "prepare_import", return_value=self.settings),
			patch.object(numbering, "ensure_counter") as counter,
			patch.object(numbering, "getseries") as allocate,
		):
			numbering.reserve_imported_sequence(frappe._dict(name="MSA17-08042"))
			counter.assert_called_once_with(self.settings, 42)
			allocate.assert_not_called()
		self.assertEqual(numbering.legacy_sequence("OLD-PLAYER-042", self.settings), 0)

	def test_retired_candidate_is_skipped_without_reusing_identity(self):
		with (
			patch.object(frappe, "db", SimpleNamespace(get_value=Mock(return_value=4))),
			patch.object(numbering, "getseries", side_effect=["005", "006"]),
			patch.object(numbering, "academy_date", return_value=date(2026, 9, 1)),
			patch("sports_app.player_ids.reserved", side_effect=[True, False]),
		):
			self.assertEqual(numbering.next_player_id(self.settings), "MSA26-09006")

	def test_public_age_inclusive_birthday_boundaries(self):
		on = date(2026, 11, 6)
		for birth, age in [("2022-11-06", 4), ("2008-11-06", 18), ("2007-11-07", 18)]:
			self.assertEqual(registration.validate_application_age(birth, on), age)
		for birth in ["2022-11-07", "2007-11-06", "2026-11-19"]:
			with self.subTest(birth=birth), self.assertRaises(frappe.ValidationError):
				registration.validate_application_age(birth, on)

	def test_leap_birthday_uses_calendar_age(self):
		self.assertEqual(registration.validate_application_age("2008-02-29", date(2027, 2, 28)), 18)
		with self.assertRaises(frappe.ValidationError):
			registration.validate_application_age("2008-02-29", date(2027, 3, 1))
