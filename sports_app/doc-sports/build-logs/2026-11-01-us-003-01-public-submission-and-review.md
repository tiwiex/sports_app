# Build log: Submittable Sports registration and staff acceptance

- Date: 2026-11-01 (Africa/Lagos)
- Story / epic: US-003-01 / EPIC-003; US-001-02 and US-003-02 integration
- Requirements: SPORTS-FR-003, SPORTS-FR-026, SPORTS-FR-029, SPORTS-FR-030, SPORTS-NFR-002, SPORTS-NFR-003, SPORTS-NFR-009
- Apps / branch: Sports App / `story/us-003-01-application-intake-and-review` (preserves prior uncommitted website changes)
- Pull requests: Not opened
- Status: Verified PoC / In review

## Intended outcome and starting context

User requested a submittable public enrollment form and a complete PoC registration workflow. Earlier demo-only submission is superseded. Public enrollment creates Sports Registration; authorized staff review then accept into the existing player/Customer/User/enrollment service, or reject with a reason.

## Policy decisions and plan

No guest list/read/update permissions. Accept only allowlisted bounded fields, rate-limit public POSTs, use a honeypot, UUID retry keys and locked idempotent writes. Return only an opaque registration reference; no public status lookup or identity/account enumeration. Keep player email uniqueness checks in staff acceptance rather than leaking existing accounts to guests.

Website pathways remain public content preferences. Intake assigns the configured academy Company/default Sports Program on the server; reviewer selects the final operational program/group/dates/status. No anonymous Company/Customer/User assignment. Only staff acceptance creates the linked records; User stays disabled and no payment/invoice/welcome email is generated.

## Work performed

New app-owned DocType Sports Registration and read-only Sports Player source-registration link; private Registrations console view; public submit service; review actions. Preserve original submission timestamp, pending-record edit history and accepted-record provenance.

## Commands and observations

- Development database backed up; Sports Registration and Sports Player provenance link synced, required-field metadata applied, content-fingerprinted console assets published and development web worker reloaded. No live Boost or production website edits.
- 80 focused Python tests passed across intake, registration/player validation, settings, console/assets/docs, Boost provider/dimensions and User role repair. Final eight intake tests rerun after tightening raw input types and required review fields; passed. JS syntax and diff whitespace checks passed. An initial focused test invocation from inside the package shadowed imports; rerun from `/tmp` passed.
- Real development-site API checks passed: strict required/allowlisted fields; no player/account/finance writes before review; unchanged retry reference; changed retry rejection; no account-existence leak (existing staff email may submit but cannot be accepted into a duplicate account).
- Rate limiter test used an isolated synthetic request identity: attempt 16 rejected after 15 hourly attempts; honeypot attempts created no records; synthetic Redis counter deleted. No real visitor counters were reset.
- Native/private checks passed: original submission timestamp survives pending correction, direct status mutation is denied, accepted records reject edits, possible Player matches are shown, rejection requires a reason, rejected submissions cannot be accepted, and no Finance-only/basic Sports role gains review access.
- Invalid initial enrollment rolled back Player/Customer/Contact/User/category creation and left the registration Pending. Existing-User conflict also left no partial player. Callback unit tests confirm deferred User jobs from failed acceptance are discarded while prior callbacks survive.
- Concurrent acceptance of one application returned one Player and exactly one initial enrollment; Customer/User linkage and disabled Website User were verified. Concurrent public retries produced one Sports Registration.
- Guest browser flow passed: submit, deliberately lose the successful response, retry to receive the same reference, receipt screen, no guest REST record/list or private API reads. Phone form checks passed at 390px and 320px with no horizontal overflow.
- Staff browser flow passed: registrations queue, private field review, program selection, acceptance into linked Player/Customer/User, rejection with reason and phone-width review. Sports-only and Finance-only role browser denials passed.
- All temporary registrations, staff/generated Users, sessions, Players, enrollments, Customers/Contacts and fixture masters removed in guaranteed cleanup; academy settings restored. Credential files removed and browser contexts closed. Cleanup targeted fixture keys/email namespace/owned records, preserving unrelated records.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Required fields/reference/original timestamp | Unit + real intake, native correction and browser receipt | Passed |
| Private duplicate review | Company-scoped review API, possible matches, guest/role denial and staff browser | Passed |
| Retry-safe acceptance and rate-limited private public intake | Lost-response retry, concurrency, rollback, isolated rate-limit and accept/reject browser checks | Passed |

Screenshots: [receipt](assets/2026-11-01-registration-receipt.png), [private review](assets/2026-11-01-registration-review.png), [accepted player](assets/2026-11-01-registration-accepted.png), [public phone](assets/2026-11-01-registration-public-phone.png), [staff phone](assets/2026-11-01-registration-review-phone.png).

## Decisions, deviations and recovery

Complete PoC means submission, staff review and resulting linked registration records. Production hardening, email verification/notifications, payment, versioned legal consent and portal activation remain separate scope. No changes to the production academy website or live Boost.

## Remaining work and release impact

Development deployment and QA cleanup completed. New submissions are real private records; staff acceptance is required before player/Customer/User creation. Earlier demo-only guides were updated and historical logs preserved. No homepage switch, production deployment, email, payment, portal activation or proposal. Story remains In progress for broader production acceptance; the PoC workflow is verified. No commit/merge/push requested.
