# US-005-01: Record player-attributed payments using ERPNext

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: In progress — invoice-first enrollment PoC
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
2. Given two players with separate automatically created Customers, when a receipt is allocated, then only the intended player obligation changes and unallocated credit is shown separately.
3. Given a repeated submit request or an existing draft, when resumed, then a second receipt is not created; failed submission leaves no false paid status.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Enrollment payment review](../../build-logs/2026-11-01-us-005-01-enrollment-payment-review.md).
- Verification summary: Current invoice-first PoC verifies draft invoice creation, unposted claims, one-click Finance submission/allocation, retry safety, failure rollback and UI/privacy controls. Earlier receipt-first evidence is historical. Full monthly billing and production reconciliation remain open.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

Earlier refinement (historical): [multi-step enrollment and draft Payment Entry review](../../build-logs/2026-11-01-us-005-01-enrollment-payment-review.md). This supersedes the previous no-payment PoC boundary; finance submission, invoice allocation and production acceptance remain separate.

## Invoice-first adjustment — 1 November 2026

New registrations create a draft Sales Invoice at Make Payment and move that invoice to Pending Review when payment is claimed. Finance verifies the bank credit and uses one Complete Payment action to submit the invoice and one fully allocated receipt atomically, with retry protection. No Payment Entry form is required. Both applicant steps remain unposted; partial failures leave no paid status. Legacy receipt-first references remain supported. [Implementation, tests and cleanup](../../build-logs/2026-11-01-us-005-01-invoice-first-payment-completion.md). The older payment-entry-first refinement above is historical. Full monthly billing, corrections and production reconciliation remain open.

## Invoice context payment confirmation — 1 November 2026

Authorised Finance users can use Confirm Payment directly from an enrollment invoice context menu while it is Pending Review. The shortcut disappears after settlement; View retains Complete Payment. Both use the same server-controlled workflow and atomic receipt service. [Build evidence](../../build-logs/2026-11-01-us-005-01-invoice-context-confirm-payment.md).

## Local commit review — 2 November 2026

[Repository scope, current checks and release boundaries](../../build-logs/2026-11-02-us-005-01-project-commit-review.md). Local commit capture does not close the remaining production scope.

## Develop integration — 2 November 2026

[Authorised merges, post-merge checks and push record](../../build-logs/2026-11-02-us-005-01-develop-integration.md).
