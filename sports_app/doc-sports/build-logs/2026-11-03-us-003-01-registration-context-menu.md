# Build log: Registration table and context menu

- Date: 2026-11-03 (Africa/Lagos)
- Story / epic: US-003-01 / EPIC-003
- Requirements: SPORTS-FR-003, SPORTS-NFR-002, SPORTS-NFR-003
- Affected apps / branch / versions: Sports App / story/us-003-01-registration-context-menu; starting HEAD 48fb0a2, existing notification/club-directory work preserved
- Pull requests: None; changes uncommitted
- Status: Verified development refinement / In review

## Intended outcome and starting context

The registration queue had a basic striped table and clicking a reference replaced the list with a full profile. The user requested the same presentation as Sales/Purchase Invoices, including a reference context menu with View and admission actions.

## Policy decisions and plan

Reuse Boost's table, reference menu and status-chip CSS classes while keeping rendering, handlers and registration rules in Sports App. No Boost source changes or private shell API calls. View opens a modal; Pending rows with document write permission additionally expose Accept/Reject. Fresh record/permission checks precede confirmation, and native server enforcement remains authoritative. Admission continues to be separate from bank verification and finance posting.

## Work performed

- Restyled the table with invoice-style bordered/sticky headers, status badges, user-formatted timestamps and a reference dropdown.
- Added keyboard-operable reference menus with View, conditional Accept registration and Reject registration. Fixed-position dropdowns remain inside the viewport; outside click/Escape, scrolling, resize and unmount close menus and clean up listeners.
- View opens the existing registration detail content in a large modal, retaining the filtered/paginated list. Existing linked invoice/receipt/player information remains available under the same read controls.
- Accept keeps enrollment choices and displays possible player matches before explicit confirmation. Reject keeps its required reason. Successful decisions refresh the list and reopen the current profile with updated state.
- List/detail APIs return a native document-write review capability only for Pending records. Existing endpoint role, Company, write, status, locking, acceptance idempotency and financial rules remain unchanged.
- Added allowlisted server sorting for Reference, Player, Pathway, Submitted on and Status before 20-row pagination, with a stable name tie-break. Header arrows/aria-sort reflect direction; sorting resets the page.
- Updated requirements, PRD, story and website guide; indexed this adjustment log for Sports Development Tools.

## Commands and observations

- `python -m unittest discover -s sports_app/tests -p 'test_*.py' -q`: 101 tests passed, including three new list capability/sort/authorization tests. Existing notification and registration/finance tests remain passing.
- `node --check sports_app/public/js/registrations.js` and `git diff --check`: passed. Removed a trailing blank line from the pending settings-story documentation.
- Chromium fixture loads the actual registration view and Boost CSS at 1440px and 390px. Passed reference dropdowns, viewport placement, keyboard open/navigation/Escape, modal View retaining the list, pending/write-only actions, possible-match acceptance confirmation, reason-required rejection, stale-record recheck, post-decision refresh, sort request and unmount cleanup. No browser errors or document-level horizontal overflow. Dialog/API are fixture stubs, not authenticated native controls or real applicant mutations.
- Initial browser overflow assertion came from an incomplete host fixture (missing the native sidebar/main layout); corrected the fixture to use the Boost structure and reran both widths successfully.
- Native read-only Moyours list/detail API check as Administrator passed safe sorting and write capability. Guest list access remained denied. Transaction rolled back; no actual applicant was accepted/rejected.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Invoice-style table and reference menu | Actual Sports view/Boost CSS browser fixture, both widths | Passed |
| View without leaving list | Modal/list retention browser assertion | Passed |
| Conditional, explicit admission actions | Capability unit/native checks; pending/read-only/completed browser cases | Passed |
| Preserve match/rejection safeguards | Confirmation/match/reason and stale-record browser checks; existing server suite | Passed |
| Safe full-result sorting | Server allowlist/order/pagination tests and client request assertion | Passed |
| No Guest access or financial changes | Native Guest denial, rollback/read-only checks; existing suite | Passed |

## Decisions, deviations and recovery

No new DocType, workflow, role or approval capability. No schema migration. Capability flags improve menu visibility and never substitute for accept/reject endpoint authorization. Existing uncommitted notification and club-directory changes remain intact on the new story branch.

## Remaining work and release impact

Development-only publication on moyours.ideltatech.com. Published content-addressed registrations.3205bf0ec17012dd.js, cleared site caches and reloaded only the development web process. Reload the console to fetch the new view. No production changes, commits/merges/pushes, new QA accounts, outbound messages or real admissions/financial postings. Authenticated native Dialog posting and production acceptance remain outside this fixture-based UI verification.
