# US-003-02 — Private player registration and enrollment

- Date: 2026-11-01
- Branch: `story/us-003-02-player-numbering-and-enrollment`
- State: In progress — private direct-registration slice implemented; public application acceptance integration remains dependent on US-003-01.
- Target: `moyours.ideltatech.com`, independent development bench; Frappe 15.71.0.
- Guide: [Players and their Customers](../players-guide.md).

## Accepted prerequisite merges

At the user's request, committed settings and its optional-console prerequisite, then merged locally with merge commits. No remote push or production release:

| Repository | Story commit | Develop merge |
|---|---|---|
| Sports App | `7645fc3` — US-001-01 settings + Sports provider | `07136cf` |
| Independent development ERP Boost | `222df81` — sports_app:US-002-01 provider contract | `98e011f` |

The live Boost checkout remains clean and unchanged. Player implementation begins from Sports develop after that merge and remains separate review work on this story branch.

## Delivered private slice

- Sports Player: server-assigned permanent ID, original registration timestamp, configurable site numbering, name/DOB/contact/guardian data and immutable company/provenance. Native rename/merge is rejected.
- Sports Enrollment: player, derived company, program/group, derived player Customer, effective dates and status. No delete privileges are granted; native version history tracks edits.
- Registration API applies academy defaults and creates player plus initial enrollment atomically. UUID request key and payload fingerprint protect retries; database current reads and settings-row transaction locks serialize concurrent retries and naming defaults.
- Players console: bounded ID/name search, same-name warning, direct registration with configured defaults, paginated profile/enrollments, additional enrollment dialog and native forms for edits.
- Sports Registrar: unassigned operating role with master reads and private player/enrollment management, without accounting transactions or general Customer creation. Configuration roles also manage players. Basic Sports Console and Finance-only roles are denied. Native Company/User Permissions remain active.
- Existing enrollment history prevents moving used program/group scope. Disabled masters do not prevent withdrawing an existing enrollment.
- Each player has their own auto-created Individual Customer; no invoice/payment or copied balance is created.

## Verification

- 49 focused Python checks pass: Sports console/settings/player policies and Boost provider/optional-dimension regressions.
- Both existing Boost JavaScript suites pass; Players JavaScript syntax and Git whitespace checks pass.
- Development database backup completed before targeted model sync. Only the new player/enrollment schema and unassigned role/master permissions were installed, then development caches/web worker reloaded.
- Real backend checks: server-applied program/group/status defaults; initial enrollment rollback on invalid dates; same request returns one player; changed payload with a reused request key rejected; same-name players get distinct IDs; name correction preserves ID/timestamp; forced native ID rename denied; withdrawal and per-player Customer linkage verified.
- Two independent Python/DB processes: same-key simultaneous registrations return one ID; different-key simultaneous registrations receive unique IDs.
- Browser profiles: Sports-only and Finance-only cannot see Players and receive 403 from the listing endpoint; registrar sees Players without Finance initialization/transaction permission. UI registration, friendly program/group names, automatic Customer, profile, ID search and native edit-form navigation verified.
- Screenshots: [desktop](assets/2026-11-01-players-desktop.png), [phone](assets/2026-11-01-players-mobile.png).
- Temporary QA users, sessions, players/enrollments, program/group and auto-created Customers/contacts were removed in a same-run finally block. Original raw Academy Settings rows restored. No financial transactions created.

Commands used for focused unit checks (from the repository root, using the development virtualenv and both app roots on PYTHONPATH):

```sh
python -m unittest sports_app.tests.test_console sports_app.tests.test_academy_settings sports_app.tests.test_players erp_boost.tests.test_console_providers erp_boost.tests.test_console_optional_dimensions
node ../erp_boost/erp_boost/tests/js/test_console_providers.js
node ../erp_boost/erp_boost/tests/js/test_journal_entry_duplicate_reset.js
git diff --check
```

Site/browser QA used temporary `/tmp/sports_players_site_qa.py`, `sports_player_worker.py` and `sports_players_browser_qa.js`, with test credentials held in a private temporary file and deleted during cleanup. Browser tests use the existing HTTPS hostname with a test-only certificate bypass, as for settings QA.

## Findings and remaining work

Concurrency testing exposed repeatable-read snapshot staleness after a transaction waited on the settings lock. Retry lookup and existing-document reload now use current locking reads. A UI check exposed asynchronous program onchange clearing the configured group; defaults are now applied in order. Browser selectors were narrowed to the native form after hidden dialog inputs caused a test ambiguity. Final runs pass and cleanup is confirmed.

Public application submission/review and acceptance are US-003-01. Full role boundaries remain US-001-03; profile financial/attendance histories and performance acceptance remain US-003-03 and their source modules. Effective fee plans, player invoice attribution and receipts remain EPIC-004/005. These dependencies are not marked complete by this slice. Academy staff must choose real setup values after QA restoration. No player changes are merged into develop yet.


## User refinement — one save, one Customer per player

The user rejected manual Customer selection and shared-family accounts. Added a unique, read-only Customer link to Sports Player. Player insertion creates the Customer and primary contact from validated name/email/phone; enrollment derives the same link. API allowlists reject supplied Customer/payer references, native forms reject reassignment, and duplicate names still create separate Customers. Existing site audit found zero players/enrollments, so no business-record reassignment was needed.

Customer creation is a narrow, role-checked service permission, not a general registrar Customer/Contact write grant. It respects ERPNext Selling Settings defaults, with existing Individual group and company-country territory fallbacks. Missing classifications require administrator setup; no global selling configuration was changed.

Program and Group metadata now enable title display in Link fields; profile rows resolve permission-filtered names. Schema sync and cache clearing make these names available after page reload.

Integration testing found that ERPNext 15 Contact.after_insert commits while linking telephone call logs. Contacts are now inserted without phones, then their phone is added on update, preserving the surrounding registration transaction. Invalid enrollment tests verify no orphan Customer or contact remains; concurrent same-key registrations reuse one player/Customer, while separate same-name players receive distinct accounts. App-owned Customer keys derive from the immutable player ID (`SPORTS-CUST-<player ID>`), avoiding ERPNext name-suffix snapshot collisions during simultaneous same-name registrations; the Customer display name remains the player name. New unit checks cover role denial and API/native Customer-reassignment rejection. Final verification: 49 unit checks, live rollback/contact-detail checks (including phone-only), both concurrent registration cases and all three browser role profiles pass. Cleanup verified zero remaining QA players, enrollments, Customers, contacts, users or sessions. [Updated registration form](assets/2026-11-01-player-registration.png).

## Subsequent program-category and documentation adjustment

Customer classification and native field visibility were refined after this initial slice. Current behavior creates a program-named Customer Group, records the initial registration program, and hides the derived enrollment Customer field. The previous Individual-group fallback described above is superseded; Customer type remains Individual. See the [separate dated adjustment log](2026-11-01-us-002-04-guardrails-docs-and-program-categories.md) for current implementation, 57 checks, browser evidence and cleanup.
