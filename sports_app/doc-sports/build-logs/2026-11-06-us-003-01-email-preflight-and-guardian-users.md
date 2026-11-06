# Build log: email preflight and shared guardian User provisioning

- Date: 2026-11-06 (Africa/Lagos)
- Stories / epic: US-003-01 and US-003-02 / EPIC-003
- Requirements: SPORTS-FR-003/029/030; SPORTS-NFR-003
- Affected app / branch: Sports App, `story/us-003-01-enrollment-image-and-invoice-acceptance`
- Pull requests: None; implementation branch remains uncommitted.
- Status: Verified on development

## Intended outcome and starting context

The public form accepted an existing email and only failed during staff acceptance. Move validation before public submission/invoice preparation. Add guardian User preparation with many players linked to one guardian, preserving separate player identities and finance.

## Policy decisions and plan

User explicitly authorizes public availability checks and guardian account creation/reuse. Return only a boolean via rate-limited POST; expose no account/profile metadata. A UUID request token preserves the application's own unchanged retry. Server controller validation rejects existing User/player/pending application conflicts; existing lock order serializes Sports intake/admission. Recheck admission identity before invoice completion. Existing duplicate applications are preserved for correction.

Create Users only during authorized player admission/registration, not from an anonymous availability check. New player and guardian Website Users stay disabled with no welcome mail. Existing guardian accounts are reused without mutations or privilege changes. Guardian links are server-owned/immutable and do not authorize portal data access. No shared Customer model, bulk backfill, automatic account activation or invitation.

## Work performed

- Added bounded email normalization, global player-email availability, pending reservation checks and limited guardian User creation/reuse.
- Added public rate-limited boolean preflight, browser blur/pre-submit checks, inline errors and correction without losing form data.
- Added server checks before successful public application insertion/invoice creation and before financial acceptance.
- Added read-only Sports Player guardian_user link, native controller safeguards and staff profile display.
- Updated shared field guidance, requirements, PRD, stories, reconciliation annotations and guides; questionnaire source unchanged.

## Commands and observations

- Python unittest discovery: 161 tests passed, including availability conflicts, own-application exclusion, token retry, roleless disabled guardian creation, existing guardian reuse, distinct email rule and rejection before Finance completion.
- Reloaded Sports Player/Sports Registration schema on the designated development site.
- Native isolated `/tmp/sports-enroll-verify.py` suite passed: age/series/photo privacy, invoice review/completion, forced rollback and retries remain working with guardian provisioning.
- Native sibling QA `/tmp/sports-sibling-verify.py`: public preflight/free/pending/used checks, unchanged token retry, duplicate server denial before extra invoices, three separate players/Users/Customers sharing exactly one guardian User, existing guardian unchanged, new Users disabled, and forced admission failure removing both new User records all passed. Initial sibling fixture omitted mandatory enrollment start_date; corrected the fixture before successful verification.
- Synthetic records, account changes, reservations, Series increments, finance and deferred mail rolled back. No test credentials or committed temporary users.

## Verification evidence

| Criterion | Check | Result |
|---|---|---|
| Early duplicate check and authoritative denial | Unit + native service / invoice counts | Passed |
| Many players / one unchanged guardian | Native three-sibling transaction + unit reuse | Passed |
| Distinct disabled Users and atomic rollback | Native account/Customer checks and injected failure | Passed |
| No duplicate Finance posting | Unit identity check precedes completion; native regression suite | Passed |
| Desktop/phone inline correction and valid retry | Chromium synthetic API fixture | Passed |

## Decisions, deviations and recovery

No existing User is attached as a player's own User. Guardians may refer to an existing account, but existing access is never modified and claimed relationships do not grant child data access. Existing rejected/pending/accepted records and invoice references remain intact; no automatic cleanup of the reported old duplicate.

## Remaining work and release impact

Desktop/phone Chromium fixture passed: duplicate player email displays inline error and invalid field before any invoice POST, correction permits submission, and age/photo/Draft/Pending Review behavior remains working. Existing Players desktop/phone browser suite passed with the guardian account field. All pinned pre-commit hooks passed on tracked files and all six new Python files explicitly; Semgrep ran 65 rules on six affected/new Python files with zero findings. Development web was restarted after asset publication, and HTTPS /academy returned 200 with player-email error markup and sibling guardian guidance. Development only; native schema synchronization and web-worker/cache/console asset refresh required. Existing players are not backfilled. Portal verification/activation remains separate work.
