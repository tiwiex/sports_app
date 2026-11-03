"""Private Company-scoped manual attendance prototype endpoints."""
from html import escape
import frappe
from frappe import _
from frappe.utils import cint, getdate, get_time, now_datetime
from sports_app import attendance as policy
from sports_app.academy import get_configured_settings, validate_company
from sports_app.registrations import request_uuid


@frappe.whitelist()
def configuration():
    policy.require_access()
    settings = get_configured_settings()
    validate_company(settings.company)
    return dict(company=settings.company, timezone=settings.timezone, today=str(policy.datetime.now(policy.ZoneInfo(settings.timezone)).date()),
        programs=frappe.get_list('Sports Program', filters={'company': settings.company, 'enabled': 1}, fields=['name','program_name'], page_length=0),
        groups=frappe.get_list('Sports Group', filters={'company': settings.company, 'enabled': 1}, fields=['name','group_name','program'], page_length=0))


@frappe.whitelist(methods=['POST'])
def create_session(values, request_key):
    policy.require_access()
    values = frappe.parse_json(values)
    if not isinstance(values, dict) or set(values) - set(policy.SESSION_FIELDS):
        frappe.throw(_('Invalid session fields.'))
    values = {k: values.get(k) or '' for k in policy.SESSION_FIELDS}
    if any(not isinstance(v, str) for v in values.values()):
        frappe.throw(_('Invalid session field values.'))
    if any(not values[k] for k in ('title','program','session_date','start_time','end_time')):
        frappe.throw(_('Complete the session title, program, date and start/end times.'))
    values.update(session_date=str(getdate(values['session_date'])), start_time=str(get_time(values['start_time'])), end_time=str(get_time(values['end_time'])))
    key = request_uuid(request_key)
    settings = get_configured_settings(for_update=True)
    validate_company(settings.company)
    with policy.transaction():
        existing = frappe.db.get_value('Sports Session', {'request_key': key}, ['name','request_hash'], as_dict=True)
        digest = policy.fingerprint(values)
        if existing:
            doc = policy.get_session(existing.name)
            if existing.request_hash != digest:
                frappe.throw(_('The retried session details changed. Start a new session request.'))
            return doc.name
        doc = frappe.get_doc(dict(doctype='Sports Session', **values, company=settings.company,
            timezone=settings.timezone, status='Scheduled', operator=frappe.session.user, request_key=key, request_hash=digest))
        doc.flags.sports_attendance_service = policy.CAPABILITY
        doc.insert()
        for player, enrollment in policy.eligible_roster(doc).items():
            row = frappe.get_doc(dict(doctype='Sports Attendance', session=doc.name, player=player, enrollment=enrollment,
                company=doc.company, identity=policy.identity(doc.name,player), status='Unmarked', source='Roster'))
            row.flags.sports_attendance_service = policy.CAPABILITY
            row.insert()
        return doc.name


@frappe.whitelist()
def list_sessions(status='', start=0):
    policy.require_access()
    settings = get_configured_settings()
    validate_company(settings.company)
    filters = {'company': settings.company}
    if status:
        if status not in ('Scheduled','Finalized','Cancelled'):
            frappe.throw(_('Invalid session status.'))
        filters['status'] = status
    rows = frappe.get_list('Sports Session', filters=filters,
        fields=['name','title','program','group','session_date','start_time','end_time','timezone','venue','status'],
        order_by='session_date desc, start_time desc, name asc', start=max(0,cint(start)), page_length=21)
    programs = {r.name:r.program_name for r in frappe.get_list('Sports Program', filters={'company':settings.company}, fields=['name','program_name'], page_length=0)}
    for row in rows:
        row['program_label'] = programs.get(row.program,row.program)
    return dict(rows=rows[:20],has_more=len(rows)>20)


@frappe.whitelist()
def roster(name):
    session = policy.get_session(name)
    rows = frappe.get_list('Sports Attendance', filters={'session':session.name,'company':session.company},
        fields=['name','player','status','source','marked_by','marked_on','correction_reason','modified'], order_by='player asc', page_length=0)
    names = [r.player for r in rows]
    players = {r.name:r.full_name for r in frappe.get_list('Sports Player',filters={'company':session.company,'name':['in',names]},fields=['name','full_name'],page_length=0)} if names else {}
    for row in rows:
        if row.player not in players:
            frappe.throw(_('You cannot read all players on this roster.'),frappe.PermissionError)
        row['player_name'] = players[row.player]
        row['modified'] = str(row.modified)
    counts = {status:sum(r.status==status for r in rows) for status in ('Unmarked',*policy.STATUSES)}
    return dict(session={k:session.get(k) for k in ('name','title','company','program','group','session_date','start_time','end_time','timezone','venue','status','operator','finalized_by','finalized_on','cancellation_reason')}, rows=rows, counts=counts)


@frappe.whitelist(methods=['POST'])
def save_attendance(name, marks):
    session = policy.get_session(name,write=True)
    policy.ensure_markable(session)
    marks = frappe.parse_json(marks)
    if not isinstance(marks,list) or not marks or len(marks)>1000:
        frappe.throw(_('Submit between 1 and 1000 attendance changes.'))
    seen=set()
    with policy.transaction():
        for mark in marks:
            if not isinstance(mark,dict) or set(mark)-{'name','status','modified','reason'} or not mark.get('name') or mark['name'] in seen:
                frappe.throw(_('Invalid or repeated attendance row.'))
            seen.add(mark['name'])
            row=frappe.get_doc('Sports Attendance',mark['name'],for_update=True)
            row.check_permission('write')
            if row.session!=session.name or row.company!=session.company:
                frappe.throw(_('Attendance row belongs to another session.'),frappe.PermissionError)
            if not isinstance(mark.get('reason',''),str):frappe.throw(_('Invalid correction reason.'))
            policy.mark_row(row,mark.get('status'),mark.get('modified'),mark.get('reason',''))
    return roster(session.name)


@frappe.whitelist(methods=['POST'])
def finalize_session(name):
    session=policy.get_session(name,write=True)
    policy.ensure_markable(session)
    if session.status=='Finalized':return roster(name)
    with policy.transaction():
        rows=frappe.get_list('Sports Attendance',filters={'session':name,'company':session.company,'status':'Unmarked'},fields=['name'],page_length=0)
        for entry in rows:
            row=frappe.get_doc('Sports Attendance',entry.name,for_update=True)
            row.check_permission('write')
            policy.mark_row(row,'Absent',str(row.modified),source='Finalization')
        session.flags.sports_attendance_service=policy.CAPABILITY
        session.update(dict(status='Finalized',finalized_by=frappe.session.user,finalized_on=now_datetime()))
        session.save()
        session.add_comment('Comment',_('Session finalized. Remaining unmarked roster players were explicitly marked Absent.'))
    return roster(name)


@frappe.whitelist(methods=['POST'])
def cancel_session(name,reason):
    session=policy.get_session(name,write=True)
    if not isinstance(reason,str) or not reason.strip() or len(reason)>1000:frappe.throw(_('Enter a cancellation reason of up to 1000 characters.'))
    if session.status=='Cancelled':return roster(name)
    if session.status!='Scheduled':frappe.throw(_('Only scheduled sessions can be cancelled in this prototype.'))
    session.flags.sports_attendance_service=policy.CAPABILITY
    session.update(dict(status='Cancelled',cancellation_reason=reason.strip()))
    session.save()
    session.add_comment('Comment',_('Session cancelled: {0}').format(escape(reason.strip())))
    return roster(name)
