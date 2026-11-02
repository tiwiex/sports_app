import json
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, patch
from uuid import uuid4
import frappe
from frappe.utils import CallbackManager
from sports_app import registrations, registrations_api


class TestPublicRegistrations(TestCase):
    def setUp(self):
        def throw(message, exc=frappe.ValidationError):
            raise exc(message)
        for target, name, value in [(frappe, "throw", throw), (frappe, "_", lambda s:s),
            (registrations, "_", lambda s:s), (registrations_api, "_", lambda s:s)]:
            active = patch.object(target, name, value); active.start(); self.addCleanup(active.stop)

    def payload(self):
        return dict(first_name="Sample", last_name="Player", birth_date="2014-05-06", gender="Girl",
            contact_email="sample@example.invalid", guardian_name="Guardian", guardian_phone="08010000000",
            guardian_email="guardian@example.invalid", home_address="Sample address")

    def test_public_payload_rejects_server_owned_and_legacy_bypass_fields(self):
        for changes in ({"company":"Other"}, {"customer":"Existing"}, {"portal_user":"Administrator"},
            {"status":"Accepted"}, {"player":"Existing"}, {"full_name":"Legacy"}):
            with self.subTest(changes=changes), self.assertRaises(frappe.ValidationError):
                registrations.public_payload({**self.payload(), **changes})
        for field in ("first_name", "last_name", "guardian_email", "birth_date"):
            values = self.payload(); values.pop(field)
            with self.subTest(field=field), self.assertRaises(frappe.ValidationError):
                registrations.public_payload(values)
        for value in ([], {}, 123):
            with self.subTest(value=value), self.assertRaises(frappe.ValidationError):
                registrations.public_payload({**self.payload(), "medical_notes": value})

    def test_raw_invalid_flags_and_oversized_body_rejected(self):
        for value in ("yes", 2, [1], {"value":1}):
            with self.subTest(value=value), self.assertRaises(frappe.ValidationError):
                registrations.public_payload({**self.payload(), "media_consent":value})
        with self.assertRaises(frappe.ValidationError): registrations.public_payload("x" * 14001)
        self.assertEqual(registrations.public_payload(self.payload()), self.payload())

    def test_request_keys_are_uuid4(self):
        key = str(uuid4()); self.assertEqual(registrations.request_uuid(key), key)
        for key in (None, "bad", "00000000-0000-1000-8000-000000000000"):
            with self.subTest(key=key), self.assertRaises(frappe.ValidationError): registrations.request_uuid(key)

    def test_native_create_cannot_forge_service_capability(self):
        from sports_app.sports_app.doctype.sports_registration.sports_registration import SportsRegistration
        for capability in (None, True, {}, "SERVICE_CAPABILITY"):
            with self.subTest(capability=capability), self.assertRaises(frappe.PermissionError):
                SportsRegistration.before_insert(SimpleNamespace(flags=frappe._dict(sports_registration_service=capability)))

    def test_private_endpoints_are_role_gated(self):
        with patch.object(registrations_api, "require_player_access", side_effect=frappe.PermissionError), patch.object(registrations, "require_player_access", side_effect=frappe.PermissionError):
            for func, args in [(registrations_api.list_registrations, ()),
                (registrations_api.get_registration, ("x",)), (registrations_api.accept_registration, ("x",)),
                (registrations_api.reject_registration, ("x", "Reason"))]:
                with self.subTest(method=func.__name__), self.assertRaises(frappe.PermissionError): func.__wrapped__(*args)

    def test_no_guest_metadata_permission_or_general_create(self):
        root = Path(registrations.__file__).parent
        doc = json.loads((root / "sports_app/doctype/sports_registration/sports_registration.json").read_text())
        self.assertEqual(doc["name"], "Sports Registration")
        self.assertEqual({row["role"] for row in doc["permissions"]}, {"Sports Registrar", "Sports Academy Administrator", "System Manager"})
        self.assertFalse(any(row.get("create") or row.get("export") or row.get("share") for row in doc["permissions"]))

    def test_failed_acceptance_drops_user_jobs_without_losing_prior_callbacks(self):
        original = CallbackManager(); prior = Mock(); orphan = Mock(); original.add(prior)
        db = SimpleNamespace(after_commit=original, savepoint=Mock(), rollback=Mock())
        with patch.object(registrations.frappe, "db", db), self.assertRaises(ValueError):
            with registrations.acceptance_transaction():
                db.after_commit.add(orphan)
                raise ValueError("Final review save failed")
        self.assertIs(db.after_commit, original)
        original.run(); prior.assert_called_once(); orphan.assert_not_called()
        db.rollback.assert_called_once_with(save_point="sports_acceptance")

    def test_successful_acceptance_preserves_deferred_callbacks(self):
        original = CallbackManager(); callback = Mock()
        db = SimpleNamespace(after_commit=original, savepoint=Mock(), rollback=Mock())
        with patch.object(registrations.frappe, "db", db):
            with registrations.acceptance_transaction(): db.after_commit.add(callback)
        callback.assert_not_called(); original.run(); callback.assert_called_once(); db.rollback.assert_not_called()
