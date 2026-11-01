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
