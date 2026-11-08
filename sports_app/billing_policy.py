"""Calendar-month calculation independent of invoice posting and sensitive reasons."""

import calendar
import hashlib
import json
import re
from datetime import date
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

import frappe
from frappe import _
from frappe.utils import getdate


def money(value):
	try:
		number = Decimal(str(value))
		if not number.is_finite() or number < 0 or number >= Decimal("100000000000"):
			raise ValueError
		return number.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
	except (ValueError, TypeError, InvalidOperation):
		frappe.throw(_("Enter a finite non-negative amount below 100 billion."))


def period(value):
	if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}", value):
		frappe.throw(_("Choose a billing month in YYYY-MM format."))
	try:
		year, month = [int(part) for part in value.split("-")]
		start = date(year, month, 1)
		return start, date(year, month, calendar.monthrange(year, month)[1])
	except ValueError:
		frappe.throw(_("Choose a valid billing month."))


def overlap(start, end, other_start, other_end):
	return getdate(start) <= (getdate(other_end) if other_end else date.max) and getdate(other_start) <= (
		getdate(end) if end else date.max
	)


def charge(enrollment, plan, decisions, month):
	start, end = period(month)
	# The accepted policy bills active-at-start memberships only. Historic suspension
	# cannot be inferred from the current status; stop rather than invent history.
	if enrollment.status == "Suspended" and overlap(enrollment.start_date, enrollment.end_date, start, end):
		frappe.throw(_("Suspended enrollment requires a reviewed billing decision."))
	if (
		enrollment.status != "Active"
		or getdate(enrollment.start_date) > start
		or (enrollment.end_date and getdate(enrollment.end_date) < start)
	):
		return None
	if plan.joining_policy != "Full fee if active at month start":
		frappe.throw(_("Configure the approved month-start billing policy."))
	if getdate(plan.effective_from) > start or (plan.effective_to and getdate(plan.effective_to) < end):
		frappe.throw(_("A single fee plan must cover the complete calendar month."))
	if not 1 <= int(plan.due_day or 0) <= 28:
		frappe.throw(_("Choose a due day from 1 to 28."))
	active = [d for d in decisions if overlap(d.effective_from, d.effective_to, start, end)]
	if len(active) > 1:
		frappe.throw(_("Overlapping approved concessions require review."))
	amount = money(plan.monthly_amount)
	if active:
		d = active[0]
		if getdate(d.effective_from) > start or (d.effective_to and getdate(d.effective_to) < end):
			frappe.throw(_("A concession changes within this month; review the charge before generating."))
		if d.coverage_type == "Full":
			amount = Decimal("0.00")
		elif d.coverage_type == "Percentage":
			percent = money(d.coverage_value)
			if not 0 < percent <= 100:
				frappe.throw(_("Percentage coverage must be greater than zero and at most 100."))
			amount = money(amount * (1 - percent / 100))
		elif d.coverage_type == "Fixed amount":
			amount = max(Decimal("0.00"), amount - money(d.coverage_value))
		else:
			frappe.throw(_("Select a valid concession coverage."))
	return dict(
		amount=str(money(amount)),
		due_date=str(date(start.year, start.month, int(plan.due_day))),
		billing_month=month,
	)


def digest(value):
	return hashlib.sha256(
		json.dumps(value, sort_keys=True, default=str, separators=(",", ":")).encode()
	).hexdigest()
