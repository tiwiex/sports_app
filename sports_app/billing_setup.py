"""Install unassigned Sports capability and a server-owned invoice reference only."""

import frappe

from sports_app.billing_access import FINANCE_ROLE, OBLIGATION


def setup_role():
	if not frappe.db.exists("Role", FINANCE_ROLE):
		frappe.get_doc(doctype="Role", role_name=FINANCE_ROLE, desk_access=1).insert(ignore_permissions=True)


def setup_billing():
	setup_role()
	if frappe.db.exists("DocType", "Sales Invoice"):
		from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

		create_custom_fields(
			{
				"Sales Invoice": [
					dict(
						fieldname="sports_billing_obligation",
						label="Sports monthly obligation",
						fieldtype="Link",
						options=OBLIGATION,
						insert_after="customer",
						read_only=1,
						no_copy=1,
						unique=1,
					)
				]
			},
			update=True,
		)


def setup_monthly_workflow():
	"""Add a narrowly conditional action only to our own installed invoice workflow."""
	name = "Sports Enrollment Invoice Review"
	if not frappe.db.exists("Workflow", name):
		return
	workflow = frappe.get_doc("Workflow", name)
	if not workflow.is_active or workflow.document_type != "Sales Invoice":
		return
	action = "Submit monthly fee"
	if not frappe.db.exists("Workflow Action Master", action):
		frappe.get_doc(doctype="Workflow Action Master", workflow_action_name=action).insert(
			ignore_permissions=True
		)
	condition = "doc.sports_billing_obligation and not doc.sports_registration"
	states = {row.state: int(row.doc_status) for row in workflow.states}
	# Reuse existing approval roles; do not create new finance grants or edit transitions.
	approvers = {
		(row.allowed, row.next_state)
		for row in workflow.transitions
		if row.action == "Approve" and states.get(row.next_state) == 1
	}
	changed = False
	for role, target in sorted(approvers):
		if any(row.action == action and row.allowed == role for row in workflow.transitions):
			continue
		workflow.append(
			"transitions",
			dict(
				state="Draft",
				action=action,
				next_state=target,
				allowed=role,
				allow_self_approval=1,
				condition=condition,
			),
		)
		changed = True
	if changed:
		workflow.save(ignore_permissions=True)
		frappe.clear_cache(doctype="Sales Invoice")


def setup_subscription_payments():
	"""Add immutable Sports receipt provenance and a Sports-only native workflow action."""
	from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

	create_custom_fields(
		{
			"Payment Entry": [
				dict(
					fieldname="sports_billing_obligation",
					label="Sports monthly obligation",
					fieldtype="Link",
					options=OBLIGATION,
					read_only=1,
					no_copy=1,
				),
				dict(
					fieldname="sports_subscription_request",
					label="Sports subscription payment request",
					fieldtype="Data",
					read_only=1,
					no_copy=1,
					unique=1,
				),
				dict(
					fieldname="sports_subscription_payload",
					label="Sports subscription payment snapshot",
					fieldtype="Data",
					read_only=1,
					no_copy=1,
					hidden=1,
				),
			]
		},
		update=True,
	)
	name = "Sports Payment Entry Review"
	if not frappe.db.exists("Workflow", name):
		return
	workflow = frappe.get_doc("Workflow", name)
	if not workflow.is_active or workflow.document_type != "Payment Entry":
		return
	action = "Receive subscription"
	if not frappe.db.exists("Workflow Action Master", action):
		frappe.get_doc(doctype="Workflow Action Master", workflow_action_name=action).insert(
			ignore_permissions=True
		)
	states = {r.state: int(r.doc_status) for r in workflow.states}
	roles = {
		(r.allowed, r.next_state)
		for r in workflow.transitions
		if r.action == "Approve" and states.get(r.next_state) == 1
	}
	changed = False
	for role, target in sorted(roles):
		if any(r.action == action and r.allowed == role for r in workflow.transitions):
			continue
		workflow.append(
			"transitions",
			dict(
				state="Draft",
				action=action,
				next_state=target,
				allowed=role,
				allow_self_approval=1,
				condition="doc.sports_billing_obligation and doc.sports_subscription_request and not doc.sports_registration",
			),
		)
		changed = True
	if changed:
		workflow.save(ignore_permissions=True)
		frappe.clear_cache(doctype="Payment Entry")
