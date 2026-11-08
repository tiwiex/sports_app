# US-005-03: Reconcile credits, refunds and payment corrections

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: In progress
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** finance manager, **I want** to correct transactions through approved ERPNext paths **so that** player history stays consistent with the ledger.

## Traceability

- Requirements: `SPORTS-FR-013`, `SPORTS-NFR-004`
- Dependencies: [US-005-02](../../backlog/user-stories/us-005-02-monthly-status-and-history.md)
- Planned branch: `story/us-005-03-corrections-and-reconciliation`
- Planned build log: `YYYY-MM-DD-us-005-03-corrections-and-reconciliation.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a cancelled receipt, return or credit note, when an authorized correction completes, then affected obligations and player balances recompute from submitted source documents.
2. Given an attempted correction by an unauthorized cashier, when called directly, then financial approval/permission rules deny the action.
3. Given a reconciliation run, when comparing obligations, invoices and allocations, then mismatches are reported by source reference, correction actors are auditable and no duplicate Sports ledger is introduced.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Subscription grid and correction slice](../../build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md).
- Verification summary: Development grid/overview and reasoned receipt cancellation verified against native invoice/receipt/ledger behavior and desktop/phone fixtures. See the dated slice below; broader credit/refund/reconciliation acceptance remains open.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q04-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-06), [BA-QNR-001-Q04-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-07), [BA-QNR-001-Q04-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-09).
- Impact: Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q04-06: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-07: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-09: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-005-payments-and-financial-history.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Subscription overview and checkbox payments — 7 November 2026

User requested the Community App Membership Admin Overview and Payments pattern for Sports subscriptions. Community source was inspected read-only; Sports owns its independent implementation with no Community runtime dependency or Boost source changes.

Sports → Scholarships & Billing opens an Overview with scoped enrollment/active counts and submitted annual/monthly billed, settled and outstanding totals. Settled includes allocations/credits and is explicitly not reported as cash receipts. Payments provides a paginated player/program-by-month grid, year and player-name filters, explicit unpaid/partial/paid/no-charge/unbilled/review/future/cancelled states, overdue indication and source invoice/receipt PDF modals. Financial status comes from native submitted invoices and outstanding amounts; no checkbox directly toggles accounting state. Fully exempt months do not produce false payments.

Authorized Finance selects up to 20 payable cells, an enabled same-company/currency Bank or Cash account, payment date and bank/cash reference, then explicitly confirms funds received. One action generates/submits an eligible missing monthly invoice if necessary and creates/submits a fully allocated Payment Entry for the remaining balance. Each cell has a separate Customer-attributed receipt, so reversal does not affect other months or players. Partial balances can be fully settled; arbitrary installment scheduling is not implemented. Native accounting, Company/Player permissions, workflow and configured approver checks remain mandatory. There are no new role grants or general finance bypasses.

A stable request key and payload hash return the same receipt on retries; changed retry inputs are rejected. Shared settings/enrollment/invoice locks serialize requests. Failure at receipt submission rolls back that cell's obligation, invoice and ledger as well as its receipt; successful independent cells are reported separately. Existing invoices retain original billing snapshots and already-paid cells are not collected again.

Activate reversal exposes selectors for submitted receipts created by this grid only. A reason, native receipt read/cancel and an allowed cancellation workflow are required. Cancellation reopens the invoice's native outstanding balance while retaining the charge and audit trail. Repeating cancellation is safe; retrying the old payment request after reversal returns Cancelled instead of creating a replacement. A new explicit confirmation may settle the reopened balance. Enrollment receipts, unrelated multi-invoice receipts, credit notes, bank reconciliations and actual cash refunds stay in their own reviewed native processes.

Automatic monthly invoice posting remains a separate implemented feature whose development activation still awaits an explicitly approved execution account. This manual checkbox collection interface does not enable it or assign Administrator. No real development balances were changed by QA; no production deployment, commit, PR or merge requested.

[Build evidence](../../build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md).

This is a verified receipt-cancellation slice. Credit notes, refunds, reconciliation reports and production correction acceptance remain open; the full story is not Done.
