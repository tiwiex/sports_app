# Build log: CoA balance display and console readiness repair

- Date: 2026-11-01 (Africa/Lagos)
- Related story: US-001-01 / EPIC-001; development ERP integration compatibility
- Requirements: SPORTS-FR-001, SPORTS-NFR-009
- Apps/branches: development ERP Boost / develop; Sports documentation / story/us-005-01-enrollment-payment-review
- Status: Verified / In review; explicitly approved repairs applied on development
- Site: moyours.ideltatech.com

## Intended outcome and findings

User reports missing CoA balances with the setting enabled and concerns about stability. Read-only checks establish:

1. Accounts Settings `show_balance_in_coa` is 1. The native API returns five root account balances, including existing non-zero values. Administrator's server and fresh boot capabilities include Account/GL Entry read. The selected finance user's native accounting roles are present, but GL Entry read is absent in both server and fresh boot permissions. ERPNext Account tree returns immediately before fetching/drawing balances when GL Entry is absent from boot.can_read.
2. The earlier Account repair restored Account rows only. GL Entry is a separate custom permission matrix: it contains four Boost-specific read rows and omits the three standard native accounting/auditor rows. Missing native rows are the same setup pattern as the earlier Account issue; no existing explicit restriction needs overwriting.
3. Recent console SQL errors originate from `get_boost_console_documents` selecting Purchase Invoice.workflow_state even though Purchase Invoice has no workflow column. A read-only audit of every enabled console select list found only that missing workflow field plus the already-guarded optional business_unit columns. No workflow should be invented merely to make a list load.
4. Database SELECT 1, cache PING and the development web worker are healthy. The Redis cache supervisor entry is FATAL because cache and socketio configuration both bind port 13003; the socketio-named Redis process is serving that port successfully. The duplicate-start log dates to 18 October. No service was stopped or reconfigured during diagnosis. This supervision issue is separate from the reproduced display/SQL defects and remains maintenance work.

## Prepared repair and verification

During diagnosis, a review-only patch was prepared at `/tmp/moyours-balance-repair-review/repair.patch` without app/site changes. After explicit user approval, this patch was applied and the workflow-filter validation was completed for dictionary and list formats. It restores only missing actual native GL permission rows (preserving custom restrictions), adds install/migrate/setup protection, and makes workflow_state an optional console select column without mutating the shared definitions. A workflow filter on a doctype without that column receives a setup message instead of a SQL exception. No transaction, workflow or schema creation is proposed.

Eight isolated tests passed against the prepared modules loaded from /tmp, including the existing Account preservation tests, GL baseline scope and present/absent optional columns. No database test mutation, new QA account/session or financial posting was needed for diagnosis. Existing unrelated working changes remain untouched.

## Approval and release impact

Automatic approval review rejected applying the repair because the request was interpreted as diagnosis, without approval for persistent GL role-permission/shared-console changes. No rejected action was executed indirectly. Only review artifacts and this diagnostic documentation were created. That diagnostic turn ended pending approval. The user subsequently explicitly approved applying and verifying both repairs; the completed work and evidence follow. No changes were made before approval.


## Approved completion — 1 November 2026

### Work performed

- Generalised the existing missing-native-permission helper for Account and GL Entry, retaining the Account entry point. Added a GL helper to install/migrate and report-permission setup so console reference rules do not mask native GL permissions on new sites.
- On Moyours, copied exactly three missing native GL permission rows from the installed ERPNext baseline: Accounts Manager, Accounts User and Auditor. All four existing Boost-specific GL rules were unchanged; no explicit custom restriction was overwritten. No new roles were assigned to any real user.
- Updated `get_boost_console_documents` to omit absent business_unit/workflow_state columns from its query-specific field list while preserving shared definitions and installed fields. Filters for an absent workflow are rejected with a clear setup message before any SQL query; installed-workflow filters remain intact. No Purchase Invoice workflow or schema column was created.
- Refreshed only the development web worker. Left the separate Redis supervision configuration unchanged.

### Verification evidence

- 14 focused tests passed across Account/GL permission preservation, optional dimension/workflow columns, absent/present workflow filters, the existing User role-editor repair and approver schema compatibility. `git diff --check` passed.
- Native site checks: Administrator and the selected finance user now have GL read in fresh boot and server checks. Sports Console, Sports Registrar and Sports Academy Administrator role-only checks still deny GL read.
- Exactly three native GL rows added; four existing custom rows matched their pre-repair snapshot. Re-running the helper returned false, with no duplicate rule.
- Existing root ledger balances and Account, GL Entry, Payment Ledger Entry, Sales Invoice and Payment Entry counts matched before and after the repair. No accounting records were created, edited or posted.
- Real browser verification with a temporary QA user carrying the relevant native accounting roles: all five CoA root balance labels rendered, including existing non-zero balances. Fresh boot included GL Entry read and there were no JavaScript errors.
- Browser requests to Purchase Invoice, Sales Invoice, Payment Entry and Journal Entry console lists each returned HTTP 200. The actual Purchase Invoice query omitted the absent workflow field. The selected real finance user's four lists were also checked in a native server session without changing its password or creating a session for it.
- Local browser screenshot `/tmp/moyours-coa-balances-restored.png` was visually inspected. It contains current academy balances and is kept local rather than exposed through the Sports documentation hub.

### Cleanup, impact and remaining maintenance

Temporary QA sessions were revoked and the account/password file removed. One automatically created, unlinked QA Contact was also removed; final checks found no matching QA user or Contact Email records. No QA invoices or receipts were needed. The GL permission metadata snapshot is `/tmp/moyours-gl-permissions-before.json`; it contains permission metadata only.

Real users must reload Desk (or log out/in if the old boot data remains) to pick up restored GL display capability. Install/migrate/setup hooks make the permission repair durable; existing custom restrictions remain authoritative. Both app changes are uncommitted alongside the preserved earlier development work. The live Boost checkout is unchanged; no commit, merge, push, full migration or production deployment was performed.

The pre-existing duplicate Redis cache/socketio port supervision issue remains separate maintenance work. Database and active cache checks passed. These two verified repairs address the reported balances and reproduced SQL list failure; they do not constitute a full production-readiness or infrastructure sign-off.
