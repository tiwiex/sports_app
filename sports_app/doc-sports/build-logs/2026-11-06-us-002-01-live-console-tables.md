# Build log: live operational console tables

- Date: 2026-11-06 (Africa/Lagos)
- Stories / epic: US-002-01 / EPIC-002; queue refinements US-003-01, US-003-02, US-009-01
- Requirements: Sports console integration and existing private data/Company boundaries; direct user refinement
- Apps / branches: Sports App `story/us-003-01-enrollment-image-and-invoice-acceptance`; independent development Boost `story/console-table-auto-refresh` from 30aba92
- Pull requests: Not opened; no commit/merge requested this turn
- Status: Verified on development

## Intended outcome and starting context

User requested watcher-style updates similar to Ingentia, which is absent from this workspace. Sports tables previously required explicit refresh. Boost had partial native document realtime support, but no provider-table watcher.

## Policy decisions and plan

Use the optional generic Boost mount.watch hook, with each Sports view declaring dependencies and a protected reread callback. No Sports logic goes into the host. Refresh the current filtered/sorted/paginated query, never inject records supplied by events. Preserve permissions and active interaction; no automatic document actions.

## Work performed

- Enrollments watch Sports Registration/Player and related invoice/receipt events.
- Players watch Player/Enrollment/User/Customer; Attendance watches Session/Attendance/Biometric Enrollment/Player/Enrollment; Clubs watches Organization/Opportunity/Interaction.
- Background render keeps existing state variables, checks current generation/abort/canApply after reads, and compares data snapshots before touching the DOM. Watcher preserves scroll and defers edits/menus/dialogs.
- Default 15-second fallback with native event debounce, hidden-tab pause, visibility/focus/socket-resume catch-up, one in-flight refresh and lifecycle cleanup.
- Old hosts continue manual refresh. Explicit Refresh behavior is retained; settings/documentation editing and the separate Next app are outside this table slice.
- Updated requirements, PRD, guide and affected story criteria; separate build evidence in both apps.

## Commands and observations

- Sports Python discovery: 161 tests passed after integration.
- Real Boost source + real Sports Enrollments Chromium fixture passed at 1440/390px: new records, equal-data DOM retention, context-menu/filter/modal deferral, hidden catch-up, actual timer fallback, abort/in-flight reply rejection and listener/room teardown. Real Finance callback preserves Company/search and rejects navigation-stale data. APIs and socket notifications are isolated fixtures; no browser ERP writes.
- Existing Boost provider VM and 22 provider/optional-dimension Python tests passed. Independent paths/inodes/Git branches prove no live Boost link/edit. Initial automatic-review symlink assumption was resolved with filesystem evidence before authorized development edits.

## Verification evidence

| Criterion | Check | Result |
|---|---|---|
| New rows and unchanged DOM | Real-code Chromium integration | Passed |
| Safe menus/filters/modals | Desktop/phone focus and menu checks | Passed |
| Hidden/poll/abort lifecycle | Chromium notification, timer and late-response assertions | Passed |
| Permission/state preservation | Protected existing API callbacks; Finance Company/search fixture; existing Python suite | Passed |
| Other Sports queues / formatting / activation | Existing enrollment/player/attendance desktop/phone regressions; pinned checks; development activation | Passed |

## Decisions, deviations and recovery

No Ingentia code was inspected/copied. The host remains generic and keeps Dashboard/CoA legacy realtime behavior. User interaction is intentionally deferred rather than replaced under the pointer. Errors retain last good rows and retry at the next bounded poll. Room authorization remains native; unavailable realtime still catches up by polling.

## Remaining work and release impact

Final watcher integration (including deletion/reconnect catch-up and report-session-only cache updates without DOM replacement), enrollment, player and attendance browser suites all passed at desktop/phone widths. Pinned Sports pre-commit checks passed, including the new fixture explicitly. Development activation verified the erp_boost import resolves into the independent dev checkout; current provider assets were published and confirmed on disk, site cache cleared and only development web restarted. Socket transport HTTP 200 / Engine.IO handshake accepted. This confirms transport availability; authenticated cross-user event delivery was not independently exercised outside the synthetic browser fixture. No claim of production validation. No schema/data changes, business actions, temporary accounts or production deployment. Publish Sports assets and clear/restart only the designated development web process. Deploy compatible Boost before Sports elsewhere and reload existing open console tabs. Wider alert center, editable documentation tables and Next attendance live/offline sync are separate scope.
