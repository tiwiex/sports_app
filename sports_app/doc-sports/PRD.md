# Sports App product requirements document

Consolidated scope (6 November 2026): the [complete backlog](backlog/README.md) merges baseline and questionnaire work into **9 existing epics and 33 story records**. Each epic now has the full story table, source coverage and unresolved decisions; proposed additions remain unestimated.

Questionnaire discovery (6 November 2026): [BA-QNR-001](discovery/README.md), [reconciliation register](discovery/BA-QNR-001-reconciliation.md). Responses refine existing scope and propose new performance, inventory, arrival/departure, notification and gateway stories. Conflicting fees, role/admission rules and unresolved provider/consent details remain decisions, not automatic product changes.

Demo refinement (5 November 2026): pending fingerprint preparation can generate a clearly simulated barcode identifier for demonstrations. It does not collect biometric data or establish attendance/authentication; actual capture remains pending hardware integration. [Guide](fingerprint-preparation-guide.md#demo-capture--barcode).

Fingerprint preparation refinement (5 November 2026): the attendance app exposes an administrator-only online consent/preparation workflow while hardware is unavailable. Sports Biometric Enrollment records are Pending capture or Withdrawn only; no biometric data is collected and no scanner identity or attendance event is inferred. Full provider/consent/retention validation remains US-007-01 work before actual capture. [Guide](fingerprint-preparation-guide.md).

Attendance refinement (5 November 2026): the dedicated Next.js app now supports online New session and eligible roster generation through existing Sports services, with same-key retry recovery. This supersedes the initial prototype's console-only session-creation scope; cancellation/finalization remain in Boost. See [US-006-04](backlog/user-stories/us-006-04-attendance-pwa.md).

Attendance frontend delivery (3 November 2026): [US-006-04](backlog/user-stories/us-006-04-attendance-pwa.md) adds a separate statically built Next.js PWA under Sports App, sharing the Frappe origin/authentication. The first slice downloads private session rosters on trusted staff devices and queues manual choices for reviewed online synchronization. Existing server role/Company/document/date/version checks remain authoritative; offline identity is a device cache, not renewed authentication. Enrollment remains HTML. Biometrics, device provisioning and production offline policy remain later acceptance work.

User scope correction (3 November 2026): enrollment remains the existing HTML implementation. The withdrawn Next.js enrollment prototype is historical evidence only; Next.js is intended for attendance. Existing manual attendance in Boost remains available while the dedicated attendance frontend is refined.

| Field | Value |
|---|---|
| Product | Generic Sports Academy Management App |
| First academy | Moyours Sports Academy (name to confirm) |
| Version / date | 0.1 / 2026-11-01 |
| Status | Draft for review; console extension prototype implemented |
| Platform | Frappe / ERPNext, Sports App, and ERP Boost |
| Source | [Client brief](requirements.txt), repository inspection, and the user's integration direction |

## 1. Product outcome

Give academy staff one operational console and one private player record connecting registration, player identity, scholarship/exemption decisions, monthly charges and payments, biometric identity references, and attendance. Deliver reusable academy configuration rather than embedding Moyours or Primero branding and football-specific rules in code.

Use ERP Boost as the shared staff console host. Sports App owns sports records and workflows; ERPNext owns accounting transactions; ERP Boost owns its existing finance experience and a proposed extension interface. Separate repositories and app lifecycles remain intact. This is a proposed architecture, not a capability already present in the reviewed code.

## 2. Evidence and boundaries

| Source reviewed | Observed state | Planning implication |
|---|---|---|
| `sports_app/sports_app/__init__.py` and `sports_app/hooks.py` | Generic scaffold, commented integration hooks; no sports DocTypes found in the module reviewed | Plan new implementation, not a port claimed complete |
| `primero/primero_website/doctype/player/player.json` | Custom public-facing Player schema, name-based identity, football positions, Guest read permission | Reuse concepts selectively; create private namespaced records with stable IDs |
| `primero/primero_website/doctype/player_application/` | Applicant details, review states, generated application reference | Adapt intake concept; preserve original application time and map acceptance to a player idempotently |
| `primero/hooks.py`, `primero/www/`, content DocTypes | Brand-specific routing, templates, public profiles, news, FAQ, banners, and team content | Rebuild configurable presentation; select content modules rather than copying all pages |
| `erp_boost/erp_boost/page/boost_console/boost_console.js` | Existing `BoostConsole`, built-in view list, finance initialization, company fallback | Requires a deliberate extension seam and lazy module initialization |
| `erp_boost/console_entry_setup.py`, `access_control.py` | Boost-specific console role allowlist, login redirect, and finance create guards | Sports roles need shell access without automatic finance access |
| `erp_boost/docs-boost/` | PRD, requirement IDs, epics, stories, ADRs, and delivery evidence | Mirror planning conventions with a separate Sports ID namespace |

Paths above are relative to each app's Python package root. Inspection establishes source structure only; no runtime or deployment compatibility was tested. Sports is in `frappe-bench-dev`; Primero and Boost are in `frappe-bench`. Combined operation requires supported app versions installed on the **same target Frappe site**. Cross-bench imports or filesystem paths are not an integration mechanism.

## 3. Scope and provenance

The client brief explicitly asks for registration, player ID, player information, management-only scholarship/exemption status, monthly payment records, payment status/history, biometric identity, and attendance history. The user additionally asks for a generic app, a configurable front end, full ERP capability, and a combined console with separate apps.

Monthly charge generation, structured scholarship rules, session rosters, device ingestion controls, reports, migration, and release gates are proposed implementation details needed to make those outcomes coherent. They remain draft scope. [The requirement baseline](concepts/requirement-baseline.md) labels provenance and maps every requirement to stories.

### First production release

- Private registration and player record with stable registration number and searchable history.
- Academy, company, sport/program, branding, and public content configuration.
- Management-only exemption decisions and governed effects on fees.
- Monthly obligations, ERPNext invoices and receipts, arrears, partial payments, corrections, and reconciled player history.
- Sessions, manual attendance, biometric identity mapping, and one validated device/provider integration.
- One role-aware Sports and Finance console, reports, controlled migration, support documentation, and pilot sign-off.

Manual attendance can be used during the pilot while hardware is validated. Biometric integration remains required for the complete client scope and cannot silently be dropped from production acceptance.

### Subsequent or separately scoped work

Parent/player self-service activation and portal workflows, payment gateway integrations, SMS/WhatsApp, advanced player performance analytics, tournament/league management, accommodation, transport, medical case management, merchandise storefront, and multiple biometric vendors. Existing ERP capabilities may be configured where needed; these extensions have no committed release or estimate.

Do not rebuild general ledger, payroll, inventory, procurement, or invoicing in Sports App. Do not migrate Primero automatically or create another staff console. A new generic platform app is not required for this first implementation.

## 4. Users and access

| Persona | Sports access | Finance / sensitive access |
|---|---|---|
| Academy registrar | Applications, private player identity, enrollment and contacts | No scholarship decision details or unrestricted accounting |
| Coach / attendance operator | Assigned sessions, roster, attendance and minimal identity | No scholarship, billing, or biometric template access |
| Cashier / finance operator | Player billing links, amounts due, receipts and payment history | Approved ERPNext/Boost financial permissions; no scholarship reason or decision record by default |
| Academy management | Academy oversight and scholarship approvals | Sensitive scholarship details; finance actions require separate finance authorization |
| System administrator | Configuration, integrations and support tooling | Administrative account controls; production support access audited |
| Auditor | Explicitly granted read-only operational and financial evidence | Sensitive records require explicit grant; no blanket scholarship access |
| Public visitor / applicant | Published content and submission of own application | No player list, private records, payments, attendance, or scholarships |

“Management only” applies to scholarship flags, reasons, attachments, and decision history across APIs, exports, search, notifications, reports, and UI. Finance can see approved charge amounts and a neutral adjustment reference where necessary; routine responses must not label a player as a scholarship recipient. Amounts can still imply a concession; management must confirm acceptable financial visibility during refinement. Administrators remain technically privileged and must use controlled support access. Hiding a tab is insufficient.

## 5. Principal workflows

### Registration and identity

Registrar captures player details directly, or reviews a public application. Acceptance creates or links exactly one Sports Player, assigns an immutable academy-scoped registration number, and establishes enrollment. Same-name players are allowed; potential duplicates are flagged using agreed identity/contact checks. Names, public slugs, and biometric vendor IDs are not primary identity. Deactivate rather than deleting referenced players. Enrollment dates determine future billing and eligible attendance.

### Monthly fees and scholarships

Finance configures effective-dated fee plans by academy/program and links each plan to company, currency, service item, income account and payment defaults. Management approves a full or partial exemption with start/end dates and reason. A controlled billing run previews eligible player-period obligations and the authorized resulting amount before creating ERPNext Sales Invoices.

A stable player/enrollment/period/charge key prevents retries and concurrent runs from generating duplicate obligations or invoices. A fully exempt period remains visible as a zero-due obligation with a restricted decision link; no fictitious payment or unnecessary zero-value invoice is required. Mid-month entry, suspension, proration, taxes and overlapping exemptions must be explicitly configured or resolved before billing; there is no silent assumed policy.

Cashier allocates a submitted ERPNext Payment Entry to the correct invoice. Each player has their own ERPNext Customer, created automatically from registration details in the same transaction. Enrollments derive this link; staff do not choose a family/payer Customer. Keep player attribution at obligation/invoice allocation level. For MVP, use one player's obligation per invoice unless a tested line-allocation design is approved.

Payment history shows invoice and receipt references, dates, period, due amount, submitted allocations, outstanding amount and correction links. Due-state rules are: Exempt (authorized zero charge), Unpaid (positive charge, no allocated receipt), Partially paid (some paid, balance remains), Paid (balance zero), or Overdue (positive balance past due date, retaining partial-payment information). Not billed is distinct from Paid or Exempt. Cancelled documents do not count; unallocated receipts are visible credits, not proof that a period is paid. Refunds, credit notes and reversals follow ERPNext permissions and workflows and recompute the view.

### Attendance and biometric identity

Operator creates a dated session for a program/group and records Present, Late, Absent or Excused attendance for eligible players. Define a single logical attendance record per player/session, with source evidence, operator and correction history. Absence follows roster finalization rather than treating every missing scan immediately as an absence.

An authorized administrator binds a provider/device identity to an existing player. Prefer provider-managed templates and opaque external IDs; never expose raw biometric material in player pages or logs. The final template boundary, consent/guardian process, retention policy and provider contract must be resolved before live enrollment. This is a product design gate, not a determination of legal compliance.

Authenticated device events include academy/device identity, external event ID, external person ID, occurrence timestamp and receive timestamp. Resolve device timezone and session window, deduplicate retries, queue unknown identities or ambiguous sessions, and allow controlled reprocessing. Manual attendance remains available during outages; replay must not overwrite a reviewed correction. A scan records attendance evidence, never a payment or admission decision.

### Shared console and configurable website

Staff use the existing Boost console route, with Sports sections for Players, Applications, Sessions, Attendance, Billing and Reports alongside permitted Finance sections. Sports-only users reach the shell without finance requests or accounting privileges. Navigation preserves academy/company, player, date and return context; revoked permissions clear cached views.

The public front end has configured academy name, logo, colors, contact details, programs, page sections and selected content. Public player profiles are opt-in projections of approved fields, never public access to the private record. Website editing and staff operations are accessible from the shared staff console; public pages are a distinct visitor surface.

## 6. App ownership and integration contract

| Layer | Owns | Must not own |
|---|---|---|
| ERPNext / Frappe | Authentication, permission primitives, Customer, Item, invoices, receipts, accounting ledger, standard ERP modules | Sports-specific duplicate financial ledger |
| ERP Boost | Existing Finance UI, common console shell, proposed provider registry, context and access composition | Sports models, scholarship logic, device processing, academy branding hardcoded in shell |
| Sports App | Namespaced sports DocTypes, academy configuration, private player aggregate, fees/obligations, attendance, device adapters, public website and console contribution | Forked Boost console, copied ERP financial posting logic |

Proposed extension contract: discover installed-app provider declarations through a documented Frappe hook, validate a versioned server manifest, return only permitted navigation and capabilities, then lazy-load declared app-owned assets and view factories. Specify namespaced view IDs, ordering, icons, context input, mount/unmount, refresh, empty/error behavior and a compatibility version. Providers reference installed code and asset paths; administrators cannot enter executable scripts in branding settings. Exact hook and API names are to be settled in [ADR-0001](adr/0001-shared-console-and-separate-app-ownership.md) and the integration spike.

Sports supplies authorization callbacks and independently permission-checked endpoints. ERP Boost retains finance authorization. Shell entry is the union of allowed module capabilities; access to data/actions remains module-specific. Do not grant `Accounts User`, `Boost Finance Manager` or `Boost Console` merely to bypass a shell allowlist. Audit the consequences of any role changes across Boost create guards, page roles, redirects and API access.

Host should work with no Sports installation and tolerate a disabled/failing provider. A Sports-only user must not trigger finance warmups. Remove client-specific company fallback from shared initialization; validate academy/company against user access. Company changes invalidate scoped caches. Sports supports Frappe-native forms for authorized setup/support, while the combined console is the planned staff workflow.

Deployment profile for this academy includes Frappe + ERPNext + ERP Boost + Sports App on one site. Sports must not be required by Boost. Whether standalone Sports installation without Boost is supported is an open packaging decision; the first release does not promise a second console or standalone production profile. Version/dependency declarations must match the chosen support policy before release.

## 7. Proposed data model

Use a `Sports` prefix to avoid collision with Primero's `Player` and `Player Application`. Settings, Program, Group, Player and Enrollment are implemented in the current development slices; other models below remain candidates.

| Record | Core purpose and links |
|---|---|
| Sports Academy Settings | Academy key, Company, locale/timezone, currency, numbering, branding, enabled modules and allowed defaults |
| Sports Program / Group | Configurable sport, program, roster/group, schedule and fee-plan association |
| Sports Application | Applicant/guardian contacts, submitted timestamp, review status and resulting player link |
| Sports Player | Stable registration number, names, DOB where required, contacts/guardian, status and protected attachments |
| Sports Enrollment | Player + academy/program/group, effective dates, status, fee plan and the player's automatically linked Customer |
| Sports Fee Plan | Effective dates, frequency, price/currency, due-date policy, ERP item/account mapping |
| Sports Scholarship / Exemption | Restricted approval, player/enrollment, scope, amount/percentage, dates, reason and decision audit |
| Sports Fee Obligation | Player/enrollment/period key, approved amount, restricted adjustment reference, invoice link and derived settlement status |
| Sports Session | Academy/program/group, occurrence times, roster, finalization state |
| Sports Attendance | Unique player/session record, final status, source, timestamps, evidence and correction history |
| Sports Biometric Identity | Restricted provider/device external identity → player mapping, enrollment/revocation metadata |
| Sports Device Event | Authenticated event ID, occurrence/receipt times, processing result, retry/error and attendance link |
| Public content / profile projection | Explicitly published fields and reusable website content; separate from private operational schema |

The player page aggregates linked records rather than storing monthly payment or attendance history in unbounded child tables. Store accounting references and recompute/reconcile derived payment summaries. Keep decision evidence separate from finance-visible fields.

## 8. ERP coverage and rollout boundary

“Full ERP” means the academy can use standard ERPNext capabilities with a guided console and appropriate configuration. It does not establish that Boost already covers every ERP module. A fit-gap workshop must produce a signed module matrix for Finance/AR/AP/banking/tax, purchasing, equipment and kit inventory, assets, HR/payroll and management reporting. HR/payroll may require another supported app; confirm target-site apps and versions. Record per module: required process, business owner, native availability, Boost coverage, missing console entry/workflow, master data, permissions, migration, acceptance evidence and release phase.

Player billing and finance reconciliation are required for the core sports release. Any other ERP module marked launch-required must be configured, tested and accessible through the shared navigation before academy-wide ERP sign-off; native forms may be the agreed guided destination. Remaining modules need explicit later phases rather than being reported complete through installation alone.

## 9. Quality targets and acceptance gates

Targets below are proposed until tested against agreed player counts, session peaks, document volumes and hardware.

| Area | Release target |
|---|---|
| Identity | No duplicate registration numbers; same-name players supported; accepted application retries produce one player |
| Billing correctness | One obligation per eligible period key; concurrent retries create no duplicate invoices; player totals reconcile to submitted ERPNext records |
| Confidentiality | No scholarship details in registrar/coach/cashier/public response payloads, search, exports or reports; direct unauthorized calls rejected |
| Attendance integrity | Duplicate and delayed device events create no duplicate logical attendance; all ambiguous/unmatched events have visible resolution state |
| Console | One staff entry; Sports-only, Finance-only and mixed-role journeys pass; Boost works without Sports |
| Generic configuration | Two different academy fixtures run without code changes, hardcoded client strings, or football-only required fields |
| Performance | Proposed p95 player search ≤2s and profile summary ≤3s at agreed pilot volume; paginate histories and load modules on demand |
| Usability | Registration, receipt lookup and attendance usable at 360px phone width and desktop, with keyboard navigation and clear validation |
| Recovery | Demonstrated backup restore and device-event replay without duplicate charges or attendance; recovery targets agreed before go-live |

See `SPORTS-NFR-*` rows in the baseline for the complete quality scope. The baseline does not certify legal, financial, biometric or deployment readiness.

## 10. Delivery plan and success measures

| Gate | Required outcome |
|---|---|
| G0 — Scope and integration | Confirm policy/device/ERP fit-gap; validate shared-console contract and target-site compatibility |
| G1 — Private player foundation | Configuration, role boundaries, registration, player ID and console integration demonstrated |
| G2 — Fees and manual attendance | Scholarship restrictions, period billing, receipts and correction reconciliation pass alongside session attendance |
| G3 — Complete client scope | Chosen biometric provider passes authenticated replay/outage checks; public branding and reports validated |
| G4 — Production | Rehearsed migration/recovery, launch-required ERP module acceptance, training and management pilot sign-off |

Sequence is detailed in [the backlog](backlog/README.md). No delivery dates, staffing commitments or story-point estimates are asserted before refinement.

Success is measured by complete required player records, searchable payment and attendance histories, reconciled opening/current balances, one shared staff entry point, no unauthorized scholarship disclosure in tested paths, and successful operation for a second academy configuration. Management should agree baseline volumes and operational measures during G0.

## 11. Open decisions and risks

| ID | Decision / risk | Owner role / deadline |
|---|---|---|
| OQ-01 | Exact academy name, sports/programs, locations, Company mapping; one academy per site or multi-academy site? Proposed MVP is one academy per site with scoped keys for future reuse | Academy management / G0 |
| OQ-02 | Required player/guardian details, age groups, duplicate checks, publication authorization and privacy/retention policy | Management + implementation lead / G1 |
| OQ-03 | Currency, monthly rates, start date, due dates, proration, taxes, suspension and withdrawal billing | Finance + management / G0 |
| OQ-04 | Scholarship approvers, full/partial treatment, overlapping awards, retroactive changes and finance visibility of concession-derived amounts | Management + finance / before fee implementation |
| OQ-05 | One Customer per player confirmed by user; refund/credit allocation and opening debt evidence remain open | Finance / before billing implementation |
| OQ-06 | Device vendor/model/SDK, ownership of templates, identifiers, supported auth, offline behavior, timezone, consent and revocation/deletion | Management + device supplier / G0; before live biometric enrollment |
| OQ-07 | Target-site Frappe/ERPNext/Boost versions, app installation policy and console extension compatibility | Technical lead / integration spike |
| OQ-08 | Launch-required ERP module list, HR/payroll app requirements and actual Boost coverage | Finance + management / G0 |
| OQ-09 | Existing data sources, import volume, opening date, active roster, history fidelity and acceptance totals | Registrar + finance / before migration |
| OQ-10 | Concurrent users/events, target hardware, backup/restore and retention targets | Technical lead + operations / before pilot |

Do not turn unknown hardware support or broad ERP expectations into implied delivered scope. Resolve each decision in its story and record accepted architecture separately from this draft.


## 12. Implementation checkpoint — 2026-11-01

US-002-01 has a v1 provider prototype on the selected development site, `moyours.ideltatech.com`, verified for Sports-only, Finance-only and mixed roles. Both apps use story branches in the development bench. Boost has an independent dev checkout at the latest reviewed source baseline `36912af`; the original live repository is clean and unchanged. See the story build log and ADR-0001 for the implemented contract and scope limits. This checkpoint does not mark broader Sports or ERP scope delivered.


### Academy settings checkpoint

US-001-01 adds one private academy configuration per site, company-scoped Programs and Groups, registration/enrollment defaults, and a default monthly fee with explicit opt-out. The Sports-owned settings view is available from the existing console to System Managers and the new Sports Academy Administrator role. No existing user receives that role automatically. Company/currency master read access does not grant accounting permissions. Actual player creation, website publishing and effective fee-plan/invoice behavior remain subsequent stories. See [the setup guide](academy-setup.md).

## Development player slice (2026-11-01)

US-001-01 and US-002-01 were accepted and merged into local development branches. US-003-02 now implements private Sports Player identity, enrollment and automatic per-player Customer links through the optional shared console. Sports Registrar is the initial player operator role; it does not receive financial transaction rights. Public applications, complete role boundaries, source-linked billing/payment/attendance histories and production acceptance remain their planned stories. See the [player build log](build-logs/2026-11-01-us-003-02-player-numbering-and-enrollment.md).

Program categorization and delivery governance refinement: new player Customers are assigned to a Customer Group named for the initial registration program. A management-only Sports Development Tools view exposes current requirements and delivery documents; every story/adjustment requires a separate indexed build log. See [current requirements](REQUIREMENTS.md) and [US-002-04](backlog/user-stories/us-002-04-development-documentation-and-build-evidence.md).

New registrations require a valid unique player email and atomically create a disabled Website User linked to the player and Customer Contact (SPORTS-FR-029). Accounts carry only the non-Desk Sports Player role, with no welcome mail or password. Existing players are not backfilled. Activation, authenticated own-record access and email-change review remain future work. The shared development Boost installation restores standard System Manager User role-editor permissions without extending Boost Admin authority.

## Public website prototype checkpoint (2026-11-01)

The client requested a PoC before preparing a proposal. US-001-02 provides a native Frappe `/academy` preview using the current Moyours brand, public academy photos and app-owned content configuration. Interactive program tabs, gallery, training/contact details and demo enrollment demonstrate the experience without reading private operational records or accepting applications. Full editor/publishing, production rollout and live applicant/account/payment workflows are deferred. See [prototype guide](website-prototype.md) and [build evidence](build-logs/2026-11-01-us-001-02-website-prototype.md).

The website menu now follows the full Moyours navigation. Existing pages outside the PoC link to the source academy website. Public-demo and staff registration share player, guardian, emergency and consent field definitions (SPORTS-FR-030). Extend Sports Player for these scalar fields; name every future app-owned DocType with the Sports prefix. Preserve the unique player account email separately from guardian email. Public application submission, payments/proof uploads and versioned consent/contract acceptance remain deferred.

## Submittable registration checkpoint (2026-11-01)

User authorized a complete PoC intake workflow, superseding the demo-only submission policy above. `/academy` now submits into Sports Registration; staff use Sports → Registrations to review possible matches, correct pending details, accept exactly once through existing player/Customer/User/enrollment creation, or reject with a reason. No guest read/list/status lookup, payment, email or portal activation is introduced. Company scope, bounded field validation, rate limiting, UUID retries, locked transitions and rollback protect intake. User-email conflicts surface only during authorized acceptance; no existing account is silently reused. Original timestamps and Player/Registration provenance persist. Full production hardening, CMS and communications remain open. See [workflow guide](website-prototype.md) and [build evidence](build-logs/2026-11-01-us-003-01-public-submission-and-review.md).

## Earlier receipt-first checkpoint (2026-11-01, superseded below)

User explicitly extended the PoC to a multi-page enrollment with a draft Payment Entry and real workflow state (SPORTS-FR-031). Confirmed initial fees are NGN 220,000 + NGN 30,000; the NGN 40,000 monthly amount is informational. Configured enrollment bank/currency/account/fee fields supply all amounts and destinations. The actual ERPNext Payment Entry number is the bank-transfer reference. Make Payment atomically creates a private registration, prospective Customer and unposted receipt. The applicant’s token-authorized claim changes Draft → Pending Review with docstatus 0 and no GL/Payment Ledger posting. Only Finance can submit after verification. Staff admission acceptance reuses the same Customer and creates the Player/disabled User/enrollment; it remains separate from finance approval. A conditional Sports-owned standard Payment Entry review workflow is added only when none exists. Existing compatible workflows are preserved; no Guest finance permissions or automatic emails are added. The receipt is an unallocated advance; invoicing/allocation, uploads and reconciliation remain future work. [Build evidence](build-logs/2026-11-01-us-005-01-enrollment-payment-review.md).

### Invoice-first enrollment refinement — 1 November 2026

Supersedes the earlier advance-receipt PoC for new enrollments. Make Payment creates a draft Sales Invoice and prospective Customer; the actual invoice number is the reference. The applicant claim moves the invoice to Pending Review, retaining docstatus 0 and creating no Payment Entry. An authorised Finance reviewer uses Complete Payment to submit the invoice and create/submit a fully allocated receipt in the same transaction. Failure leaves both unposted; retries do not duplicate settlement. Existing selected-approver, native finance, workflow and Company/User Permission controls apply. Player admission remains separate. Legacy receipt references are retained. This slice covers full initial-fee settlement, not recurring monthly billing, partial/overpayments or production reconciliation. [Build evidence](build-logs/2026-11-01-us-005-01-invoice-first-payment-completion.md).

## Club and partner relations — 2 November 2026

New EPIC-009 covers generic organisation relationships, sport-independent opportunities and internal correspondence. Initial scope includes a sourced Nigerian/international football directory and staff-assessed1–5 relationship priority, not a club-performance ranking. Management-only access, Company boundaries and native validation apply. Imported prospects do not become Customers/Suppliers automatically. Outreach, player sharing and external portal access require future explicit controls and are not triggered by this slice. See [US-009-01](backlog/user-stories/us-009-01-club-partner-relations.md).

Club directory table/contact refinement (2 November 2026): tabular directory and interaction views include optional public email with attributable source/purpose. Reviewed contact enrichment is explicit, Company-scoped and non-destructive; contact-form routes remain available where a suitable email is not published.

Club table sorting refinement (2 November 2026): server-side allowlisted column sorting and combined organization/email, country, priority, relationship and email-presence filters apply before pagination. Default organization ordering is alphabetical; changing tabs clears filters/sort state.

## Payment review notification refinement — 3 November 2026

SPORTS-FR-034 adds configurable payment review emails to Sports Academy Settings and the Sports settings console. On the first applicant payment claim, queue a linked notification alongside the unposted Pending Review transition. Legacy receipt references receive the same notification. Retries do not notify again; failed transactions leave no queued message. Blank disables notifications. Recipients must still have existing document access and Finance approval permissions. Email content clearly distinguishes an applicant claim from bank clearance; no token, player contact details or bank account details are included. This supersedes the historical no-automatic-email boundary for this specific event.

## Registration review interface — 3 November 2026

The private registration queue adopts Boost's invoice table styling: sortable Reference, Player, Pathway, Submitted on and Status columns; status badges; reference action dropdowns. View opens a registration modal, preserving the current filtered/paginated list. Accept/Reject are offered only for pending registrations with write permission and re-fetch current state before confirmation. Acceptance retains possible-match review and enrollment choices; rejection requires a reason. Admission remains separate from payment approval. Sports owns this UI and API; Boost's reusable shell is unchanged.

## Enrollment review terminology — 3 November 2026

The staff queue is labelled **Enrollments**, with **Enrollment application** identifying incoming admissions requests. Acceptance creates the player and program membership already shown under Players. This is a presentation change; application and dated membership records retain their separate responsibilities and existing links. The modal replaces the flat definition list with grouped responsive cards and consistent label/value fields. Current admission permissions, explicit confirmation, possible-match checks, rejection reason and independent Finance review remain in effect.

## Manual attendance prototype checkpoint — 3 November 2026

Sports Session and Sports Attendance now provide a development prototype of US-006-01/02. The shared console offers session creation/listing, fixed eligible rosters, manual statuses, explicit absence finalization, reasoned corrections and per-record native audit history. Staff access reuses existing Sports management roles and native Company/document restrictions. Responsible operator is the creator; later operator assignment and coach-specific group scope remain future policy. No manual roster exceptions, cross-session player report/rate denominator, biometric identity/device adapter or production readiness is claimed. See the [attendance guide](attendance-guide.md) and build evidence.

## Player presentation refinement — 3 November 2026

The private Players queue uses the Enrollments table/reference-menu style. View opens a grouped responsive modal with identity, linked accounts, paginated program memberships, contacts and consent choices while retaining search/list context. New program enrollment remains permission-controlled and reuses the player's existing Customer; it creates no invoice/payment. Full payment/attendance history aggregation remains US-003-03 follow-up.

Story tracking refinement (6 November 2026): [Sports story review](story-review-guide.md) adds management-only status/MoSCoW and Mark Done controls. Other documentation remains read-only; edits are version-checked, audited and synchronized to epic/master inventories. This is planning metadata, not automatic implementation acceptance.

## Enrollment refinement — 6 November 2026

User-approved refinement of SPORTS-FR-003/030/031 and SPORTS-NFR-003: optional private player portrait, year-based enrollment application reference, queue invoice/workflow columns, Draft → Pending Review on applicant transfer claim, and one authorized acceptance action submitting the linked invoice and allocated receipt with admission. Native Finance and Boost approval controls remain mandatory; an applicant claim never proves bank clearance. Ordinary no-invoice intake remains supported. Existing references and fees remain unchanged. Scholarship/partial-payment exceptions remain unresolved. See [US-003-01](backlog/user-stories/us-003-01-application-intake-and-review.md) and [build evidence](build-logs/2026-11-06-us-003-01-enrollment-image-and-invoice-acceptance.md).

## Configurable enrollment references — 6 November 2026

Academy Settings exposes **Enrollment naming series**, default `MSA-ENR-.YYYY.-.#####` (example `MSA-ENR-2026-00001`). A literal uppercase prefix, optional year and 4–10 counter digits are supported, for example `CLUB-ENR-.######`. This supersedes the earlier fixed `SPORTS-APP-YYYY-#####` choice. Only new enrollment applications use the configured series; existing application references, accepted program membership IDs, player IDs and invoice transfer references remain unchanged. Native Frappe series counters allocate references. [Build evidence](build-logs/2026-11-06-us-003-01-configurable-enrollment-series.md).

## Confirmed player numbering and public age rule — 6 November 2026

User clarification confirms BA-QNR-001-Q02-07/Q02-08: **MSA + two-digit creation year + hyphen + two-digit creation month + continuous serial**, e.g. `MSA26-08005` followed by `MSA26-09006`. The sequence also continues across year boundaries. The backend uses the academy timezone and a locked Company-scoped counter whose key excludes month, year, editable prefix and application series. Minimum sequence width defaults to three digits and expands naturally; prefix/width remain management settings. On first initialization, seed after the highest existing matching player reference in that Company. Existing prototype IDs of another format stay unchanged and are not interpreted as legacy serials. Existing IDs are immutable; no identity, Customer or finance references are renamed.

The player reference is independent of the configurable **enrollment application** series (`MSA-ENR-.YYYY.-.#####`), accepted Sports Enrollment membership IDs and ERPNext invoice numbering. Current development player defaults are MSA / 3 digits. This supersedes the old prefix-plus-counter-only player ID format for new players.

Public HTML enrollment accepts ages **4 through 18 inclusive**, calculated from calendar birthdays against the academy-local date. Show an inline age error and enforce date bounds in the browser; reject invalid ages in the server-owned public application controller before creating a successful application/invoice. Under-4, 19-or-older and future DOBs are rejected. A February 29 birthday reaches the next age on March 1 in a non-leap year. Enforce on new applications/DOB corrections, without retroactively blocking unchanged historical applications or imposing this public intake policy on ordinary updates to existing player records. Private staff intake policy is not broadened by this web-form refinement.

Provenance: numbering is **Both** (baseline plus questionnaire, now user-confirmed); the explicit 4–18 public restriction is user direction informed by the supplied web-form screenshot, not a claim that the questionnaire stated those exact limits.

[Build evidence](build-logs/2026-11-06-us-003-02-player-series-and-public-age-policy.md).

## Player email preflight and shared guardian identity — 6 November 2026

User refinement: a player email must be unique before public enrollment is submitted, not only when staff accepts it. Normalize player email; reject addresses already used by a User (including email-field aliases such as Administrator), Sports Player or another Pending Sports Registration. Rejected applications release their pending reservation. Browser preflight runs on leaving the player-email field and again before Make Payment/Submit, returning only availability; server validation remains authoritative under the existing settings lock. Preserve token-bound unchanged retries. Show a specific inline error and retain entered details. Review older applications again before financial completion, so a known conflicting email does not start the posting process.

At authorized acceptance/direct player registration, create the player's separate disabled Website User and create or reuse the guardian User. A server-owned **guardian_user** link on Sports Player supports many players to one guardian. Siblings retain separate player emails, Users, Customers and enrollment/finance histories. Player and guardian email on one form must differ. New guardian accounts are disabled Website Users without Desk roles or welcome mail; existing guardian accounts retain their original type, enabled state, roles and profile. Guardian email repetition is permitted; it never becomes a shared payer Customer. Account creation/linkage participates in the same admission transaction and rolls back on failure.

A supplied guardian email is an unverified identity reference, not proof of guardianship or permission to access children. This change does not activate accounts, grant guardian portal permissions, send invitations or implement the parent portal. Existing records are not bulk-backfilled or automatically merged; existing duplicate applications require staff/Finance correction. This user-approved account preparation refines the earlier player-only provisioning decision while leaving portal activation/access as separate scope.

[Build evidence](build-logs/2026-11-06-us-003-01-email-preflight-and-guardian-users.md).

## Live operational tables — 6 November 2026

The installed Boost host now offers an optional mounted-table watcher. Sports Enrollments, Players, Attendance sessions and Clubs & Partners declare their own relevant DocTypes and retain their authorized APIs, filters, sorting, page offsets and generation guards. Committed native notifications coalesce into a background reread; a 15-second fallback catches missed notifications or writes without events. Only matching records on the current filtered/sorted page appear. Equal responses keep the existing DOM.

Updates pause while a filter/input/select, context menu or dialog is in use, then catch up. Hidden tabs do not poll; resuming/reconnecting triggers a reread. Host abort/unmount removes timers/listeners; responses recheck signal/generation/application safety. Explicit Refresh remains supported. The compatibility hook is generic and does not hardcode Sports into Boost. On an older host without the hook, manual refresh remains available. This slice updates operational queue tables; editable documentation/settings forms and the separate Next attendance application are not remounted by it.

No permissions, financial state, record identity, schema or website enrollment behavior changes. No production edits/deployment.

[Build evidence](build-logs/2026-11-06-us-002-01-live-console-tables.md).


## Sports menu counts — 6 November 2026

Sports-owned menu badges show pending enrollment applications, total players, attendance sessions and clubs/partners in the configured academy. Counts use native permission-filtered aggregate reads, independent of Finance access; unauthorized entries are omitted. Zero is displayed explicitly. Badges refresh on relevant received native notifications, window focus and a 15-second visible-console fallback, survive sidebar redraws, and clear after failed reads. Settings, documents and the attendance-app shortcut have no artificial record total. No Sports dependency is added to Boost.

SPORTS-FR-019/020; SPORTS-NFR-006. [Build evidence](build-logs/2026-11-06-us-002-01-sports-menu-badges.md). Existing wider story status is unchanged.


## Legacy player import and numbering setup — 6 November 2026

Player setup refinement: Academy Settings exposes the existing player prefix/digit width plus **Player starting sequence**, a positive whole-number minimum (default 1). Set 126 to continue after legacy sequence 125. The Company counter uses the highest of the configured minimum minus one, existing issued counter and matching imported player suffixes. Changing prefix/month/year or lowering the minimum never resets numbering; existing player IDs and links remain unchanged. Enrollment application and invoice series remain independent.

Native Data Import is enabled for Sports Player, with import permission restricted to System Manager/Sports Academy Administrator roles and management checks enforced in the controller. Native Company/User Permissions still apply; imported Company must match the configured academy. Use Insert New Records with each legacy player number in the **ID** column. Preserve historical IDs verbatim; after successful insertion reserve the matching continuous suffix under the same settings/Series locks, including imports after the counter was already initialized. Nonmatching legacy formats are preserved without guessing their suffix; set the starting sequence explicitly after reconciliation. Blank IDs use automatic numbering. Do not merge duplicates or rewrite existing identities.

Player email/account validation and automatic separate Customer/disabled player User/shared guardian account preparation remain in force for imports. Imports create no invoices, receipts, balances or attendance history; create program memberships separately using staff tools. Missing/duplicate emails require source-data correction rather than placeholders or silent existing-account reuse. Obtain and review the real roster before an actual import; this adjustment prepares tooling and does not complete the migration/pilot story.

SPORTS-FR-001/004/024; SPORTS-NFR-003. User refinement of existing numbering and BA-QNR-001 legacy-roster discovery, not new questionnaire wording. [Build evidence](build-logs/2026-11-06-us-003-02-legacy-import-and-sequence-floor.md). Wider delivery states remain unchanged.


## Audited player ID correction — 6 November 2026

Authorized exception to the earlier immutable-ID rule: Administrator, System Manager or Sports Academy Administrator with native Player write access and permitted configured Company may use **Change Player ID** from the Players reference menu/profile or native Player form. Require a new unique 2–140-character ID (letters/digits/hyphens/underscores), a reason and current source revision. No general native rename or merge permission is granted; direct renames and all merges remain blocked by the controller.

Use native Frappe rename to update Link/Dynamic Link records and attachment ownership while preserving the same Customer, User, guardian, enrollment identities and accounting documents/amounts. Reserve old/new matching player suffixes without resetting the Company sequence. Keep append-only **Sports Player ID Change** records with old/new IDs as historical Data fields, current Player link, Company, reason, operator/time and request identity. Lost-response retries are idempotent and must match actor/payload/current scope. Existing/retired IDs cannot be reused by correction or new intake/import.

Repair derived Sports Attendance identity hashes and row modification versions atomically. Session and roster-row locks precede native link updates; enrollment and fingerprint-preparation writes share the settings lock to serialize identity changes. Unchanged attendance results remain idempotent; changed stale offline marks require fresh roster/conflict review. Operators must refresh downloaded rosters without deleting pending offline work. Existing preparation consent/demo references and request provenance stay intact; uncertain old-ID preparation retries require review rather than creating another preparation.

Any rename, derived-key, counter or audit failure rolls the operation back. This corrects the Player identifier only; no invoice submission/payment, account activation, customer/user renaming, bulk renumber or production roster cleanup is included. It supersedes the earlier blanket prohibition only through this management service.

SPORTS-FR-004/024; SPORTS-NFR-003. User-authorized refinement; questionnaire transcript unchanged. [Build evidence](build-logs/2026-11-06-us-003-02-audited-player-id-correction.md). Wider story states remain unchanged.

## Central player record — 6 November 2026

SPORTS-FR-005 / US-003-03: **Players → Player ID → View** retains the existing profile and memberships, adding independently paginated native invoices, receipts, attendance/session references, and management-only fingerprint preparation history. Native ERPNext role, field and Company/User Permissions control financial reads; this adds no accounting roles or posting actions. Submitted Sales Invoice outstanding amounts are grouped by original currency. This summary excludes drafts/cancelled invoices and is not a full customer GL balance or an unallocated-advance reconciliation. Restricted histories show Restricted rather than a misleading zero; no linked Customer yields empty financial history.

Derive age from DOB using the academy date. Staff with Player write permission may edit preferred foot using source-revision protection. Append-only Sports Player Measurement records hold an assessment date and height in cm and/or weight in kg; values must be positive, finite and at least 0.01, and dates must fall between DOB and today. Existing historical observations cannot be overwritten; corrections are new dated observations.

Management may add birth certificates, medical reports or other supporting documents with title, optional document date and a private file. Sports Player Document is an immutable, automatically submitted archive record with native attachment protection; this internal archive submission has no financial effect. Private files inherit management/Company access through their parent; generic upload, public conversion, reattachment, replacement, cancellation, rename and deletion are blocked. Generic File listings also respect permitted document parents. No new medical or scholarship content is exposed through the broadly readable Player record. PDF files are limited to 5 MB/100 pages, unencrypted and without active content/forms/annotations; JPEG/PNG/WebP images are limited to 2 MB and normalized. No real biometric capture is provided; demo references remain explicitly labelled.

Injury/absence automation, scholarship decisions, returning-player undertakings and final retention policy remain separate refinements. Public enrollment is unchanged. [Implementation and verification](build-logs/2026-11-06-us-003-03-central-player-record.md).

## Player profile tabs — 6 November 2026

The central profile uses **Player details**, **Program enrollments**, **Invoices & receipts**, **Attendance & fingerprint**, **Measurements**, and **Documents** tabs. Player identity and common actions remain visible above the tab strip. Choose a tab or use arrow/Home/End keys while focusing the tab strip; on phones, scroll the strip horizontally. Only the selected panel is displayed. Same-player membership paging/refresh retains the active tab; a different player starts at Player details. Creating a program enrollment opens Program enrollments. Each history retains its own pagination and existing permission restrictions. This is a Sports-only presentation refinement, with no financial, document-security or public-enrollment behavior change. [Build log](build-logs/2026-11-06-us-003-03-tabbed-player-profile.md).

Player photo placement refinement (6 November 2026): a permitted private portrait appears beside the player name in the persistent header above the tabs, remaining visible across sections. Age and preferred foot stay within Player details. No photo duplication or privacy changes. [Build log](build-logs/2026-11-06-us-003-03-profile-header-photo.md).
