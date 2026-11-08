# Scholarships and monthly billing

Open **Sports → Scholarships & Billing** in the shared console. This view is contributed by Sports App; Boost remains generic.

## Access

Academy administrators (Sports Academy Administrator or System Manager, and Administrator) can configure fee plans and create/approve/revoke decisions. **Sports Finance** is a dedicated, initially unassigned role for restricted decision reads and billing. Coaches/registrars without that role have no access to scholarship lists, reasons, benefits or decisions, including through sharing. Finance cannot approve or revoke decisions.

The capability does not grant ERPNext accounting rights or unrestricted player access. Operators must also hold the appropriate existing native Company, Player, Enrollment, Customer, Item, Account and Cost Center read permissions; generation/submission additionally requires native Sales Invoice read/create/submit and configured workflow approval rights. An existing console-access role (Sports Console or Sports Registrar) is also needed; this release retains the host’s existing page roles. Assign roles deliberately to the chosen finance operator. No new role is assigned automatically.

## Configure a fee plan first

In **Fee plans → New fee plan**, select the program, monthly amount, company currency, effective month, due day (1–28), non-stock sales service item, income ledger and cost center. Monthly default is NGN40,000 on the current Moyours configuration; other academies use their own currency/settings and editable plan amount. No enabled plan, account mapping, item or due day is silently seeded. This implementation requires company accounting currency, rather than automatic FX conversion.

Select **Full fee if active at month start**. Plans start on the first day of a month; an optional end is the final day of a month. Enabled plans for a program cannot overlap. To change a future fee, close the existing plan at a month end and create the next plan. Editing a plan cannot rewrite a generated invoice. The Academy Settings **Monthly fees enabled** switch controls whether generation is allowed.

## Record and review scholarship decisions

Use **Scholarship decisions → New scholarship decision**. Select the program enrollment, effective dates, monthly fee coverage (Full, Percentage or Fixed amount) and a confidential reason. Fixed amounts use company currency. Record kit, trip, trial and tournament benefits separately; recording these benefits does not issue stock or pay for a trip. The record starts as Draft.

Open its reference menu to **View**, **Approve** or **Revoke**. Approval records the management actor/time, and overlapping approved decisions for an enrollment are rejected. Approved decisions cannot be overwritten. Revocation requires a reason and records actor/time; it retains the original record. An optional end date is explicit; no automatic expiry/review interval or payment-free enrollment admission is invented.

Changes affect ungenerated charges only. Submitted or draft issued invoices are not silently recalculated. Corrections require Finance review using native cancellation/credit-note procedures and explicit reconciliation; generation will not create a replacement behind a cancelled/deleted invoice reference. Supporting-file attachments to scholarship decisions are disabled in this slice; do not put scholarship reasons into broadly visible player fields or invoice remarks.

## Automatic monthly invoices

Invoices are submitted automatically for **completed calendar months**. An eligible Active January-1 enrollment has January–October invoices by 7 November; November is billed on 1 December. The established month-start eligibility rule still applies: mid-month joiners start with the following month. Current Pending/Withdrawn/Completed memberships are not billed; historical suspension/reactivation history is not reconstructed.

Enable automatic billing and select an enabled execution User in Academy Settings. Native Company/player/accounting/workflow permissions apply. A Sports daily job catches up from enrollment dates, applies the period's effective fee plan and approved concession, and retries failures. Enrollment, plan and settings saves also request catch-up after commit. There is no per-month Generate step. The old global start-date floor is superseded and hidden. Configured start dates/rates cannot silently rewrite an existing invoice.

Monthly billing is a read-only status and exception view. Resolve missing/incomplete/overlapping plans, disabled mappings and mid-month scholarship exceptions; automatic processing will retry. Full coverage records zero due without an invoice or receipt. Existing posted and cancelled references retain their history; cancellation requires reviewed correction, never automatic replacement.

## Record subscription payments

Open **Payments**, choose the year and optionally filter by player. Each row is a program enrollment. Unchecked boxes represent posted unpaid/partial invoices; checked green boxes represent settled invoices. A dash indicates no payable charge (for example current/future/ineligible months); pending/review indicators have explanatory tooltips. Use the **⋯** documents menu for source invoice/receipt PDFs. Checkbox selection itself writes nothing.

Choose the receiving Bank/Cash account if none is configured, verify the payment date and optionally enter the bank/cash reference. The saved receiving ledger is preselected only if valid and permitted. Check up to 20 received months, click **Save payments** and explicitly confirm funds received. Native submitted receipts settle the remaining balances. A blank reference receives a stable generated identifier. The action never creates an invoice; unbilled or draft charges must first complete automatic processing. No bank clearance is inferred.

Activate reversal enables receipt selection on applicable paid cells. Enter a reason and use Reverse selected; native cancellation rights/workflow are required. It cancels only grid receipts, reopens the invoice balance and retains the charge/audit trail. A new deliberate payment confirmation may settle it again. Existing receipts that allocate multiple unrelated invoices, enrollment payments, cash refunds and credit notes stay in their own native review paths.

## Current release boundary

Existing Moyours enrollment charges migrate to NGN250,000. Future enrollment prices come from the configurable Enrollment charges table; the monthly subscription is separate. Installment schedules, grace/notice periods, refunds, automatic arrears penalties, scholarship admission exceptions, mid-period concession proration and stock-benefit fulfillment still need explicit policy/refinement. This does not change attendance eligibility automatically.

[EPIC-004](backlog/epics/EPIC-004-scholarships-and-monthly-billing.md) · [Build evidence](build-logs/2026-11-06-epic-004-scholarships-and-monthly-billing.md).

## Reuse ERPNext Subscription Plan pricing

In **Fee plans → New fee plan**, optionally select **ERPNext Subscription Plan**. Use an existing one-month Fixed Rate plan in the company currency with an enabled non-stock sales Item. The dialog fills its Item and amount; the server always uses that plan’s current values when saving or previewing, regardless of manually edited overrides. Operators need native Subscription Plan and Item read access; this feature grants neither.

The fee-plan list reflects values captured when the Sports plan was last saved. **Monthly billing → Preview** resolves the current native price. A native plan change invalidates an ungenerated preview; reload it before generation. Existing invoices and obligations are never recalculated. Without a linked Subscription Plan, the selected service Item and manual monthly rate continue to apply.

This reuses ERPNext pricing without creating native Subscription records or a competing native Subscription schedule. Sports runs the monthly schedule and applies scholarship controls; proration and automatic parent emails remain outside this slice. The public website’s monthly amount is information only, configured separately. [Adjustment evidence](build-logs/2026-11-07-us-001-01-configurable-enrollment-items-and-subscription-pricing.md).

## Automatic monthly receivables — 7 November 2026

Explicit user direction supersedes the earlier manual/draft-only monthly policy: eligible Active enrollments are billed automatically each calendar month and positive charges are submitted to native ERPNext accounting, producing outstanding receivables. The first-day/full-fee eligibility rule and approved concessions remain unchanged; mid-month joiners begin the following month. No payment/receipt or bank clearance is inferred.

Academy Settings → Monthly fees now controls automatic submission, an explicit earliest billing month (first-day date) and the enabled System User that executes billing. A daily Sports scheduler processes the current month and retries missed months from that start date only, evaluated in academy timezone. Months before the start are not backfilled. Disabled monthly fees or automatic billing stops the job. Native Company/Player/Enrollment/accounting scope, invoice read/create/submit, workflow conditions and configured approver checks remain mandatory. No user roles are granted.

Deterministic enrollment/month keys, shared settings and enrollment locks, immutable snapshots and per-row rollback prevent duplicate obligations/invoices/ledger posting. Existing submitted invoices remain unchanged; legacy drafts resume under the same reference. Cancelled invoices require reviewed correction. Full concessions create zero obligations without invoices or receipts. Failures do not stop other rows: failed enrollment/month keys enter native Error Log and staff can inspect the Monthly billing preview. An unreadable or invalid execution user fails the native scheduled job; jobs and errors are visible in Desk Scheduled Job Type / Error Log.

The Sports-owned invoice workflow gains a conditional Submit monthly fee transition for existing invoice-approval roles, applicable only to a valid Sports monthly obligation without enrollment-application provenance. Ordinary invoices and enrollment payment review retain their existing paths. Custom third-party workflows are not rewritten; if no permitted synchronous submitted transition exists, the charge fails safely. No Boost code/global settings or native Subscription scheduler is changed. No automatic parent invoice/reminder email is introduced; normal installed native notification hooks retain their configured behavior.

Manual Preview and Generate and submit invoices remain available for authorized recovery, with the same posting behavior and native permissions. Source changes require a new preview for ungenerated charges. This adjustment does not complete installment/refund/grace/returning-player or automatic reminder policy scope.

[Automatic monthly receivables](build-logs/2026-11-07-us-004-03-automatic-monthly-receivables.md).

## Subscription overview and checkbox payments — 7 November 2026

User requested the Community App Membership Admin Overview and Payments pattern for Sports subscriptions. Community source was inspected read-only; Sports owns its independent implementation with no Community runtime dependency or Boost source changes.

Sports → Scholarships & Billing opens an Overview with scoped enrollment/active counts and submitted annual/monthly billed, settled and outstanding totals. Settled includes allocations/credits and is explicitly not reported as cash receipts. Payments provides a paginated player/program-by-month grid, year and player-name filters, explicit unpaid/partial/paid/no-charge/unbilled/review/future/cancelled states, overdue indication and source invoice/receipt PDF modals. Financial status comes from native submitted invoices and outstanding amounts; no checkbox directly toggles accounting state. Fully exempt months do not produce false payments.

Authorized Finance selects up to 20 payable cells, an enabled same-company/currency Bank or Cash account, payment date and bank/cash reference, then explicitly confirms funds received. One action generates/submits an eligible missing monthly invoice if necessary and creates/submits a fully allocated Payment Entry for the remaining balance. Each cell has a separate Customer-attributed receipt, so reversal does not affect other months or players. Partial balances can be fully settled; arbitrary installment scheduling is not implemented. Native accounting, Company/Player permissions, workflow and configured approver checks remain mandatory. There are no new role grants or general finance bypasses.

A stable request key and payload hash return the same receipt on retries; changed retry inputs are rejected. Shared settings/enrollment/invoice locks serialize requests. Failure at receipt submission rolls back that cell's obligation, invoice and ledger as well as its receipt; successful independent cells are reported separately. Existing invoices retain original billing snapshots and already-paid cells are not collected again.

Activate reversal exposes selectors for submitted receipts created by this grid only. A reason, native receipt read/cancel and an allowed cancellation workflow are required. Cancellation reopens the invoice's native outstanding balance while retaining the charge and audit trail. Repeating cancellation is safe; retrying the old payment request after reversal returns Cancelled instead of creating a replacement. A new explicit confirmation may settle the reopened balance. Enrollment receipts, unrelated multi-invoice receipts, credit notes, bank reconciliations and actual cash refunds stay in their own reviewed native processes.

Automatic monthly invoice posting remains a separate implemented feature whose development activation still awaits an explicitly approved execution account. This manual checkbox collection interface does not enable it or assign Administrator. No real development balances were changed by QA; no production deployment, commit, PR or merge requested.

[Build evidence](build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md).

## Checkbox invoice-only and delivery refinement — 7 November 2026

Payments month checkboxes now support **Generate invoices** (receivables only, including historical eligible months) separately from **Save payments** (confirmed receipt collection). Invoice-only generation does not require bank details or post a receipt. Future months are rejected here. Payment references are optional and generated deterministically if blank; a configured receiving ledger is preselected only when permitted/valid. Billing exceptions show their reason. This supersedes the earlier mandatory-reference UI requirement; native finance controls and effective fee-plan snapshots remain authoritative.

Sports release URLs now ensure complete, web-readable versioned assets are published before advertisement; old hashes remain available. No Boost change. [Historical test evidence](build-logs/2026-11-07-us-004-03-january-test-and-checkbox-invoices.md) · [Asset recovery](build-logs/2026-11-07-us-005-01-extension-asset-recovery.md).

## Completed-month automation and payment-only checkboxes — 7 November 2026

Explicit user correction supersedes the earlier month-start issuance, automation-start floor and checkbox invoice-generation interactions. **Submit monthly invoices automatically after their calendar month ends**, catching up from each currently Active enrollment's start date. Keep the approved full-fee eligibility at the first day of each billed month, dated fee-plan rates, concessions and native accounting mappings. A January-1 enrollment is eligible for January–October invoices on 7 November; November becomes eligible on 1 December. Midmonth joiners still begin with the following full month. Existing invoices/receipts remain authoritative and are not silently cancelled/repriced.

The Sports daily task now derives completed periods from each enrollment, so the deprecated global start-date value cannot hide historical obligations. Native settings retain that value for compatibility but hide its editor. Automation enablement and the enabled, deliberately selected execution User remain required, with native Company/read/create/submit/workflow/approver controls and no role grants. Enrollment, fee-plan and Academy Settings updates request a deduplicated catch-up after commit; the daily job provides ongoing month-boundary generation and failure retries. Install/migrate registers the Sports daily Scheduled Job Type. Opening a grid does not post accounting.

**Payments checkboxes mean receipt collection only.** Unpaid/partial cells are unchecked, paid cells are checked with a green background; unbilled/not-due/future/review/no-charge cells have no payable checkbox. Check the received months and Save payments, with explicit funds confirmation. The payment API refuses a missing or unsubmitted invoice and never creates its charge. The Generate invoices button is removed from Payments and the Generate and submit invoices button is removed from Monthly billing; that tab is a read-only status/exception view. Native accountant recovery services are not the ordinary workflow. The compact yearly grid keeps amounts/status in tooltips and invoice/receipt PDF links under a documents menu. Activate reversal selects permitted grid receipts, requires a reason and restores the native outstanding balance without deleting the charge.

The first corrected run registered the missing daily task and posted nine missing completed-month invoices for the retained January test enrollment. January–October now each have a submitted native invoice. No payment or email was created, and existing invoices/receipts were preserved, including an already-posted November test invoice from the earlier manual flow. New automatic runs exclude current/future months. Existing selected execution account, automation switch, saved fee plans and global scheduler configuration were not changed.

[Build evidence](build-logs/2026-11-07-us-004-03-completed-month-automation-payment-only-grid.md). Earlier dated refinements below/above remain historical where superseded.


## Payments summary cards — 7 November 2026

SPORTS-FR-011 / SPORTS-FR-012 / SPORTS-FR-023, US-005-02: Payments also displays the Overview's Program enrollments, Active enrollments, Billed this year and Outstanding cards above the payment controls. The same permission-scoped Overview API supplies selected-year totals across all visible enrollments, independently of grid pagination/player search; this scope is stated beside the cards. Refresh, year changes and completed payment/reversal actions reload totals. Enrollment counts retain the Overview's current enrollment semantics. No billing/payment, permission or schema change.

[Build evidence](build-logs/2026-11-07-us-005-02-payment-summary-cards.md).


## Summary card colours — 7 November 2026

US-005-02 / SPORTS-FR-011, SPORTS-FR-012, SPORTS-FR-023: Overview and Payments share coloured summary cards: blue enrollments, teal active enrollments, green billed amounts, red positive outstanding balances and green cleared balances. Soft matching backgrounds, accent borders and bold values follow the Community App visual direction; text labels retain meaning independently of colour. This is a visual refinement with unchanged financial totals and scope. [Build evidence](build-logs/2026-11-07-us-005-02-summary-card-colours.md).
