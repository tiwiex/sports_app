# Build log: continuous player IDs and public age validation

- Date: 2026-11-06 (Africa/Lagos)
- Stories / epic: US-003-02 and US-003-01 / EPIC-003
- Requirements: SPORTS-FR-004/030; SPORTS-NFR-003
- Affected app / branch: Sports App, `story/us-003-01-enrollment-image-and-invoice-acceptance`
- Pull requests: None; changes remain on the branch.
- Status: Verified on development

## Intended outcome and starting context

User confirmed questionnaire example MSA17-08001 means academy/year/month/continuous sequence. August 08005 must be followed by September 09006; keep application IDs separate. Add the screenshot's 4–18 age policy to the public form.

## Policy decisions and plan

Backend-only player autoname uses academy-local creation date and a stable Company counter. Hold existing Academy Settings lock plus native Series row lock. Key excludes date/prefix/application series. First use seeds matching historical MSA year/month IDs, not unrelated prototype IDs. Preserve all existing IDs and account links. Prefix/sequence width are existing protected settings, relabelled clearly; development defaults set explicitly to MSA and three digits. No application or invoice series changes.

Public age validation uses calendar years, inclusive fourth birthday through the day before nineteenth birthday, with academy-local date supplied to HTML. February 29 birthdays age on March 1 in non-leap years. Enforce new public applications/DOB corrections; avoid retroactive age rejection on unchanged older records. Original questionnaire stays immutable; the age limit is separately attributed to user direction.

## Work performed

- Added backend player-numbering helper with independent native counter and compatible legacy-sequence seeding.
- Updated Player autoname, settings labels/defaults/preview and validation for 3–10 sequence digits.
- Added inline HTML age error, DOB min/max and calendar validation, plus server-controller rejection.
- Updated questionnaire reconciliation, affected story criteria, PRD, requirements and guides with provenance.

## Commands and observations

- Python unittest discovery: 154 tests passed, including month/year/prefix counter stability, Company separation, legacy seeding, exact fourth/nineteenth birthday and leap-birthday coverage.
- Development Settings schema reloaded and player prefix/width saved as MSA/3; existing IDs untouched.
- First native check exposed Frappe's default modified-order assumption for the internal Series table. Explicit name ordering fixes that lookup; no core changes made.

## Verification evidence

| Criterion | Check | Result |
|---|---|---|
| Continuous independent player numbering | Unit/native month and year transitions | Passed |
| Existing IDs and legacy counter floor | Unit seed test/native retained-reference assertions | Passed |
| Public age bounds, server enforcement | Unit birthday/leap checks + direct public-service calls | Passed |
| Browser age error and valid submission | Desktop/phone fixture | Passed |

## Decisions, deviations and recovery

Existing old-format prototype IDs are preserved, not renumbered or guessed into the confirmed legacy format. Full legacy import remains a separate migration activity. Failed allocations roll back with their transaction; counter digits specify minimum padding, not a maximum capacity. No Finance approval bypass or Boost source modification.

## Remaining work and release impact

154 Python tests and all pinned pre-commit hooks passed; Semgrep ran 65 rules against five affected/new Python files with zero findings. Native rollback QA verified consecutive August/September/January allocation, separate application series, and direct-service under-4/19-year-old rejection with unchanged application/invoice/File counts. The existing synthetic invoice/receipt/admission rollback and retry suite also passed. Desktop/phone Chromium fixture verified future/too-old DOB errors, inclusive min/max birthday bounds, and valid photograph/payment submission. All synthetic data, Series allocations, deferred jobs and temporary QA configuration rolled back; only the explicitly saved development MSA/3 defaults persist. No temporary users created. Published Sports console assets, restarted only development web, and verified HTTPS /academy returned 200 with academy-date and age-error markup. Temporary QA scripts: /tmp/sports-enroll-verify.py and /tmp/sports-academy-browser.cjs; persistent regression coverage: tests/test_player_numbering_and_age.py. Development only. Normal release requires settings schema synchronization, web restart and refreshed content-addressed Sports assets. No data import, identity renames or production deployment authorized/performed.
