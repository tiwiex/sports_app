# US-004-03: Generate monthly obligations and ERPNext invoices safely

## Header

- Epic: [EPIC-004](../epics/EPIC-004-scholarships-and-monthly-billing.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** finance operator, **I want** to preview and generate period charges **so that** every eligible player has one auditable monthly obligation.

## Traceability

- Requirements: `SPORTS-FR-010`, `SPORTS-NFR-003`
- Dependencies: [US-004-02](../../backlog/user-stories/us-004-02-fee-plans-and-policy.md), [US-003-02](../../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md)
- Planned branch: `story/us-004-03-monthly-obligations-and-invoices`
- Planned build log: `YYYY-MM-DD-us-004-03-monthly-obligations-and-invoices.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a roster and month, when previewed, then eligible players, amounts, due dates, exemptions and exceptions are shown with validated accounting mappings.
2. Given repeated or concurrent billing runs for the same player/enrollment/period/charge key, when committed or retried after failure, then one obligation and at most one active invoice are produced per key.
3. Given a fully exempt period, when generated, then the zero-due obligation is recorded without a false receipt; positive obligations link to ERPNext invoices and partial failures can be safely resumed.

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
- Source references: [BA-QNR-001-Q04-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-10).
- Impact: Needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q04-10: Yes answers multiple billing options; confirm monthly schedule, invoice timing, proration and arrears policy before automation.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-004-scholarships-and-monthly-billing.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
