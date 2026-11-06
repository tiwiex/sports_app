from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4

import frappe

from sports_app import enrollment_accounts as accounts
from sports_app import players
from sports_app import registrations_api as api


class TestEnrollmentAccounts(TestCase):
	def setUp(self):
		def throw(message, exc=frappe.ValidationError):
			raise exc(message)

		for target, key, value in [(frappe, "throw", throw), (accounts, "_", lambda s: s)]:
			active = patch.object(target, key, value)
			active.start()
			self.addCleanup(active.stop)

	def test_existing_user_player_and_pending_app_reserve_player_email(self):
		for conflict in ["User", "Sports Player", "Sports Registration", None]:
			db = SimpleNamespace(exists=Mock(side_effect=lambda dt, *args: dt == conflict))
			with patch.object(frappe, "db", db):
				self.assertEqual(accounts.player_email_available("player@example.invalid"), conflict is None)

	def test_acceptance_excludes_own_application_but_not_siblings(self):
		db = SimpleNamespace(exists=Mock(return_value=False))
		with patch.object(frappe, "db", db):
			self.assertTrue(accounts.player_email_available("player@example.invalid", "APP"))
			self.assertEqual(
				db.exists.call_args.args[1],
				{"contact_email": "player@example.invalid", "status": "Pending", "name": ["!=", "APP"]},
			)

	def test_preflight_returns_only_boolean_and_own_retry_can_continue(self):
		for own in [False, "APP"]:
			with (
				patch.object(frappe, "db", SimpleNamespace(exists=Mock(return_value=own))),
				patch.object(accounts, "player_email_available", return_value=False),
				patch.object(frappe.utils, "validate_email_address"),
			):
				result = api.check_player_email.__wrapped__.__wrapped__(
					" Player@Example.invalid ", str(uuid4())
				)
				self.assertEqual(result, {"available": bool(own)})

	def test_multiple_players_reuse_existing_guardian_without_user_edits(self):
		with (
			patch.object(players, "require_player_access"),
			patch.object(frappe, "db", SimpleNamespace(exists=Mock(return_value="guardian@example.invalid"))),
			patch.object(frappe, "get_doc") as create,
			patch.object(frappe.utils, "validate_email_address"),
		):
			for email in ["first@example.invalid", "second@example.invalid"]:
				player = frappe._dict(
					contact_email=email, guardian_email="Guardian@Example.invalid", db_set=Mock()
				)
				self.assertEqual(accounts.create_guardian_user(player), "guardian@example.invalid")
				player.db_set.assert_called_once_with(
					"guardian_user", "guardian@example.invalid", update_modified=False
				)
			create.assert_not_called()

	def test_same_player_and_guardian_email_is_rejected(self):
		with (
			patch.object(players, "require_player_access"),
			patch.object(frappe.utils, "validate_email_address"),
			self.assertRaises(frappe.ValidationError),
		):
			accounts.create_guardian_user(
				frappe._dict(contact_email="same@example.invalid", guardian_email="Same@Example.invalid")
			)

	def test_new_guardian_is_disabled_roleless_website_user_without_mail(self):
		user = SimpleNamespace(
			flags=frappe._dict(),
			enabled=0,
			user_type="Website User",
			roles=[],
			name="guardian@example.invalid",
			insert=Mock(),
		)
		player = frappe._dict(
			contact_email="child@example.invalid",
			guardian_email="guardian@example.invalid",
			guardian_name="Guardian",
			db_set=Mock(),
		)
		flags = frappe._dict(setting_role=False)
		with (
			patch.object(players, "require_player_access"),
			patch.object(frappe, "flags", flags),
			patch.object(frappe, "db", SimpleNamespace(exists=Mock(return_value=False))),
			patch.object(frappe, "get_doc", return_value=user) as create,
			patch.object(frappe.utils, "validate_email_address"),
		):
			accounts.create_guardian_user(player)
			self.assertFalse(flags.setting_role)
			self.assertEqual(create.call_args.kwargs["enabled"], 0)
			self.assertEqual(create.call_args.kwargs["send_welcome_email"], 0)
			self.assertEqual(create.call_args.kwargs["roles"], [])
			user.insert.assert_called_once_with(ignore_permissions=True)

	def test_duplicate_email_is_checked_before_financial_completion(self):
		from contextlib import nullcontext

		from sports_app import enrollment_invoices, players_api

		doc = frappe._dict(
			name="APP",
			status="Pending",
			company="Academy",
			program="PROGRAM",
			payment_customer="",
			sales_invoice="INV",
			acceptance_key=str(uuid4()),
		)
		with (
			patch.object(api, "require_player_access"),
			patch.object(api, "registration_settings", return_value=frappe._dict(company="Academy")),
			patch.object(api, "review_record", return_value=doc),
			patch.object(api, "today", return_value="2026-11-06"),
			patch.object(api, "acceptance_transaction", return_value=nullcontext()),
			patch.object(players, "validate_player_email", side_effect=frappe.ValidationError),
			patch.object(enrollment_invoices, "complete_payment") as complete,
			patch.object(players_api, "register_player") as register,
			self.assertRaises(frappe.ValidationError),
		):
			api.accept_registration.__wrapped__("APP")
		complete.assert_not_called()
		register.assert_not_called()
