# Build log: US-001-01 academy and program settings

- Date: 2026-11-01
- Story / epic: US-001-01 / EPIC-001
- Requirements: SPORTS-FR-001, SPORTS-FR-006
- App / branch: Sports App, `story/us-001-01-academy-and-program-settings`
- Status: Verified development implementation / accepted for local develop merge
- Pull request: Not opened; user requested local commit and develop merge. No remote push requested.

## Starting context

The Sports console provider from US-002-01 already exists as uncommitted review work. This story preserves that work and adds configuration in Sports App only. The independent dev Boost checkout is unchanged by this story; the original live Boost checkout remains clean.

## Work performed

- Added Sports Academy Settings (Single), Sports Program and Sports Group, with native administrator forms and server-side validation.
- Added a permission-checked Academy Settings console view, program/group dialogs, save/read-back, registration preview and stale-save detection.
- Created the unassigned Sports Academy Administrator role. It receives configuration access and read-only Company/Currency master access, with native company User Permission restrictions. It receives no accounting role or transaction rights.
- Added explicit program/group company and enabled-state checks, protected defaults and company-move checks.
- Required academy name, company, currency, valid timezone, prefix/digits, program and enrollment status; enforce positive monthly fee when enabled and reject negatives.
- Preserved Sports-only overview access and filtered the settings menu and endpoints by configuration authority.
- Declared ERPNext as the linked-master prerequisite; kept Boost optional for native setup.
- Added [academy setup instructions](../academy-setup.md).

## Policy boundaries

One academy per site is the implemented configuration. Sports/program names are configurable. Default group is optional but must belong to the selected default program when set. A default monthly fee is a future fee-plan input, not an invoice or posting instruction. Disabled monthly fees permit zero; enabled fees require a positive amount. Existing player IDs are not allocated or renumbered in this story.

Actual company, program/group, timezone and pricing choices are left for academy staff; no invented academy policy is persisted by QA. Future enrollment/billing stories must validate their own authorization and the applicable configuration before acting.

## Deployment evidence

- Target: `moyours.ideltatech.com` in `frappe-bench-dev`.
- Database backup completed before schema sync: `20261101_121358-moyours_ideltatech_com-database.sql.gz` in the site's private backups.
- Ran role creation, targeted Sports schema sync, console/master-permission setup and site cache clearing. Reloaded the development web process for new Python endpoints. Unrelated historical migrations were not run.
- Existing users were not assigned the new role. Live Boost was not modified or migrated.

## Verification

| Acceptance / boundary | Evidence | Result |
|---|---|---|
| Configurable academy fixtures | Unit fixtures cover different academy names, companies, sports, NGN/EUR, Lagos/Berlin timezones and prefixes/digit counts | Pass |
| Installed model roundtrips | Real Football and Swimming configurations, program/group links, timezones and prefixes saved/read back on the dev site; transaction rolled back | Pass |
| Unauthorized company | Unit API/company denial plus native Frappe company-permission evaluation using an in-memory out-of-scope Company and permission fixture; no extra Company or User Permission record created | Pass |
| Required/invalid defaults | Missing company/program, timezone, numbering, enrollment status, fee opt-out/invalid amounts, cross-company program and mismatched group tests | Pass |
| Role boundaries | Basic Sports user has no settings menu and gets 403 from configuration API; configuration-only operator reaches settings without accounting roles | Pass |
| Browser workflow | Program/group dialogs, form save and persisted read-back; desktop and 390px phone screenshots | Pass |
| Regression | Combined 42 Python checks, provider JavaScript suite and existing Journal Entry duplicate-reset JavaScript suite | Pass |
| Cleanup | Backend fixture transaction fully rolled back; original Single rows restored; browser test masters deleted; all temporary accounts deleted and sessions revoked | Pass |

The live scope check uses synthetic permission input with actual Frappe permission evaluation, not a second persisted Company. The separate pure fixtures validate NGN/EUR; database roundtrips use the site's enabled currency. No financial posting was tested or created.

## Verification recovery

Browser testing exposed a missing Currency read permission for configuration-only users; role setup now grants that master read permission. The test helper also needed to exclude editable dialogs from its notice-dismiss handler and wait for asynchronously mounted controls. Backend fixture rollback-to-savepoint retained naming-series locks; the corrected helper ends the transaction fully before browser writes. A leftover test-owned program was audited and removed before another QA cycle; final cleanup explicitly asserts no QA programs/groups/accounts remain.

Browser tests use the site's normal nginx URL. Its existing expired certificate requires a test-only certificate bypass; renewal is an existing environment follow-up. The configuration-only path makes no Finance initialization requests and avoids requiring unfinished finance workflow setup.

## Review and remaining work

User confirmed settings works and accepted local commit and develop merge on 2026-11-01. Program/group setup is available in the menu, while actual academy policy remains unset after test restoration. US-001-02 covers publishing the configurable website; US-001-03 expands the broader sports permission model. Player ID issuance/enrollment behavior and effective fee plans/billing remain their own stories.


## Follow-up: existing System Manager could not load settings

The reported failure was reproduced with the site's existing System Manager profile, which had no Company restrictions but lacked Company read access under the active custom permission matrix. Original QA covered Administrator (which bypasses permission checks) and the dedicated Sports role, leaving this profile untested. Role setup now supplies read-only Company/Currency master access to both supported configuration roles, preserving explicit Company User Permissions and existing custom rules.

An unsaved Single also inherited the global Company through Frappe's new-document defaults. Configuration loading now uses saved values or schema defaults only; an unconfigured company/currency stays blank rather than being treated as an academy selection. Saved values are preserved. Save and dependent-operation company checks remain enforced.

Verified `get_configuration` under the existing affected user's role profile: the view data loads, permitted academy companies are available, and unsaved company/currency values remain blank. No personal role assignment or academy policy was changed. Added three regression checks covering both administrator roles, blank settings and preservation of saved values; the final combined suite has 45 passing Python tests. Reloaded only the development web process.
