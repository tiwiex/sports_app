# Build log: configurable enrollment naming series

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-003-01 / EPIC-003; settings interaction US-001-01
- Requirements: SPORTS-FR-003/030; SPORTS-NFR-003
- Affected app / branch: Sports App, `story/us-003-01-enrollment-image-and-invoice-acceptance`
- Pull requests: None; changes remain on the implementation branch.
- Status: Verified on development

## Intended outcome and starting context

Replace the prior fixed SPORTS-APP application prefix with a configurable reference. User selected MSA-ENR as default. Keep generic Sports ownership and existing records.

## Policy decisions and plan

Store native Frappe notation in Academy Settings: MSA-ENR-.YYYY.-.#####. Accept a literal uppercase prefix, optional YYYY year and 4–10 counter digits; reject expressions, path separators and unsupported tokens. Empty legacy configuration falls back to the schema default. Native settings/console use the existing management permissions and stale-write protection. No counter-reset control is exposed.

## Work performed

- Added Enrollment naming series to Sports Academy Settings, API allowlist and Sports console form.
- Sports Registration autoname reads validated saved configuration and uses native Frappe counters.
- Existing references are never renamed. Sports Enrollment program memberships, player IDs and invoice series are unchanged.
- Updated story criteria, requirements, PRD and enrollment guide; preserved earlier build evidence as history.

## Commands and observations

- Python unittest discovery: 149 tests passed. Added default/custom-format, invalid-expression/counter and controller configuration coverage. Made existing registration translation mocking independent of module import order.
- Reloaded Sports Academy Settings and Sports Registration on moyours.ideltatech.com; published the formatted console settings asset and restarted only the development web process.
- Native rollback QA (`/tmp/sports-enroll-verify.py`): settings API exposes MSA default; application gets MSA-ENR-year-five digits; temporary QA-ENR six-digit no-year setting generates a new matching reference while the earlier reference remains. Existing portrait privacy, Draft/Pending Review, combined invoice/receipt/admission, forced failure rollback and retry assertions all passed. All synthetic records and temporary configuration rolled back; no financial posting, mail or account persisted.
- All pinned pre-commit hooks passed. Initial Prettier formatting was applied and the full hooks rerun successfully.

## Verification evidence

| Criterion | Verification | Result |
|---|---|---|
| Default and editable validated series | Unit tests / native configuration | Passed |
| Native naming and old references preserved | Synthetic default/custom registration, rollback | Passed |
| Existing financial acceptance unchanged | Native invoice/payment/admission rollback suite | Passed |

## Decisions, deviations and recovery

This is the public enrollment application reference (Sports Registration), not a renaming of accepted program memberships. Earlier fixed SPORTS-APP-series decision is superseded. Naming changes affect future allocations only; returning to a previously used prefix resumes its native counter.

## Remaining work and release impact

No production changes or business-reference renames. Development-only schema reload and web restart required; normal migration exposes the field on other sites. Build log and updated guide remain available in Sports Development Tools.
