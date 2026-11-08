# Build log: Subscription overview, payment grid and receipt reversal

- Date: 7 November 2026 (Africa/Lagos)
- Story / epic: US-005-01, US-005-02, US-005-03 / EPIC-005; US-004-03 integration
- Requirements: SPORTS-FR-010/011/012/013, SPORTS-NFR-003/004
- Affected apps / branch: Sports App only / story/epic-004-scholarships-and-monthly-billing
- Pull requests: None requested; existing work remains uncommitted.
- Status: Verified development slice

## Intended outcome and starting context

User likes Community App Membership Admin Overview and checkbox Payments with reversal, and explicitly requested the same subscription-updating interaction for Sports. Inspected local Community page JS and membership_dues.py read-only. The supplied deployed URL was not accessible to the web tool; local implementation supplied the relevant interaction evidence. Community App remains independent and unchanged.

## Policy decisions and plan

Retain effective plans, native Customer-per-player, existing month-start eligibility and concession rules. Checkbox selection stages an explicit bank-confirmed collection; it cannot mark a player paid without real submitted accounting. Generate any missing eligible invoice and submit its full remaining-balance receipt together. Use separate receipts per cell to limit reversal scope. Selected receipt reversal is transactional as a batch. Reversal means cancelling a mistaken receipt and reopening receivables, not deleting charges or sending a cash refund. Scheduled privileged activation remains pending from the previous adjustment; this request does not approve an execution identity.

## Work performed

- Added subscription_payments.py: scoped overview totals, paginated yearly player/program grid, future/eligible/missing/zero/partial/paid/review/cancelled states, overdue flag, native account list, confirmed collection and reasoned receipt cancellation.
- Added read-only Sports obligation/request/payload fields on native Payment Entry. Unique deterministic request identity plus immutable payload/provenance guards, locks, exact invoice allocation and per-cell transaction/savepoint protect retries/rollback and prevent external provenance injection or reassignment.
- Added Receive subscription transition only to Sports-owned Payment Entry workflow, reusing existing approval roles and restricting its condition to generated Sports subscription receipts. Native configured payment approver, read/create/submit/cancel and workflow rules remain. No role assignments or Boost bypass configuration.
- Added subscription_console.js and provider assets; Scholarships & Billing defaults to Overview and includes Payments, keeping monthly invoices, fee plans, scholarships and history. Clear selected count/amount, receipt/invoice PDF modals, confirmation/reversal reason and explicit result messages. Editable/selected/busy grids are protected from background refresh; small screens scroll the grid horizontally.
- Updated baseline, PRD, guides, source reconciliation and synchronized story inventories. US-005-01 moves to In review, US-005-02/03 In progress for their verified slices; full refund/reconciliation scope is not Done.

## Commands and observations

- Full isolated Python suite: 247 checks passed, including bounded/scalar/unique selections, year filters, accounting rights, bank Company/currency/type, textual month query scope, ordinary receipt isolation, immutable provenance and reasoned native cancellation.
- Native rollback-only synthetic QA: generated submitted monthly charge and allocated submitted receipt from one unbilled cell; native invoice becomes Paid, retry returns same receipt, changed payload rejected. Cancellation reopened invoice and retained submitted charge; cancellation retry and old-request retry did not create a second receipt; distinct new confirmation settled reopened balance. Receipt submission failure rolled back its newly generated invoice/obligation/GL. Full coverage produced No charge. Invalid bank and native permission denial rejected.
- Guaranteed cleanup restored all tracked player/program/Customer/receipt/invoice/GL/payment-ledger/email counts. No actual charges or emails persisted. A temporary disabled Finance account with the installed Boost Finance Manager capability and a native Player User Permission saw exactly one permitted player in grid and overview; Guest was denied. The account and User Permission were rolled back and its cache cleared. Native partial-payment check collected only the remaining NGN30,000 after an existing NGN10,000 receipt. An invalid later receipt rolled back the entire selected cancellation batch.
- Browser actual-source fixtures at 1440/390: checkbox stages without writes, correct payment metadata/source revision, receipt links/paid/reopened states, reasoned reversal, hidden denied controls, escaped names and bounded horizontal overflow passed. Existing billing/scholarship/plan regression fixture also passed.
- Frappe Semgrep: zero findings on changed backend. Pinned lint passed. Expected missing-plan exceptions are rendered as Review billing cells with the message flag restored, avoiding repeated popup dialogs.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Customer-attributed collection and source ledger | Native combined invoice/receipt lifecycle | Passed; rolled back |
| Duplicate-safe retries and rollback | Same/changed requests, final-submit failure | Passed |
| Receipt reversal restores receivable | Native cancel/retry/re-payment | Passed; no invoice deletion |
| Monthly status/overview and controls | Desktop/phone fixtures and native read APIs | Passed; scoped Finance and Guest checks passed |

## Decisions, deviations and recovery

Initial native grid test found YYYY-MM Data cannot use Frappe date-converting BETWEEN; switched to explicit twelve month keys and added regression coverage. Browser synthetic crypto UUID support was supplied by the fixture, matching secure-context deployment. No production app/source edits and no real emails; normal review escalations used for browser/database checks.

## Remaining work and release impact

Development-only additive Payment Entry fields and Sports-owned conditional workflow installed. Automatic billing remains disabled with no execution user or job activation. Sports-only assets published; development web reloaded. HTTPS smoke checks passed: exact published asset hashes, Guest denied overview/grid, zero real subscription receipts/obligations and automatic billing still disabled. Native test fixtures and real finance counts remain separate. No production deployment, commit, PR or merge. Generic external receipts/refunds/reconciliation and scheduled-execution-account decision remain separate.
