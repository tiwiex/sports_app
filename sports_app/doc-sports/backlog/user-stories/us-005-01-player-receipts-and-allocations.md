# US-005-01: Record player-attributed payments using ERPNext

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: In review
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

## Payment review email adjustment — 3 November 2026

- Sports Academy Settings and its console expose Payment review email addresses as comma-separated text. Invalid addresses are rejected; duplicates and surrounding spaces are normalized. Blank disables this notification.
- The first website payment claim queues a review email linked to its Sales Invoice (or legacy Payment Entry) in the same transaction as Pending Review. No duplicate on retries and no mail after rollback. Applicant claims remain unposted.
- The email asks staff to verify the bank credit; receiving it grants no read, approval or posting permissions.
- [Build evidence and release notes](../../build-logs/2026-11-03-us-005-01-payment-review-emails.md). Wider billing/reconciliation scope remains open.

## Administrator payment review diagnosis — 3 November 2026

[Read-only diagnosis](../../build-logs/2026-11-03-us-005-01-administrator-payment-review-diagnosis.md): the pending invoice remains unposted; Administrator lacks explicit invoice approver configuration, while the configured Finance reviewer is eligible. Additional Administrator approval access awaits the user's decision; no payment was completed during investigation.

## Administrator approval enabled — 3 November 2026

Following explicit user approval, Administrator is now an additional Sales Invoice approver on Moyours. Completion eligibility for ACC-SINV-2026-00003 was verified without posting payment; the existing Finance reviewer remains enabled. [Applied configuration and preservation checks](../../build-logs/2026-11-03-us-005-01-administrator-approver-enabled.md). This supersedes the pending decision recorded in the earlier diagnosis.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q02-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-01), [BA-QNR-001-Q02-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-09), [BA-QNR-001-Q04-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-01), [BA-QNR-001-Q04-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-02), [BA-QNR-001-Q04-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-03), [BA-QNR-001-Q04-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-04).
- Impact: Confirmed / needs clarification; Conflicting / needs clarification; Expanded.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q02-01: Online and staff intake; payment confirms admission subject to approved scholarship/part-payment exceptions. No automatic bank clearance from a claim.
  - BA-QNR-001-Q02-09: Online and staff intake; payment confirms admission subject to approved scholarship/part-payment exceptions. No automatic bank clearance from a claim.
  - BA-QNR-001-Q04-01: Source mentions 150k/220k including 30k kit and 40k subscription; PoC uses 220k registration +30k kit =250k excluding monthly40k. Obtain approved itemized fee schedule before changes.
  - BA-QNR-001-Q04-02: Bank transfer and downloadable receipts; admin confirms payment. Map authorized admins to existing approver controls, not general admin finance access.
  - BA-QNR-001-Q04-03: Bank transfer and downloadable receipts; admin confirms payment. Map authorized admins to existing approver controls, not general admin finance access.
  - BA-QNR-001-Q04-04: Bank transfer and downloadable receipts; admin confirms payment. Map authorized admins to existing approver controls, not general admin finance access.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-005-payments-and-financial-history.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Combined admission/payment refinement — 6 November 2026

An authorized reviewer may now accept a pending application and complete its linked Pending Review invoice/allocated receipt in one atomic operation. The existing standalone Finance action remains available. Draft/unclaimed invoices remain unposted. Native finance rights and configured Boost approvals still apply. This supersedes the mandatory two-step admission/finance sequence. [Acceptance criteria](us-003-01-application-intake-and-review.md#accepted-enrollment-refinement--6-november-2026); [build evidence](../../build-logs/2026-11-06-us-003-01-enrollment-image-and-invoice-acceptance.md).

## Accepted PDF/manual-delivery refinement — 7 November 2026

Invoice/receipt links open clearly styled native PDFs. Add elapsed-time columns using finance creation/application submission timestamps. The operator-confirmed Email receipt action is restricted to posted positive Receive receipts and native read/print/email plus scoped player/Company/Customer access. Preserve source records, zero financial posting and duplicate-safe queued delivery. This is subsequent user direction supplementing BA-QNR-001-Q04-12. Automatic reminders, schedules, WhatsApp and broader delivery acceptance are not complete.

[Build evidence](../../build-logs/2026-11-07-us-003-03-pdf-receipts-email-and-elapsed-time.md) · [Operator guide](../../players-guide.md).

## Main-table PDF refinement — 7 November 2026

Main Players/Enrollments expose permission-scoped document links/actions and elapsed age. PDF links open a modal with download fallback and use selectable Sports Academy Invoice / Sports Academy Receipt backend Print Formats. The Settings document logo is configurable; Moyours reuses its website crest. Native Company/Customer/document permissions and deliberate receipt-email confirmation remain authoritative. Do not change global print defaults or broader story acceptance state.

[Build evidence](../../build-logs/2026-11-07-us-003-03-main-table-finance-and-branded-pdf-modal.md) · [Operator guide](../../players-guide.md).

## Subscription overview and checkbox payments — 7 November 2026

User requested the Community App Membership Admin Overview and Payments pattern for Sports subscriptions. Community source was inspected read-only; Sports owns its independent implementation with no Community runtime dependency or Boost source changes.

Sports → Scholarships & Billing opens an Overview with scoped enrollment/active counts and submitted annual/monthly billed, settled and outstanding totals. Settled includes allocations/credits and is explicitly not reported as cash receipts. Payments provides a paginated player/program-by-month grid, year and player-name filters, explicit unpaid/partial/paid/no-charge/unbilled/review/future/cancelled states, overdue indication and source invoice/receipt PDF modals. Financial status comes from native submitted invoices and outstanding amounts; no checkbox directly toggles accounting state. Fully exempt months do not produce false payments.

Authorized Finance selects up to 20 payable cells, an enabled same-company/currency Bank or Cash account, payment date and bank/cash reference, then explicitly confirms funds received. One action generates/submits an eligible missing monthly invoice if necessary and creates/submits a fully allocated Payment Entry for the remaining balance. Each cell has a separate Customer-attributed receipt, so reversal does not affect other months or players. Partial balances can be fully settled; arbitrary installment scheduling is not implemented. Native accounting, Company/Player permissions, workflow and configured approver checks remain mandatory. There are no new role grants or general finance bypasses.

A stable request key and payload hash return the same receipt on retries; changed retry inputs are rejected. Shared settings/enrollment/invoice locks serialize requests. Failure at receipt submission rolls back that cell's obligation, invoice and ledger as well as its receipt; successful independent cells are reported separately. Existing invoices retain original billing snapshots and already-paid cells are not collected again.

Activate reversal exposes selectors for submitted receipts created by this grid only. A reason, native receipt read/cancel and an allowed cancellation workflow are required. Cancellation reopens the invoice's native outstanding balance while retaining the charge and audit trail. Repeating cancellation is safe; retrying the old payment request after reversal returns Cancelled instead of creating a replacement. A new explicit confirmation may settle the reopened balance. Enrollment receipts, unrelated multi-invoice receipts, credit notes, bank reconciliations and actual cash refunds stay in their own reviewed native processes.

Automatic monthly invoice posting remains a separate implemented feature whose development activation still awaits an explicitly approved execution account. This manual checkbox collection interface does not enable it or assign Administrator. No real development balances were changed by QA; no production deployment, commit, PR or merge requested.

[Build evidence](../../build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md).

7 November refinement: [historical checkbox invoice generation and retained January test](../../build-logs/2026-11-07-us-004-03-january-test-and-checkbox-invoices.md) verified, plus [missing extension asset recovery](../../build-logs/2026-11-07-us-005-01-extension-asset-recovery.md). No whole-story Done assertion or production release.

## Completed-month automation and payment-only checkboxes — 7 November 2026

Explicit user correction supersedes the earlier month-start issuance, automation-start floor and checkbox invoice-generation interactions. **Submit monthly invoices automatically after their calendar month ends**, catching up from each currently Active enrollment's start date. Keep the approved full-fee eligibility at the first day of each billed month, dated fee-plan rates, concessions and native accounting mappings. A January-1 enrollment is eligible for January–October invoices on 7 November; November becomes eligible on 1 December. Midmonth joiners still begin with the following full month. Existing invoices/receipts remain authoritative and are not silently cancelled/repriced.

The Sports daily task now derives completed periods from each enrollment, so the deprecated global start-date value cannot hide historical obligations. Native settings retain that value for compatibility but hide its editor. Automation enablement and the enabled, deliberately selected execution User remain required, with native Company/read/create/submit/workflow/approver controls and no role grants. Enrollment, fee-plan and Academy Settings updates request a deduplicated catch-up after commit; the daily job provides ongoing month-boundary generation and failure retries. Install/migrate registers the Sports daily Scheduled Job Type. Opening a grid does not post accounting.

**Payments checkboxes mean receipt collection only.** Unpaid/partial cells are unchecked, paid cells are checked with a green background; unbilled/not-due/future/review/no-charge cells have no payable checkbox. Check the received months and Save payments, with explicit funds confirmation. The payment API refuses a missing or unsubmitted invoice and never creates its charge. The Generate invoices button is removed from Payments and the Generate and submit invoices button is removed from Monthly billing; that tab is a read-only status/exception view. Native accountant recovery services are not the ordinary workflow. The compact yearly grid keeps amounts/status in tooltips and invoice/receipt PDF links under a documents menu. Activate reversal selects permitted grid receipts, requires a reason and restores the native outstanding balance without deleting the charge.

The first corrected run registered the missing daily task and posted nine missing completed-month invoices for the retained January test enrollment. January–October now each have a submitted native invoice. No payment or email was created, and existing invoices/receipts were preserved, including an already-posted November test invoice from the earlier manual flow. New automatic runs exclude current/future months. Existing selected execution account, automation switch, saved fee plans and global scheduler configuration were not changed.

[Adjustment evidence](../../build-logs/2026-11-07-us-004-03-completed-month-automation-payment-only-grid.md). Existing review states remain; this does not mark expanded refund/reconciliation policies Done.
