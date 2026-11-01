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
