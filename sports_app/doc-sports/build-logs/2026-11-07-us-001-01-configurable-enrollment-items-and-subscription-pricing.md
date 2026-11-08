# Build log: configurable enrollment Items and native subscription pricing

- Date: 2026-11-07 (Africa/Lagos)
- Stories / epic: US-001-01, US-003-01, US-004-02/03 / EPIC-004
- Requirements: SPORTS-FR-001/003/008/009/010/031; SPORTS-NFR-003/007
- Affected app / branch: Sports App / `story/epic-004-scholarships-and-monthly-billing`
- Status: Verified development refinement; EPIC-004 stories remain In review.
- Pull requests: None requested for this adjustment; source changes remain uncommitted.

## Request and starting context

User requested existing Item-based subscription pricing, reuse of ERPNext subscriptions if practical, and an invoice-style enrollment Item/quantity/rate table instead of hardcoded registration/jersey charges. Preserve prior EPIC-004 work, Academy Settings tabs, saved invoice/payment references and scholarship controls. Boost remains unchanged.

## Policy and design

Reuse native **Subscription Plan** for one Month, interval count 1, company currency and Fixed Rate. Native `get_plan_rate` resolves pricing with quantity/prorate factor 1. The server derives the linked plan’s enabled non-stock sales Item and current amount; manual overrides are ignored. Native Plan and Item read permissions remain required. The Sports plan list shows its last-saved values; monthly previews resolve the current native rate. A changed native plan invalidates ungenerated preview hashes. Existing generated obligations/invoices remain immutable.

Manual Sports monthly preview, concession handling and draft generation remain authoritative. Native ERPNext Subscription processing can submit invoices and commits per subscription in `process_all`; starting that parallel lifecycle would complicate transactional scholarship/retry controls. No native **Subscription** records, scheduler changes, automatic posting/email or proration are enabled. Unlinked Sports plans retain their existing manual Item/rate behavior.

Enrollment settings use **Sports Enrollment Charge** child rows: existing enabled sales Item, positive quantity (up to four decimals), nonnegative rate and server-derived amount. Configure 1–30 rows with a positive total. Native-style settings grid remains in Website payments; saving preserves all tabs. Public breakdown and invoice lines use arbitrary configured rows, including safe text labels and quantities. Stock Items may be charged with `update_stock=0`; billing does not distribute stock. The website monthly amount remains explicitly informational.

## Files and behavior

- New `enrollment_charges.py` and Sports Enrollment Charge DocType; parent settings Table and migration marker. Old scalar fee/Item fields remain physically present, hidden and deprecated, for migration/compatibility.
- `academy.py` retains loaded child rows rather than treating them as Singles scalars. `settings_api.py` projects safe child values, rejects unexpected child metadata/shapes and removes deprecated scalar inputs.
- `enrollment_payments.py` / `enrollment_invoices.py` calculate dynamic totals, snapshot all invoice rows and guard quantity/rate/amount. Existing invoice snapshots lacking per-row amount derive it from their saved rate/quantity for display; old receipt references remain supported.
- `payment_setup.py` migrates saved charges once, including payment-disabled sites, and removes fixed enrollment Item creation. No existing Item is deleted or renamed.
- `subscription_pricing.py`, Sports Fee Plan, `fee_plans.py`, `monthly_billing.py`, `billing_api.py` reuse optional native Plan pricing and include its revision in preview hashes.
- Sports settings/billing/public website JS, HTML and CSS provide the grid, optional Plan selector and dynamic charge rows.
- Requirements, PRD, setup/billing guides, affected stories and BA-QNR-001 reconciliation record this subsequent user refinement. The questionnaire transcript/hash and story review states are preserved. This log is indexed for Sports Development Tools.

## Schema, data and release impact

Development site: `moyours.ideltatech.com`, independent development bench. Reloaded additive Sports Enrollment Charge, Sports Academy Settings and Sports Fee Plan metadata. Migrated only the existing two settings charges once. Confirmed NGN250,000 before/after; repeat migration left rows unchanged. A hash of every existing application’s payment snapshot and invoice/payment references matched before/after. After migration, an empty table cannot resurrect old fees. Existing invoice and receipt snapshots are not rewritten.

Published Sports-owned content-addressed assets and cleared development caches using `/tmp/sports-billing-publish.py`; existing console provider roles stayed unchanged. Restarted only `frappe-bench-dev-web:frappe-bench-dev-frappe-web`. No Boost page-role synchronization, permission grants, native automatic subscriptions, real billing run, production changes, commit, merge or push.

## Verification and observations

| Acceptance criterion | Actual check | Result |
|---|---|---|
| Configurable Item quantities/amounts; safe row API; legacy compatibility | Full isolated unittest suite | **221 passed** |
| Settings API retains child rows, arbitrary invoice lines and saved prices | `/tmp/sports-charge-native-qa.py`, commits blocked, development native ERPNext controllers | Passed: three rows, quantity 2, draft NGN250,000; changed settings did not alter retry/reference/snapshot; tampered quantity rejected |
| Native Plan is authoritative and stale price cannot generate | Same native rollback QA | Passed: manual 999 overridden by native 40,000; native price change rejected stale preview; fresh preview produced draft 45,000 with native service Item |
| No duplicate ledger/payment or automatic subscription | Tracked native counts, blocked commits and final rollback | Passed; no Subscription, Payment Entry or GL Entry added; all temporary records removed; original two settings rows restored |
| Scholarship privacy, Company/User scope, failures/retries and lock serialization | `/tmp/sports-billing-qa.py` | Passed, including two independent DB connections; temporary disabled QA users/records rolled back |
| Settings grid payload and tabs survive editing | `tests/js/test_player_numbering_settings_browser.cjs`, 1440/390 widths | Passed with actual Sports view and synthetic native controls/API; row DTO included Item/qty/rate only |
| Subscription Plan selector fills Item/rate | `tests/js/test_billing_browser.cjs`, 1440/390 | Passed with actual Sports view and synthetic dialogs/API |
| Dynamic payment breakdown and escaped labels | `tests/js/test_enrollment_charges_browser.cjs`, 1440/390, actual development-rendered template/CSS/JS | Passed: three rows, quantity/rate, NGN total, reference; HTML-like Item name remained text; no overflow/page errors; all financial APIs stubbed |
| Syntax/style/security | Pinned pre-commit hooks; Frappe Semgrep rule set on 12 changed backend files, final recheck on payment/settings APIs; `git diff --check` | Passed; zero Semgrep findings |
| Published site and access boundaries | Verified-certificate HTTPS reads | Academy 200, exact current public JS/CSS and hashed Settings/Billing bundles; Guest denied private settings/native pricing APIs |
| App independence | Read-only status of development/live Boost | Both clean; no Boost source changes |

Commands used: development env Python `-m unittest discover -s sports_app/tests -p 'test_*.py'`; Playwright with `/tmp/foot-angel-browser-qa/node_modules/playwright` and `/tmp/sports-console-browser`; pinned pre-commit with caches under `/tmp`; Semgrep using `/tmp/frappe-semgrep-rules/rules`. The public template fixture uses a synthetic CSRF token; browser tests do not prove native control internals or initiate accounting writes. Native settings/API/controller checks separately verify persistence and ERP behavior.

Formatting hooks corrected initial formatting; final checks passed. Tests initially needed the established no-site translation/whitelist fixture pattern; corrected fixtures and reran the full suite. Native QA initially could not render CSRF without a web session; only the isolated template fixture uses a stub token. No credentials or player PII are recorded.

## Cleanup, limitations and recovery

All temporary native QA users, Items, programs, applications, Customers, players, plans, obligations and draft invoices were rolled back in guaranteed cleanup. Commit-blocking assertions and tracked counts confirmed no real financial posting. The only lasting business-data change is the additive settings migration preserving NGN250,000. Original pricing snapshots/references are retained. Browser endpoints are synthetic; physical stock distribution and native Subscription lifecycle scheduling are not part of this refinement.

Refresh already-open consoles to load new asset URLs. For other sites, normal Sports migration creates the new metadata and copies their own saved charges; review their settings before enabling payments. Do not remove the child schema or restore old code against newly issued multi-row invoices without a reviewed data-compatible rollback. Manual future price edits affect new applications and ungenerated monthly charges only. No complete EPIC-004 acceptance or unresolved payment/proration policy is implied.
