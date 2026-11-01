# Console asset refresh and Boost-style documentation modals

- Date: 2026-11-01 (Africa/Lagos)
- Story / epic: US-002-04 / EPIC-002; US-003-02 / EPIC-003
- Requirements: SPORTS-FR-026, SPORTS-FR-028, SPORTS-NFR-006, SPORTS-NFR-009
- Branch: `story/us-003-02-player-numbering-and-enrollment`
- Status: Verified / In review

## Request and findings

User still saw the old mandatory Payer Customer control after migration and requested Development Tools match Boost's layout and modal popups. The old description is absent from current Sports source and the development asset symlink resolves to that source. Boost's v1 asset loader requests unchanged canonical asset paths with Frappe's version number, which need not change for an app-only edit. Existing browser caches can therefore retain the obsolete form. Migration does not replace a running page's JavaScript.

## Implementation

Sports now publishes immutable, content-fingerprinted JavaScript assets during install/migrate setup. The provider references those filenames, compatible with the existing host validator/loader. Changed source gets a new URL; earlier published files remain available to already-open pages. Canonical source files remain authoritative and generated releases are ignored by Git. A browser reload fetches the new provider manifest and fresh asset URLs.

Development Tools reuses the host's card, KPI and activity-tab styles without copying the shell. Document Open actions use a large Frappe dialog; links navigate inside that dialog, and unmount/close invalidate late loads. Role checks, sanitized Markdown and safe document-root access remain unchanged. Registration retains automatic per-player Customer creation, with no payer selector.

## Verification and release

- 59 Python checks pass: console/provider permissions, content-fingerprint changes and immutable prior content, settings/player policies and secure documentation access.
- Both existing Boost JavaScript regression suites, new JS syntax checks and Git whitespace checks pass.
- Ran the actual Sports install/migrate setup function on the development site to publish assets and clear caches, then reloaded the dev web worker. No schema migration was needed for this adjustment.
- Browser seeded an obsolete Players factory in memory, then loaded Players. The new fingerprinted script replaced it; no canonical `players.js` request was made. The form has no payer control, retains friendly program/group names, and a real registration still creates its own Customer. Native enrollment Customer field remains hidden. This tests an obsolete loaded factory, not an observation of the reporting user's private cache.
- Registration role, rollback and both concurrency cases pass with the existing real-site harness. Test-created Customers/contacts/categories and academy settings were cleaned/restored.
- Management browser check passes for six Boost-style cards, KPIs/tabs, modal open, relative document links inside the modal, close/reopen, activity search/log opening and traversal rejection. No inline article reader remains on the hub.
- Desktop and phone checked. Cards stack on phones; activity tabs wrap. Phone document width measured 375px within a 390px viewport, with document tables scrolling within the modal.
- All temporary QA accounts/sessions and business fixtures were removed in finally cleanup. Existing academy data and live Boost were preserved. No commit, merge, push or production release is included.


## Commands and evidence

```sh
python -m unittest sports_app.tests.test_console sports_app.tests.test_console_assets sports_app.tests.test_academy_settings sports_app.tests.test_players sports_app.tests.test_development_docs erp_boost.tests.test_console_providers erp_boost.tests.test_console_optional_dimensions
node ../erp_boost/erp_boost/tests/js/test_console_providers.js
node ../erp_boost/erp_boost/tests/js/test_journal_entry_duplicate_reset.js
node --check sports_app/public/js/development_tools.js
git diff --check
```

Python used the development virtualenv with both app roots on PYTHONPATH. Deployment helper `/tmp/publish_sports_console_assets.py` called `sports_app.console.setup_console`. QA used the previously authorized three temporary profiles through `/tmp/sports_players_site_qa.py`, plus focused `/tmp/sports_docs_site_qa.py` runs. Private temporary credential files were deleted. Test-only HTTPS certificate bypass remained necessary for the existing environment.

Published current URLs include `players.287491014e2b81e5.js` and `development_tools.3a8cada511ba3611.js` under `/assets/sports_app/js/releases/`. No Boost provider-contract changes were required. Future install/migrate hooks publish the latest source automatically; an already-open browser page still needs one reload to fetch its new manifest.

A modal test initially matched both its title and the document heading. Narrowing the test to the article fixed that ambiguity. Visual review then found the fixed desktop card grid could overflow phones; responsive columns and wrapping tabs corrected it, and the focused modal/phone checks were repeated successfully.

Artifacts: [registration](assets/2026-11-01-registration-fingerprinted.png), [cards desktop](assets/2026-11-01-development-tools-cards-desktop.png), [cards phone](assets/2026-11-01-development-tools-cards-mobile.png), [document modal desktop](assets/2026-11-01-development-tools-modal-desktop.png), [document modal phone](assets/2026-11-01-development-tools-modal-mobile.png).
