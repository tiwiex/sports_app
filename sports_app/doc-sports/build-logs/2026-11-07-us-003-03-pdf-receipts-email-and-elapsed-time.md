# Build log: PDF invoice/receipt links, manual receipt email and elapsed age

- Date: 2026-11-07 (Africa/Lagos)
- Stories / epics: US-003-01, US-003-03, US-005-01/04; EPIC-003/005
- Requirements: SPORTS-FR-003/005/011/031/041; SPORTS-NFR-002/006
- Affected app / branch: Sports App / story/epic-004-scholarships-and-monthly-billing
- Status: Verified development refinement; broader story scopes not marked Done.
- Pull requests: None requested; preserve existing uncommitted settings/EPIC-004 changes.

## Intended outcome and starting context

User requested PDF invoice/receipt links after enrollment acceptance and in the player profile, obvious clickable styling, Email receipt in context menus, and elapsed-time columns in minutes/hours/days.

## Policy decisions and plan

Keep all changes Sports-owned. Use native permission-checked PDF downloads and existing print format defaults. Explicit operator email confirmation requires posted positive Customer Receive receipt, scoped Player/Customer/Company and native receipt read/print/email permission. Default a permitted guardian email, otherwise player email; operator reviews one address. Disabled future Website User accounts stay disabled and may receive this transactional receipt. No automatic admission email, reminders, account activation or new finance permissions.

## Work performed

- Added Sports-owned `public/js/finance_documents.js`, loaded by the Sports enrollment/player provider assets. Invoice/receipt links use the native PDF endpoint, a new tab, underline/link colour and a visible PDF ↗ indicator. Enrollment detail references also use this helper.
- Receipt-reference menu provides Email receipt for eligible posted positive Customer Receive entries. Accepted application menus offer the same action for their linked posted receipt. No action is shown for drafts/cancellations or operators lacking native receipt read/print/email.
- Added `receipt_delivery.py`: scoped player/Company/Customer access, native read/print/email checks on every context/send request, field-permitted guardian/player default, one validated operator-confirmed recipient, receipt-row lock and per-dialog UUID. A deterministic native Communication ID prevents a lost-response retry from producing another queued email; changing the recipient with the same key is rejected.
- PDF attachment uses the native configured Payment Entry print format and Frappe PDF generator. Native `attach_print`/printview unconditionally commits an Access Log on this installed version. The service instead calls native `get_html_and_style`, renders the fixed packaged `www/printview.html` layout, generates PDF and inserts its access log inside the surrounding savepoint. It never changes core Frappe code or test-mode flags. PDF/queue failure rolls back Communication/access-log changes.
- Native `frappe.sendmail(now=False)` queues the PDF and links it to Communication/Payment Entry. A missing outgoing account or empty queue result raises an error. Receipt emails are transactional and may reach disabled future Website Users without activating accounts; Communication’s notification-only disabled-user filter is not applied. Queue status is not proof of delivery.
- Profile invoice/receipt reads include permission-checked creation timestamps and server-derived elapsed seconds. Enrollment uses its submitted timestamp. The final Elapsed column renders minutes/hours/days, recalculates every 30 seconds and stops timers on view abort/removal. Source dates, accounting state and balances remain unchanged.
- Updated requirements, PRD, player/website guides, relevant stories, epic/inventory and reconciliation evidence. US-005-04 is In progress for manual receipt delivery, with reminder scheduling/WhatsApp/broader delivery policy still outstanding. Other story states stay unchanged.

## Commands and observations

- Full isolated suite: development env Python `-m unittest discover -s sports_app/tests -p 'test_*.py'` — **227 passed**.
- Pinned pre-commit hooks on all changed backend/UI/test files — passed (Ruff, Python/JSON checks, Prettier, ESLint). Formatting was applied before the final clean pass.
- Frappe Semgrep rules over five changed backend files — no unresolved findings. One broad SSTI warning was reviewed: template source is the literal packaged native Frappe path, never caller-provided text. A documented line-level suppression is limited to that call.
- Native `/tmp/sports-receipt-delivery-qa.py` on `moyours.ideltatech.com`, commits blocked — passed. Generated a real posted receipt PDF; outbound submission was stubbed and no email sent. Confirmed native role denial, Company/Customer scoping, elapsed projections, one Communication for retries, changed-recipient rejection and PDF failure rollback.
- Native cleanup tracked Communication, Email Queue, Access Log, User, Sales Invoice, Payment Entry and GL Entry counts. Every tracked count was restored after rollback; temporary disabled Sports-only QA user was removed. Existing financial records were not posted, cancelled or changed.
- Actual-module Playwright fixtures at 1440/390 widths: `test_central_profile_browser.cjs`, `test_registrations_browser.cjs` and `test_players_browser.cjs` — passed. Checked native PDF URLs/new-tab target/obvious styling, minutes/hours/day labels, email dialog/default/explicit action, accepted-menu eligibility, responsive layout and existing view/review/paging behavior. Browser APIs/native controls were synthetic; they did not email anyone or change real data.
- `/tmp/sports-receipt-mail-readiness.py` read-only check — a default outgoing Payment Entry account exists; site email is not muted. SMTP/inbox delivery was deliberately not exercised.
- Published Sports-only hashed assets using `/tmp/sports-billing-publish.py` and cleared development caches. Existing provider roles remained unchanged; no Boost page-role sync or permission grants. Restarted only the development Frappe web process.
- Verified-certificate HTTPS checks returned exact current `finance_documents`, `player_profile` and `registrations` bundles; anonymous receipt-context access was denied. `git diff --check` passed.

## Verification evidence

| Acceptance criterion | Check | Result |
|---|---|---|
| Financial references open clearly marked PDFs | Actual module browser at desktop/phone; native receipt PDF generation | Passed |
| Receipt context action requires posted state and native email rights | Unit and native Guest/Sports-only denial; accepted queue/menu browser | Passed |
| Operator-reviewed address, PDF attachment and duplicate-safe queue request | Unit payload checks, native Communication retry and failure rollback with outbound submission stubbed | Passed |
| Elapsed-time last column uses correct timestamp | Native server-age projection; browser minutes/hours/days; 30-second timer implementation/lifecycle review | Passed |
| Existing records and independent Boost remain intact | Tracked native counts/rollback, clean Boost status, Sports-only publication | Passed |

## Decisions, deviations and recovery

No new schema/DocTypes, real receipt email, accounting posting, role assignment or production deployment. All temporary native fixtures were rolled back. Frappe’s print helper commit was discovered during commit-blocked QA and replaced with a transaction-safe use of native rendering; the initial attempted QA was rolled back cleanly. Native PDF generation emits CSS compatibility warnings but returned a valid PDF; no assertion treats warning-free output as a requirement.

Keep the normal print/PDF installation and configured outgoing account working. Queued delivery can subsequently fail at SMTP; authorized operators inspect the native Communication/Email Queue. A new dialog creates a new deliberate resend request, while retrying the same open dialog reuses its UUID. PDF links retain native access/print policy, including native rules for draft/cancelled printing. No unposted entry is represented or emailed as a cleared receipt.

## Remaining work and release impact

Refresh already-open consoles to load the new provider asset list. Reuse the unchanged native invoice/payment approval workflow. Automatic reminders, delivery schedules, receipt-design customization, WhatsApp and final production acceptance remain outside this refinement. Changes remain uncommitted on the existing branch; no commit, PR, merge or push was requested. Broader user stories are not marked Done.
