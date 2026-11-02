# Build log: Restore native Chart of Accounts permissions

- Date: 2026-11-01 (Africa/Lagos)
- Related story / epic: sports_app:US-001-01 / EPIC-001; shared ERP setup compatibility adjustment
- Requirements: SPORTS-FR-001; preserve native ERP permissions and narrow Sports access
- Affected apps / branches: development ERP Boost / develop (uncommitted); Sports documentation only
- Site: moyours.ideltatech.com, independent development bench
- Pull requests: None
- Status: Verified / In review

## Intended outcome and starting context

Administrator saw Details and View Ledger but no Edit, Delete or Add Child in the native Account tree. Server permission checks allowed all four actions, while a freshly built Administrator boot payload reported Account write/create/delete false. The company has no parent company, so this was not a consolidated-company restriction.

## Policy decisions and plan

The user explicitly approved repairing development ERP Boost and the Moyours site, adding regression coverage/logs and verifying child-account creation. An earlier automatic review declined mutation while only diagnosis was authorised; implementation began after explicit user approval.

Frappe replaces the entire DocPerm matrix when Custom DocPerm rows exist. Boost reference-read setup inserted custom rows without retaining native Account rules. Repair only missing standard Account rows, copying their actual DocPerm values and identifying them by role, permission level and owner condition. Preserve every existing custom rule, including deliberate restrictions. Do not grant accounting write rights to Sports or Boost-only roles. Do not touch invoice/payment permissions.

## Work performed

- Added `erp_boost.permissions.account.restore_missing_account_permissions`.
- Added install/migrate hooks for existing installations and called the helper before Account reference-read setup for new configurations.
- Invalidate Account metadata and cached boot payloads when rows are added; repeated calls do nothing.
- Added four tests covering native rights, unchanged existing restrictions, no invented baseline and permission-level/owner matching.
- Applied the helper on the authorised development site: five missing ERPNext rows restored (Accounts User, Accounts Manager, Auditor, Sales User, Purchase User); all 17 pre-existing custom rows were identical afterward.
- System Manager's existing custom read-only row was preserved. Administrator receives full browser capabilities from the restored native accounting roles; no artificial Administrator/System Manager rule was invented.

## Commands and observations

- `python -m unittest erp_boost.tests.test_account_permissions erp_boost.tests.test_user_role_editor erp_boost.tests.test_payment_approver_schema -v`: 8 tests passed.
- Real site checks: fresh Administrator boot contains Account read/write/create/delete; second repair run returns false with no duplicate rows.
- Native `erpnext.accounts.utils.add_ac` created a temporary child under the academy Asset root without ignore-permission flags; save/edit and delete also succeeded. Rolled back the entire QA transaction after committing the permission repair.
- Account count, GL Entry count, Payment Ledger Entry count and the full academy Account tree (names, parents, lft/rgt) matched the pre-QA snapshot after rollback. No QA account remains.
- Evaluated the installed native Frappe tree toolbar and ERPNext Account toolbar conditions using verified site capabilities: Edit, Delete, Add Child and View Ledger are available; Details is absent. This was a JavaScript logic check, not a logged-in end-to-end browser session.
- Role-only checks against real effective Account metadata: Sports Console and Sports Registrar have no Account access; Sports Academy Administrator, Boost Viewer, Boost Admin and Boost Finance Manager remain read-only. Accounts Manager has the native read/write/create/delete rights. Role combinations continue to aggregate under Frappe's normal rules.
- `git diff --check` passed for development ERP Boost.

## Data impact, cleanup and recovery

Only the five missing standard Account permission rows were committed on the development site. No accounting transaction or account-tree change persisted. Existing custom-row snapshot is held at `/tmp/moyours-account-permissions-before.json` for comparison; it contains permission metadata, not credentials or player records. No QA users, passwords, messages or sessions were created. Existing unrelated changes were preserved.

## Remaining work and release impact

Users must reload Desk to obtain fresh boot permissions; log out/in if the old tree is still displayed. The code is uncommitted and must accompany a later reviewed development release to keep the repair durable across site setup/migration. The live ERP Boost checkout is unchanged. No full migration, production deployment, commit, merge or push was performed. Other DocTypes' custom matrices were not reset or broadened.
