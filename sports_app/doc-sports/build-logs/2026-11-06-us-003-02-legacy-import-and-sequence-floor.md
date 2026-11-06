# Build log: legacy player import and configurable sequence floor

- Date: 2026-11-06 (Africa/Lagos)
- Stories / epics: US-001-01, US-003-02, US-008-03 / EPIC-001/003/008
- Requirements: SPORTS-FR-001/004/024; SPORTS-NFR-003
- Affected app / branch: Sports App / story/us-003-01-enrollment-image-and-invoice-acceptance
- Pull requests: None for this adjustment.
- Status: Verified development refinement

## Intended outcome and starting context

User wants to import existing players before setup and control subsequent player numbering. Prefix/width already existed; the old counter seeded legacy references only on its first allocation, so a later import would not advance an existing counter.

## Policy decisions and plan

Preserve historical IDs using native Data Import's ID column, restricted to academy managers and configured Company. Keep server-owned automatic IDs for ordinary intake and immutable existing identities. Add a validated positive starting-sequence minimum, not a destructive reset. Reserve successful matching legacy suffixes even after counter initialization under existing settings/Series locks. No arbitrary naming-expression execution, account merge, application/invoice counter change or live import.

## Work performed

- Added Player starting sequence setting, validation, console field and illustrative preview.
- Enabled native Sports Player import metadata and management-role import permission. Controller requires management and the configured Company during native import.
- Shared counter helper advances to maximum configured/imported/issued floor, never lowers it. Native imported IDs skip automatic naming; successful imports reserve their suffix without allocating another ID. Nonmatching legacy IDs are retained without interpreting their sequence.
- Updated requirements, PRD, affected stories and step-by-step import guide. Existing unique email, Customer/User and guardian rules still apply; no fee/receipt/history import.

## Commands and observations

- Initial Sports regression passed: 171 tests, including new floor validation/advance/no-reset, import management/Company checks and imported suffix reservation.
- Final pinned pre-commit hooks passed. Frappe Semgrep scanned all three changed Python runtime files with zero findings. Full Sports suite: 171 tests passed.
- Actual settings source in Chromium passed at 1440/390px: displayed starting sequence, changed prefix/minimum preview, and saved payload with source revision. FieldGroup/API are synthetic; no browser ERP writes.
- Native `/tmp/sports-legacy-schema.py` reloaded only Sports Player and Sports Academy Settings metadata on Moyours development. No existing player identities or stored numbering settings changed.
- Native `/tmp/sports-legacy-import-qa.py` exercised Frappe Importer.insert_record with real Sports controllers, temporary ID/email/account data and a guarded commit method. Verified verbatim historical ID, auto Customer/disabled Website User, advancing an initialized counter, duplicate-ID denial, next-month continuity, raised floor, no decrease/reset, nonmatching legacy ID retention and ordinary client-supplied ID being ignored. No invoices, receipts or memberships created.
- Guaranteed rollback restored original Player/Customer/User/Contact/Enrollment/Invoice/Payment counts and removed synthetic Users. No actual client roster imported or temporary login sessions created.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Continuous floor and protected import policy | Unit tests | Passed |
| Native retained IDs, retry conflicts, sequence continuity and rollback | Native Importer/controller/Series QA with blocked commits | Passed |
| Exposed setting and responsive save/preview | Actual settings source desktop/phone fixture | Passed |
| Static checks and metadata | Pinned hooks, Semgrep, 171 tests and scoped metadata reload | Passed |

## Decisions, deviations and recovery

Use native Data Import and ID mapping rather than a second legacy-ID field/custom importer. Starting sequence is a minimum because previously issued numbers cannot be reused; changing prefix does not reset Company numbering. No actual roster was supplied. Existing historical account conflicts require reconciliation before import. Per-row native import success is not a claim of batch atomicity.

## Remaining work and release impact

Sports Academy Settings/Sports Player metadata synchronized on the designated development site; current content-addressed provider assets published/verified and cache cleared. Development web restart completed successfully. Reload open console tabs. All synthetic data and Series allocations rolled back. No production deployment, real player import, commit/merge, ID rename, existing role assignment or historical finance import. US-008-03 remains Proposed for the actual data migration/pilot.
