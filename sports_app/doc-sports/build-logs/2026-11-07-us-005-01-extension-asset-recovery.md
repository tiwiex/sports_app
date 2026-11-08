# Build log: Scholarships & Billing extension asset recovery

- Date: 7 November 2026 (Africa/Lagos)
- Story / epic: US-005-01 / EPIC-005; console delivery support
- Requirements: SPORTS-FR-011/012, SPORTS-NFR-003
- Affected apps / branch: Sports App only / story/epic-004-scholarships-and-monthly-billing
- Pull requests: None requested.
- Status: Verified development fix

## Intended outcome and starting context

User reported This extension could not be loaded after interrupted checkbox work. Local diagnosis found the source-derived subscription_console JavaScript URL referred to a release file that had never been published. JavaScript syntax checks passed.

## Policy decisions and plan

Repair only Sports assets and native development web delivery. Preserve accounting records, roles, existing scheduler settings, Community App and Boost. Ensure every advertised content-hashed asset exists completely before its URL is returned.

## Work performed

Published the missing bundle. console_assets.asset_url now ensures its allowlisted source bytes are published before returning a URL. Publication uses an atomic temporary-file rename, retains old immutable versions for open pages, and repairs damaged or web-unreadable release files. Public JavaScript releases use 0644 permissions so the separate web-server process can serve them. No arbitrary filenames are accepted.

## Commands and observations

An initial atomic-file check exposed temporary-file default 0600 permissions as HTTP 403; fixed publication to set public static-asset mode before rename and repair older unreadable output. A transient indentation error was caught by lint, corrected and rechecked before final publication. Final pinned lint passed. Full isolated suite: 249 passed, including missing/new/damaged release recovery, old-version retention, safe names, temporary-file cleanup and file permissions.

Actual-source subscription desktop/phone fixture passed Overview/Payments and checkbox invoice/payment/reversal controls. Sports-only assets were published, development cache cleared and only development web restarted. Final verified HTTPS checks returned HTTP 200 with exact JavaScript bytes for every Scholarships & Billing provider asset. Native configuration, overview and retained test-player grid all loaded successfully without mutations.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Provider never advertises missing new bundle | Temporary-directory source-edit regression | Passed |
| Static asset readable/complete | Atomic publication + 0644 regression + HTTPS exact bytes | Passed |
| Billing content loads | Native read APIs + desktop/phone fixture | Passed |
| Existing test finance preserved | Rollback QA and retained January invoice | Passed; January remains unpaid |

## Decisions, deviations and recovery

No Boost shell changes or approval bypasses. The previous interrupted task's usage-limit review failure is historical; this fix's approved actions were publication, development restart, read-only checks and rollback-only QA.

## Remaining work and release impact

Fix published on the development site. Users should reload the console to fetch its manifest. No production deployment, schema migration, role grants, scheduler changes, commit, PR or merge. The separately requested synthetic January fixture remains intentionally available.
