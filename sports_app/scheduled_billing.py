"""Sports-only daily retries of monthly receivables under an explicit finance user."""

import frappe
from frappe import _
from frappe.utils import add_months, cint, getdate

from sports_app.academy import get_configured_settings
from sports_app.billing_access import enrollment_record, require_billing
from sports_app.billing_policy import period
from sports_app.monthly_billing import build, existing, generate_rows, submit_obligation
from sports_app.player_numbering import academy_date
from sports_app.registrations import acceptance_transaction


def validate_configuration(settings):
	if not cint(settings.get("automatic_monthly_billing")):
		return
	user = settings.get("monthly_billing_user")
	if not user or not frappe.db.exists("User", {"name": user, "enabled": 1, "user_type": "System User"}):
		frappe.throw(_("Select an enabled System User for billing automation."))


def months(settings, enrollment_start):
	"""Only completed calendar months, starting at this membership's join month."""
	start = getdate(enrollment_start).replace(day=1)
	current = academy_date(settings).replace(day=1)
	while start < current:
		yield str(start)[:7]
		start = getdate(add_months(start, 1))


def request_catchup(doc=None, method=None):
	"""Membership/fee configuration edits request catch-up after their transaction commits."""
	settings = get_configured_settings()
	if cint(settings.monthly_fees_enabled) and cint(settings.get("automatic_monthly_billing")):
		frappe.enqueue(
			"sports_app.scheduled_billing.run",
			enqueue_after_commit=True,
			job_id="sports-completed-month-billing",
			deduplicate=True,
		)


def setup_schedule():
	"""Register only the Sports daily task, without enabling global scheduling or granting roles."""
	method = "sports_app.scheduled_billing.run"
	if not frappe.db.exists("Scheduled Job Type", {"method": method}):
		frappe.get_doc(doctype="Scheduled Job Type", method=method, frequency="Daily").insert(
			ignore_permissions=True
		)


def run():
	"""Scheduler entry only; never exposed to Guest or the console as an RPC."""
	settings = get_configured_settings()
	if not (cint(settings.monthly_fees_enabled) and cint(settings.get("automatic_monthly_billing"))):
		return
	original_user = frappe.session.user
	try:
		validate_configuration(settings)
		# Audited: scheduler-only, management-selected enabled user; native rights rechecked below.
		frappe.set_user(settings.monthly_billing_user)  # nosemgrep: frappe-setuser
		# Re-read under the normal shared settings lock; manual runs serialize here too.
		settings = require_billing()
		if not (cint(settings.monthly_fees_enabled) and cint(settings.automatic_monthly_billing)):
			return
		validate_configuration(settings)
		if settings.monthly_billing_user != frappe.session.user:
			frappe.throw(_("Billing automation user changed; retry the scheduled run."))
		if not all(frappe.has_permission("Sales Invoice", p) for p in ("read", "create", "submit")):
			frappe.throw(_("Billing automation user requires native invoice read/create/submit permissions."))
		failures = []
		rows = frappe.get_list(
			"Sports Enrollment",
			filters={"company": settings.company, "status": "Active"},
			fields=["name", "start_date", "end_date"],
			order_by="name asc",
			page_length=0,
		)
		for row in rows:
			for month in months(settings, row.start_date):
				first, _last = period(month)
				if getdate(row.start_date) > first or (row.end_date and getdate(row.end_date) < first):
					continue
				try:
					with acceptance_transaction():
						enrollment_record(row.name)
						old = existing(row.name, month)
						if old:
							submit_obligation(old)
							continue
						built = build(row.name, month)
						if not built:
							continue
						result = generate_rows(
							month, [{"enrollment": row.name, "source_hash": built[0]["source_hash"]}]
						)[0]
						if result.get("state") == "Exception":
							frappe.throw(result["error"])
				except Exception:
					# Keep confidential concession reasons out of shared logs.
					failures.append(f"{month} / {row.name}")
		if failures:
			frappe.log_error(
				title="Sports monthly billing: charges require review",
				message="Failed enrollment/month keys (retry daily; inspect Monthly billing preview):\n"
				+ "\n".join(failures),
			)
		return {"failed": len(failures)}
	finally:
		# Always restore caller identity, including configuration/permission failures.
		frappe.set_user(original_user)  # nosemgrep: frappe-setuser
