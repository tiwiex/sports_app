# Build log: main-table finance actions and branded PDF modals

- Date: 2026-11-07 (Africa/Lagos)
- Stories: US-003-01/03, US-005-01/04, US-001-01
- Requirements: SPORTS-FR-001/003/005/011/031/041; SPORTS-NFR-002/006
- App / branch: Sports App / `story/epic-004-scholarships-and-monthly-billing`
- Status: Verified development refinement; broader stories retain their existing review states.
- PR: Not requested; prior uncommitted settings/EPIC-004 work preserved.

## Intended outcome and starting context

User clarified that the main Players and Enrollments tables also need financial links/actions and elapsed ages. PDFs should open in a modal. Create reusable backend invoice/receipt Print Formats using the website logo; keep Boost independent and preserve finance permissions. This supersedes ordinary new-tab navigation from the preceding refinement; older evidence is retained.

## Policy decisions and plan

Main Players shows **Latest invoice**, **Latest receipt** and **Elapsed**. Latest is newest by creation/name; older financial records remain in the profile history. Native permission-filtered Company/Customer reads determine references; no finance IDs are returned when Customer or transaction read access is absent. Receipt selection is submitted Customer Receive; emailing still additionally requires positive amount and native read/print/email. Main Enrollments links its own invoice and posted receipt and exposes the matching menu actions. Receipt PDF reference must belong to the scoped application/company.

PDF anchors remain visually recognizable. Ordinary clicks open a large modal containing the native PDF URL and Open / download fallback; modifier-click retains browser new-tab behavior. Templates are explicit Sports formats, not global ERPNext defaults. Other companies/sites keep their own branding and permissions.

## Work performed

- `printing.py`: bounded latest-document projections and install/migrate setup for two app-owned backend Print Formats. `players_api.py` supplies latest accessible references, email eligibility and registration age. Existing player sorting/paging remains bounded and unchanged.
- Main `players.js` adds latest invoice/receipt links, context actions and elapsed column. Main `registrations.js` adds linked invoice/receipt cells and PDF context actions. Inner financial/history links reuse the same modal helper.
- `finance_documents.js` provides modal preview using native PDF endpoint and explicit format name, descriptive iframe title, close cleanup and Open / download fallback. Native PDF permissions still apply. Email remains operator-confirmed and duplicate-safe.
- Backend formats **Sports Academy Invoice** and **Sports Academy Receipt**, stored under `sports_app/print_format/`, include packaged Jinja templates under `templates/print_formats/`. They use a shared green/gold header, logo, source references/dates, readable party/line details, currency-aware totals and clear document state. Invoice shows net/discount/tax/total/outstanding. Receipt shows recorded amount, optional currency difference, invoice allocations and unallocated amount; it does not claim every invoice is settled. Draft/cancelled records never claim a valid receipt.
- `receipt_delivery.py` explicitly uses Sports Academy Receipt for the queued PDF attachment while preserving its transaction-safe native rendering and access-log path.
- Academy Settings gains configurable **Document logo** (`print_logo`) in General. PDF branding uses it for the configured academy company, otherwise the document Company logo. The development academy uses the existing public website crest. Company branding and global print defaults are not overwritten.
- Requirements, PRD, player/website/setup guides, affected stories and source reconciliation link this refinement. Original questionnaire transcript and story states are preserved; automatic reminders/WhatsApp remain outside this slice.

## Commands and observations

- Isolated full suite: development Python `-m unittest discover -s sports_app/tests -p 'test_*.py'` — **230 passed**. New tests cover no-customer/read-denied behavior, native company/customer/posted-Receive filters and bounded latest selection without permission bypass.
- Pinned pre-commit on changed backend/UI/metadata/tests — passed: Python/JSON, Ruff, Prettier and ESLint. Formatter corrections were followed by a clean final pass.
- Frappe Semgrep rules on six changed backend files — **zero findings**. `git diff --check` passed.
- `/tmp/sports-branded-print-schema.py` — additive Sports settings metadata and two backend formats installed on `moyours.ideltatech.com`; configured the existing crest only when the new document-logo value was blank. Default-print-format Property Setters matched before/after. No financial records changed.
- `/tmp/sports-branded-pdf-qa.py` — actual native invoice/receipt PDFs generated, source references and NGN250,000 totals checked with PDF text extraction. Main Players/Enrollments returned permitted financial references and elapsed ages. Commit-blocked rollback restored Sales Invoice, Payment Entry, GL Entry, Communication, Email Queue and Access Log counts.
- Visually inspected rasterized actual invoice/receipt PDFs, including crest, green/gold styling, readable names/columns, correct invoice line quantities and totals. Corrected long customer-ID/receipt heading wrapping before completing review. Local artifacts are under `/tmp/sports-branded-*`; real-player documents were not added to the repository or published as test files.
- `/tmp/sports-print-states-qa.py` — native templates mark draft/cancelled states correctly; a synthetic 45-line invoice produced multiple PDF pages retaining its final item and total. In-memory copies only, no saved accounting edits.
- `/tmp/sports-receipt-delivery-qa.py` — native branded receipt attachment, scoped permissions, same-key Communication reuse, changed-recipient rejection and PDF failure rollback passed. A temporary disabled Sports-only operator received no main-player finance IDs and could not open delivery context; Guest also denied. All temporary users/logs/Communications rolled back. SMTP/queue submission remained stubbed; no external email sent.
- Playwright actual-module fixtures at **1440 / 390**: Players, Enrollments, central profile and Academy Settings passed. Tests covered main-table columns/menus, modal iframe URLs with explicit branded format, fallback links, inner/profile compatibility, existing review/search/paging/permission behavior, logo setting compatibility and responsive controls. Dialog/API controls were synthetic; native rendering was verified separately.
- Published Sports-only content-addressed assets via `/tmp/sports-billing-publish.py`, cleared development cache and restarted only `frappe-bench-dev-web:frappe-bench-dev-frappe-web`. Existing provider roles unchanged; no Boost page-role sync or permissions mutation.
- Verified-certificate HTTPS smoke checks served exact current main Players/Enrollments/modal/settings assets. Guest was denied the player list and a branded invoice PDF.
- Development and live Boost checkouts both remained clean. No production services or repositories changed.

## Verification evidence

| Acceptance criterion | Check | Result |
|---|---|---|
| Main player/enrollment financial links/actions and final elapsed column | Native projections plus desktop/phone module browser fixtures | Passed |
| PDF opens in modal with download fallback | Actual helper/browser iframe and explicit format URL checks | Passed |
| Branded backend invoice/receipt with website logo | Native PDF generation, text extraction and visual review | Passed |
| Draft/cancelled and multi-page output remains truthful/readable | Native synthetic-state/45-line PDF checks | Passed |
| Native Company/Customer/read/email boundaries remain intact | Unit filters, native Sports-only/Guest denial, HTTPS denial | Passed |
| No unintended finance/email/global-default changes | Blocked commits, rollback counts, default-print-format comparison | Passed |

## Decisions, deviations and recovery

No real email delivery, invoice/payment posting, role assignment, production deployment, commit, PR, merge or push. Native PDF generation reports existing CSS compatibility warnings but produces valid readable PDFs; all stated checks are based on generated output. Default global ERPNext print formats remain unchanged. Existing invoices, financial snapshots and receipt references are preserved.

The only lasting development data additions are two Sports Print Formats, additive settings metadata and its previously blank document-logo setting. Standard migration repeats format synchronization; it does not seed Moyours branding on other sites. Old console assets remain available for already-open sessions.

## Remaining work and release impact

Refresh the console to load the current asset/provider URLs. The backend print selector now offers both Sports formats. Browser PDF embedding depends on its PDF viewer; the modal always provides Open / download. Latest main-table links are shortcuts, not a replacement for the complete paginated player financial history. Other academies can change Document logo without changing Sports code. Wider policy, reminder scheduling and final production acceptance remain in their existing stories.
