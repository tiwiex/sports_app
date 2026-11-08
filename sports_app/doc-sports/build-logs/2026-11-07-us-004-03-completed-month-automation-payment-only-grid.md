# Build log: Completed-month automation and payment-only checkbox grid

- Date: 7 November 2026 (Africa/Lagos)
- Story / epic: US-004-03, US-005-01/02 / EPIC-004/005
- Requirements: SPORTS-FR-010/011/012, SPORTS-NFR-003/004
- Affected apps / branch: Sports App only / story/epic-004-scholarships-and-monthly-billing
- Pull requests: None requested; existing changes remain uncommitted.
- Status: Verified development refinement; release smoke checks recorded below

## Intended outcome and starting context

User explicitly corrected the workflow: invoices must be submitted automatically once months have elapsed, without payment; checkboxes should only post received payments, following Community's simple grid. Earlier invoice-generation button and current-month issuance refinements are historical and superseded.

## Policy decisions and plan

Catch up only completed calendar months from each currently Active enrollment's join date, retaining first-day full-fee eligibility, saved effective plans/concessions and native ERP permissions. No active-month/future automatic billing and no fictional receipts. Existing invoices/receipts are not cancelled or recalculated. Daily/month-boundary processing plus after-commit enrollment/plan/settings catch-up, under the already-selected enabled execution User. No new account choice, role grant or global scheduler setting change.

## Work performed

- scheduled_billing derives periods from membership dates instead of the obsolete November floor and excludes the current month. Install/migrate registers the previously absent Sports daily Scheduled Job Type. Added deduplicated after-commit requests on Enrollment, Fee Plan and Academy Settings updates.
- Registered the missing daily job and performed the expressly requested catch-up on development. Nine missing submitted invoices were created; the January test enrollment now has submitted January–October charges. No receipts or emails were created. Existing November invoices/receipts from the older workflow remain unchanged.
- Payment API refuses missing/draft charges and cannot generate invoices. Removed both generation buttons from the console; Monthly billing now displays status/exceptions. Native recovery services remain separate from the ordinary payment workflow.
- Compact year grid shows green checked paid markers, unchecked posted balances, and nonpayable not-due/future/pending indicators. Amounts/issues are tooltips; source PDFs remain in documents menus. Single-receipt paid markers become selectors in reversal mode; reason/native cancellation controls remain.
- Hidden obsolete start-date editor without deleting its saved value. Aligned requirements/PRD/guides/story evidence and discovery register; original questionnaire transcript/hash preserved. Broader story review states unchanged.

## Commands and observations

Preflight: automation already enabled, existing enabled execution User already selected, saved floor 2026-11-01, but **no Sports daily job existed**. Existing fee plans covered January–October and November onward. Development scheduler/default/short/long workers were RUNNING.

- Isolated Python suite: 252 checks passed. Completed-month/year rollover, enrollment-derived catch-up ignoring legacy floor, after-commit requests, native rights, unchanged posted charges and row failures covered. Added explicit proof payment cannot create a missing invoice.
- Native rollback dry run: January–October catch-up, submitted invoices, no current/future new charges, no PE/email, unchanged retries, all original counts restored.
- Approved application run: **9 new submitted invoices**, 10 completed-month invoices for the January test enrollment, **0 new payments / 0 emails**, one Daily job, existing execution account/switch/floor preserved. Native fee plans unchanged. Commit retained the requested receivables.
- Read-only/rollback follow-up: actual grid shows all completed charges; unbilled November is Not due and December Future. A pre-existing November test invoice was correctly retained. Rerun changed no accounting counts. A native enrollment save invoked after-commit catch-up; that temporary edit rolled back.
- Actual-source 1440/390 browser fixtures: checkbox-only payment with no generation call/button, green paid marker, compact source-document menus, reversal, denied controls and horizontal mobile scroll passed. Billing/scholarship/fee-plan/settings regressions passed.
- Frappe Semgrep: zero findings. Pinned lint passes after formatter fixes. No temporary users or real test receipt/cash movement left behind.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Automatic posted completed months | Native dry run and applied catch-up | Passed; 9 missing charges submitted |
| No automatic payment or duplicate ledger | Counts and repeat scheduler | Passed; no PE/email and no duplicate charges |
| Future/current months deferred | Calendar boundary units/native grid | Passed; existing older invoices preserved |
| Checkbox means payment only | Backend guard and desktop/phone fixture | Passed |
| Automatic lifecycle wired | Daily job/worker status, native on_update hook | Passed |

## Decisions, deviations and recovery

The user's chosen existing enabled execution account was reused; no previously rejected account selection or implicit role grant was attempted. The current instruction explicitly authorizes completed-month receivables. Missing or invalid fee plans remain visible exceptions rather than guessed charges. Historical suspension periods are not reconstructed from current Active status; broader policy remains open. A misplaced hook insertion into a commented example was caught and fixed by AST/lint checks before release.

## Remaining work and release impact

Development-only change; no production deployment, commit, PR, merge, Community App or Boost source modification. The legacy November floor remains stored but no longer suppresses historical catch-up. Existing November invoices from earlier manual testing were retained. Production accounting/reconciliation acceptance and unrelated refund/grace policy remain open. Release checks passed: targeted Settings metadata reload hid the obsolete floor while preserving saved configuration and accounting counts; Sports-only assets were published, the development web process reloaded, and all billing assets returned HTTP 200 with exact JavaScript bytes over verified HTTPS. Native configuration, overview and January test-player grid reads passed. Final lint passed. No full bench migration or global scheduler enablement was performed.
