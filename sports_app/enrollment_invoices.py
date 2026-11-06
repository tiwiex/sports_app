"""Invoice-first enrolment and atomic, finance-authorised payment completion."""

import hmac
import json

import frappe
from frappe import _
from frappe.utils import cint, now_datetime, today

from sports_app.academy import validate_company
from sports_app.enrollment_payments import _money, _response, payment_configuration
from sports_app.registrations import acceptance_transaction, intake_settings, request_uuid

INVOICE_CAPABILITY = object()


def invoice_configuration(settings):
	config = payment_configuration(settings)
	company = frappe.get_doc("Company", settings.company)
	account = (
		frappe.get_doc("Account", company.default_income_account) if company.default_income_account else None
	)
	if (
		not account
		or account.company != company.name
		or account.disabled
		or account.is_group
		or account.root_type != "Income"
	):
		frappe.throw(_("Set an active company default income account for enrollment invoicing."))
	center = frappe.get_doc("Cost Center", company.cost_center) if company.cost_center else None
	if not center or center.company != company.name or center.is_group or center.disabled:
		frappe.throw(_("Set a company default cost center for enrollment invoicing."))
	config.update(income_account=account.name, cost_center=center.name, items=[])
	for field, amount, label in (
		("enrollment_registration_item", config["registration_fee"], "Registration fee"),
		("enrollment_jersey_item", config["jersey_fee"], "Jersey (2 sets)"),
	):
		if not amount:
			continue
		code = settings.get(field)
		item = frappe.get_doc("Item", code) if code else None
		if not item or item.disabled or item.is_stock_item or not item.is_sales_item:
			frappe.throw(_("Configure active non-stock enrollment fee items in Academy Settings."))
		config["items"].append(
			dict(
				item_code=code,
				item_name=label,
				description=label,
				qty=1,
				rate=amount,
				uom=item.stock_uom,
				stock_uom=item.stock_uom,
				conversion_factor=1,
				income_account=account.name,
				cost_center=center.name,
			)
		)
	return config


def invoice_workflow():
	from frappe.model.workflow import get_workflow_name

	name = get_workflow_name("Sales Invoice")
	if not name:
		frappe.throw(_("Enrollment invoice review workflow is not configured."))
	workflow = frappe.get_doc("Workflow", name)
	states = {s.state: cint(s.doc_status) for s in workflow.states}
	if (
		workflow.workflow_state_field != "workflow_state"
		or not workflow.states
		or workflow.states[0].state != "Draft"
		or states.get("Draft") != 0
		or states.get("Pending Review") != 0
	):
		frappe.throw(_("Enrollment invoice workflow needs Draft and Pending Review states with docstatus 0."))
	return workflow


def prepare_invoice(player, pathway, request_key, website=""):
	from sports_app.players import _ensure_program_category, _insert_identity_customer
	from sports_app.registrations_api import _submit_registration

	settings = intake_settings()
	with acceptance_transaction():
		receipt = _submit_registration(player, pathway, request_key, website)
		app = frappe.get_doc("Sports Registration", receipt["reference"], for_update=True)
		if app.get("sales_invoice"):
			invoice = frappe.get_doc("Sales Invoice", app.sales_invoice, for_update=True)
			validate_enrollment_invoice(invoice)
			if invoice.docstatus == 2:
				frappe.throw(_("This invoice was cancelled. Contact the academy."))
			return _response(app, invoice)
		if app.payment_entry:  # preserve older enrolments; never generate a second obligation
			payment = frappe.get_doc("Payment Entry", app.payment_entry, for_update=True)
			if payment.docstatus == 2:
				frappe.throw(_("This payment reference was cancelled. Contact the academy."))
			return _response(app, payment)
		if app.status != "Pending":
			frappe.throw(_("Contact the academy about this reviewed registration."))
		config = invoice_configuration(settings)
		invoice_workflow()
		group = _ensure_program_category(
			frappe.db.get_value("Sports Program", app.program, "program_name").strip()
		)
		prospect = frappe._dict(app.as_dict())
		prospect.contact_email = None  # prevent Contact auto-binding an existing login
		customer = _insert_identity_customer(
			prospect, frappe.get_doc("Company", app.company), group, "SPORTS-CUST-REG-" + app.name
		)
		invoice = frappe.get_doc(
			dict(
				doctype="Sales Invoice",
				company=app.company,
				customer=customer.name,
				posting_date=today(),
				due_date=today(),
				currency=config["currency"],
				conversion_rate=1,
				debit_to=config["paid_from"],
				cost_center=config["cost_center"],
				update_stock=0,
				is_pos=0,
				taxes=[],
				taxes_and_charges=None,
				workflow_state="Draft",
				sports_registration=app.name,
				remarks="Enrollment fees for registration " + app.name,
				items=config["items"],
			)
		)
		invoice.flags.sports_invoice_service = INVOICE_CAPABILITY
		invoice.flags.ignore_boost_access_control = True
		invoice.insert(ignore_permissions=True)
		if _money(invoice.grand_total) != _money(config["total"]) or invoice.taxes:
			frappe.throw(
				_("Enrollment invoice totals must match the configured fees without extra taxes or charges.")
			)
		app.db_set(
			dict(
				sales_invoice=invoice.name,
				payment_customer=customer.name,
				payment_snapshot=json.dumps(config),
			),
			update_modified=False,
		)
		return _response(app, invoice)


def validate_enrollment_invoice(doc, method=None):
	previous = doc.get_doc_before_save() if callable(getattr(doc, "get_doc_before_save", None)) else None
	if (
		previous
		and previous.get("sports_registration")
		and previous.get("sports_registration") != doc.get("sports_registration")
	):
		frappe.throw(_("Enrollment invoice provenance cannot be removed or reassigned."))
	if not doc.get("sports_registration") or doc.flags.sports_invoice_service is INVOICE_CAPABILITY:
		return
	app = frappe.get_doc("Sports Registration", doc.sports_registration)
	config = json.loads(app.payment_snapshot or "{}")
	if (
		app.get("sales_invoice") != doc.name
		or app.payment_customer != doc.customer
		or app.company != doc.company
	):
		frappe.throw(_("Enrollment invoice provenance cannot be reassigned."))
	if (
		doc.currency != config.get("currency")
		or doc.debit_to != config.get("paid_from")
		or _money(doc.grand_total) != _money(config.get("total"))
		or _money(doc.conversion_rate) != 1
	):
		frappe.throw(_("Enrollment invoice currency, receivable and total must match the registration."))
	if (
		doc.is_return
		or doc.is_pos
		or doc.update_stock
		or doc.taxes
		or doc.discount_amount
		or doc.additional_discount_percentage
		or doc.write_off_amount
		or doc.get("advances")
	):
		frappe.throw(_("Enrollment invoice charges cannot be changed or offset outside Finance correction."))
	expected = config.get("items", [])
	if len(doc.items) != len(expected):
		frappe.throw(_("Enrollment invoice fee lines cannot change."))
	for row, saved in zip(doc.items, expected, strict=False):
		if (
			any(row.get(k) != saved.get(k) for k in ("item_code", "income_account", "cost_center", "uom"))
			or _money(row.qty) != 1
			or _money(row.rate) != _money(saved["rate"])
			or _money(row.amount) != _money(saved["rate"])
		):
			frappe.throw(_("Enrollment invoice fee lines cannot change."))


def claim_invoice(reference, request_key):
	key = request_uuid(request_key)
	settings = intake_settings()
	name = frappe.db.get_value(
		"Sports Registration", {"sales_invoice": str(reference)}, "name", for_update=True
	)
	if not name:
		frappe.throw(_("Invalid payment reference or registration token."), frappe.PermissionError)
	app = frappe.get_doc("Sports Registration", name, for_update=True)
	if not hmac.compare_digest(str(app.request_key), key):
		frappe.throw(_("Invalid payment reference or registration token."), frappe.PermissionError)
	invoice = frappe.get_doc("Sales Invoice", app.sales_invoice, for_update=True)
	validate_enrollment_invoice(invoice)
	if invoice.docstatus == 2:
		frappe.throw(_("This invoice was cancelled. Contact the academy."))
	if invoice.docstatus == 1 or invoice.workflow_state == "Pending Review":
		return _response(app, invoice)
	if app.status not in ("Pending", "Accepted") or invoice.workflow_state != "Draft":
		frappe.throw(_("This invoice cannot be moved to review."))
	invoice_workflow()
	# Applicant claims are not approvals and grant no Guest invoice permissions.
	invoice.db_set(dict(workflow_state="Pending Review", sports_claimed_on=now_datetime()))
	invoice.add_comment(
		"Comment",
		"Applicant reported a bank transfer. Awaiting Finance verification; invoice and payment remain unposted.",
	)
	from sports_app.payment_notifications import notify_payment_review

	notify_payment_review(app, invoice, settings)
	return _response(app, invoice)


def can_complete_payment(user=None):
	user = user or frappe.session.user
	if not user or user == "Guest":
		return False
	roles = set(frappe.get_roles(user))
	if user != "Administrator" and not roles.intersection(
		{"Accounts Manager", "System Manager", "Boost Finance Manager", "Boost Invoice Approver"}
	):
		return False
	if not all(
		frappe.has_permission(dt, p, user=user)
		for dt, p in (
			("Sales Invoice", "read"),
			("Sales Invoice", "write"),
			("Sales Invoice", "submit"),
			("Payment Entry", "read"),
			("Payment Entry", "create"),
			("Payment Entry", "submit"),
		)
	):
		return False
	if "erp_boost" in frappe.get_installed_apps():
		from erp_boost.api import is_valid_invoice_approver, is_valid_payment_entry_approver

		return bool(
			is_valid_invoice_approver(user, "Sales Invoice") and is_valid_payment_entry_approver(user)
		)
	return True


def require_finance_access(company=None):
	if not can_complete_payment():
		frappe.throw(
			_("Invoice and payment approval permissions are required to complete enrollment payments."),
			frappe.PermissionError,
		)
	if company:
		validate_company(company)


@frappe.whitelist()
def completion_access(name):
	doc = frappe.get_doc("Sales Invoice", name)
	doc.check_permission("read")
	validate_company(doc.company)
	if not (
		doc.get("sports_registration")
		and doc.docstatus == 0
		and doc.get("workflow_state") == "Pending Review"
		and can_complete_payment()
	):
		return False
	if frappe.db.get_value("Sports Registration", doc.sports_registration, "status") == "Rejected":
		return False
	from frappe.model.workflow import get_transitions

	return any(t.action == "Complete Payment" for t in get_transitions(doc))


@frappe.whitelist(methods=["POST"])
def complete_payment(name):
	require_finance_access()
	# Same settings → application → invoice lock order as public preparation/claim.
	intake_settings()
	app_name = frappe.db.get_value(
		"Sports Registration", {"sales_invoice": str(name)}, "name", for_update=True
	)
	if not app_name:
		frappe.throw(_("Select an enrollment invoice."))
	app = frappe.get_doc("Sports Registration", app_name, for_update=True)
	invoice = frappe.get_doc("Sales Invoice", app.sales_invoice, for_update=True)
	require_finance_access(invoice.company)
	invoice.check_permission("read")
	invoice.check_permission("submit")
	validate_enrollment_invoice(invoice)
	if invoice.docstatus == 1 and app.payment_entry:
		payment = frappe.get_doc("Payment Entry", app.payment_entry)
		if payment.docstatus == 1 and _money(invoice.outstanding_amount) == 0:
			from sports_app.enrollment_payments import validate_sports_payment

			validate_sports_payment(payment)
			return dict(invoice=invoice.name, payment_entry=payment.name, state="Paid")
	if invoice.docstatus != 0 or invoice.workflow_state != "Pending Review" or app.status == "Rejected":
		frappe.throw(_("Only an unposted enrollment invoice awaiting review can be completed."))
	from frappe.model.workflow import apply_workflow, get_transitions

	actions = [t.action for t in get_transitions(invoice) if t.action == "Complete Payment"]
	if not actions:
		frappe.throw(
			_("The invoice workflow does not allow you to complete this payment."), frappe.PermissionError
		)
	with acceptance_transaction():
		apply_workflow(invoice.as_dict(), "Complete Payment")
		app.reload()
		if not app.payment_entry:
			frappe.throw(_("The invoice payment was not completed."))
		return dict(invoice=invoice.name, payment_entry=app.payment_entry, state="Paid")


def validate_finance_submission(doc, method=None):
	if not doc.get("sports_registration"):
		return
	require_finance_access(doc.company)
	validate_enrollment_invoice(doc)
	previous = doc.get_doc_before_save()
	if not previous or previous.workflow_state != "Pending Review":
		frappe.throw(_("Send the enrollment invoice to review before completing payment."))
	app = frappe.get_doc("Sports Registration", doc.sports_registration)
	if app.status == "Rejected":
		frappe.throw(_("Rejected registrations require Finance correction before payment completion."))


def record_invoice_payment(doc, method=None):
	"""Runs in the invoice submission transaction, including native workflow UI."""
	if not doc.get("sports_registration"):
		return
	require_finance_access(doc.company)
	from frappe.model.workflow import apply_workflow

	from sports_app.enrollment_payments import PAYMENT_CAPABILITY, EnrollmentDraftPayment

	app = frappe.get_doc("Sports Registration", doc.sports_registration, for_update=True)
	if app.payment_entry:
		frappe.throw(_("This enrollment already has a payment. Review it with Finance."))
	config = json.loads(app.payment_snapshot)
	payment = EnrollmentDraftPayment(
		dict(
			doctype="Payment Entry",
			payment_type="Receive",
			company=doc.company,
			posting_date=doc.posting_date,
			party_type="Customer",
			party=doc.customer,
			paid_from=config["paid_from"],
			paid_to=config["paid_to"],
			paid_from_account_currency=config["currency"],
			paid_to_account_currency=config["currency"],
			paid_amount=config["total"],
			received_amount=config["total"],
			source_exchange_rate=1,
			target_exchange_rate=1,
			bank_account=config["bank_account"],
			reference_no=doc.name,
			reference_date=today(),
			workflow_state="Draft",
			sports_registration=app.name,
			custom_selected_approver=frappe.session.user,
			references=[
				dict(
					reference_doctype="Sales Invoice",
					reference_name=doc.name,
					total_amount=doc.grand_total,
					outstanding_amount=doc.grand_total,
					allocated_amount=config["total"],
				)
			],
		)
	)
	payment.flags.sports_payment_service = PAYMENT_CAPABILITY
	payment.insert()  # current Finance user must have normal create permission
	app.db_set("payment_entry", payment.name, update_modified=False)
	payment.db_set("workflow_state", "Pending Review", update_modified=False)
	apply_workflow(payment.as_dict(), "Approve")
	doc.reload()
	if _money(doc.outstanding_amount) != 0:
		frappe.throw(_("Payment did not settle the enrollment invoice; nothing has been completed."))
	doc.add_comment("Comment", "Finance verified the bank transfer and completed payment: " + payment.name)
