"""Transaction-bound notifications for token-authorized website payment claims."""
import json
from html import escape

import frappe
from frappe import _
from frappe.utils import get_url_to_form, validate_email_address


def review_recipients(value):
    """Accept plain comma-separated addresses, normalize and deduplicate them."""
    value = "" if value is None else value
    if not isinstance(value, str) or any(char in value for char in "\r\n;<>"):
        frappe.throw(_("Enter comma-separated email addresses for payment review."))
    recipients = []
    for part in value.split(","):
        address = part.strip().lower()
        if not address:
            continue
        address = validate_email_address(address, throw=True)
        if address not in recipients:
            recipients.append(address)
    if len(recipients) > 50:
        frappe.throw(_("Enter no more than 50 payment review email addresses."))
    return recipients


def notify_payment_review(application, document, settings):
    """Queue alongside the first review transition; caller holds the record lock.

    No SMTP call or commit here: rollback removes both the claim and Email Queue
    entry. Already-reviewed/posted retry paths never call this helper.
    """
    recipients = review_recipients(settings.get("payment_review_emails"))
    if not recipients:
        return
    if application.company != settings.company or document.company != application.company:
        frappe.throw(_("Payment review settings do not match the enrollment company."), frappe.PermissionError)
    if document.doctype not in ("Sales Invoice", "Payment Entry"):
        frappe.throw(_("Invalid enrollment payment document."))
    snapshot = json.loads(application.payment_snapshot)
    reference = escape(document.name)
    url = escape(get_url_to_form(document.doctype, document.name), quote=True)
    message = "".join([
        "<p>", _("A website applicant has reported a bank transfer for enrollment."), "</p>",
        "<p>", _("Reference"), ": <strong>", reference, "</strong><br>",
        _("Company"), ": ", escape(application.company), "<br>",
        _("Expected amount"), ": ", escape(str(snapshot["currency"])), " ", escape(str(snapshot["total"])), "</p>",
        "<p>", _("Awaiting Finance review. This is an applicant's payment claim, not confirmation of cleared funds. Verify the bank credit before completing payment."), "</p>",
        '<p><a href="', url, '">', _("Review payment"), "</a></p>",
    ])
    frappe.sendmail(
        recipients=recipients,
        subject=_("Enrollment payment awaiting review: {0}").format(document.name),
        message=message,
        reference_doctype=document.doctype,
        reference_name=document.name,
        delayed=True,
        now=False,
        expose_recipients=False,
        add_unsubscribe_link=0,
    )
