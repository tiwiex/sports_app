# Player self-service Users and restored User role editor

- Date: 2026-11-01 (Africa/Lagos)
- Story / epic: US-003-02 / EPIC-003; access foundation US-001-03 / EPIC-001
- Requirements: SPORTS-FR-021, SPORTS-FR-026, SPORTS-FR-029, SPORTS-NFR-002, SPORTS-NFR-003, SPORTS-NFR-009
- Apps: Sports App and independent development ERP Boost
- Branches: Sports `story/us-003-02-player-numbering-and-enrollment`; Boost `develop` (local uncommitted correction)
- Status: Verified / In review

## Request and policy

User reported missing Roles on the native Administrator User form and requested an automatic User for future player self-service. User explicitly selected requiring a unique email for new player registrations.

The active custom User permission matrix had only Boost Admin at level 0. Core System Manager level-0 and level-1 permissions were masked. Frappe's role-editor gate derives eligible roles from writable level-1 User permissions; an empty set hides the editor even for Administrator.

Automatic approval review rejected an initial proposal to grant Boost Admin new level-1 powers. No rejected edit executed. The accepted safer correction restores only the existing core System Manager DocPerm baseline into the custom matrix; no Boost role gains additional user-administration powers.

## Implementation

- Boost repairs the standard System Manager baseline on install/migrate and after the existing access-control setup patch; no core Frappe edits or live checkout changes.
- New players require one valid, normalized, unused email. Existing User accounts or existing player emails are rejected for administrator review rather than silently linked/reassigned.
- A read-only unique User link is created with player/Customer/Contact/enrollment. The generated account is a disabled Website User with the non-Desk Sports Player marker role. No staff, Customer portal or accounting roles; no welcome mail/password/invitation sent.
- Customer's existing Contact links to the User. Future portal activation, authenticated own-record endpoints and email-change workflow remain separate work.
- Registration scopes after-commit callbacks so failed savepoint operations cannot enqueue jobs for rolled-back User records. Native request failures still receive Frappe's full rollback.

## Verification, cleanup and deployment

- 66 focused Sports/Boost Python tests passed (`python -m unittest` across console, assets, academy settings, players, documentation, provider/dimensions and User permission repair). The initial invocation from the package directory shadowed imports; rerunning from `/tmp` passed.
- Both Boost JavaScript regression suites passed: provider lifecycle/access and Journal Entry duplication. Both app diffs passed `git diff --check`; Sports player/documentation JS syntax checks passed.
- Development-site registration QA passed: required/unique email, staff-email rejection, disabled Website User with only Sports Player, no password/auth entry, no Desk or financial/player read permission, Contact linkage, atomic rollback including User/category, repeated requests, same-name distinct players and concurrent same/different-key registrations.
- Desktop/phone browser registration passed with required email, no payer selection, friendly program/group labels, User link, native form and profile. Sports-only and Finance-only users remained denied player access. Documentation card/tab/modal browser regressions passed.
- Native Administrator User form showed **71 role controls** when viewed by a temporary System Manager. No actual Administrator login/password or role assignments were changed. Screenshot: [User role editor](assets/2026-11-01-user-role-editor.png).
- Applied targeted Sports schema/role sync, published fingerprinted assets, restored development User permission baseline and restarted only the development web worker. Standard System Manager is the only writable level-1 User role; Boost Admin level-1 row count remains zero. Live Boost checkout is clean.
- All temporary staff accounts, generated player Users, sessions, players, enrollments, Customers, Contacts and fixture masters were removed; academy settings restored. Browser credential files removed. No welcome email or account activation sent.

## Decisions, deviations and recovery

ERPNext's User update hook infers a Customer portal role from matching Contact email. Initial integration QA exposed its nested save and notification-permission failure. Provisioning now temporarily uses ERPNext's supported `frappe.flags.setting_role` guard, restores its original value in `finally`, and verifies the resulting account has no extra role/Desk access. A regression test verifies the flag is restored even on failed creation. Core behavior outside this bounded operation is unchanged.

## Remaining work and release impact

Existing users/players are not backfilled, and no real accounts are activated. Portal activation, own-record authorization and email-change review remain separate work; the wider role-boundary story is not complete. Account email changes are currently blocked after linking. This adjustment is uncommitted, with no merge or push. Source helper/hook changes are required in the independent development Boost checkout as well as Sports. Migration reapplies the permission baseline and publishes Sports assets; reload an already-open browser tab.
