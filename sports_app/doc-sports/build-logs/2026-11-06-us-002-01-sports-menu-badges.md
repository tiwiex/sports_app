# Build log: Sports menu number badges

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: sports_app:US-002-01 / EPIC-002
- Requirements: SPORTS-FR-019/020, SPORTS-NFR-006
- Affected app / branch: Sports App / story/us-003-01-enrollment-image-and-invoice-acceptance
- Pull requests: Not opened for this adjustment.
- Status: Verified development refinement

## Intended outcome and starting context

Sports navigation lacked the record badges shown for Finance. Boost populates Finance badges through its own summary and does not count optional app records.

## Policy decisions and plan

Keep Sports counts and DOM presentation in Sports App. Show pending enrollment applications, total players, sessions and organizations in the configured academy. Do not invent counts for configuration, documentation or a shortcut. Preserve native record permissions, Company/User Permissions, existing menu routing and handlers. Zero is meaningful; missing permission is not zero.

## Work performed

- Added protected navigation_api.get_counts with capability and native DocType read checks, validated configured Company and permission-filtered get_list aggregates. No unfiltered db.count/get_all calls, record identities or guest API.
- Extended Sports-owned console_navigation.js with native badge styling, descriptive accessible count labels, retained state across host redraws, visible-console polling every 15 seconds, received native list/doc-update triggers and focus catch-up. No API request without visible Sports navigation; single in-flight request and unchanged-text checks prevent observer request loops. Failed reads clear previous totals.
- Updated desktop/phone fixture and added permission/scope unit tests; updated current requirements, PRD, guide and story.

## Commands and observations

- Five isolated navigation API tests passed: native Company/filter aggregates, basic-console/Finance denial, missing DocType permissions, registrar versus management access, Company denial and zero totals.
- Actual source in Chromium passed at 1440/390px: event updates, explicit zero, native-only menu no requests, no observer request loop, redraw persistence without duplicates, error clearing/recovery, existing grouping/collapse/navigation unaffected.
- Native Moyours development read confirmed all four aggregate queries work under Administrator; native Guest denied. No record writes; rollback/destroy guaranteed.

- Final pinned pre-commit checks passed after normal formatter changes. Frappe Semgrep rules passed with zero findings after wrapping the access error in the translation helper. Full Sports discovery passed: 166 tests.
- Content-addressed assets published, current development provider assets verified on disk, development cache cleared and only frappe-bench-dev web restarted successfully. Live Boost checkout was not edited.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Meaningful Sports counts without Finance coupling | Native development aggregates and source inspection | Passed |
| Permission and Company boundaries | Five API unit tests; native Guest denial | Passed |
| Stable responsive sidebar and automatic updates | Real-source Chromium desktop/phone fixture | Passed |
| Pinned checks and development asset activation | Pinned hooks; Frappe static rules; full Sports suite; development publish/cache/restart | Passed |

## Decisions, deviations and recovery

Counts describe configured-academy totals, independent of the current table's search/page. Enrollment badge describes the default Pending queue, not accepted/rejected applications. Received socket notifications invalidate the counts; 15-second polling catches events for rooms not joined by the active table. A page-lifetime listener/timer is installed once by the existing Sports sidebar singleton; it performs no reads on hidden/non-console pages. No new server broadcast or biometric/finance behavior.

## Remaining work and release impact

No schema, permission, user, accounting or business-data changes. No live Boost edits, production deployment, commit or merge. Publish content-addressed Sports assets, clear development cache/restart development web and reload open browser tabs. Existing application work remains intact. Authenticated multi-user socket delivery is not independently exercised by the synthetic browser fixture.
