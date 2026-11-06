# Manual attendance prototype

For a separate phone app with downloaded rosters and offline manual capture, use [Next.js attendance app](https://moyours.ideltatech.com/sports-attendance). See the [device/sync guide](attendance-app-guide.md). Session creation and finalization remain in Boost; enrollment remains HTML.

Open **Sports → Attendance** in the Boost console. Access currently uses Sports Registrar, Sports Academy Administrator or System Manager, with native document and Company permissions. A coach-specific role/assigned-group scope is not implemented in this prototype.

## Create a training session

1. Choose **New session** and enter a title, program, optional group, date, start/end times and venue.
2. Times use the academy timezone shown on the session. Sessions must start and end on the same day. The creating staff member is recorded as responsible operator.
3. Creating the session snapshots players with **Active** enrollments whose start/end dates include the session date, in the selected company/program/group. Multiple matching enrollments produce one roster entry per player. Pending, Suspended, Withdrawn, Completed, future-starting and expired enrollments are excluded.
4. If the roster is empty, check the enrollment status/dates under Players before creating a new session. Creation does not activate enrollments or admit applicants. Scheduling/roster scope is fixed after creation; cancel and recreate a session when it is wrong. There is no manual add-player exception yet.

## Record attendance

Open a session from the list. Choose Present, Late, Absent or Excused, then **Save attendance**. **Mark unmarked Present** fills the selectors; it does not save until you choose Save attendance. On phones, scroll the roster horizontally for correction and audit columns. Late is a manual choice; there is no automatic lateness threshold.

Unmarked means no decision has been recorded. It is not automatically treated as absence. Attendance can be recorded on the session date or afterward, never before the academy-local session date.

**Finalize session** asks for confirmation and marks all remaining Unmarked players Absent. Save unsaved changes first. Finalization records its operator/time. Already recorded statuses remain unchanged.

## Corrections and history

Changing a recorded status requires a reason, including after finalization. Status changes record the actor, time and source, with old/new status and reason in comments and native Version history. The **History** link opens the attendance record. Session counts show statuses separately; attendance rates and cross-session player reports are not implemented yet.

Concurrent stale changes are rejected; use **Refresh roster** to reload current values (confirm discarding unsaved changes when prompted). A failed batch saves none of its changes. Retrying the same recorded status does not create another audit entry.

## Cancel a session

Scheduled sessions can be cancelled with a reason. A cancelled roster is read-only and remains available for review. Finalized-session cancellation/reopening is future scope. Records cannot be deleted through the normal forms or console.

## Boundaries

This is manual attendance only. No fingerprint enrollment, templates, device connection, device-event ingestion, offline replay, automatic check-in/out or biometric attendance exists yet. No Customer, invoice, payment, fee-exemption or medical data is returned by the attendance API. Attendance never changes admission or payment status.

Biometric integration will later map authenticated device events to these session/player attendance records after device selection, identity/consent policy and replay/correction rules are agreed.
