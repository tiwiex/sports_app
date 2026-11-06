# Build log: enrollment portrait and combined invoice acceptance

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-003-01 / EPIC-003; financial interaction US-005-01
- Requirements: SPORTS-FR-003/030/031; SPORTS-NFR-003
- Affected app / branch: Sports App, `story/us-003-01-enrollment-image-and-invoice-acceptance`, based on develop c8530f4
- Pull requests: Not opened; this request authorizes implementation on a branch.
- Status: Verified on designated development site

## Intended outcome and starting context

Refine existing HTML enrollment rather than move it to Next. Add a private portrait, readable application IDs, invoice visibility and one-step authorized financial admission. Existing Make Payment/Draft and applicant claim/Pending Review behavior already existed and is retained.

## Policy decisions and plan

The user's combined acceptance instruction supersedes the mandatory separate finance/admission action. It does not bypass native Finance permissions or configured Boost approvals. Optional portrait; no inferred public media permission. Existing IDs, fees and bank details retained. No historical accepted application is automatically charged again.

## Work performed

- Added private server-owned portrait fields on Sports Registration and Sports Player. Sanitized, bounded JPEG/PNG/WebP input is re-encoded, metadata stripped and stored as a private attachment owned by Administrator; no arbitrary guest URL upload. Image participates in retry fingerprint, while old no-image fingerprints stay compatible.
- Added frontend selection/preview/validation and transfer to the accepted player.
- New applications use SPORTS-APP-YYYY-#####; existing names untouched.
- Queue projects only an application/company-matching invoice reference and workflow state. Acceptance eligibility depends on pending/write rights and linked invoice/finance eligibility; rejection stays independently available.
- Acceptance invokes the existing protected invoice completion service within the same transaction as player admission. Nested savepoints are unique; failed operations drop deferred commit jobs. No Boost source change.
- Updated story acceptance criteria, requirement baseline and PRD. Build logs remain discoverable through existing Sports Development Tools document discovery.

## Commands and observations

- Python unittest discovery: 146 tests passed, including eight new portrait/privacy, finance eligibility, provenance, nested rollback callback and admission retry checks.
- Reloaded only Sports Registration and Sports Player schema on moyours.ideltatech.com; published content-addressed Sports console assets. No full migration/permission repair.
- Native verification command: development Python `/tmp/sports-enroll-verify.py`; browser fixture `/tmp/sports-academy-browser.cjs` with rendered template `/tmp/sports-academy-refined.html` (temporary local QA artifacts). Persistent regression tests: `tests/test_enrollment_refinement.py` and `tests/js/test_registrations_browser.cjs`.
- Native development-site synthetic verification: new series, private portrait/retry (Administrator ownership and native Guest read denial verified), draft acceptance denial, Pending Review, submitted invoice and allocated submitted receipt, player portrait transfer and repeat acceptance all passed.
- Injected admission failure after financial completion: application stays Pending, invoice returns to unposted Pending Review, no receipt remains. Passed.
- Synthetic native transaction fully rolled back; no player/customer/invoice/payment or mail job committed. No temporary QA account created. Template rendered successfully for browser fixture. Native dependency CSS/deprecation warnings did not affect assertions.

## Verification evidence

| Acceptance criterion | Check | Result |
|---|---|---|
| Private portrait + stable retry | Unit + native private File / retry / player transfer | Passed |
| Year series; existing references preserved | Native new application naming; no rename operation | Passed |
| Draft / review / combined acceptance | Native workflow and allocated receipt | Passed |
| No partial posting or duplicate payment | Native forced failure + repeated acceptance; nested callback unit test | Passed |
| Queue and frontend desktop/phone | Chromium fixtures, actual HTML/JS + console source with synthetic API/Dialog | Passed |

## Decisions, deviations and recovery

The native finance workflow creates both the submitted invoice and its allocated receipt on completion. Combined acceptance reuses this implementation, avoiding a new payment process. Finance-denied or draft-linked applications cannot be accepted; finance must verify a reported transfer. Existing standalone payment completion stays available.

## Remaining work and release impact

146 Python tests passed; all pinned pre-commit hooks passed; Semgrep ran 72 rules with zero findings, plus 63 rules explicitly against the two new Python files with zero findings. The designated development web process was restarted; HTTPS `/academy` returned 200 with the new image field and content-versioned JavaScript. Desktop/phone HTML portrait selection/preview/payload, Draft payment and review-claim fixture passed; enrollment console browser suite passed. Development schema updated; production not changed. Later release needs the two DocType schema reloads/migration and normal web-worker reload/cache refresh. Scholarship, partial-payment and production policy decisions remain open. Story stays In progress; no assertion that all questionnaire scope is Done.
