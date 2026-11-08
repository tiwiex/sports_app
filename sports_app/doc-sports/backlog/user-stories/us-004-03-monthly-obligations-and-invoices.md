# US-004-03: Generate monthly obligations and ERPNext invoices safely

## Header

- Epic: [EPIC-004](../epics/EPIC-004-scholarships-and-monthly-billing.md)
- State: In review
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
3. Given enabled automatic billing and an eligible Active enrollment, daily scheduling creates and submits one native invoice per month from the configured start, posting receivables, applying concessions and retaining native execution-user/workflow permissions; retries resume drafts without duplication and failures are visible.
4. Given a fully exempt period, when generated, then the zero-due obligation is recorded without a false receipt; positive obligations link to ERPNext invoices and partial failures can be safely resumed.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [EPIC-004 implementation](../../build-logs/2026-11-06-epic-004-scholarships-and-monthly-billing.md).
- Verification summary: Prototype slice verified by 213 Python checks, actual-source desktop/phone browser fixture and native development role/overlap/retry/rollback checks. Two independent database connections confirmed shared-lock serialization. No real charges or ledger posting persisted.
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

## Accepted implementation and remaining scope — 6 November 2026

User confirmed management approval/revocation, dedicated unassigned Sports Finance read/billing capability, month-start full-fee eligibility, unchanged NGN250,000 enrollment and configurable NGN40,000 monthly default. Native accounting/player access remains required. See [guide](../../billing-guide.md) and [build log](../../build-logs/2026-11-06-epic-004-scholarships-and-monthly-billing.md). This supersedes unresolved role/cadence/fee-conflict notes above only for this accepted prototype policy.

The central EPIC-004 console now supports restricted draft/approved/revoked decisions, explicit effective fee plans, final-amount-only previews, retry-safe draft invoice generation and zero-due obligations. Issued invoice snapshots are immutable; later scholarship/plan changes require reviewed correction rather than silent recalculation. Current membership status does not reconstruct historical suspension dates. Full policy scope for installments, grace/notice, refunds, scholarship admission exceptions and fulfillment of benefit entitlements remains unaccepted/unimplemented. Story is In review, with the verified slice recorded; do not mark the expanded epic Done on prototype evidence alone. No PR/merge is requested for this implementation turn.

## Accepted Item-pricing refinement — 7 November 2026

Enrollment charges are selected existing sales Items with quantity/rate rows in Academy Settings, driving public labels and native invoice lines. Monthly plans optionally reuse a one-month, company-currency Fixed Rate ERPNext Subscription Plan and its service Item/rate. Manual previews, immutable snapshots, scholarship privacy and native approval/payment controls remain in force. No native automatic Subscription is created. Migration preserves the current enrollment total; row edits affect new applications only. Verify arbitrary charge counts/quantities, unchanged retries, native Plan read permissions and stale-price rejection. This adjustment does not close unresolved EPIC-004 policy scope or change story review state.

[Build evidence](../../build-logs/2026-11-07-us-001-01-configurable-enrollment-items-and-subscription-pricing.md) · [Setup guide](../../academy-setup.md) · [Billing guide](../../billing-guide.md).

## Automatic monthly receivables — 7 November 2026

Explicit user direction supersedes the earlier manual/draft-only monthly policy: eligible Active enrollments are billed automatically each calendar month and positive charges are submitted to native ERPNext accounting, producing outstanding receivables. The first-day/full-fee eligibility rule and approved concessions remain unchanged; mid-month joiners begin the following month. No payment/receipt or bank clearance is inferred.

Academy Settings → Monthly fees now controls automatic submission, an explicit earliest billing month (first-day date) and the enabled System User that executes billing. A daily Sports scheduler processes the current month and retries missed months from that start date only, evaluated in academy timezone. Months before the start are not backfilled. Disabled monthly fees or automatic billing stops the job. Native Company/Player/Enrollment/accounting scope, invoice read/create/submit, workflow conditions and configured approver checks remain mandatory. No user roles are granted.

Deterministic enrollment/month keys, shared settings and enrollment locks, immutable snapshots and per-row rollback prevent duplicate obligations/invoices/ledger posting. Existing submitted invoices remain unchanged; legacy drafts resume under the same reference. Cancelled invoices require reviewed correction. Full concessions create zero obligations without invoices or receipts. Failures do not stop other rows: failed enrollment/month keys enter native Error Log and staff can inspect the Monthly billing preview. An unreadable or invalid execution user fails the native scheduled job; jobs and errors are visible in Desk Scheduled Job Type / Error Log.

The Sports-owned invoice workflow gains a conditional Submit monthly fee transition for existing invoice-approval roles, applicable only to a valid Sports monthly obligation without enrollment-application provenance. Ordinary invoices and enrollment payment review retain their existing paths. Custom third-party workflows are not rewritten; if no permitted synchronous submitted transition exists, the charge fails safely. No Boost code/global settings or native Subscription scheduler is changed. No automatic parent invoice/reminder email is introduced; normal installed native notification hooks retain their configured behavior.

Manual Preview and Generate and submit invoices remain available for authorized recovery, with the same posting behavior and native permissions. Source changes require a new preview for ungenerated charges. This adjustment does not complete installment/refund/grace/returning-player or automatic reminder policy scope.

[Adjustment evidence](../../build-logs/2026-11-07-us-004-03-automatic-monthly-receivables.md). State remains In review; financial automation is verified separately from expanded unresolved policy scope.

7 November: the [subscription payment grid](../../build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md) can generate and submit a missing eligible invoice and its independently confirmed receipt in one transactional cell action. Scheduled activation remains separate.

7 November refinement: [historical checkbox invoice generation and retained January test](../../build-logs/2026-11-07-us-004-03-january-test-and-checkbox-invoices.md) verified, plus [missing extension asset recovery](../../build-logs/2026-11-07-us-005-01-extension-asset-recovery.md). No whole-story Done assertion or production release.

## Completed-month automation and payment-only checkboxes — 7 November 2026

Explicit user correction supersedes the earlier month-start issuance, automation-start floor and checkbox invoice-generation interactions. **Submit monthly invoices automatically after their calendar month ends**, catching up from each currently Active enrollment's start date. Keep the approved full-fee eligibility at the first day of each billed month, dated fee-plan rates, concessions and native accounting mappings. A January-1 enrollment is eligible for January–October invoices on 7 November; November becomes eligible on 1 December. Midmonth joiners still begin with the following full month. Existing invoices/receipts remain authoritative and are not silently cancelled/repriced.

The Sports daily task now derives completed periods from each enrollment, so the deprecated global start-date value cannot hide historical obligations. Native settings retain that value for compatibility but hide its editor. Automation enablement and the enabled, deliberately selected execution User remain required, with native Company/read/create/submit/workflow/approver controls and no role grants. Enrollment, fee-plan and Academy Settings updates request a deduplicated catch-up after commit; the daily job provides ongoing month-boundary generation and failure retries. Install/migrate registers the Sports daily Scheduled Job Type. Opening a grid does not post accounting.

**Payments checkboxes mean receipt collection only.** Unpaid/partial cells are unchecked, paid cells are checked with a green background; unbilled/not-due/future/review/no-charge cells have no payable checkbox. Check the received months and Save payments, with explicit funds confirmation. The payment API refuses a missing or unsubmitted invoice and never creates its charge. The Generate invoices button is removed from Payments and the Generate and submit invoices button is removed from Monthly billing; that tab is a read-only status/exception view. Native accountant recovery services are not the ordinary workflow. The compact yearly grid keeps amounts/status in tooltips and invoice/receipt PDF links under a documents menu. Activate reversal selects permitted grid receipts, requires a reason and restores the native outstanding balance without deleting the charge.

The first corrected run registered the missing daily task and posted nine missing completed-month invoices for the retained January test enrollment. January–October now each have a submitted native invoice. No payment or email was created, and existing invoices/receipts were preserved, including an already-posted November test invoice from the earlier manual flow. New automatic runs exclude current/future months. Existing selected execution account, automation switch, saved fee plans and global scheduler configuration were not changed.

[Adjustment evidence](../../build-logs/2026-11-07-us-004-03-completed-month-automation-payment-only-grid.md). Existing review states remain; this does not mark expanded refund/reconciliation policies Done.
