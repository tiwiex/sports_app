# US-005-02: Show monthly payment status and source history

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** finance operator, **I want** to review period balances and receipts from the player record **so that** arrears and completed payments are clear.

## Traceability

- Requirements: `SPORTS-FR-012`
- Dependencies: [US-005-01](../../backlog/user-stories/us-005-01-player-receipts-and-allocations.md), [US-003-03](../../backlog/user-stories/us-003-03-central-player-profile.md)
- Planned branch: `story/us-005-02-monthly-status-and-history`
- Planned build log: `YYYY-MM-DD-us-005-02-monthly-status-and-history.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given unpaid, partial, paid, exempt, unbilled and overdue examples, when history is loaded, then each state follows PRD rules and overdue preserves the partial-payment amount.
2. Given submitted allocations, cancelled documents and unallocated credits, when totals are calculated, then only valid allocated amounts settle obligations and totals reconcile to source documents.
3. Given an authorized user and a date/period filter, when drilling into a row, then invoice/receipt dates, references and correction links are visible without disclosing scholarship decisions.

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
- Source references: [BA-QNR-001-Q01-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-01), [BA-QNR-001-Q01-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-02), [BA-QNR-001-Q04-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-06), [BA-QNR-001-Q04-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-07), [BA-QNR-001-Q04-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-09), [BA-QNR-001-Q04-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-13), [BA-QNR-001-Q06-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-01), [BA-QNR-001-Q10-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-02), [BA-QNR-001-Q10-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-03).
- Impact: Changed; Confirmed / expanded; Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q01-01: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q01-02: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q04-06: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-07: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-09: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-13: No automatic unpaid-fee suspension; misconduct suspension/dismissal is reviewed. Display arrears without automatic exclusion; preserve any manual disciplinary audit.
  - BA-QNR-001-Q06-01: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q10-02: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q10-03: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-005-payments-and-financial-history.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
