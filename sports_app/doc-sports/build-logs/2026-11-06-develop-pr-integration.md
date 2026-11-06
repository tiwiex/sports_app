# Build log: Consolidated Sports develop integration

- Date: 2026-11-06 (Africa/Lagos)
- Stories / epics: EPIC-001–009 consolidated backlog; US-006-04, US-007-01, US-002-02 and US-002-04 implementation/refinements
- Requirements: existing mapped Sports requirements and questionnaire additions SPORTS-FR-038–042
- App / source branch: Sports App / story/us-007-01-fingerprint-preparation
- Target: develop, via GitHub pull request; local develop fast-forward after remote merge
- Status: Local verification passed; PR/merge results recorded in linked GitHub history

## Intended outcome and starting context

User authorized committing accumulated Sports work, opening/merging a PR into develop and fast-forwarding local develop. Source branch includes the previously committed club/attendance/player improvements plus pending Next attendance, biometric preparation/demo, questionnaire reconciliation and console review/navigation refinements. Current user-entered review metadata and its generated audit logs are preserved.

## Policy decisions and plan

Commit the coherent Sports App work and its evidence. Preserve existing IDs, user edits and original questionnaire documents. Keep HTML enrollment, app separation and real biometric acceptance boundaries. Use a normal PR merge without bypassing branch protections; verify local/remote develop alignment afterward. No live-site deployment is requested.

## Work performed

Prepared the complete pending source/documentation/test set, including Next attendance source/lockfile, retired enrollment compatibility redirects, consent/preparation DocType/API, simulated capture, separate fingerprint directory, 82-question discovery register, nine consolidated epics, story-review metadata editing and Sports-owned navigation styling. Generated dependencies, Next output and fingerprinted console releases remain ignored. Static attendance export is built/published as a deployment step, not committed.

Inspected pre-existing failed GitHub CI run 41451925820: Server failed at Install MariaDB Client. Replaced unavailable version-specific client package with mariadb-client, pinned bench bootstrap to Frappe version-15, added required ERPNext version-15 installation, used Node22 and added an attendance static-build job. No application behavior is changed by the CI setup repair.

## Commands and observations

- Fetched origin: source was one commit ahead of develop with no remote-only divergence before this integration.
- Full Python unittest discovery: 138 tests passed.
- Next production build passed; offline shell prepared with 20 public assets. Build output remains ignored.
- Chromium fixtures passed at 1440/390px for the real attendance export/worker/IndexedDB with synthetic APIs, story-review autosave/queue/focus behavior and Sports/Boost navigation grouping. No ERP records or story review states were written by these browser fixtures.
- git diff whitespace checks passed. Final PR/CI/merge status is recorded in the GitHub PR and the completion report; local checks are not a claim that remote CI passed.

## Verification evidence

| Criterion | Evidence | Result |
|---|---|---|
| Backend regression | 138 Python tests | Passed |
| Attendance build | Next static production build | Passed |
| Attendance/review/sidebar UX | Three desktop/phone browser suites | Passed |
| Source provenance | Reconciliation and per-adjustment logs retained | Preserved |
| PR / fast-forward | GitHub PR history and final Git branch verification | Required integration step |

## Decisions, deviations and recovery

No schema migration, permission repair, financial posting, email, actual biometric collection or production deployment performed for integration. No temporary accounts/records created. Existing user review edits and original questionnaire bytes are included intentionally. Earlier historical logs retain their original no-commit statements; this log records the later integration authorization.

## Remaining work and release impact

Full hardware/provider, policy, commercial acceptance and proposed questionnaire stories remain open. Marking this integration merged must not mark whole epics or proposed stories Done. Fresh deployments require the documented Node22 attendance build/publish step and migration for the new Sports Biometric Enrollment DocType; the designated development site already has the preparation schema. This PR is repository integration, not production release.

## PR verification follow-up

PR: https://github.com/tiwiex/sports_app/pull/1. The GitHub connector could read but lacked PR-write access; the authenticated GitHub CLI created the PR.

Initial remote attendance build and dependency audit passed. Server setup then exposed CI-container TLS/client defaults; the local test-container CLI now explicitly skips SSL and the test site uses TCP 127.0.0.1. These settings apply only to the GitHub CI container. Initial lint exposed accumulated formatting and missing JSX parsing. Applied the repository-pinned Ruff/Prettier formatting, enabled JSX parsing, documented browser-page fixture globals, replaced an accidental undeclared fixture temporary with a const and fixed the remaining small Ruff diagnostics. Normalized an en dash in a validation message and used the Python3.10 union form for isinstance; no business policy changed.

All pinned pre-commit hooks pass locally. Rechecked 138 Python tests and all six desktop/phone browser suites (attendance PWA, development controls, navigation, players, registrations and native attendance); all passed. Next static production build also passed after formatting. Generated content-addressed console assets are republished from formatted source; old assets remain available. Remote check results are recorded on the PR, separately from this local evidence.

## Native and semantic CI follow-up

The full native CI environment now installs Frappe/ERPNext/Sports successfully and ran all138 tests; its only remaining test failure was a contract test importing optional erp_boost directly on a Sports-only bench. That test now supplies a temporary module fixture for the optional host and restores sys.modules afterward, preserving the approver-boundary assertion without making Boost required.

Added explicit type annotations to whitelisted API arguments while retaining JSON payload and optional-value forms, wrapped literal user-facing errors in Frappe translation, and used native keyword document construction. Tests isolate translation where no Frappe site/cache exists. Rewrote permission capability expressions into named booleans so their consumed return values are clear to the scanner. Fixed whitespace in a translated sort label. Four deliberately public routes (anonymous attendance bootstrap and rate-limited enrollment/payment submissions) retain their existing access/validation and carry narrow reviewed-endpoint Semgrep annotations, not a global rule exclusion. Private-data and token/idempotency coverage remains in the test suites.

Final local verification after these changes: 138 tests passed; all twelve pinned pre-commit checks passed; 76-rule Frappe/Python correctness scan completed with zero findings and zero parsing errors. CI database TLS defaults apply only to the ephemeral test container, including child import commands. No production/site permission changes.
