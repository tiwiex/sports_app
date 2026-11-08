"""Permission-scoped subscription overview, month grid and native receipt actions."""

import frappe
from frappe import _
from frappe.utils import getdate

from sports_app.billing_access import CAPABILITY, OBLIGATION, enrollment_record, require_billing
from sports_app.billing_policy import digest, money, period
from sports_app.monthly_billing import build, existing, generate_rows
from sports_app.player_numbering import academy_date
from sports_app.registrations import acceptance_transaction, request_uuid


def require_finance(*permissions):
	settings = require_billing()
	for doctype, action in permissions:
		if not frappe.has_permission(doctype, action):
			frappe.throw(_("Native accounting permissions are required."), frappe.PermissionError)
	return settings


def selected_year(value):
	if not str(value).isdigit() or not 2000 <= int(value) <= 2099:
		frappe.throw(_("Choose a year between 2000 and 2099."))
	return int(value)


def invoices_for(settings, enrollments, year):
	obligations = frappe.get_list(
		OBLIGATION,
		filters={
			"company": settings.company,
			"enrollment": ["in", enrollments or [""]],
			"billing_month": ["in", [f"{year}-{m:02d}" for m in range(1, 13)]],
		},
		fields=["name", "enrollment", "billing_month", "amount", "currency", "sales_invoice", "source_hash"],
		page_length=0,
	)
	invoices = frappe.get_list(
		"Sales Invoice",
		filters={
			"company": settings.company,
			"sports_billing_obligation": ["in", [o.name for o in obligations] or [""]],
		},
		fields=[
			"name",
			"docstatus",
			"currency",
			"grand_total",
			"outstanding_amount",
			"due_date",
			"sports_billing_obligation",
		],
		page_length=0,
	)
	return obligations, {r.name: r for r in invoices}


@frappe.whitelist()
def overview(year: str | int):
	settings = require_finance(("Sales Invoice", "read"))
	year = selected_year(year)
	enrollments = frappe.get_list(
		"Sports Enrollment",
		filters={"company": settings.company},
		fields=["name", "player", "status"],
		page_length=0,
	)
	# Player permissions must constrain aggregate counts as well as grid rows.
	visible = set(
		frappe.get_list("Sports Player", filters={"company": settings.company}, pluck="name", page_length=0)
	)
	enrollments = [r for r in enrollments if r.player in visible]
	obligations, invoices = invoices_for(settings, [r.name for r in enrollments], year)
	months = []
	for month in range(1, 13):
		key = f"{year}-{month:02d}"
		rows = [
			invoices[o.sales_invoice]
			for o in obligations
			if o.billing_month == key
			and o.sales_invoice in invoices
			and invoices[o.sales_invoice].docstatus == 1
		]
		billed = sum((money(r.grand_total) for r in rows), money(0))
		outstanding = sum((money(r.outstanding_amount) for r in rows), money(0))
		months.append(
			dict(
				month=key,
				invoices=len(rows),
				billed=str(billed),
				settled=str(billed - outstanding),
				outstanding=str(outstanding),
			)
		)
	return dict(
		year=year,
		currency=settings.currency,
		enrollments=len(enrollments),
		active=sum(r.status == "Active" for r in enrollments),
		months=months,
		billed=str(sum((money(r["billed"]) for r in months), money(0))),
		outstanding=str(sum((money(r["outstanding"]) for r in months), money(0))),
	)


def preview_charge(enrollment, month):
	# Expected missing-plan exceptions are cell states, not a stack of alert dialogs.
	muted = frappe.flags.mute_messages
	try:
		frappe.flags.mute_messages = True
		return build(enrollment, month)
	finally:
		frappe.flags.mute_messages = muted


@frappe.whitelist()
def grid(year: str | int, start: str | int = 0, search: str = ""):
	settings = require_finance(("Sales Invoice", "read"))
	year = selected_year(year)
	if not str(start).isdigit() or len(str(start)) > 6 or len(search) > 100:
		frappe.throw(_("Invalid subscription grid filter."))
	filters = {"company": settings.company}
	if search:
		filters["full_name"] = ["like", "%" + search + "%"]
	players = frappe.get_list("Sports Player", filters=filters, fields=["name", "full_name"], page_length=0)
	players = {p.name: p.full_name for p in players}
	rows = frappe.get_list(
		"Sports Enrollment",
		filters={"company": settings.company, "player": ["in", list(players) or [""]]},
		fields=["name", "player", "program", "status"],
		order_by="name asc",
		start=int(start),
		page_length=21,
	)
	obligations, invoices = invoices_for(settings, [r.name for r in rows[:20]], year)
	lookup = {(o.enrollment, o.billing_month): o for o in obligations}
	payments = (
		frappe.get_list(
			"Payment Entry",
			filters={
				"company": settings.company,
				"sports_billing_obligation": ["in", [o.name for o in obligations] or [""]],
				"docstatus": 1,
			},
			fields=["name", "sports_billing_obligation"],
			page_length=0,
		)
		if frappe.has_permission("Payment Entry", "read")
		else []
	)
	current = str(academy_date(settings))[:7]
	result = []
	for row in rows[:20]:
		cells = []
		for number in range(1, 13):
			month = f"{year}-{number:02d}"
			cell = dict(
				month=month,
				state="Future" if month > current else "Not due" if month == current else "Not billed",
			)
			old = lookup.get((row.name, month))
			if old:
				cell.update(source_hash=old.source_hash, outstanding="0.00", amount=str(money(old.amount)))
				invoice = invoices.get(old.sales_invoice)
				if not old.sales_invoice:
					cell["state"] = "No charge"
				elif not invoice:
					cell["state"] = "Restricted invoice"
				else:
					cell.update(
						invoice=invoice.name,
						outstanding=str(money(invoice.outstanding_amount)),
						overdue=bool(
							invoice.docstatus == 1
							and money(invoice.outstanding_amount)
							and getdate(invoice.due_date) < academy_date(settings)
						),
					)
					cell["state"] = (
						"Cancelled"
						if invoice.docstatus == 2
						else "Draft"
						if invoice.docstatus == 0
						else "Paid"
						if money(invoice.outstanding_amount) == 0
						else "Partial"
						if money(invoice.outstanding_amount) < money(invoice.grand_total)
						else "Unpaid"
					)
				cell["receipts"] = [p.name for p in payments if p.sports_billing_obligation == old.name]
			elif month < current:
				try:
					built = preview_charge(row.name, month)
					if built:
						values, _invoice = built
						cell.update(
							state="Not billed" if money(values["amount"]) else "No charge",
							source_hash=values["source_hash"],
							amount=values["amount"],
							outstanding=values["amount"],
						)
					else:
						cell["state"] = "Not eligible"
				except (frappe.ValidationError, frappe.PermissionError) as error:
					cell["state"] = "Review billing"
					cell["issue"] = frappe.utils.strip_html(str(error))
			cells.append(cell)
		program = frappe.get_doc("Sports Program", row.program)
		program.check_permission("read")
		result.append(
			dict(
				enrollment=row.name,
				player=row.player,
				player_name=players[row.player],
				program=program.program_name,
				cells=cells,
			)
		)
	accounts = frappe.get_list(
		"Account",
		filters={
			"company": settings.company,
			"disabled": 0,
			"is_group": 0,
			"account_type": ["in", ["Bank", "Cash"]],
			"account_currency": settings.currency,
		},
		fields=["name"],
		page_length=0,
	)
	return dict(
		year=year,
		rows=result,
		has_more=len(rows) > 20,
		currency=settings.currency,
		today=str(academy_date(settings)),
		payment_accounts=[r.name for r in accounts],
		default_payment_account=settings.get("enrollment_bank_account")
		if settings.get("enrollment_bank_account") in {r.name for r in accounts}
		else None,
		can_generate=all(frappe.has_permission("Sales Invoice", p) for p in ("read", "create", "submit")),
		can_pay=all(frappe.has_permission("Payment Entry", p) for p in ("read", "create", "submit"))
		and all(frappe.has_permission("Sales Invoice", p) for p in ("read", "create", "submit")),
		can_reverse=all(frappe.has_permission("Payment Entry", p) for p in ("read", "cancel")),
	)


def parse_rows(rows):
	rows = frappe.parse_json(rows)
	if (
		not isinstance(rows, list)
		or not 1 <= len(rows) <= 20
		or any(
			not isinstance(r, dict)
			or set(r) != {"enrollment", "month", "source_hash", "outstanding"}
			or not isinstance(r.get("enrollment"), str)
			or not 1 <= len(r["enrollment"]) <= 140
			or not isinstance(r.get("month"), str)
			or not isinstance(r.get("source_hash"), str)
			for r in rows
		)
	):
		frappe.throw(_("Select between 1 and 20 subscription cells."))
	if len({(r["enrollment"], r["month"]) for r in rows}) != len(rows):
		frappe.throw(_("Select each subscription month once."))
	for row in rows:
		period(row["month"])
		money(row["outstanding"])
	return rows


@frappe.whitelist(methods=["POST"])
def generate_invoices(rows: str | list):
	"""The same selected cells may create receivables without claiming funds received."""
	settings = require_finance(*[("Sales Invoice", p) for p in ("read", "create", "submit")])
	rows = parse_rows(rows)
	if any(row["month"] >= str(academy_date(settings))[:7] for row in rows):
		frappe.throw(_("Select current or historical subscription months."))
	result = []
	for row in rows:
		generated = generate_rows(
			row["month"], [{"enrollment": row["enrollment"], "source_hash": row["source_hash"]}]
		)[0]
		result.append(dict(**generated, month=row["month"]))
	return result


def bank_account(name, settings, allow_disabled=False):
	doc = frappe.get_doc("Account", name)
	doc.check_permission("read")
	if (
		doc.company != settings.company
		or (doc.disabled and not allow_disabled)
		or doc.is_group
		or doc.account_type not in ("Bank", "Cash")
		or doc.account_currency != settings.currency
	):
		frappe.throw(_("Select an enabled Bank/Cash account in the academy company currency."))
	return doc


def transition(payment, target):
	from frappe.model.workflow import apply_workflow, get_transitions, get_workflow_name

	payment.check_permission("submit" if target == 1 else "cancel")
	name = get_workflow_name("Payment Entry")
	if not name:
		payment.submit() if target == 1 else payment.cancel()
		return payment
	workflow = frappe.get_doc("Workflow", name)
	if payment.meta.queue_in_background:
		frappe.throw(_("Subscription payments require synchronous workflow processing."))
	states = {r.state: int(r.doc_status) for r in workflow.states}
	action = next(
		(t.action for t in get_transitions(payment, workflow) if states.get(t.next_state) == target), None
	)
	if not action:
		frappe.throw(
			_("The payment workflow does not permit this action for your account."), frappe.PermissionError
		)
	payment = apply_workflow(payment.as_dict(), action)
	if not payment or payment.docstatus != target:
		frappe.throw(_("Payment did not reach the required accounting state."))
	return payment


@frappe.whitelist(methods=["POST"])
def pay(rows: str | list, paid_to: str, posting_date: str, reference_no: str, request_key: str):
	settings = require_finance(*[("Payment Entry", p) for p in ("read", "create", "submit")])
	rows = parse_rows(rows)
	request_key = request_uuid(request_key)
	posting = getdate(posting_date)
	if not posting_date or posting > academy_date(settings) or len(reference_no) > 140:
		frappe.throw(
			_("Enter a valid payment date (not in the future) and a reference up to 140 characters.")
		)
	bank = bank_account(paid_to, settings)
	result = []
	for row in rows:
		try:
			with acceptance_transaction():
				enrollment, player = enrollment_record(row["enrollment"])
				if row["month"] > str(academy_date(settings))[:7]:
					frappe.throw(_("Future subscription months cannot be paid from this grid."))
				key = digest([frappe.session.user, request_key, row["enrollment"], row["month"]])
				payload = digest([row, bank.name, str(posting), reference_no.strip()])
				previous = frappe.db.get_value("Payment Entry", {"sports_subscription_request": key}, "name")
				if previous:
					payment = frappe.get_doc("Payment Entry", previous, for_update=True)
					payment.check_permission("read")
					if (
						payment.sports_subscription_payload != payload
						or payment.company != settings.company
						or payment.party != player.customer
					):
						frappe.throw(_("Payment retry changed. Refresh and use a new confirmed selection."))
					result.append(
						dict(
							enrollment=enrollment.name,
							month=row["month"],
							receipt=payment.name,
							state="Cancelled" if payment.docstatus == 2 else "Paid",
						)
					)
					continue
				old = existing(enrollment.name, row["month"])
				if not old or not old.sales_invoice:
					frappe.throw(
						_("The monthly invoice is awaiting automatic billing. No payment was posted.")
					)
				invoice = frappe.get_doc("Sales Invoice", old.sales_invoice, for_update=True)
				invoice.check_permission("read")
				if (
					invoice.docstatus != 1
					or invoice.customer != player.customer
					or invoice.company != settings.company
					or invoice.currency != settings.currency
					or invoice.sports_billing_obligation != old.name
				):
					frappe.throw(_("Subscription invoice is not a submitted charge for this player."))
				amount = money(invoice.outstanding_amount)
				if not amount or amount != money(row["outstanding"]):
					frappe.throw(_("Outstanding amount changed. Refresh before confirming payment."))
				payment = make_payment(
					invoice,
					old,
					bank,
					posting,
					reference_no.strip() or f"SUB-{row['month']}-{key[:12]}",
					key,
					payload,
					amount,
				)
				result.append(
					dict(enrollment=enrollment.name, month=row["month"], receipt=payment.name, state="Paid")
				)
		except (frappe.ValidationError, frappe.PermissionError) as error:
			result.append(
				dict(enrollment=row["enrollment"], month=row["month"], state="Exception", error=str(error))
			)
	return result


def make_payment(invoice, obligation, bank, posting, reference, key, payload, amount):
	payment = frappe.get_doc(
		doctype="Payment Entry",
		payment_type="Receive",
		company=invoice.company,
		posting_date=str(posting),
		party_type="Customer",
		party=invoice.customer,
		paid_from=invoice.debit_to,
		paid_to=bank.name,
		paid_from_account_currency=invoice.currency,
		paid_to_account_currency=bank.account_currency,
		paid_amount=amount,
		received_amount=amount,
		source_exchange_rate=1,
		target_exchange_rate=1,
		reference_no=reference,
		reference_date=str(posting),
		cost_center=invoice.cost_center,
		sports_billing_obligation=obligation.name,
		sports_subscription_request=key,
		sports_subscription_payload=payload,
		remarks="Subscription payment / " + obligation.billing_month,
		references=[
			dict(
				reference_doctype="Sales Invoice",
				reference_name=invoice.name,
				allocated_amount=amount,
				total_amount=invoice.grand_total,
				outstanding_amount=amount,
				due_date=invoice.due_date,
			)
		],
	)
	if payment.meta.has_field("custom_selected_approver"):
		payment.custom_selected_approver = frappe.session.user
	payment.flags.sports_subscription_service = CAPABILITY
	payment.insert()
	return transition(payment, 1)


@frappe.whitelist(methods=["POST"])
def reverse(payment_entries: str | list, reason: str):
	settings = require_finance(("Payment Entry", "read"), ("Payment Entry", "cancel"))
	names = frappe.parse_json(payment_entries)
	if (
		not isinstance(names, list)
		or not 1 <= len(names) <= 20
		or any(not isinstance(n, str) for n in names)
		or not reason.strip()
		or len(reason) > 500
	):
		frappe.throw(
			_("Select 1-20 subscription receipts and enter a reversal reason (up to 500 characters).")
		)
	result = []
	with acceptance_transaction():
		for name in sorted(set(names)):
			payment = frappe.get_doc("Payment Entry", name, for_update=True)
			payment.check_permission("read")
			payment.check_permission("cancel")
			if not payment.get("sports_subscription_request") or not payment.get("sports_billing_obligation"):
				frappe.throw(_("Only receipts created by this subscription grid can be reversed here."))
			obligation = frappe.get_doc(OBLIGATION, payment.sports_billing_obligation)
			enrollment_record(obligation.enrollment)
			if payment.company != settings.company or obligation.company != settings.company:
				frappe.throw(_("Receipt belongs to another company."), frappe.PermissionError)
			validate_payment(payment)
			if payment.docstatus == 1:
				payment.add_comment("Comment", "Subscription payment reversal: " + reason.strip())
				transition(payment, 2)
			elif payment.docstatus != 2:
				frappe.throw(_("Only submitted subscription receipts can be reversed."))
			result.append(dict(receipt=name, state="Cancelled"))
	return result


def validate_payment(doc, method=None):
	previous = doc.get_doc_before_save()
	fields = ("sports_billing_obligation", "sports_subscription_request", "sports_subscription_payload")
	if previous and any(previous.get(f) != doc.get(f) for f in fields):
		frappe.throw(_("Subscription receipt provenance cannot be changed."))
	if not any(doc.get(f) for f in fields):
		return
	if doc.is_new() and doc.flags.sports_subscription_service is not CAPABILITY:
		frappe.throw(_("Create subscription receipts through the payment grid."), frappe.PermissionError)
	settings = require_billing()
	obligation = frappe.get_doc(OBLIGATION, doc.sports_billing_obligation)
	obligation.check_permission("read")
	_enrollment, player = enrollment_record(obligation.enrollment)
	if (
		doc.company != settings.company
		or obligation.company != settings.company
		or doc.party != player.customer
		or doc.payment_type != "Receive"
		or doc.party_type != "Customer"
		or doc.get("sports_registration")
		or len(doc.references) != 1
		or doc.references[0].reference_doctype != "Sales Invoice"
		or doc.references[0].reference_name != obligation.sales_invoice
		or money(doc.references[0].allocated_amount) != money(doc.paid_amount)
		or money(doc.paid_amount) != money(doc.received_amount)
		or not money(doc.paid_amount)
		or doc.paid_from_account_currency != settings.currency
		or doc.paid_to_account_currency != settings.currency
		or doc.deductions
		or money(doc.unallocated_amount or 0)
	):
		frappe.throw(_("Subscription receipt must retain its player invoice and full allocation."))
	bank_account(doc.paid_to, settings, allow_disabled=not doc.is_new())
	if previous and any(
		str(previous.get(f)) != str(doc.get(f))
		for f in (
			"party",
			"company",
			"paid_from",
			"paid_to",
			"paid_amount",
			"received_amount",
			"posting_date",
			"reference_no",
		)
	):
		frappe.throw(_("Submitted subscription payment details are immutable; reverse with a reason."))
