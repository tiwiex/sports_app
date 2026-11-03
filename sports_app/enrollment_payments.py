"""Public enrollment invoice routing and legacy receipt claim compatibility."""
import hmac
import json
import math
from decimal import Decimal
import frappe
from frappe import _
from frappe.rate_limiter import rate_limit
from frappe.utils import flt, now_datetime
from sports_app.registrations import intake_settings, request_uuid
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry

PAYMENT_CAPABILITY = object()


class EnrollmentDraftPayment(PaymentEntry):
    """In-memory factory for a fixed Customer receipt, not a global PE override.

    ERPNext's set_missing_values calls its permission-checked UI account lookup.
    Populate that metadata only for this service's configured accounts instead;
    all remaining native PaymentEntry.validate and document hooks still execute.
    Subsequent native Finance edits use the ordinary ERPNext controller.
    """
    def set_missing_values(self):
        if self.flags.sports_payment_service is not PAYMENT_CAPABILITY or self.payment_type != "Receive" or self.party_type != "Customer":
            frappe.throw(_("Invalid enrollment receipt factory."), frappe.PermissionError)
        from erpnext.accounts.utils import get_balance_on
        from erpnext.accounts.party import complete_contact_details
        self.party_name = frappe.db.get_value("Customer", self.party, "customer_name")
        self.contact_person = frappe.db.get_value("Customer", self.party, "customer_primary_contact")
        complete_contact_details(self)
        self.party_balance = get_balance_on(party_type="Customer", party=self.party, date=self.posting_date,
            company=self.company, ignore_account_permission=True)
        self.party_account = self.paid_from
        for prefix in ("paid_from", "paid_to"):
            account = self.get(prefix)
            self.set(prefix + "_account_currency", frappe.db.get_value("Account", account, "account_currency"))
            self.set(prefix + "_account_type", frappe.db.get_value("Account", account, "account_type"))
            self.set(prefix + "_account_balance", get_balance_on(account, self.posting_date, ignore_account_permission=True))
        self.party_account_currency = self.paid_from_account_currency


def _money(value):
    return Decimal(str(value or 0)).quantize(Decimal("0.01"))


def payment_configuration(settings):
    if not settings.get("enrollment_payments_enabled"):
        frappe.throw(_("Online payment instructions are not configured. Contact the academy."))
    currency = settings.enrollment_payment_currency
    total = flt(settings.enrollment_registration_fee) + flt(settings.enrollment_jersey_fee)
    fees = [flt(settings.enrollment_registration_fee), flt(settings.enrollment_jersey_fee), flt(settings.enrollment_monthly_fee)]
    if not currency or not all(math.isfinite(value) for value in fees) or total <= 0 or min(fees) < 0:
        frappe.throw(_("Configure valid enrollment fees and currency."))
    bank = frappe.get_doc("Bank Account", settings.enrollment_bank_account)
    if bank.disabled or not bank.is_company_account or bank.company != settings.company or not bank.account or not bank.bank_account_no:
        frappe.throw(_("Configure an active academy bank account."))
    for name, kind in ((bank.account, "Bank"), (settings.enrollment_receivable_account, "Receivable")):
        account = frappe.get_doc("Account", name)
        if account.disabled or account.is_group or account.company != settings.company or account.account_type != kind or (account.account_currency or currency) != currency:
            frappe.throw(_("Enrollment accounts must be active, in the academy company and payment currency."))
    if frappe.db.get_value("Company", settings.company, "default_currency") != currency:
        frappe.throw(_("This PoC requires enrollment and company currencies to match."))
    return dict(currency=currency, registration_fee=flt(settings.enrollment_registration_fee),
        jersey_fee=flt(settings.enrollment_jersey_fee), monthly_fee=flt(settings.enrollment_monthly_fee), total=total,
        bank=bank.bank, account_number=bank.bank_account_no, account_name=bank.account_name,
        bank_account=bank.name, paid_to=bank.account, paid_from=settings.enrollment_receivable_account)


def _response(app, payment):
    snapshot = json.loads(app.payment_snapshot)
    return {"reference":payment.name, "state":payment.workflow_state, "docstatus":payment.docstatus,
        "document_type":payment.get("doctype") or "Payment Entry",
        "settled":bool(payment.docstatus == 1 and (payment.get("doctype") != "Sales Invoice" or _money(payment.outstanding_amount) == 0)),
        **{key:snapshot[key] for key in ("currency","registration_fee","jersey_fee","monthly_fee","total","bank","account_number","account_name")}}


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=15, seconds=3600, methods=["POST"])
def make_payment(player, pathway, request_key, website=""):
    from sports_app.enrollment_invoices import prepare_invoice
    return prepare_invoice(player, pathway, request_key, website)


def validate_sports_payment(doc, method=None):
    previous = doc.get_doc_before_save() if callable(getattr(doc, "get_doc_before_save", None)) else None
    if previous and previous.get("sports_registration") and previous.get("sports_registration") != doc.get("sports_registration"):
        frappe.throw(_("Sports payment provenance cannot be removed or reassigned."))
    if not doc.get("sports_registration"):
        return
    if doc.flags.sports_payment_service is PAYMENT_CAPABILITY:
        return
    app = frappe.get_doc("Sports Registration", doc.sports_registration)
    config = json.loads(app.payment_snapshot or "{}")
    if app.payment_entry != doc.name or app.payment_customer != doc.party or app.company != doc.company:
        frappe.throw(_("Sports payment provenance cannot be reassigned."))
    if doc.payment_type != "Receive" or doc.party_type != "Customer" or doc.paid_from != config.get("paid_from") or doc.paid_to != config.get("paid_to"):
        frappe.throw(_("Sports enrollment payment accounts cannot be reassigned."))
    if _money(doc.paid_amount) != _money(config.get("total")) or _money(doc.received_amount) != _money(config.get("total")) or doc.paid_from_account_currency != config.get("currency") or doc.paid_to_account_currency != config.get("currency"):
        frappe.throw(_("Sports enrollment payment amounts/currency must match the registration snapshot."))

    if app.get("sales_invoice"):
        refs = doc.get("references") or []
        if len(refs) != 1 or refs[0].reference_doctype != "Sales Invoice" or refs[0].reference_name != app.sales_invoice or _money(refs[0].allocated_amount) != _money(config.get("total")):
            frappe.throw(_("Enrollment receipts must settle their linked invoice in full."))


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=30, seconds=3600, methods=["POST"])
def payment_made(reference, request_key):
    if frappe.db.exists("Sales Invoice", {"name": str(reference), "sports_registration": ["is", "set"]}):
        from sports_app.enrollment_invoices import claim_invoice
        return claim_invoice(reference, request_key)
    key = request_uuid(request_key)
    settings = intake_settings()  # consistent lock ordering; no guest-selected company/accounts
    name = frappe.db.get_value("Sports Registration", {"payment_entry":str(reference)}, "name", for_update=True)
    if not name:
        frappe.throw(_("Invalid payment reference or registration token."), frappe.PermissionError)
    app = frappe.get_doc("Sports Registration", name, for_update=True)
    if not hmac.compare_digest(str(app.request_key), key):
        frappe.throw(_("Invalid payment reference or registration token."), frappe.PermissionError)
    payment = frappe.get_doc("Payment Entry", app.payment_entry, for_update=True)
    validate_sports_payment(payment)
    if payment.docstatus == 2:
        frappe.throw(_("This payment has been cancelled. Contact the academy."))
    if payment.docstatus == 1 or payment.workflow_state == "Pending Review":
        return _response(app, payment)
    if app.status not in ("Pending", "Accepted") or payment.workflow_state != "Draft":
        frappe.throw(_("This payment cannot be moved to review. Contact the academy."))
    from frappe.model.workflow import get_workflow_name
    workflow = frappe.get_doc("Workflow", get_workflow_name("Payment Entry"))
    if workflow.workflow_state_field != "workflow_state" or not any(row.state=="Pending Review" and int(row.doc_status)==0 for row in workflow.states):
        frappe.throw(_("Payment review workflow is incompatible."))
    # A token-authorized payment claim is not a finance approval. Narrow DB update
    # preserves docstatus=0 and avoids granting Guest general workflow/PE rights or
    # triggering Boost's approval-email hook. Record an explicit audit comment.
    payment.db_set(dict(workflow_state="Pending Review", sports_claimed_on=now_datetime()))
    payment.add_comment("Comment", "Applicant reported a bank transfer. Awaiting Finance verification; no receipt has been posted.")
    from sports_app.payment_notifications import notify_payment_review
    notify_payment_review(app, payment, settings)
    return _response(app, payment)
