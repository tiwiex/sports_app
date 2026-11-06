# Build log: Club column filters and sorting

- Date: 2 November 2026 (Africa/Lagos)
- Story / epic: US-009-01 / EPIC-009
- Requirements: SPORTS-FR-032, SPORTS-FR-033, SPORTS-NFR-006
- Affected app / branch: sports_app / story/us-009-01-club-partner-relations
- Pull requests: None; uncommitted development adjustment
- Status: Verified / In Review

## Intended outcome and starting context

User requested filters and sortable columns, particularly Organization and Country. The previous table already offered country, priority, email-presence and text filters, but headers were not interactive.

## Policy decisions and plan

Keep the generic Boost shell unchanged. Filter and order native permission-aware Sports queries before pagination; accept only allowlisted sort columns/directions. Preserve management and Company access checks. Never sort friendly linked organization labels by opaque IDs.

## Work performed

relations_api.py accepts allowlisted per-DocType sorting and validated relationship filters, with stable name tie-break. Fetch one extra record to determine Next accurately; return 30 visible rows. relations.js adds clickable accessible header controls, direction arrows, clearer Organization or email search, Relationship filter and Clear filters. Sort/filter changes reset pagination; tab changes reset tab-specific state. Organization columns support name, country, sport, priority, relationship, public email and email-purpose ordering. Other tabs support their own title/type/status/date columns; linked organization labels remain unsortable. Updated requirements, PRD, story and guide.

## Commands and observations

- Development Python unittest discovery: 93 tests passed, including query allowlisting, combined filters, stable ordering, pagination and rejected invalid sort/status inputs.
- node --check: source and published JavaScript passed.
- Chromium fixture runner /tmp/qa_relations_sort.cjs: actual provider with public catalogue fixture passed header toggle, aria-sort, Next/reset, combined organization/country/email/relationship filters, clear filters, tab reset and 1440/390/320px contained layout checks. This was a local provider fixture, not an authenticated full-console browser session.
- Native read-only /tmp/qa_relations_sort_native.py on moyours.ideltatech.com: all 171 records paginated exactly once in each Organization/Country ascending/descending mode. Combined UK + United + published-email + Prospect query returned the expected two records. Transaction rolled back and connection closed.
- Published Sports assets, cleared development site cache and restarted only development web. HTTPS fetched relations.5012fe8ec290dd97.js matches source byte-for-byte.

## Verification evidence

| Acceptance criterion | Check | Result |
|---|---|---|
| Management/Company scope | Existing access gates retained; isolated access tests and Company-constrained native query | Passed |
| Full-directory sorting | Native name/country asc/desc pagination, deterministic tie-break | Passed, 171 unique rows per mode |
| Combined filters and usable table | Browser fixture, unit query assertions, native combined query | Passed |
| Safe input and clear sorting state | Allowlist rejection tests, keyboard-capable buttons and aria-sort | Passed |

## Decisions, deviations and recovery

No DocType/schema, business data, permissions, correspondence or finance changes. No QA accounts created or emails sent. Temporary verification fixtures contain public catalogue fields only. Existing uncommitted feature work preserved. Priority ordering uses the existing Select values 1–5/Unrated; staff assessment semantics unchanged.

## Remaining work and release impact

Published only to Moyours development. Live Boost unchanged; no commits, merges or pushes. Operators with the console already open should refresh to load the new content-addressed asset. Full external club outreach and consent-controlled player sharing remain separate backlog slices.
