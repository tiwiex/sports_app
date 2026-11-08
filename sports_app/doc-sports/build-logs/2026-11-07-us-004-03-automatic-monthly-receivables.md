# Build log: Automatic monthly receivables

- Date: 7 November 2026 (Africa/Lagos)
- Story / epic: US-004-03 / EPIC-004; settings support US-001-01
- Requirements: SPORTS-FR-010, SPORTS-NFR-003, SPORTS-FR-009
- Affected apps / branch: Sports App only / story/epic-004-scholarships-and-monthly-billing
- Pull requests: None requested; uncommitted development work.
- Status: Verified implementation; activation awaits execution-user approval

## Intended outcome and starting context

User explicitly replaced manual submission with automatic monthly posting while players are active, so accounting records receivables. Earlier dated logs preserve the historical manual/draft-only decision and are superseded for this behavior.

## Policy decisions and plan

Retain calendar-month full-fee eligibility at month start and scholarship rules. Configure earliest billing month and finance execution user; run daily in academy timezone for current/missed months from that start only. Submit invoices, never create fictitious payment/receipt. Zero due produces an obligation only. No automatic native Subscription records or parent email/reminders.

## Work performed

- Added `scheduled_billing.py`, daily scheduler hook and three Academy Settings fields: enable automatic submission, earliest month and execution User. Native user enablement, Sports/native permissions and Company restrictions apply without new role assignments.
- `monthly_billing.py` now submits positive invoices transactionally and resumes old drafts; read/create/submit and native workflow/approver checks apply. Existing submitted records are never posted twice; cancellation requires reviewed correction. Scheduler failures use native Error Log with enrollment/month keys and no confidential reasons, while other rows continue.
- Added idempotent, conditional Submit monthly fee action to Sports-owned invoice workflow only, reusing existing approval roles. Ordinary non-Sports invoices cannot use this action. No Boost source or global approval bypass settings changed.
- Billing console explains schedule state/start, provides manual recovery and accurately says Generate and submit invoices. Settings tab exposes all three controls.
- Aligned requirements, PRD, story, billing/setup guides and discovery refinement; questionnaire source remains immutable. Story remains In review, with unresolved broader policy work retained.

## Commands and observations

- Isolated Python suite: 238 passed, including scheduler boundaries, disabled switches, retry without repricing, per-row failure isolation/private log content, native submit rights, ended enrollments and cancelled/already-submitted invoices.
- Native rollback-only development QA: synthetic NGN40,000 invoice submitted and Unpaid, outstanding 40,000; balanced GL debit/credit and receivable account debit, native Payment Ledger Entry. Repeated generation/scheduled runs retained references and ledger counts. Submission failure rolled back obligation/invoice/ledger together. Full scholarship had zero obligation/no invoice; withdrawn/midmonth joiners excluded. Legacy draft resumed under same reference. Ordinary invoice offered no monthly submission transition.
- Guaranteed rollback restored all tracked document/GL/Payment Ledger/email counts; no real invoices/payments/emails persisted. No QA users were needed.
- Development scheduler readiness: enabled, not paused/maintenance; zero real fee plans, obligations and monthly invoices before activation. Fee plans must be deliberately configured before any real monthly billing.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| One obligation/invoice per eligible period | Unit suite and native repeated runs | Passed |
| Native submitted receivable | Synthetic invoice + GL + payment ledger | Passed; rolled back |
| Scholarships and eligibility | Full/zero, inactive and midmonth fixtures | Passed |
| Failure recovery and native controls | Submission rollback, legacy draft resume, workflow scope | Passed |
| Desktop and phone controls | Actual-source synthetic browser fixtures | Passed; enable/start/user save payload checked at both widths |

## Decisions, deviations and recovery

Initial native run correctly refused submission without a selected approver. Sports now selects the execution actor on an otherwise unassigned monthly invoice and native approver validation remains authoritative. Added a conditional direct submission transition to avoid unnecessary pending-review notifications during automatic billing; no changes to Boost code. Custom workflows without a permitted direct submitted transition fail safely instead of being rewritten. Browser sandbox required normal escalation. Automatic approval review rejected persistent immediate activation under Administrator: user had authorized automatic billing but not that privileged execution identity. The rejected command did not run. The safe alternative installed only additive settings schema and Sports-scoped conditional workflow, leaving automatic billing disabled, no execution user assigned and no scheduler activated. No workaround activated privileged posting.

## Remaining work and release impact

Development schema and conditional Sports workflow are installed; updated Sports assets published and only development web reloaded. Automatic billing remains disabled pending explicit execution-user/activation approval; no daily job was activated. Pinned lint and desktop/phone browser checks passed. Frappe Semgrep flagged two scheduler user-switch lines: manually reviewed as a non-whitelisted management-configured enabled user switch with normal native permission rechecks and finally restoration; narrowly annotated with rationale. No permission bypass is granted. Production not deployed. No commits, PR or merge requested. Install/migrate registers the scheduler and adds fields, but automation defaults disabled on other installations until explicitly configured. Installment/refund/grace and automatic reminder scope remains open.
