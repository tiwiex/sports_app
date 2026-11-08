# Configure an academy

Open the shared console at `/app/boost-console`, expand **Sports**, and select **Academy Settings**.

System Managers can configure the academy. For a configuration-only operator, assign **Sports Academy Administrator** and restrict their allowed Company records with standard Frappe User Permissions. Both supported administrator roles receive read-only Company/Currency master access for configuration, with company User Permissions still enforced. The Sports role grants no accounting transaction permissions. Basic **Sports Console** users can open Sports but cannot view or change settings.

## First setup

1. In **General**, select the academy's existing ERPNext Company. Only permitted companies are listed.
2. Open **Programs & groups** and use **New Program** to add a program name, sport and company. Sports are free text, so swimming, tennis, football or another sport can be configured without code changes.
3. Use **New Group** to add a group under an enabled program. The company follows the program.
4. Enter academy name, fee currency and timezone in **General**. In **Enrollment defaults**, select an enabled default program and, optionally, a default group belonging to it.
5. In **Player IDs**, set a registration prefix of 2–20 uppercase letters, digits or hyphens, starting with a letter; choose 3–10 digits. The displayed example is a preview and does not allocate a player ID. Existing IDs will never be renumbered by changing these defaults.
6. In **Enrollment defaults**, select Pending or Active. In **Monthly fees**, enable fees and enter a positive default monthly fee, or explicitly disable them. Website fee items, bank/receivable accounts and payment-review recipients remain in **Website payments**.
7. Select **Save Settings**. Refreshing the view reads the saved configuration.

Programs and groups can be edited from the same screen. Choose replacement defaults before disabling or moving a default program/group. A program with groups cannot be moved to another company. Saving settings with an unrelated or disabled default is rejected.

One academy configuration per Frappe site is supported by this story. Program/group records have explicit company scope; this does not implement multiple independent academy configurations on one site.

## Scope of these defaults

Saving settings does not register a player, allocate a registration number, generate an invoice, collect payment or publish website branding. The monthly fee is a configuration default for future fee plans. Effective pricing, proration, tax/account mappings and invoicing remain in the fee-plan and billing stories. The public website is US-001-02.

The demo site's business defaults are left for academy staff to select. Verification uses temporary fixtures and restores the original state afterward.

## Installation and access

Sports App requires ERPNext for Company/currency masters. Boost is optional for native setup; the Sports menu requires the compatible Boost console provider host. Standard install/migrate hooks create the Sports roles and synchronize the optional host's Page roles. Existing users are not assigned new roles automatically.

For a controlled schema-only development update after source changes, run role setup before model sync, then console setup and cache clearing. This story used that sequence on the backed-up `moyours.ideltatech.com` site rather than running unrelated historical migrations.

Native DocType forms remain available to authorized administrators for support. The same server validations apply to native forms, REST writes and the Sports console endpoints.

Player management now uses these defaults; see the [Players guide](players-guide.md).

Sports install/migrate setup publishes content-fingerprinted console JavaScript in `public/js/releases`. A changed source gets a new asset URL, preventing reuse of cached older forms. Reload an already-open console after an update; migration does not replace running browser code. Canonical sources remain in `public/js`, and older generated assets are retained for in-flight pages.

## Navigating settings tabs

Use General, Player IDs, Enrollment defaults, Monthly fees, Website payments and Programs & groups. The Save Settings button applies values from all tabs, including hidden ones. Switching tabs does not save or discard edits. Creating/editing a program or group refreshes its lists while preserving unsaved settings and the selected tab. If required-field validation fails, the relevant tab opens. The player-number example stays in Player IDs.

On phones, scroll the tab strip horizontally. With a tab focused, use Left/Right arrows or Home/End to navigate. Server permissions, Company filtering and stale-save checks are unchanged. [Build log](build-logs/2026-11-06-us-001-01-tabbed-academy-settings.md).

## Configure enrollment charge Items

In **Website payments → Enrollment charges**, add rows using existing enabled ERPNext sales Items. Set Quantity and Rate; Amount is calculated and validated again on save. Add, remove or reorder rows as required, up to 30. A payment-enabled setup requires at least one row and a positive total. Item names, quantities and prices drive both the public payment page and the draft invoice. Charging a stock Item does not issue stock.

Existing Moyours settings migrate to the same NGN250,000 total once. Subsequent changes affect new applications only; returning applicants retain their saved invoice prices. The old separate registration/jersey fee fields are hidden and deprecated. Refresh an already-open settings editor after this upgrade. Monthly fee information on the website does not create a recurring invoice; configure actual pricing in **Scholarships & Billing → Fee plans**. See [billing guide](billing-guide.md) and [build evidence](build-logs/2026-11-07-us-001-01-configurable-enrollment-items-and-subscription-pricing.md).

## Main-table document actions and branded PDF modals — 7 November 2026

Subsequent user refinement supersedes the normal new-tab PDF interaction above: ordinary clicks open an in-console **PDF preview** modal with an Open / download fallback. Ctrl/Cmd-click still supports the browser’s normal new-tab behaviour. Main **Players** adds **Latest invoice**, **Latest receipt** and final **Elapsed** columns, plus View invoice PDF / View receipt PDF / Email receipt in the player menu when permitted. Latest refers to newest creation time; the player profile retains access to older documents. Main **Enrollments** has linked invoice and posted receipt columns and matching context actions, without opening the inner profile first.

Financial references use native permission-filtered Company/Customer queries. Sports-only staff without finance access receive no finance IDs. Email retains posted Receive/read/print/email checks and explicit recipient confirmation. No accounting states or dates change.

Backend Print Formats **Sports Academy Invoice** and **Sports Academy Receipt** provide green/gold branding, existing website crest on Moyours, clear reference/date/party/line-item/total sections and draft/cancelled indicators. The receipt shows only its recorded amount and allocations; it does not claim all customer invoices are settled. Sports PDF preview/download and receipt email explicitly choose these formats. They do not replace ERPNext global print defaults. **Academy Settings → General → Document logo** configures the Sports PDF logo; another academy can use its own image, falling back to its Company logo. This deployment reuses Moyours’ existing public crest and leaves Company branding unchanged.

[Build evidence](build-logs/2026-11-07-us-003-03-main-table-finance-and-branded-pdf-modal.md).

## Automatic monthly accounting

In **Monthly fees**, enable **Automatically submit monthly invoices**, select the earliest month using its first day and select an enabled System User with Sports billing access and native invoice submission/approval rights. Monthly fees must also be enabled and a valid effective fee plan must cover each program. The Sports daily job generates/submits monthly receivables and retries failures without duplicating invoices. Payments remain separately confirmed. No roles are assigned automatically. See the [billing guide](billing-guide.md) and [Automatic monthly receivables](build-logs/2026-11-07-us-004-03-automatic-monthly-receivables.md).

## Completed-month billing correction — 7 November

Automatic monthly posting now catches up from enrollment dates after each month closes. The former global automatic-start floor is hidden and ignored. Enable automation and select the permitted execution account; no manual generation step is required. Enrollment/fee-plan/settings saves request catch-up after commit, and the registered daily task handles month boundaries and retries. [Evidence](build-logs/2026-11-07-us-004-03-completed-month-automation-payment-only-grid.md).


## Sports Academy landing dashboard — 7 November 2026

SPORTS-FR-023 / SPORTS-NFR-002 / SPORTS-NFR-005, US-008-02: replace the Sports Academy introductory text with a read-only dashboard. Coloured cards show visible player counts, current Active program memberships, Pending applications and non-cancelled sessions in the academy's current month. The next five Scheduled sessions from today show title, date/time and venue with native record links. Active memberships are enrollment counts, not unique active players or reconstructed historical eligibility.

Authorized finance users also see selected-year monthly subscription Billed, Settled and Outstanding totals with a twelve-month billed/outstanding chart. Reuse the existing permission-scoped subscription Overview service: submitted monthly invoices only, not enrollment fees/all ERP revenue; Settled includes accounting credits and is not cash receipts. The year filter affects financial totals only. Operational counts remain current. Missing native permissions show Restricted, not zero; no scholarship, biometric or player contact data is included.

Role-scoped shortcuts use the existing host dashboard navigation to Players, Enrollments, Attendance, Scholarships & Billing and Academy Settings. Refresh, year changes and host data-change watchers update the dashboard, with loading, empty, restricted, retry and unmount protection. Desktop and phone layouts use the same coloured summary style. This delivers the landing-dashboard slice; broader date/program filters, exports, attendance outcome reporting and production p95 acceptance remain open. [Build evidence](build-logs/2026-11-07-us-008-02-academy-landing-dashboard.md).
