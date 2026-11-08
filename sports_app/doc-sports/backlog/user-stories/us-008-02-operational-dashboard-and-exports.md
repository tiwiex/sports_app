# US-008-02: Provide authorized academy dashboards and exports

## Header

- Epic: [EPIC-008](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** academy manager, **I want** to review registration, collections and attendance summaries **so that** operational exceptions are visible from the shared console.

## Traceability

- Requirements: `SPORTS-FR-023`, `SPORTS-NFR-002`, `SPORTS-NFR-005`
- Dependencies: [US-005-02](../../backlog/user-stories/us-005-02-monthly-status-and-history.md), [US-006-03](../../backlog/user-stories/us-006-03-attendance-history-and-summary.md), [US-002-02](../../backlog/user-stories/us-002-02-sports-console-provider.md)
- Planned branch: `story/us-008-02-operational-dashboard-and-exports`
- Planned build log: `YYYY-MM-DD-us-008-02-operational-dashboard-and-exports.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given an authorized role, when filtering academy, program and dates, then player counts, billed/collected/outstanding amounts and attendance totals reconcile to drill-through rows.
2. Given registrar, coach, cashier and management roles, when viewing or exporting, then allowed fields and scope are enforced server-side; scholarship detail is management-only and biometric identifiers are omitted.
3. Given agreed pilot volumes, when paging histories and opening dashboard/profile views, then measured p95 timings meet agreed targets or unresolved performance work blocks release.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: Not started.
- Verification summary: Not implemented or verified.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q01-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-01), [BA-QNR-001-Q01-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-02), [BA-QNR-001-Q01-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-05), [BA-QNR-001-Q04-14](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-14), [BA-QNR-001-Q06-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-01), [BA-QNR-001-Q06-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-04), [BA-QNR-001-Q06-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-05), [BA-QNR-001-Q08-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-04), [BA-QNR-001-Q10-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-02), [BA-QNR-001-Q10-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-03).
- Impact: Confirmed / expanded.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q01-01: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q01-02: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q01-05: Role-authorized downloadable reports for manual external sharing; no automatic external disclosure.
  - BA-QNR-001-Q04-14: Monthly income/outstanding balances and attendance reports; performance reports depend on new performance metrics, not financial inference.
  - BA-QNR-001-Q06-01: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q06-04: Monthly income/outstanding balances and attendance reports; performance reports depend on new performance metrics, not financial inference.
  - BA-QNR-001-Q06-05: Role-authorized downloadable reports for manual external sharing; no automatic external disclosure.
  - BA-QNR-001-Q08-04: Role-authorized downloadable reports for manual external sharing; no automatic external disclosure.
  - BA-QNR-001-Q10-02: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q10-03: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).


## Sports Academy landing dashboard — 7 November 2026

SPORTS-FR-023 / SPORTS-NFR-002 / SPORTS-NFR-005, US-008-02: replace the Sports Academy introductory text with a read-only dashboard. Coloured cards show visible player counts, current Active program memberships, Pending applications and non-cancelled sessions in the academy's current month. The next five Scheduled sessions from today show title, date/time and venue with native record links. Active memberships are enrollment counts, not unique active players or reconstructed historical eligibility.

Authorized finance users also see selected-year monthly subscription Billed, Settled and Outstanding totals with a twelve-month billed/outstanding chart. Reuse the existing permission-scoped subscription Overview service: submitted monthly invoices only, not enrollment fees/all ERP revenue; Settled includes accounting credits and is not cash receipts. The year filter affects financial totals only. Operational counts remain current. Missing native permissions show Restricted, not zero; no scholarship, biometric or player contact data is included.

Role-scoped shortcuts use the existing host dashboard navigation to Players, Enrollments, Attendance, Scholarships & Billing and Academy Settings. Refresh, year changes and host data-change watchers update the dashboard, with loading, empty, restricted, retry and unmount protection. Desktop and phone layouts use the same coloured summary style. This delivers the landing-dashboard slice; broader date/program filters, exports, attendance outcome reporting and production p95 acceptance remain open. [Build evidence](../../build-logs/2026-11-07-us-008-02-academy-landing-dashboard.md).
