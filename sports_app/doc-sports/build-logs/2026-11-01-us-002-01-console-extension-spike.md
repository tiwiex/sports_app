# Build log: US-002-01 console extension spike

- Date: 2026-11-01
- Story: sports_app:US-002-01 / EPIC-002
- Requirements: SPORTS-FR-020, SPORTS-NFR-001
- Branch in both apps: `story/us-002-01-console-extension-spike`
- Pull requests: Not opened; local changes available for review.
- Status: Verified development prototype / story accepted for local develop merge.

## Outcome and scope

Implement a generic installed-app provider interface in ERP Boost and a minimal Sports-owned overview, with one staff route and separate app ownership. No player, invoice, payment or attendance data is created by the sample.

## Work performed

- Host manifest validation, per-request installed-app discovery and role/callback authorization, safe diagnostics and failure isolation.
- Bootstrap separates shell entry from Finance access; finance initialization is deferred until authorized and failures expose no fallback finance views.
- Lazy app assets use network error and timeout handling without global UI freeze; mount/unmount, abort and stale-load handling isolate views.
- Sports supplies its own hook, role, optional host setup, login redirect and placeholder UI.
- Dynamic Page roles avoid exporting client roles into Boost's generic JSON.
- Restored the pre-existing missing Boost `__version__` to `0.0.1`, matching installed package metadata, so editable installation works.
- Documented v1 contract (`erp_boost/docs-boost/concepts/console-provider-contract.md`) in the host repository. Cross-bench deployments must use their own checkout paths.

## Selected demo site and installation

The user selected `moyours.ideltatech.com`, initially installed with Frappe, ERPNext and Sports App. Frappe is 15.71.0 in this bench; the original Boost bench uses 15.68.1.

1. Database backup completed: `20261101_114036-moyours_ideltatech_com-database.sql.gz` in the selected site's private backups; no backup contents exposed.
2. Bench soft-linked the existing Boost repository into the development bench. Initial editable installation failed because the package lacked a version; version restoration resolved it.
3. Completed Bench app registration without overwriting source or restarting the original Boost bench.
4. Installed `erp_boost` on the selected site. The first install did not import models; a targeted `frappe.model.sync.sync_for("erp_boost")` imported the missing Page/DocTypes without running historical migration patches.
5. Ran `sports_app.console.setup_console`, built assets for both apps, cleared the selected site's cache and reloaded the development web process to recognize the new package.
6. Read-only live bootstrap returned the Sports overview with Finance enabled for Administrator and no provider diagnostics; HTTP ping returned `pong`.

## Verification evidence

| Area | Evidence | Result |
|---|---|---|
| Contract, validation and isolation | Host unit suite covers valid/invalid versions, namespace/assets, denied roles, disabled and failing providers, mixed/finance-only bootstrap, page roles and finance guard | Pass |
| Separate installation | Host tests use an internal fixture, with no Sports import dependency; Sports tests cover setup without Boost | Pass |
| Sports setup and redirect | Role manifest, optional host, role creation and preservation of explicit login redirect tests | Pass |
| Existing Finance behavior | Optional-dimension Python regression tests and Journal Entry duplicate-reset JavaScript regression test | Pass |
| Client lifecycle | Node VM tests exercise Sports-only/no-finance initialization, mixed roles, mount/refresh/unmount, abort, stale assets, cleanup failures, asset cache/retry and fail-closed bootstrap | Pass |
| Test-site role and browser journeys | Sports-only, Finance-only and mixed roles; details below | Pass |

The final combined Python run has 31 passing tests in the independent development environment. The same initial suite passed on the original Boost environment. Runtime financial posting, invoice approvals and broader company/navigation regressions belong to US-002-03 and subsequent delivery; no real transaction was created for this spike.

## Temporary-account controls

The user explicitly approved three temporary Sports-only/Finance-only/mixed-role accounts for browser checks with immediate session revocation and deletion. The runner creates them only inside a try/finally workflow; cleanup runs on failed assertions, browser errors and subprocess timeouts. Credentials are stored in a mode-0600 temporary file, never printed, and removed in cleanup. The first site attempt identified the missing Page and confirmed successful account/session cleanup.

## Remaining work

User accepted local commits and merge into develop on 2026-11-01. No remote push or production release is included. Full Sports workflows, richer context and wider Finance regression remain subsequent stories. ADR-0001 is accepted for the development prototype; production rollout remains US-002-02/03.


## Checkout correction and baseline evidence

The initial development link pointed into the live Boost checkout. On the user's clarification, this was replaced with an independent clone and all 10 story files were transferred and byte-verified before restoring live source.

| Checkout / branch | Baseline | Final condition |
|---|---|---|
| Original live Boost: `us-009-05-payment-entry-stabilization` | `36912af22b7030dbd77e8eb5ce55013feb2466c3` | Restored clean; no story edits |
| Independent dev Boost: local `develop` | Same `36912af` | Advanced only in dev to preserve the six newer commits |
| Independent dev Boost: `story/us-002-01-console-extension-spike` | Same `36912af` | Story changes retained for review |
| Original live repository's local `develop` | `8200371e949a6908befce5e018e267bf473e07cd` | Unchanged; six commits behind live baseline |
| Sports: `story/us-002-01-console-extension-spike` | `97794ff03fcdb8eaa421e88043b7664cc876bace` | Separate app and story changes |

Development Python import and asset paths now resolve into `/home/frappe/frappe-bench-dev/apps/erp_boost`. Development web/workers were reloaded after re-registration. The original live bench was not restarted or migrated. A source transfer snapshot is retained in `/tmp/sports-boost-checkout-transfer` for recovery.

## Final browser and live-site evidence

The headless Chromium run used the site's normal nginx URL. The existing expired TLS certificate required a test-only `ignoreHTTPSErrors` option; renewal remains an environment follow-up. Raw gunicorn-port attempts could not load nginx-managed static assets and were replaced with the normal site URL.

- Sports-only: one navigation view (`sports_app:overview`), rendered sample, Refresh works, no Finance initialization API calls; direct finance summary request returned 403.
- Finance-only: 54 allowed navigation items; no Sports contribution; normal finance initialization remains enabled.
- Mixed: 55 allowed navigation items; expanding Sports and selecting its view renders app-owned content inside the same shell.
- No browser JavaScript errors in the three tested journeys. Existing exchange-rate reminder was closed through its normal UI.
- All temporary QA accounts were deleted and their sessions revoked after every attempt; private credential file removed in finally.
- Screenshots are captured as development evidence in `assets/`.

Initial Finance startup raised `Unknown column workflow_state` on this fresh site. A dev-only guard now counts native drafts without querying absent workflow columns and returns an explicit `workflow_setup_missing` notice; missing approver metadata never broadens scope. The site's invoice approval policies were not silently enabled. Read-only summary, bank-account and voucher-type startup methods now pass. Finance role defaults were initialized using the existing seed function for the initially empty matrix. Broader workflow setup and transaction acceptance remain separate work.

## Final checks

- 31 Python tests passed: provider/permissions/fresh-workflow guards, Sports setup/login, optional dimensions, installation roles and website-access regressions.
- JavaScript provider/lifecycle/asset failure tests passed.
- Existing Journal Entry duplicate-reset JavaScript regression passed.
- Both repositories pass `git diff --check`.
- No invoices, payments or attendance records were created by this spike.
