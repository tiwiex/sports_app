# US-005-02: Show monthly payment status and source history

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: In progress
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
- Build log: [Subscription grid and correction slice](../../build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md).
- Verification summary: Development grid/overview and reasoned receipt cancellation verified against native invoice/receipt/ledger behavior and desktop/phone fixtures. See the dated slice below; broader credit/refund/reconciliation acceptance remains open.
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

## Subscription overview and checkbox payments — 7 November 2026

User requested the Community App Membership Admin Overview and Payments pattern for Sports subscriptions. Community source was inspected read-only; Sports owns its independent implementation with no Community runtime dependency or Boost source changes.

Sports → Scholarships & Billing opens an Overview with scoped enrollment/active counts and submitted annual/monthly billed, settled and outstanding totals. Settled includes allocations/credits and is explicitly not reported as cash receipts. Payments provides a paginated player/program-by-month grid, year and player-name filters, explicit unpaid/partial/paid/no-charge/unbilled/review/future/cancelled states, overdue indication and source invoice/receipt PDF modals. Financial status comes from native submitted invoices and outstanding amounts; no checkbox directly toggles accounting state. Fully exempt months do not produce false payments.

Authorized Finance selects up to 20 payable cells, an enabled same-company/currency Bank or Cash account, payment date and bank/cash reference, then explicitly confirms funds received. One action generates/submits an eligible missing monthly invoice if necessary and creates/submits a fully allocated Payment Entry for the remaining balance. Each cell has a separate Customer-attributed receipt, so reversal does not affect other months or players. Partial balances can be fully settled; arbitrary installment scheduling is not implemented. Native accounting, Company/Player permissions, workflow and configured approver checks remain mandatory. There are no new role grants or general finance bypasses.

A stable request key and payload hash return the same receipt on retries; changed retry inputs are rejected. Shared settings/enrollment/invoice locks serialize requests. Failure at receipt submission rolls back that cell's obligation, invoice and ledger as well as its receipt; successful independent cells are reported separately. Existing invoices retain original billing snapshots and already-paid cells are not collected again.

Activate reversal exposes selectors for submitted receipts created by this grid only. A reason, native receipt read/cancel and an allowed cancellation workflow are required. Cancellation reopens the invoice's native outstanding balance while retaining the charge and audit trail. Repeating cancellation is safe; retrying the old payment request after reversal returns Cancelled instead of creating a replacement. A new explicit confirmation may settle the reopened balance. Enrollment receipts, unrelated multi-invoice receipts, credit notes, bank reconciliations and actual cash refunds stay in their own reviewed native processes.

Automatic monthly invoice posting remains a separate implemented feature whose development activation still awaits an explicitly approved execution account. This manual checkbox collection interface does not enable it or assign Administrator. No real development balances were changed by QA; no production deployment, commit, PR or merge requested.

[Build evidence](../../build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md).

This is the verified grid/overview slice alongside the central player history. Broader unallocated-credit reporting and production reconciliation acceptance remain open; the full story is not Done.

## Completed-month automation and payment-only checkboxes — 7 November 2026

Explicit user correction supersedes the earlier month-start issuance, automation-start floor and checkbox invoice-generation interactions. **Submit monthly invoices automatically after their calendar month ends**, catching up from each currently Active enrollment's start date. Keep the approved full-fee eligibility at the first day of each billed month, dated fee-plan rates, concessions and native accounting mappings. A January-1 enrollment is eligible for January–October invoices on 7 November; November becomes eligible on 1 December. Midmonth joiners still begin with the following full month. Existing invoices/receipts remain authoritative and are not silently cancelled/repriced.

The Sports daily task now derives completed periods from each enrollment, so the deprecated global start-date value cannot hide historical obligations. Native settings retain that value for compatibility but hide its editor. Automation enablement and the enabled, deliberately selected execution User remain required, with native Company/read/create/submit/workflow/approver controls and no role grants. Enrollment, fee-plan and Academy Settings updates request a deduplicated catch-up after commit; the daily job provides ongoing month-boundary generation and failure retries. Install/migrate registers the Sports daily Scheduled Job Type. Opening a grid does not post accounting.

**Payments checkboxes mean receipt collection only.** Unpaid/partial cells are unchecked, paid cells are checked with a green background; unbilled/not-due/future/review/no-charge cells have no payable checkbox. Check the received months and Save payments, with explicit funds confirmation. The payment API refuses a missing or unsubmitted invoice and never creates its charge. The Generate invoices button is removed from Payments and the Generate and submit invoices button is removed from Monthly billing; that tab is a read-only status/exception view. Native accountant recovery services are not the ordinary workflow. The compact yearly grid keeps amounts/status in tooltips and invoice/receipt PDF links under a documents menu. Activate reversal selects permitted grid receipts, requires a reason and restores the native outstanding balance without deleting the charge.

The first corrected run registered the missing daily task and posted nine missing completed-month invoices for the retained January test enrollment. January–October now each have a submitted native invoice. No payment or email was created, and existing invoices/receipts were preserved, including an already-posted November test invoice from the earlier manual flow. New automatic runs exclude current/future months. Existing selected execution account, automation switch, saved fee plans and global scheduler configuration were not changed.

[Adjustment evidence](../../build-logs/2026-11-07-us-004-03-completed-month-automation-payment-only-grid.md). Existing review states remain; this does not mark expanded refund/reconciliation policies Done.


## Payments summary cards — 7 November 2026

SPORTS-FR-011 / SPORTS-FR-012 / SPORTS-FR-023, US-005-02: Payments also displays the Overview's Program enrollments, Active enrollments, Billed this year and Outstanding cards above the payment controls. The same permission-scoped Overview API supplies selected-year totals across all visible enrollments, independently of grid pagination/player search; this scope is stated beside the cards. Refresh, year changes and completed payment/reversal actions reload totals. Enrollment counts retain the Overview's current enrollment semantics. No billing/payment, permission or schema change.

[Build evidence](../../build-logs/2026-11-07-us-005-02-payment-summary-cards.md).


## Summary card colours — 7 November 2026

US-005-02 / SPORTS-FR-011, SPORTS-FR-012, SPORTS-FR-023: Overview and Payments share coloured summary cards: blue enrollments, teal active enrollments, green billed amounts, red positive outstanding balances and green cleared balances. Soft matching backgrounds, accent borders and bold values follow the Community App visual direction; text labels retain meaning independently of colour. This is a visual refinement with unchanged financial totals and scope. [Build evidence](../../build-logs/2026-11-07-us-005-02-summary-card-colours.md).
