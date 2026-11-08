# Build log: Sports Academy landing dashboard

- Date: 7 November 2026 (Africa/Lagos)
- Story / epic: US-008-02 / EPIC-008
- Requirements: SPORTS-FR-023, SPORTS-NFR-002, SPORTS-NFR-005
- Affected apps / branches / versions: Sports App, `story/epic-004-scholarships-and-monthly-billing`, current development checkout
- Pull requests: None requested
- Status: Verified development dashboard slice

## Intended outcome and starting context

User requested a dashboard in Sports Academy. The landing view previously displayed introductory paragraphs only. Existing subscription Overview totals and Community-inspired card colours already served the billing view.

## Policy decisions and plan

Provide current operational counts, upcoming sessions, annual subscription totals/chart and existing workflow shortcuts. Use configured academy company/timezone, native list and Company permissions, role capabilities and existing subscription summary. The financial year selector does not change current operational counts. Do not call Settled cash received. Exclude scholarship/biometric/contact data. Show Restricted for unavailable metrics.

## Work performed

- Added `dashboard.py`: console gate before settings access, configured Company validation, native permission checks, visible-player intersection for Active enrollments, scoped counts and bounded upcoming session query. Reuses subscription Overview only with native read privileges; returns permitted shortcuts without any role grants.
- Replaced `public/js/console_overview.js` with responsive green hero, four coloured operational cards, role-scoped shortcuts, Billed/Settled/Outstanding cards, accessible monthly bar chart and upcoming sessions. Uses existing host `data-dashboard-view` navigation; no Boost source edits/import. Text uses DOM textContent, record IDs are URL-encoded. Refresh/watch/year requests respect abort and generation checks, with empty/restricted/error retry states.
- Added six backend tests and a desktop/phone browser fixture. Updated baseline, PRD, setup guide, story and indexed evidence. Existing broader story acceptance/state is not marked Done.

## Commands and observations

- Full isolated Python test suite: **258 passed**, including six new dashboard tests.
- Desktop/phone browser fixture at 1440px/390px: passed cards/chart values, escaped strings, shortcut contract, year refresh, restricted/empty/error retry states, no page overflow and unmount protection. Screenshots `/tmp/sports-dashboard-1440.png` and `/tmp/sports-dashboard-390.png` visually inspected.
- Native rollback-only development smoke on `moyours.ideltatech.com`: dashboard totals reconciled to the existing billing service, player count matched scoped rows, upcoming list bounded to five, native Guest denied, no player/enrollment/invoice/payment count changes. One dashboard sample **0.241s**; not a p95 performance claim.
- Final scoped pre-commit checks passed (Ruff, Prettier, ESLint, AST and conflict/whitespace checks). Frappe Semgrep: 36 Python rules, zero findings. Initial lint formatting issues and missing API year annotation were corrected. Semgrep's default cache/settings writes were redirected to `/tmp`/version checks disabled to respect sandbox paths.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Useful Sports Academy landing summary | Desktop/phone fixture and screenshots | Passed |
| Native scope and confidentiality | Six unit tests plus native Guest/scoped read smoke | Passed |
| Reconciled subscription figures without new financial state | Existing Overview equality; rollback-only native smoke | Passed |
| Host navigation and lifecycle compatibility | Existing host contract inspection; browser fixture | Passed |

## Decisions, deviations and recovery

No data/schema changes, temporary accounts, scheduler changes, payments, invoices or emails. Native smoke always rolls back. Existing checkout work preserved. Session count includes Scheduled/Finalized sessions this calendar month, excludes Cancelled; upcoming list includes Scheduled dates from today, including today's sessions. Synthetic strings deliberately contain markup to verify escaped rendering.

## Remaining work and release impact

Development assets published, provider cache cleared and only the development web process reloaded. Release smoke passed: Sports Academy asset returned HTTPS 200 with exact JavaScript bytes, native scoped dashboard loaded, unauthenticated HTTP API denied (401/403). No production deployment, commit, PR, merge, Boost or Community source changes. Prior immutable landing asset remains available for rollback. Broader date/program filters, exports, attendance outcome reporting and production p95 acceptance remain outside this slice.
