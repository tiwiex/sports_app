# Build log: Manual attendance prototype

- Date: 2026-11-03 (Africa/Lagos)
- Stories / epic: US-006-01, US-006-02; partial dependency evidence US-006-03 / EPIC-006
- Requirements: SPORTS-FR-014, SPORTS-FR-015, SPORTS-NFR-002, SPORTS-NFR-003, SPORTS-NFR-004, SPORTS-NFR-006
- Affected apps / branch / versions: Sports App / story/us-006-01-attendance-prototype, base HEAD 48fb0a2 plus preserved pending work
- Pull requests: None; changes uncommitted
- Status: Verified development prototype / In review

## Intended outcome and starting context

The user requested an attendance prototype and explicitly reminded us to record a build log. Fingerprint hardware/model/API and biometric policies are not selected. Implement the manual operational workflow first; do not simulate fingerprint enrollment or claim device integration.

## Policy decisions and plan

- Existing Sports Registrar, Sports Academy Administrator and System Manager operators, with native document and Company permissions. Do not invent a coach-assignment policy or grant finance access.
- Same-day sessions with academy timezone, current creator as responsible operator, program/optional group, venue and date/start/end time. Overlapping sessions remain explicit choices.
- Fixed creation-time roster from Active enrollments whose inclusive effective dates cover the session day. Deduplicate overlapping enrollments per player. No manual roster exception or automatic admission/activation.
- Present/Late/Absent/Excused are explicit staff decisions. Unmarked becomes Absent only after confirmed finalization. Future-date marking/finalization and cancelled-session marking are blocked.
- Recorded-status corrections require a reason and retain old/new status, actor, time, source, comments and native Version history. Finalized sessions remain correctable with a reason.

## Work performed

- Added Sports Session and Sports Attendance DocTypes/controllers with tracked changes, Company links, protected scheduling/provenance, unique session request keys and unique session/player identity. Normal native/REST writes cannot forge the private service capability. Delete is blocked; scheduled sessions can be cancelled with a reason.
- Added attendance.py policies and attendance_api.py endpoints for configuration, session create/list, roster, atomic batch marking, explicit finalization and cancellation. Standard roles, document permissions and Company checks remain enforced. APIs return no customer/payment/medical details.
- Session create retries reuse the existing session when the normalized fingerprint matches. Settings/session/row locks, expected-modified conflict checks and savepoints protect repeat/concurrent operations. Same-status replay is a no-op; a failed batch rolls back preceding changes.
- Added the Sports Attendance console provider/asset: session list/filter/pagination, creation dialog, friendly program/group labels, roster modal, totals, save/bulk selection, explicit finalization, correction reasons, safe roster refresh, cancel/read-only behavior and per-record History links. Tables are keyboard focusable and horizontally scrollable on phones.
- Updated requirements, PRD, epic/stories, overview and an attendance guide. Stories remain In progress; the cross-session reporting/coach-scope story remains Proposed.

## Commands and observations

- Full Sports unit suite: 113 tests passed. New policy/API checks cover eligibility boundaries, deduplication, role/company guards, forged capability, correction reasons, actor/source, no-op retries, optimistic conflicts, transaction rollback, protected input and finalization policy.
- Node syntax and git whitespace checks passed.
- Native Moyours QA used a synthetic program/group, minimal player/enrollment fixtures and sessions inside a rollback-only transaction with commits and outbound mail blocked. Minimal player/enrollment fixture insertion deliberately bypassed identity/customer/user hooks to isolate attendance; intake creation is not re-tested by this fixture.
- Native QA passed date filtering, overlapping-enrollment deduplication, repeat session creation, forged-service denial, actual unique session/player constraint, stale-batch rollback, repeat marking without extra audit comments, no automatic absence, explicit/repeat finalization, reason-required correction, Version audit, cancelled/future guards and Guest denial across all seven endpoints.
- After QA, all Session/Attendance/Program/Group/Player/Enrollment/Comment/Version and invoice/receipt/GL/payment-ledger counts returned to baseline. No real attendance, identity accounts, external email or financial posting remains from tests.
- Chromium fixture loads actual attendance.js and Boost CSS at 1440px/390px. Passed session creation, roster selection/save, unsaved-change guard, explicit finalization confirmation, correction reason payload, cancellation/read-only controls, History links, no page-level horizontal overflow and unmount cleanup. Dialog/API are fixtures; native business validation was checked separately above. Synthetic previews inspected: [desktop](assets/2026-11-03-attendance-1440.png), [phone](assets/2026-11-03-attendance-390.png).

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Dated session/operator and enrollment roster | Native create/roster and unit eligibility checks | Passed |
| One logical player/session, retry safety | Native unique constraint, overlap and request/status retry checks | Passed |
| Manual save/finalization/correction audit | Native save, explicit absence, reason and Version checks | Passed |
| Conflict rollback and private endpoints | Native batch conflict and Guest denial, unit Company guard | Passed |
| Usable console at desktop/phone | Actual view/CSS fixture and inspected synthetic previews | Passed |

## Decisions, deviations and recovery

Manual-only prototype. No fingerprint material/device ID endpoint, device emulator, offline event queue, automatic lateness/checkout, manual roster exception, coach-group assignment or attendance-rate calculation is supplied. Session operator is the creator. Group-restricted coach and cross-session report acceptance are not claimed. Existing pending enrollment/email/club work was preserved.

## Data/schema changes and cleanup

Loaded only the two additive DocTypes on moyours.ideltatech.com through native reload APIs, rather than a full migration. No new roles or finance configuration changes. All synthetic QA rows and audits were rolled back. Preview screenshots contain synthetic data only. Existing user approvals, invoices, receipts and rosters are unchanged.

## Remaining work and release impact

Published attendance.9a6ed973e30cff1b.js and console_overview.8390aaa5cfb47f7a.js to Moyours development, cleared caches and restarted only its web process. Fresh configuration/session API reads and HTTPS byte-for-byte asset checks passed; no test sessions remain. Sports Development Tools discovers this indexed log and guide. No production deployment, commit/merge/push, real attendance recording or biometrics. Further scope includes assigned-group coach boundaries, roster exceptions, date-range player reports/rates, final-session cancellation policy, hardware enrollment/authenticated replay and production acceptance. Sequential lock/conflict checks passed; parallel load testing is not claimed.
