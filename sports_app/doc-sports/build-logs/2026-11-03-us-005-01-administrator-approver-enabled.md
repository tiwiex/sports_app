# Build log: Enable Administrator enrollment payment approval

- Date: 2026-11-03 (Africa/Lagos)
- Story / epic: US-005-01 / EPIC-005
- Requirements: SPORTS-FR-031, SPORTS-NFR-002, SPORTS-NFR-003
- App / branch: Moyours site configuration; Sports App documentation on story/us-003-01-enrollment-review-layout
- Pull requests: None
- Status: Applied / eligibility verified

## Intended outcome and starting context

Administrator could not complete ACC-SINV-2026-00003 because the combined service requires explicit Boost invoice approver configuration. The user explicitly approved adding Administrator as an additional Sales Invoice approver after reviewing the role/settings change. See the [prior diagnosis](2026-11-03-us-005-01-administrator-payment-review-diagnosis.md).

## Policy decisions and plan

Enable only the approved Administrator invoice-approval configuration on moyours.ideltatech.com. Preserve the existing Finance reviewer, all other access/settings, and the actual invoice. Verify eligibility without applying a workflow transition or posting a payment. Existing Payment Entry approval rules already recognize Administrator; no additional payment-approver flag is needed.

## Work performed

- Added the explicit Boost Invoice Approver Has Role child to Administrator.
- Added the Administrator Boost User Role Access child under Boost Settings, with Approver and Sales Approver enabled. Purchase Approver and approval bypass remain disabled.
- Inserted only the intended child records through native document insertion; did not save User or the full Boost Settings managed-role matrix. Cleared Administrator's user cache.
- Compared existing Has Role records and unrelated Boost access rows before/after; preserved all existing entries. Confirmed the prior named Finance reviewer remains eligible.

## Commands and observations

Native Python site operation in one transaction, committing only after approval-eligibility and preservation assertions passed. A separate fresh-connection check confirmed Administrator is a valid Sales Invoice approver, not a configured Purchase Invoice approver, and completion_access returns true for ACC-SINV-2026-00003.

## Verification evidence

| Acceptance criterion | Check | Result |
|---|---|---|
| Administrator eligible for Sales Invoice/payment completion | Native can_complete_payment and completion_access, repeated on fresh connection | Passed |
| Existing Finance reviewer retained | Prior named reviewer capability check | Passed |
| Other roles/access entries preserved | Full before/after existing-row comparison | Passed |
| No actual payment posting | Invoice/Payment Entry/GL Entry/Payment Ledger Entry counts and invoice state unchanged | Passed |
| Scope remains Sales approval | Native approver checks: Sales true, Purchase false | Passed |

## Decisions, deviations and recovery

This explicitly approved site configuration supersedes the earlier decision to leave Administrator unconfigured on Moyours. No global Administrator bypass or source-code permission exception was introduced. Existing invoice/receipt workflow and financial provenance validations still apply.

## Remaining work and release impact

Reload the console/invoice while logged in as Administrator, verify the real bank credit, then use Confirm Payment or Complete Payment. ACC-SINV-2026-00003 remains docstatus 0 / Pending Review with NGN 250,000 outstanding; no receipt or ledger entry was created by this adjustment. Full financial posting was intentionally not performed as a verification step. No migration, application deployment, production site change, email, commit, merge or push. Existing pending Sports work remains intact.
