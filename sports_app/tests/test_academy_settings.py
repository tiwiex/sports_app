from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch

import frappe

from sports_app import academy, console, settings_api


def valid_values(**changes):
	values = dict(
		academy_name="Moyours Academy",
		company="Moyours",
		currency="NGN",
		timezone="Africa/Lagos",
		registration_prefix="MOY",
		registration_digits=5,
		default_enrollment_status="Pending",
		default_program="Football",
		monthly_fees_enabled=1,
		default_monthly_fee=15000,
	)
	values.update(changes)
	return values


class TestAcademySettings(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, name, value in (
			(academy, "_", lambda text: text),
			(settings_api, "_", lambda text: text),
			(frappe, "throw", throw),
		):
			active = patch.object(target, name, value)
			active.start()
			self.addCleanup(active.stop)

	def test_enrollment_grid_rejects_child_metadata_and_wrong_shapes(self):
		with (
			patch.object(settings_api, "require_settings_access"),
			patch.object(frappe, "parse_json", side_effect=lambda v: v),
		):
			for rows in ({}, [{"doctype": "User"}], [{}] * 31):
				with self.assertRaises(frappe.ValidationError):
					settings_api.save_configuration.__wrapped__({"enrollment_items": rows})

	def test_two_academies_are_configuration_not_code(self):
		for values in (
			valid_values(),
			valid_values(
				academy_name="River Club",
				company="River",
				currency="EUR",
				timezone="Europe/Berlin",
				registration_prefix="RIVER",
				registration_digits=7,
				default_program="Swimming",
				default_monthly_fee=45,
			),
		):
			with self.subTest(academy=values["academy_name"]):
				academy.validate_settings_values(values)

	def test_missing_defaults_are_named(self):
		with self.assertRaises(frappe.ValidationError) as result:
			academy.validate_settings_values(valid_values(default_program="", company=""))
		self.assertIn("Default program", str(result.exception))
		self.assertIn("Company", str(result.exception))

	def test_invalid_numbering_timezone_and_fees_rejected(self):
		for change in (
			dict(registration_prefix="../x"),
			dict(registration_digits=2),
			dict(timezone="Invalid/Zone"),
			dict(default_monthly_fee=0),
			dict(default_monthly_fee=-1),
			dict(default_enrollment_status="Surprise"),
		):
			with self.subTest(change=change), self.assertRaises(frappe.ValidationError):
				academy.validate_settings_values(valid_values(**change))

	def test_no_fees_requires_explicit_opt_out(self):
		academy.validate_settings_values(valid_values(monthly_fees_enabled=0, default_monthly_fee=0))

	def test_out_of_scope_company_denied(self):
		doc = object()
		with (
			patch.object(academy.frappe, "get_doc", return_value=doc),
			patch.object(academy.frappe, "has_permission", return_value=False),
			self.assertRaises(frappe.PermissionError),
		):
			academy.validate_company("Other Company")

	def test_settings_menu_is_not_a_basic_sports_capability(self):
		with (
			patch.object(academy, "can_manage_settings", return_value=False),
			patch("sports_app.players.can_manage_players", return_value=False),
			patch("sports_app.billing_access.can_read", return_value=False),
		):
			self.assertEqual(len(console.get_provider()["views"]), 1)
		with (
			patch.object(academy, "can_manage_settings", return_value=True),
			patch("sports_app.players.can_manage_players", return_value=True),
			patch("sports_app.billing_access.can_read", return_value=True),
		):
			self.assertIn("sports_app:settings", [row["key"] for row in console.get_provider()["views"]])
			self.assertIn("sports_app:development", [row["key"] for row in console.get_provider()["views"]])

	def test_settings_api_rejects_non_managers(self):
		with patch.object(academy, "can_manage_settings", return_value=False):
			for func, args in (
				(settings_api.get_configuration, ()),
				(settings_api.save_configuration, ({},)),
				(settings_api.save_program, ({},)),
				(settings_api.save_group, ({},)),
			):
				with self.subTest(endpoint=func.__name__), self.assertRaises(frappe.PermissionError):
					func.__wrapped__(*args)

	def test_settings_api_rejects_arbitrary_document_fields(self):
		with patch.object(settings_api, "require_settings_access"), self.assertRaises(frappe.ValidationError):
			settings_api.save_configuration.__wrapped__({"owner": "Administrator"})

	def test_stale_settings_are_not_overwritten(self):
		doc = SimpleNamespace(modified="2026-11-01 10:00:00", check_permission=Mock())
		with (
			patch.object(settings_api, "require_settings_access"),
			patch.object(settings_api, "get_configured_settings", return_value=doc),
			self.assertRaises(frappe.TimestampMismatchError),
		):
			settings_api.save_configuration.__wrapped__({"modified": "2026-11-01 09:00:00"})

	def test_settings_reject_cross_company_program(self):
		doc = frappe._dict(valid_values())
		doc.as_dict = lambda: valid_values()
		program = SimpleNamespace(company="Another", enabled=1, check_permission=Mock())
		with (
			patch.object(academy, "require_settings_access"),
			patch.object(academy, "validate_company"),
			patch.object(academy.frappe, "db", SimpleNamespace(exists=Mock(return_value=True))),
			patch.object(academy.frappe, "get_doc", return_value=program),
			self.assertRaises(frappe.ValidationError),
		):
			academy.validate_settings(doc)

	def test_default_group_must_belong_to_default_program(self):
		values = valid_values(default_group="OTHER-GROUP")
		doc = frappe._dict(values)
		doc.as_dict = lambda: values
		program = SimpleNamespace(name="Football", company="Moyours", enabled=1, check_permission=Mock())
		group = SimpleNamespace(program="Swimming", company="Moyours", enabled=1, check_permission=Mock())
		with (
			patch.object(academy, "require_settings_access"),
			patch.object(academy, "validate_company"),
			patch.object(academy.frappe, "db", SimpleNamespace(exists=Mock(return_value=True))),
			patch.object(academy.frappe, "get_doc", side_effect=[program, group]),
			self.assertRaises(frappe.ValidationError),
		):
			academy.validate_settings(doc)

	def test_empty_single_does_not_inherit_global_company_or_currency(self):
		class Settings:
			def __init__(self):
				self.values = {"company": "Global company", "currency": "USD"}
				self.meta = SimpleNamespace(
					get_field=lambda name: SimpleNamespace(
						fieldtype="Data",
						default={
							"registration_digits": 5,
							"default_enrollment_status": "Pending",
							"monthly_fees_enabled": 1,
						}.get(name),
					)
				)

			def set(self, name, value):
				self.values[name] = value

		doc = Settings()
		with (
			patch.object(academy.frappe, "get_single", return_value=doc),
			patch.object(academy.frappe, "db", SimpleNamespace(get_singles_dict=lambda dt: {})),
		):
			result = academy.get_configured_settings()
		self.assertIsNone(result.values["company"])
		self.assertIsNone(result.values["currency"])
		self.assertEqual(result.values["registration_digits"], 5)

	def test_saved_settings_values_are_preserved(self):
		doc = SimpleNamespace(meta=SimpleNamespace(get_field=lambda name: None), set=Mock())
		stored = {key: "saved" for key in academy.SETTINGS_FIELDS}
		with (
			patch.object(academy.frappe, "get_single", return_value=doc),
			patch.object(academy.frappe, "db", SimpleNamespace(get_singles_dict=lambda dt: stored)),
		):
			self.assertIs(academy.get_configured_settings(), doc)
		doc.set.assert_not_called()

	def test_enrollment_series_defaults_and_supported_patterns(self):
		self.assertEqual(academy.enrollment_series(None), "MSA-ENR-.YYYY.-.#####")
		self.assertEqual(academy.enrollment_series(""), "MSA-ENR-.YYYY.-.#####")
		for series in ("MSA-ENR-.YYYY.-.#####", "RIVER-ENR-.######"):
			self.assertEqual(academy.enrollment_series(series), series)
			academy.validate_settings_values(valid_values(enrollment_naming_series=series))

	def test_enrollment_series_rejects_expressions_and_invalid_counters(self):
		for series in (
			"field:company",
			"format:{company}",
			"MSA-ENR-.###",
			"MSA-ENR-.###########",
			"MSA-ENR-.MM.-.#####",
			"../../MSA-.#####",
			"msa-.#####",
			123,
		):
			with self.subTest(series=series), self.assertRaises(frappe.ValidationError):
				academy.enrollment_series(series)

	def test_application_autoname_uses_saved_setting_without_touching_other_references(self):
		from sports_app.sports_app.doctype.sports_registration import sports_registration as controller

		doc = SimpleNamespace(name=None)
		with (
			patch.object(
				controller,
				"get_configured_settings",
				return_value=frappe._dict(enrollment_naming_series="RIVER-ENR-.######"),
			),
			patch("frappe.model.naming.make_autoname", return_value="RIVER-ENR-000001") as autoname,
		):
			controller.SportsRegistration.autoname(doc)
			self.assertEqual(doc.name, "RIVER-ENR-000001")
			autoname.assert_called_once_with("RIVER-ENR-.######", doc=doc)
