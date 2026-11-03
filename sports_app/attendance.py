"""Session roster snapshots and controlled manual attendance; no biometric data."""
import hashlib
import json
from html import escape
from contextlib import contextmanager
from datetime import datetime
from zoneinfo import ZoneInfo

import frappe
from frappe import _
from frappe.utils import getdate, get_time, now_datetime
from sports_app.academy import validate_company
from sports_app.players import require_player_access, is_eligible

CAPABILITY = object()
STATUSES = ('Present', 'Late', 'Absent', 'Excused')
SESSION_FIELDS = ('title', 'program', 'group', 'session_date', 'start_time', 'end_time', 'venue')


def require_access():
    # Prototype operators are existing authorized Sports staff; no coach scope is inferred.
    require_player_access()


@contextmanager
def transaction():
    frappe.db.savepoint('sports_attendance')
    try:
        yield
    except Exception:
        frappe.db.rollback(save_point='sports_attendance')
        raise


def prevent_delete():
    frappe.throw(_('Attendance records are retained for audit. Cancel a session instead.'))


def identity(session, player):
    return hashlib.sha256(json.dumps([session, player]).encode()).hexdigest()


def fingerprint(values):
    return hashlib.sha256(json.dumps({key: str(values.get(key) or '') for key in SESSION_FIELDS}, sort_keys=True).encode()).hexdigest()


def require_service(doc):
    require_access()
    if doc.flags.sports_attendance_service is not CAPABILITY:
        frappe.throw(_('Use Sports Attendance in the console to change sessions or attendance.'), frappe.PermissionError)
    validate_company(doc.company)


def validate_session(doc):
    require_service(doc)
    previous = doc.get_doc_before_save()
    if previous and any(str(previous.get(k) or '') != str(doc.get(k) or '') for k in (*SESSION_FIELDS, 'company', 'timezone', 'operator', 'request_key', 'request_hash')):
        frappe.throw(_('Session scheduling and roster scope cannot change after creation. Cancel and create another session.'))
    if doc.status not in ('Scheduled', 'Finalized', 'Cancelled'):
        frappe.throw(_('Invalid session status.'))
    if get_time(doc.start_time) >= get_time(doc.end_time):
        frappe.throw(_('Session end time must be after start time on the same day.'))
    if not (doc.title or '').strip() or len(doc.title) > 140 or len(doc.venue or '') > 140:
        frappe.throw(_('Enter a session title and venue of at most 140 characters.'))
    program = frappe.get_doc('Sports Program', doc.program)
    program.check_permission('read')
    if program.company != doc.company or (not previous and not program.enabled):
        frappe.throw(_('Choose an enabled program in the academy company.'))
    if doc.group:
        group = frappe.get_doc('Sports Group', doc.group)
        group.check_permission('read')
        if group.company != doc.company or group.program != doc.program or (not previous and not group.enabled):
            frappe.throw(_('Choose an enabled group in this program.'))


def validate_attendance(doc):
    require_service(doc)
    session = frappe.get_doc('Sports Session', doc.session)
    session.check_permission('read')
    player = frappe.get_doc('Sports Player', doc.player)
    player.check_permission('read')
    enrollment = frappe.get_doc('Sports Enrollment', doc.enrollment)
    enrollment.check_permission('read')
    previous = doc.get_doc_before_save()
    if (session.company != doc.company or player.company != doc.company or enrollment.company != doc.company
            or enrollment.player != doc.player or (not previous and (enrollment.program != session.program
            or (session.group and enrollment.group != session.group)))):
        frappe.throw(_('Attendance must use the session company, player and roster enrollment.'))
    if session.status == 'Cancelled':
        frappe.throw(_('Cancelled sessions cannot be marked.'))
    if previous:
        if any(previous.get(k) != doc.get(k) for k in ('session', 'player', 'enrollment', 'company', 'identity')):
            frappe.throw(_('Attendance identity and roster provenance cannot change.'))
        if previous.status != doc.status and previous.status != 'Unmarked' and not (doc.correction_reason or '').strip():
            frappe.throw(_('A reason is required to correct recorded attendance.'))
    elif doc.status != 'Unmarked' or doc.source != 'Roster' or not is_eligible(enrollment, session.session_date):
        frappe.throw(_('New roster entries require an active, date-eligible enrollment.'))
    if doc.identity != identity(doc.session, doc.player) or doc.status not in ('Unmarked', *STATUSES):
        frappe.throw(_('Invalid attendance identity or status.'))


def eligible_roster(session):
    filters = {'company': session.company, 'program': session.program, 'status': 'Active', 'start_date': ['<=', session.session_date]}
    if session.group:
        filters['group'] = session.group
    enrollments = frappe.get_list('Sports Enrollment', filters=filters,
        fields=['name', 'player', 'start_date', 'end_date', 'status'],
        order_by='player asc, start_date asc, name asc', page_length=0)
    unique = {}
    for row in enrollments:
        if is_eligible(row, session.session_date):
            unique.setdefault(row.player, row.name)
    return unique


def get_session(name, write=False):
    require_access()
    doc = frappe.get_doc('Sports Session', name, for_update=write)
    doc.check_permission('write' if write else 'read')
    validate_company(doc.company)
    return doc


def ensure_markable(session):
    if session.status == 'Cancelled':
        frappe.throw(_('Cancelled sessions cannot be marked.'))
    if getdate(session.session_date) > datetime.now(ZoneInfo(session.timezone)).date():
        frappe.throw(_('Attendance cannot be marked or finalized before the session date.'))


def mark_row(row, status, expected_modified, reason='', source='Manual'):
    if status not in STATUSES:
        frappe.throw(_('Select Present, Late, Absent or Excused.'))
    if row.status == status:
        return False  # Lost-response retry must not duplicate audit entries.
    if not expected_modified or str(row.modified) != str(expected_modified):
        frappe.throw(_('Attendance changed. Refresh the roster before saving.'), frappe.TimestampMismatchError)
    reason = (reason or '').strip()
    if len(reason) > 1000 or (row.status != 'Unmarked' and not reason):
        frappe.throw(_('Enter a correction reason of up to 1000 characters.'))
    old = row.status
    row.flags.sports_attendance_service = CAPABILITY
    row.update(dict(status=status, source=source, marked_by=frappe.session.user, marked_on=now_datetime(), correction_reason=reason))
    row.save()
    row.add_comment('Comment', _('Attendance: {0} → {1}. Source: {2}. Reason: {3}').format(old, status, source, escape(reason) if reason else _('Initial marking')))
    return True
