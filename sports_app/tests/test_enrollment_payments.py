import json
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch
import frappe
from sports_app import enrollment_payments as payments
from sports_app.registration_origin import registration_origin, current_registration


class TestEnrollmentPayments(TestCase):
    def setUp(self):
        def throw(message, exc=frappe.ValidationError): raise exc(message)
        for target,name,value in [(frappe,"throw",throw),(payments,"_",lambda s:s)]:
            active=patch.object(target,name,value);active.start();self.addCleanup(active.stop)

    def payment(self, **changes):
        doc=frappe._dict(name="ACC-PAY-2026-00001",sports_registration="REG",party="CUSTOMER",company="Academy",
            payment_type="Receive",party_type="Customer",paid_from="Debtors",paid_to="Bank",paid_amount=250000,
            received_amount=250000,paid_from_account_currency="NGN",paid_to_account_currency="NGN",flags=frappe._dict())
        doc.update(changes);return doc

    def app(self):
        return frappe._dict(payment_entry="ACC-PAY-2026-00001",payment_customer="CUSTOMER",company="Academy",
            payment_snapshot=json.dumps(dict(paid_from="Debtors",paid_to="Bank",total=250000,currency="NGN")))

    def test_linked_payment_provenance_and_financial_values_are_locked(self):
        with patch.object(payments.frappe,"get_doc",return_value=self.app()):
            payments.validate_sports_payment(self.payment())
            for changes in (dict(party="Other"),dict(company="Other"),dict(paid_to="Other"),dict(paid_amount=1),dict(received_amount=1),dict(paid_to_account_currency="USD"),dict(payment_type="Pay"),dict(name="OTHER")):
                with self.subTest(changes=changes),self.assertRaises(frappe.ValidationError):payments.validate_sports_payment(self.payment(**changes))

    def test_unrelated_payment_entries_are_unaffected(self):
        payments.validate_sports_payment(frappe._dict(sports_registration=None))

    def test_forged_boolean_service_flag_cannot_bypass_payment_checks(self):
        with patch.object(payments.frappe,"get_doc",return_value=self.app()),self.assertRaises(frappe.ValidationError):
            payments.validate_sports_payment(self.payment(party="Other",flags=frappe._dict(sports_payment_service=True)))

    def test_registration_origin_is_server_scoped_and_resets_on_error(self):
        self.assertIsNone(current_registration())
        doc=object()
        with self.assertRaises(ValueError):
            with registration_origin(doc):
                self.assertIs(current_registration(),doc)
                raise ValueError()
        self.assertIsNone(current_registration())

    def test_public_response_excludes_accounting_ids_identity_and_token(self):
        snapshot=dict(currency="NGN",registration_fee=220000,jersey_fee=30000,monthly_fee=40000,total=250000,
            bank="Bank",account_number="123",account_name="Academy",bank_account="INTERNAL",paid_to="LEDGER",paid_from="DEBTORS")
        app=frappe._dict(payment_snapshot=json.dumps(snapshot),request_key="SECRET",contact_email="PRIVATE")
        payment=frappe._dict(name="PE",workflow_state="Draft",docstatus=0)
        result=payments._response(app,payment)
        self.assertEqual(result["reference"],"PE");self.assertEqual(result["docstatus"],0)
        self.assertFalse(set(result)&{"request_key","contact_email","bank_account","paid_to","paid_from"})

    def test_disabled_setup_cannot_generate_financial_records(self):
        with self.assertRaises(frappe.ValidationError):payments.payment_configuration(frappe._dict(enrollment_payments_enabled=0))
