# Sports App product requirements document

| Field | Value |
|---|---|
| Product | Generic Sports Academy Management App |
| First academy | Moyours Sports Academy (name to confirm) |
| Version / date | 0.1 / 2026-11-01 |
| Status | Draft for review; implementation not started |
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

Parent/player self-service accounts, payment gateway integrations, SMS/WhatsApp, advanced player performance analytics, tournament/league management, accommodation, transport, medical case management, merchandise storefront, and multiple biometric vendors. Existing ERP capabilities may be configured where needed; these extensions have no committed release or estimate.

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

Cashier allocates a submitted ERPNext Payment Entry to the correct invoice. One guardian/payer Customer may fund multiple players: store player attribution at obligation/invoice allocation level and never infer a player's debt from the entire Customer balance. For MVP, use one player's obligation per invoice unless a tested line-allocation design is approved.

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

Names below are candidates, not created DocTypes. Use a `Sports` prefix to avoid collision with Primero's `Player` and `Player Application`.

| Record | Core purpose and links |
|---|---|
| Sports Academy Settings | Academy key, Company, locale/timezone, currency, numbering, branding, enabled modules and allowed defaults |
| Sports Program / Group | Configurable sport, program, roster/group, schedule and fee-plan association |
| Sports Application | Applicant/guardian contacts, submitted timestamp, review status and resulting player link |
| Sports Player | Stable registration number, names, DOB where required, contacts/guardian, status and protected attachments |
| Sports Enrollment | Player + academy/program/group, effective dates, status, fee plan and payer Customer |
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
| OQ-05 | Payer Customer model, shared guardians, refund/credit allocation and opening debt evidence | Finance / before billing implementation |
| OQ-06 | Device vendor/model/SDK, ownership of templates, identifiers, supported auth, offline behavior, timezone, consent and revocation/deletion | Management + device supplier / G0; before live biometric enrollment |
| OQ-07 | Target-site Frappe/ERPNext/Boost versions, app installation policy and console extension compatibility | Technical lead / integration spike |
| OQ-08 | Launch-required ERP module list, HR/payroll app requirements and actual Boost coverage | Finance + management / G0 |
| OQ-09 | Existing data sources, import volume, opening date, active roster, history fidelity and acceptance totals | Registrar + finance / before migration |
| OQ-10 | Concurrent users/events, target hardware, backup/restore and retention targets | Technical lead + operations / before pilot |

Do not turn unknown hardware support or broad ERP expectations into implied delivered scope. Resolve each decision in its story and record accepted architecture separately from this draft.
