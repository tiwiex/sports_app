# US-008-03: Rehearse migration and validate production readiness

## Header

- Epic: [EPIC-008](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** implementation lead, **I want** to import verified opening data and complete a controlled pilot **so that** the academy can adopt the system with support evidence.

## Traceability

- Requirements: `SPORTS-FR-022`, `SPORTS-FR-024`, `SPORTS-FR-025`, `SPORTS-NFR-008`
- Dependencies: [US-001-02](../../backlog/user-stories/us-001-02-configurable-public-website.md), [US-002-03](../../backlog/user-stories/us-002-03-console-login-and-finance-regression.md), [US-005-03](../../backlog/user-stories/us-005-03-corrections-and-reconciliation.md), [US-006-03](../../backlog/user-stories/us-006-03-attendance-history-and-summary.md), [US-007-03](../../backlog/user-stories/us-007-03-device-replay-and-exception-review.md), [US-008-01](../../backlog/user-stories/us-008-01-erp-fit-gap-and-module-matrix.md), [US-008-02](../../backlog/user-stories/us-008-02-operational-dashboard-and-exports.md)
- Planned branch: `story/us-008-03-migration-pilot-and-production-readiness`
- Planned build log: `YYYY-MM-DD-us-008-03-migration-pilot-and-production-readiness.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given legacy roster, balances and attendance sources, when a dry run and rerun execute, then external IDs, rejected rows and opening totals reconcile; unverifiable history is labeled rather than fabricated.
2. Given all launch-required ERP modules and the selected biometric provider, when business owners run agreed scenarios, then configuration, permissions, accounting, manual/device attendance and end-to-end player journeys have signed evidence; any outstanding ERP delivery task blocks its module acceptance.
3. Given a backup and cutover rehearsal, when restore/replay and rollback steps are exercised, then identities and balances remain consistent and the release has trained operators, runbook, support owners, recovery targets and management sign-off.

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
