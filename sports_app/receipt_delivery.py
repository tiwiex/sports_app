"""Operator-requested delivery of a permission-checked posted Customer receipt."""

import hashlib
from uuid import UUID

import frappe
from frappe import _
from frappe.model import get_permitted_fields
from frappe.utils import get_formatted_email, validate_email_address

from sports_app.player_profile import player_record


def eligible(doc):
	return bool(doc.docstatus == 1 and doc.payment_type == "Receive" and doc.paid_amount > 0)


def can_email(doc):
	return eligible(doc) and all(doc.has_permission(p) for p in ("read", "print", "email"))


def receipt_record(name, receipt, lock=False):
	player = player_record(name)
	doc = frappe.get_doc("Payment Entry", receipt, for_update=lock)
	for permission in ("read", "print", "email"):
		doc.check_permission(permission)
	if (
		not eligible(doc)
		or doc.company != player.company
		or doc.party_type != "Customer"
		or not player.customer
		or doc.party != player.customer
	):
		frappe.throw(_("Select a posted receipt belonging to this player."), frappe.PermissionError)
	return player, doc


def receipt_pdf(doc):
	"""Native print layout without Printview's unconditional Access Log commit."""
	from frappe.utils.pdf import get_pdf
	from frappe.www.printview import get_html_and_style

	format_name = "Sports Academy Receipt"
	rendered = get_html_and_style(
		"Payment Entry", name=doc.name, print_format=format_name, no_letterhead=False
	)
	if not rendered.get("html"):
		frappe.throw(_("The receipt print format could not be rendered."))
	# Security review: literal packaged Frappe template; never caller-supplied template source.
	html = frappe.render_template(  # nosemgrep
		"www/printview.html",
		dict(
			body=rendered["html"],
			print_style=rendered["style"],
			lang=frappe.local.lang or "en",
			layout_direction="ltr",
			title=doc.name,
			doctype="Payment Entry",
			name=doc.name,
			print_format=format_name,
			letterhead="",
			no_letterhead=0,
			key="",
			comment="",
		),
	)
	pdf = get_pdf(html)
	frappe.get_doc(
		doctype="Access Log",
		user=frappe.session.user,
		export_from="Payment Entry",
		reference_document=doc.name,
		file_type="PDF",
		method="Print",
		page="Sports receipt email",
	).db_insert()
	return dict(fname=doc.name.replace("/", "-") + ".pdf", fcontent=pdf)


@frappe.whitelist()
def context(name: str, receipt: str):
	player, doc = receipt_record(name, receipt)
	fields = set(get_permitted_fields("Sports Player", permission_type="read"))
	recipient = next(
		(player.get(k) for k in ("guardian_email", "contact_email") if k in fields and player.get(k)), ""
	)
	return dict(receipt=doc.name, recipient=recipient)


@frappe.whitelist(methods=["POST"])
def send(name: str, receipt: str, recipient: str, request_key: str):
	from sports_app.registrations import acceptance_transaction

	with acceptance_transaction():
		return _send(name, receipt, recipient, request_key)


def _send(name, receipt, recipient, request_key):
	try:
		if str(UUID(request_key, version=4)) != request_key:
			raise ValueError
	except (ValueError, TypeError, AttributeError):
		frappe.throw(_("Invalid delivery request. Reopen the email dialog."))
	if not isinstance(recipient, str) or len(recipient) > 254 or any(c in recipient for c in ",;\r\n<>"):
		frappe.throw(_("Enter one recipient email address."))
	recipient = recipient.strip().lower()
	if not recipient or validate_email_address(recipient, throw=True) != recipient:
		frappe.throw(_("Enter one valid recipient email address."))
	player, doc = receipt_record(name, receipt, lock=True)
	key = (
		"sports-receipt-"
		+ hashlib.sha256(f"{frappe.session.user}|{receipt}|{request_key}".encode()).hexdigest()[:32]
	)
	existing = frappe.db.get_value("Communication", key, ["recipients", "reference_name"], as_dict=True)
	if existing:
		if existing.recipients != recipient or existing.reference_name != doc.name:
			frappe.throw(_("This delivery request already has different details. Reopen the dialog."))
		return dict(communication=key, state="Queued", duplicate=True)
	comm = frappe.get_doc(
		doctype="Communication",
		subject=_("Academy payment receipt: {0}").format(doc.name),
		content=_("Please find your academy payment receipt attached as a PDF."),
		sender=get_formatted_email(frappe.session.user),
		recipients=recipient,
		communication_medium="Email",
		sent_or_received="Sent",
		reference_doctype="Payment Entry",
		reference_name=doc.name,
	)
	# Narrow, audit-linked Communication creation, after native document permissions.
	comm.insert(ignore_permissions=True, set_name=key)
	if not comm.get_outgoing_email_account():
		frappe.throw(_("Configure a default outgoing Email Account before sending receipts."))
	attachment = receipt_pdf(doc)
	# Transactional receipt delivery must also reach disabled future Website Users;
	# do not apply Communication's notification-only disabled-user filtering.
	queued = frappe.sendmail(
		recipients=[recipient],
		sender=comm.sender,
		subject=comm.subject,
		message=comm.content,
		attachments=[attachment],
		reference_doctype="Payment Entry",
		reference_name=doc.name,
		communication=comm.name,
		now=False,
	)
	if not queued:
		frappe.throw(_("Receipt email was not queued. Check the outgoing account and recipient status."))
	return dict(communication=comm.name, state="Queued", duplicate=False)
