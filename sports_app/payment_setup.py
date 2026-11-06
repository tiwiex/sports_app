"""Install additive Sports links and a default review workflow, never replace one."""

import frappe


def setup_payment_fields():
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(
		{
			"Payment Entry": [
				dict(
					fieldname="sports_registration",
					label="Sports Registration",
					fieldtype="Link",
					options="Sports Registration",
					insert_after="party",
					read_only=1,
					no_copy=1,
					unique=1,
				),
				dict(
					fieldname="sports_claimed_on",
					label="Sports payment claimed on",
					fieldtype="Datetime",
					insert_after="sports_registration",
					read_only=1,
					no_copy=1,
				),
			]
		},
		update=True,
	)


def ensure_payment_workflow():
	active = frappe.get_all(
		"Workflow", filters={"document_type": "Payment Entry", "is_active": 1}, pluck="name"
	)
	if active:
		workflow = frappe.get_doc("Workflow", active[0])
		states = {row.state: int(row.doc_status) for row in workflow.states}
		if (
			workflow.workflow_state_field != "workflow_state"
			or not workflow.states
			or workflow.states[0].state != "Draft"
			or states.get("Draft") != 0
			or states.get("Pending Review") != 0
		):
			frappe.throw(
				"Enrollment payments require Draft and Pending Review states with docstatus 0 in the active Payment Entry workflow."
			)
		return
	for state, style in [
		("Draft", ""),
		("Pending Review", "Warning"),
		("Submitted", "Success"),
		("Cancelled", "Danger"),
	]:
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc(dict(doctype="Workflow State", workflow_state_name=state, style=style)).insert(
				ignore_permissions=True
			)
	for action in ("Complete", "Approve", "Cancel"):
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc(dict(doctype="Workflow Action Master", workflow_action_name=action)).insert(
				ignore_permissions=True
			)
	workflow = frappe.get_doc(
		dict(
			doctype="Workflow",
			workflow_name="Sports Payment Entry Review",
			document_type="Payment Entry",
			workflow_state_field="workflow_state",
			is_active=1,
			send_email_alert=0,
			states=[
				dict(state="Draft", doc_status=0, allow_edit="Accounts User"),
				dict(state="Pending Review", doc_status=0, allow_edit="Accounts User"),
				dict(state="Submitted", doc_status=1, allow_edit="Accounts Manager"),
				dict(state="Cancelled", doc_status=2, allow_edit="Accounts Manager"),
			],
			transitions=[
				dict(
					state="Draft",
					action="Complete",
					next_state="Pending Review",
					allowed="Accounts User",
					allow_self_approval=1,
				),
				dict(
					state="Pending Review",
					action="Approve",
					next_state="Submitted",
					allowed="Boost Finance Manager",
					allow_self_approval=1,
				),
				dict(
					state="Pending Review",
					action="Approve",
					next_state="Submitted",
					allowed="System Manager",
					allow_self_approval=1,
				),
				dict(
					state="Submitted",
					action="Cancel",
					next_state="Cancelled",
					allowed="Boost Finance Manager",
					allow_self_approval=1,
				),
				dict(
					state="Submitted",
					action="Cancel",
					next_state="Cancelled",
					allowed="System Manager",
					allow_self_approval=1,
				),
			],
		)
	)
	workflow.transitions = [row for row in workflow.transitions if frappe.db.exists("Role", row.allowed)]
	workflow.insert(ignore_permissions=True)
	frappe.clear_cache(doctype="Payment Entry")


def setup_payment_support():
	if not frappe.db.exists("DocType", "Sports Registration"):
		return
	setup_payment_fields()
	if frappe.db.get_single_value("Sports Academy Settings", "enrollment_payments_enabled"):
		ensure_payment_workflow()
		setup_invoice_support()


def setup_invoice_support():
	"""Add enrolment fields/items and seed a workflow only if none is active."""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(
		{
			"Sales Invoice": [
				dict(
					fieldname="sports_registration",
					label="Sports Registration",
					fieldtype="Link",
					options="Sports Registration",
					insert_after="customer",
					read_only=1,
					no_copy=1,
					unique=1,
				),
				dict(
					fieldname="sports_claimed_on",
					label="Sports payment claimed on",
					fieldtype="Datetime",
					insert_after="sports_registration",
					read_only=1,
					no_copy=1,
				),
			]
		},
		update=True,
	)
	settings = frappe.get_single("Sports Academy Settings")
	if not settings.enrollment_payments_enabled:
		return
	for field, code in (
		("enrollment_registration_item", "Sports Registration Fee"),
		("enrollment_jersey_item", "Sports Jersey Fee"),
	):
		if settings.get(field):
			continue
		if not frappe.db.exists("Item", code):
			group = frappe.db.get_value("Item Group", {"is_group": 0}, "name") or frappe.db.get_value(
				"Item Group", {"is_group": 1}, "name"
			)
			uom = frappe.db.get_value("UOM", {"name": "Nos"}, "name") or frappe.db.get_value(
				"UOM", {}, "name"
			)
			if not group or not uom:
				frappe.throw("Configure an Item Group and unit of measure for enrollment fees.")
			frappe.get_doc(
				dict(
					doctype="Item",
					item_code=code,
					item_name=code,
					item_group=group,
					stock_uom=uom,
					is_stock_item=0,
					is_sales_item=1,
					include_item_in_manufacturing=0,
				)
			).insert(ignore_permissions=True)
		item = frappe.get_doc("Item", code)
		if item.disabled or item.is_stock_item or not item.is_sales_item:
			frappe.throw("Configure compatible active non-stock enrollment fee items.")
		frappe.db.set_single_value("Sports Academy Settings", field, code)
	ensure_invoice_workflow()


def ensure_invoice_workflow():
	active = frappe.get_all(
		"Workflow", filters={"document_type": "Sales Invoice", "is_active": 1}, pluck="name"
	)
	if active:
		from sports_app.enrollment_invoices import invoice_workflow

		workflow = invoice_workflow()
		states = {s.state: int(s.doc_status) for s in workflow.states}
		if not any(
			t.state == "Pending Review" and t.action == "Complete Payment" and states.get(t.next_state) == 1
			for t in workflow.transitions
		):
			frappe.throw(
				"The existing Sales Invoice workflow must include an authorised Complete Payment transition from Pending Review to a submitted state. Existing workflows are not replaced automatically."
			)
		if workflow.name == "Sports Enrollment Invoice Review":
			_ensure_standard_draft_transitions(workflow)
		return
	for state, style in (
		("Draft", ""),
		("Pending Review", "Warning"),
		("Approved", "Success"),
		("Cancelled", "Danger"),
	):
		if not frappe.db.exists("Workflow State", state):
			frappe.get_doc(dict(doctype="Workflow State", workflow_state_name=state, style=style)).insert(
				ignore_permissions=True
			)
	for action in ("Complete", "Approve", "Complete Payment", "Cancel"):
		if not frappe.db.exists("Workflow Action Master", action):
			frappe.get_doc(dict(doctype="Workflow Action Master", workflow_action_name=action)).insert(
				ignore_permissions=True
			)
	roles = [
		role
		for role in ("Accounts Manager", "System Manager", "Boost Invoice Approver", "Boost Finance Manager")
		if frappe.db.exists("Role", role)
	]
	transitions = []
	for role in roles:
		transitions += [
			dict(
				state="Draft",
				action="Complete",
				next_state="Pending Review",
				allowed=role,
				allow_self_approval=1,
			),
			dict(
				state="Pending Review",
				action="Complete Payment",
				next_state="Approved",
				allowed=role,
				allow_self_approval=1,
				condition="doc.sports_registration",
			),
			dict(
				state="Pending Review",
				action="Approve",
				next_state="Approved",
				allowed=role,
				allow_self_approval=1,
				condition="not doc.sports_registration",
			),
			dict(
				state="Approved", action="Cancel", next_state="Cancelled", allowed=role, allow_self_approval=1
			),
		]
	workflow = frappe.get_doc(
		dict(
			doctype="Workflow",
			workflow_name="Sports Enrollment Invoice Review",
			document_type="Sales Invoice",
			workflow_state_field="workflow_state",
			is_active=1,
			send_email_alert=0,
			states=[
				dict(state="Draft", doc_status=0, allow_edit="Accounts User"),
				dict(state="Pending Review", doc_status=0, allow_edit="Accounts User"),
				dict(state="Approved", doc_status=1, allow_edit="Accounts Manager"),
				dict(state="Cancelled", doc_status=2, allow_edit="Accounts Manager"),
			],
			transitions=transitions,
		)
	).insert(ignore_permissions=True)
	_ensure_standard_draft_transitions(workflow)
	frappe.clear_cache(doctype="Sales Invoice")


def _ensure_standard_draft_transitions(workflow):
	"""Keep ordinary non-Sports invoice entry usable in our default workflow."""
	changed = False
	for role in ("Accounts User", "Boost Data Entry", "Boost Sales Data Entry"):
		if not frappe.db.exists("Role", role) or any(
			t.state == "Draft" and t.action == "Complete" and t.allowed == role for t in workflow.transitions
		):
			continue
		workflow.append(
			"transitions",
			dict(
				state="Draft",
				action="Complete",
				next_state="Pending Review",
				allowed=role,
				allow_self_approval=1,
				condition="not doc.sports_registration",
			),
		)
		changed = True
	if changed:
		workflow.save(ignore_permissions=True)
		frappe.clear_cache(doctype="Sales Invoice")
