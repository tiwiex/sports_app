# US-005-01: Record player-attributed payments using ERPNext

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** cashier, **I want** to allocate receipts to the correct player invoice **so that** monthly collections are accurate and traceable.

## Traceability

- Requirements: `SPORTS-FR-011`, `SPORTS-NFR-003`
- Dependencies: [US-004-03](../../backlog/user-stories/us-004-03-monthly-obligations-and-invoices.md), [US-002-03](../../backlog/user-stories/us-002-03-console-login-and-finance-regression.md)
- Planned branch: `story/us-005-01-player-receipts-and-allocations`
- Planned build log: `YYYY-MM-DD-us-005-01-player-receipts-and-allocations.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given an authorized cashier and a player invoice, when recording and submitting payment, then the resulting ERPNext Payment Entry identifies the correct company, Customer, currency and allocation.
2. Given two players sharing a guardian Customer, when a receipt is allocated, then only the intended player obligation changes and unallocated credit is shown separately.
3. Given a repeated submit request or an existing draft, when resumed, then a second receipt is not created; failed submission leaves no false paid status.

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
