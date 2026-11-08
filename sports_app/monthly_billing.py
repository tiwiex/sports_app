"""Preview and idempotent monthly invoice generation with native submission."""

import json

import frappe
from frappe import _
from frappe.utils import cint, getdate

from sports_app.billing_access import (
	CAPABILITY,
	OBLIGATION,
	PLAN,
	SCHOLARSHIP,
	enrollment_record,
	require_billing,
)
from sports_app.billing_policy import charge, digest, money, period
from sports_app.fee_plans import mapping
from sports_app.registrations import acceptance_transaction


def key_for(company, enrollment, month):
	return (
		"SPORTS-BILL-"
		+ month.replace("-", "")
		+ "-"
		+ digest([company, enrollment, month, "Monthly subscription"])[:24]
	)


def build(name, month):
	start, end = period(month)
	enrollment, player = enrollment_record(name)
	plans = frappe.get_list(
		PLAN,
		filters={
			"company": enrollment.company,
			"program": enrollment.program,
			"enabled": 1,
			"effective_from": ["<=", start],
		},
		fields=["name"],
		page_length=0,
	)
	plans = [frappe.get_doc(PLAN, r.name) for r in plans]
	plans = [p for p in plans if not p.effective_to or getdate(p.effective_to) >= start]
	if len(plans) != 1:
		frappe.throw(_("Configure exactly one enabled fee plan for this program and month."))
	plan = plans[0]
	plan.check_permission("read")
	pricing_revision = None
	if plan.get("subscription_plan"):
		from sports_app.subscription_pricing import resolve

		pricing = resolve(plan.subscription_plan, plan.currency)
		plan.item = pricing["item"]
		plan.monthly_amount = pricing["monthly_amount"]
		pricing_revision = pricing["subscription_revision"]
	item = mapping(plan)
	# Restricted decisions are read only inside an already-authorized billing service.
	# Their reasons, status, benefit flags and identities never enter the preview.
	decisions = frappe.get_all(
		SCHOLARSHIP,
		filters={"company": enrollment.company, "enrollment": name, "docstatus": 1},
		fields=["name", "modified", "effective_from", "effective_to", "coverage_type", "coverage_value"],
	)
	calculated = charge(enrollment, plan, decisions, month)
	if calculated is None:
		return None
	customer = frappe.get_doc("Customer", player.customer)
	customer.check_permission("read")
	if customer.disabled:
		frappe.throw(_("The player's Customer is disabled."))
	company = frappe.get_doc("Company", enrollment.company)
	receivable = (
		frappe.get_doc("Account", company.default_receivable_account)
		if company.default_receivable_account
		else None
	)
	if (
		not receivable
		or receivable.company != company.name
		or receivable.disabled
		or receivable.is_group
		or receivable.account_type != "Receivable"
		or receivable.account_currency != plan.currency
	):
		frappe.throw(_("Configure a valid company receivable account in the billing currency."))
	receivable.check_permission("read")
	values = dict(
		**calculated,
		player=player.name,
		player_name=player.full_name,
		enrollment=name,
		company=enrollment.company,
		plan=plan.name,
		currency=plan.currency,
	)
	invoice = dict(
		company=enrollment.company,
		customer=customer.name,
		remarks="Monthly academy subscription " + month + " / " + enrollment.name,
		posting_date=str(start),
		set_posting_time=1,
		due_date=calculated["due_date"],
		currency=plan.currency,
		conversion_rate=1,
		debit_to=receivable.name,
		cost_center=plan.cost_center,
		update_stock=0,
		is_pos=0,
		taxes=[],
		taxes_and_charges=None,
		items=[
			dict(
				item_code=item.name,
				item_name=item.item_name,
				description="Monthly academy subscription — " + month,
				qty=1,
				rate=calculated["amount"],
				uom=item.stock_uom,
				stock_uom=item.stock_uom,
				conversion_factor=1,
				income_account=plan.income_account,
				cost_center=plan.cost_center,
			)
		],
	)
	values["source_hash"] = digest(
		[
			values,
			str(plan.modified),
			pricing_revision,
			str(enrollment.modified),
			[(d.name, str(d.modified)) for d in decisions],
			invoice,
		]
	)
	return values, invoice


def existing(name, month):
	settings = require_billing()
	key = key_for(settings.company, name, month)
	if frappe.db.exists(OBLIGATION, key):
		doc = frappe.get_doc(OBLIGATION, key, for_update=True)
		doc.check_permission("read")
		if doc.company != settings.company or doc.enrollment != name:
			frappe.throw(_("Billing identity mismatch."))
		return doc


def validate_obligation(doc):
	require_billing()
	if doc.flags.sports_billing_service is not CAPABILITY or not doc.is_new():
		frappe.throw(
			_("Billing obligations are immutable and can only be generated from a preview."),
			frappe.PermissionError,
		)
	period(doc.billing_month)
	if doc.name != key_for(doc.company, doc.enrollment, doc.billing_month):
		frappe.throw(_("Invalid billing obligation identity."))


def public_obligation(doc):
	invoice_state = "No invoice required"
	if doc.sales_invoice:
		invoice = frappe.get_doc("Sales Invoice", doc.sales_invoice)
		invoice.check_permission("read")
		invoice_state = (
			"Cancelled — reviewed correction required"
			if invoice.docstatus == 2
			else ("Draft" if invoice.docstatus == 0 else invoice.status)
		)
	return dict(
		enrollment=doc.enrollment,
		player=doc.player,
		amount=str(money(doc.amount)),
		currency=doc.currency,
		due_date=str(doc.due_date),
		obligation=doc.name,
		sales_invoice=doc.sales_invoice,
		state=invoice_state,
		source_hash=doc.source_hash,
	)


@frappe.whitelist()
def preview(month: str, program: str | None = None, start: str | int = 0):
	settings = require_billing()
	first, last = period(month)
	if not str(start).isdigit() or len(str(start)) > 6:
		frappe.throw(_("Invalid preview page."))
	filters = {"company": settings.company, "start_date": ["<=", last]}
	if program:
		filters["program"] = program
	rows = frappe.get_list(
		"Sports Enrollment",
		filters=filters,
		fields=["name", "player", "start_date", "end_date", "status"],
		order_by="name asc",
		start=int(start),
		page_length=21,
	)
	result = []
	for row in rows[:20]:
		if row.end_date and getdate(row.end_date) < first:
			continue
		try:
			old = existing(row.name, month)
			if old:
				result.append(public_obligation(old))
				continue
			calculation = build(row.name, month)
			if calculation is None:
				result.append(
					dict(enrollment=row.name, player=row.player, state="Not eligible at month start")
				)
				continue
			values, _invoice = calculation
			result.append(dict(**values, state="Ready to generate"))
		except (frappe.ValidationError, frappe.PermissionError) as error:
			result.append(dict(enrollment=row.name, player=row.player, state="Exception", error=str(error)))
	return dict(
		rows=result,
		has_more=len(rows) > 20,
		can_generate=bool(
			cint(settings.monthly_fees_enabled)
			and frappe.has_permission("Sales Invoice", "create")
			and frappe.has_permission("Sales Invoice", "read")
			and frappe.has_permission("Sales Invoice", "submit")
		),
	)


@frappe.whitelist(methods=["POST"])
def generate(month: str, rows: str | list):
	return generate_rows(month, rows)


def generate_rows(month, rows):
	settings = require_billing()
	if not cint(settings.monthly_fees_enabled):
		frappe.throw(_("Monthly fees are disabled in Academy Settings."))
	period(month)
	if not all(frappe.has_permission("Sales Invoice", p) for p in ("create", "read", "submit")):
		frappe.throw(
			_("Native Sales Invoice read/create/submit permissions are required."), frappe.PermissionError
		)
	rows = frappe.parse_json(rows)
	if (
		not isinstance(rows, list)
		or not 1 <= len(rows) <= 20
		or any(not isinstance(r, dict) or set(r) != {"enrollment", "source_hash"} for r in rows)
	):
		frappe.throw(_("Choose between 1 and 20 preview rows."))
	result = []
	for row in rows:
		try:
			with acceptance_transaction():
				enrollment_record(row["enrollment"])
				old = existing(row["enrollment"], month)
				if old:
					submit_obligation(old)
					result.append(public_obligation(old))
					continue
				built = build(row["enrollment"], month)
				if not built or built[0]["source_hash"] != row["source_hash"]:
					frappe.throw(_("Billing source changed. Preview again before generating."))
				values, invoice_values = built
				key = key_for(values["company"], values["enrollment"], month)
				doc = frappe.get_doc(
					doctype=OBLIGATION,
					name=key,
					**{k: v for k, v in values.items() if k != "player_name"},
					invoice_snapshot=json.dumps(invoice_values),
				)
				doc.flags.sports_billing_service = CAPABILITY
				doc.insert()
				if money(values["amount"]):
					invoice = frappe.get_doc(
						doctype="Sales Invoice", sports_billing_obligation=doc.name, **invoice_values
					)
					invoice.flags.sports_billing_service = CAPABILITY
					invoice.insert()
					doc.db_set("sales_invoice", invoice.name, update_modified=False)
					submit_invoice(invoice)
				result.append(public_obligation(doc))
		except (frappe.ValidationError, frappe.PermissionError) as error:
			result.append(dict(enrollment=row["enrollment"], state="Exception", error=str(error)))
	return result


def validate_invoice(doc, method=None):
	old = doc.get_doc_before_save()
	previous = old.get("sports_billing_obligation") if old else None
	link = doc.get("sports_billing_obligation")
	if not link and not previous:
		return
	require_billing()
	if previous and link != previous:
		frappe.throw(_("Monthly billing provenance cannot be changed."))
	obligation = frappe.get_doc(OBLIGATION, link)
	obligation.check_permission("read")
	if obligation.sales_invoice and obligation.sales_invoice != doc.name:
		frappe.throw(_("This monthly obligation already has an invoice."))
	if not obligation.sales_invoice and obligation.flags.sports_billing_service is not CAPABILITY:
		# During initial insertion the persisted obligation has no invoice link yet;
		# only the generation service supplies this in-process capability.
		if doc.flags.sports_billing_service is not CAPABILITY:
			frappe.throw(
				_("Generate monthly invoices from a current billing preview."), frappe.PermissionError
			)
	snapshot = json.loads(obligation.invoice_snapshot)
	for field in ("company", "customer", "currency", "posting_date", "due_date", "debit_to", "cost_center"):
		if str(doc.get(field) or "") != str(snapshot[field] or ""):
			frappe.throw(_("Monthly invoice must retain its approved billing snapshot."))
	if (
		doc.get("sports_registration")
		or doc.is_pos
		or doc.is_return
		or doc.update_stock
		or doc.taxes
		or doc.discount_amount
		or doc.additional_discount_percentage
		or len(doc.items) != 1
	):
		frappe.throw(_("Monthly invoice charges cannot be changed; use a reviewed correction."))
	line, expected = doc.items[0], snapshot["items"][0]
	if (
		any(
			str(line.get(k) or "") != str(expected[k] or "")
			for k in ("item_code", "income_account", "cost_center", "uom")
		)
		or money(line.rate) != money(expected["rate"])
		or money(line.qty) != money(1)
		or money(doc.grand_total) != money(obligation.amount)
	):
		frappe.throw(_("Monthly invoice amount or accounting mapping changed."))


def prevent_invoice_delete(doc, method=None):
	if doc.get("sports_billing_obligation"):
		frappe.throw(
			_(
				"Monthly invoice provenance is retained. Use the native reviewed cancellation or credit-note process."
			)
		)


def submit_obligation(obligation):
	"""Resume an existing draft; never replace cancelled or already posted invoices."""
	if not obligation.sales_invoice:
		return
	invoice = frappe.get_doc("Sales Invoice", obligation.sales_invoice, for_update=True)
	invoice.check_permission("read")
	if invoice.docstatus == 2:
		frappe.throw(_("Cancelled monthly invoice requires reviewed correction."))
	if invoice.docstatus == 0:
		submit_invoice(invoice)


def submit_invoice(invoice):
	"""Use native permissions and workflow transitions; never bypass approval rules."""
	from frappe.model.workflow import apply_workflow, get_transitions, get_workflow_name

	invoice.check_permission("submit")
	if invoice.meta.has_field("custom_selected_approver") and not invoice.get("custom_selected_approver"):
		invoice.custom_selected_approver = frappe.session.user
		invoice.save()
	workflow_name = get_workflow_name("Sales Invoice")
	if not workflow_name:
		invoice.submit()
		return
	workflow = frappe.get_doc("Workflow", workflow_name)
	if invoice.meta.queue_in_background:
		frappe.throw(_("Monthly billing requires synchronous Sales Invoice submission."))
	states = {row.state: cint(row.doc_status) for row in workflow.states}
	for _step in range(3):
		transitions = get_transitions(invoice, workflow)
		action = next((t.action for t in transitions if states.get(t.next_state) == 1), None)
		if not action:
			frappe.throw(_("Billing user cannot submit this invoice through the active workflow."))
		invoice = apply_workflow(invoice.as_dict(), action)
		if invoice and invoice.docstatus == 1:
			return
	frappe.throw(_("Monthly invoice did not reach a submitted workflow state."))
