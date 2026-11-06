# Build log: Players table and profile layout

- Date: 2026-11-03 (Africa/Lagos)
- Story / epic: US-003-03 / EPIC-003; related US-003-02
- Requirements: SPORTS-FR-005, SPORTS-FR-004/006, SPORTS-NFR-005/006/007
- Affected apps / branches / versions: Sports App, `story/us-003-03-player-profile-layout`, based on `48fb0a2`; existing pending work preserved.
- Pull requests: None; no commit, merge or push performed.
- Status: Verified development presentation slice

## Intended outcome and starting context

User requested Players match Enrollments. Previously opening a player replaced the list with a flat profile and plain membership table.

## Policy decisions and plan

Reuse the Boost table/reference menu conventions and Frappe modal; keep Sports-owned rendering and APIs. Preserve one automatic Customer per player, existing permission/company checks and membership creation. This refinement does not finish the complete linked-history story.

## Work performed

- `public/js/players.js`: bordered sortable list, Player ID reference menu, View and permission-scoped New program enrollment actions. Grouped responsive profile modal retains list/search, with identity, linked accounts, paginated program memberships, player/guardian/emergency contacts and explicit consent choices. Friendly dates/program/group names and native record links retained.
- `players_api.py`: allowlisted server sorting with stable pagination; profile shared-field metadata; capability requires both enrollment-create and player-write. Existing role, company, document-read and private field allowlists retained. Action rechecks permission before opening membership creation.
- Added focused Python presentation checks and repeatable Chromium fixture; aligned PRD, requirements, player guide and affected stories.

## Commands and observations

- Python unittest discovery: 116 tests passed.
- `node --check sports_app/public/js/players.js` and `git diff --check`: passed.
- `test_players_browser.cjs` using installed Playwright/Chromium: passed at 1440px and 390px.
- Native read-only Moyours API check: sorted list, profile metadata/capability and Guest denial passed; connection rolled back.
- Published `players.88a6981f44d000b2.js`, cleared development cache, restarted development web workers. HTTPS response 200 matched source bytes.

## Verification evidence

| Acceptance criterion / refinement | Check / artifact | Result |
|---|---|---|
| Search/list and identity presentation | Browser sorting, reference/keyboard menu, retained search/list | Passed |
| Grouped profile and memberships | Modal sections, explicit negative consent, pagination, add-membership payload/refresh | Passed with Dialog/API fixture |
| Responsive layout | [Desktop](assets/2026-11-03-player-profile-1440.png), [Phone](assets/2026-11-03-player-profile-390.png) | Passed; synthetic fixtures |
| Permission boundaries | Python allowlist/sorting/capability tests; browser read-only menu and fresh denial; native Guest denial | Passed for changed scope |
| Whole US-003-03 | Payment/attendance history aggregation and pilot latency | Not completed by this slice |

## Decisions, deviations and recovery

Browser fixture uses the actual Players JS, shared registration field definitions and Boost CSS with stubbed Frappe Dialog/API. It verifies presentation/interaction, not a full authenticated admission or finance transaction. No real membership or payment was created for this adjustment. Existing pending attendance, club and enrollment work was preserved.

## Remaining work and release impact

Available on Moyours development after console reload. No DocType/schema migration, account/role changes or live Boost edits. No QA accounts created; native checks rolled back and browser fixtures are synthetic. Full financial/attendance histories, broader privacy roles and agreed pilot-volume performance remain future story acceptance work. Documentation is discovered through the existing management-only Development Tools allowlist.
