# Build log: January test player and checkbox invoice generation

- Date: 7 November 2026 (Africa/Lagos)
- Story / epic: US-004-03, US-005-01 / EPIC-004/005
- Requirements: SPORTS-FR-010/011, SPORTS-NFR-003
- Affected apps / branch: Sports App only / story/epic-004-scholarships-and-monthly-billing
- Pull requests: None requested.
- Status: Verified development refinement; synthetic fixture retained by user request

## Intended outcome and starting context

User requested an Active player who joined January 2026 to test generating old invoices, and Community-style checkbox simplicity. Existing saved plans now cover January–October (Backdated 2026) and November onward (Monthly Fee); no plan/rate/accounting mapping was changed by this adjustment.

## Policy decisions and plan

Use the same month checkboxes for invoice-only generation and confirmed funds collection. Keep native permissions, immutable snapshots and month-start eligibility; reject future months in this grid action. Do not infer payment from invoice generation.

## Work performed

Added Generate invoices to the Payments grid and a bounded POST service using the existing native monthly generator. It requires no bank/payment reference or receipt. Existing checked-month Save payments retains explicit funds confirmation, preselects the saved receiving ledger only if it appears in the native permitted account list, and accepts an optional reference with deterministic server fallback. Unconfigured accounts are not guessed. Review billing cells show their sanitized reason.

Created the explicitly requested synthetic player TEST January 2026 Player (MSA26-11003), Active enrollment SPORTS-ENR-00019 starting 2026-01-01, in the configured program. The player Customer and disabled user provisioning follow the normal registration service. Retained January invoice ACC-SINV-2026-00008, posted 2026-01-01, NGN40,000 outstanding, with balanced native GL and original plan snapshot. Generation retry returns that invoice. February onward remains available for deliberate user testing according to current saved plans and existing scheduler settings. The existing enabled scheduler/start date were not changed.

## Commands and observations

Native user-requested fixture creation/generation committed only the synthetic player/dependencies and January invoice. No Payment Entry or test email was created by that operation. The initial remaining payment verification was stopped by automatic approval review's usage-limit failure and did not execute. On resuming, a fresh approved rollback-only QA run verified blank-reference collection through a selected permitted bank, native submitted receipt, same-request retry and receipt reversal. Guaranteed rollback restored receipt/GL/payment-ledger/email counts and retained the January invoice unpaid at NGN40,000. No fictional receipt or cash movement persists.

Actual-source desktop/phone browser fixture verified check → Generate invoices without bank input/payment, then check → Save payments using the provided configured account and optional blank reference. Existing paid/reversal controls still pass. Isolated suite including later asset-recovery regressions: 249 passed. Pinned lint passed. The UI release was completed during the separately logged extension recovery.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Historic January invoice | Retained synthetic player and native invoice | Passed; NGN40,000 unpaid |
| Generation retry/no receipt | Native duplicate generation | Same invoice; no receipt |
| Simple checkbox actions | 1440/390 browser fixture | Passed |
| Optional-reference payment/reversal | Native rollback-only QA | Passed; all temporary accounting removed |

## Decisions, deviations and recovery

The configured receiving account was absent from the native allowed account list, so QA explicitly selected an allowed bank rather than changing settings or assuming an account. Existing backdated prices were reused. Original numbering uses creation month; membership start date is separately January.

## Remaining work and release impact

Retained fixture is intentional for user review and should not be treated as a real academy member. No production deployment, commit, PR, merge, Boost/Community source or scheduler configuration changes. Broader refund/credit reconciliation scope remains open.
