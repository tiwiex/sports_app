# Sports App requirements

## Fingerprint preparation — 5 November 2026

Directory refinement (SPORTS-FR-037): expose Fingerprint enrollments as a separate searchable, paginated table in the attendance app. Player actions and enrollment references open the selected player’s Fingerprint registration form. Keep player/request references in the form and provide a return action preserving table search/page. Reuse existing records; no new database table or capture state.

Visual demo refinement (SPORTS-FR-037): show a generic fingerprint illustration with a clearly simulated scan animation during Demo capture, and completion only after the demo code is confirmed. Keep the barcode/reference underneath. The drawing is identical for all players, contains no collected biometric data and respects reduced-motion preferences. No real capture-status or attendance changes.

Demo refinement (SPORTS-FR-037): administrator-only Demo capture generates one stable, unique DEMO-prefixed random numeric reference per pending preparation and renders a CODE128 barcode. Record operator/time, reject withdrawn requests and preserve the code across retries/withdrawal history. UI may show Demo captured (simulated) but real status remains Pending capture. No fingerprint data, real enrolled state, barcode authentication or automatic attendance.

Player-list refinement: administrator-only searchable directory includes all permitted academy players, even those without a request. Show name/ID, latest preparation status (Not prepared, Pending capture, Withdrawn), finger and request reference. Paginate in stable name/ID order, retain Company/native permission scope, and refresh after prepare/withdraw. No consent-person details in the directory payload; these remain in the selected player's protected history.

SPORTS-FR-037: Administrator-only online preparation linked to an existing Company-scoped player, with selected finger, supplied consent person/relationship/reference/date and explicit confirmation. Sports Biometric Enrollment retains Pending capture or Withdrawn status and auditable withdrawal reason. Prevent duplicate pending requests and changed-payload retries. No raw fingerprint/template/image, external identity mapping, captured/enrolled status or biometric attendance until validated hardware integration. Do not copy consent metadata into offline rosters. [US-007-01](backlog/user-stories/us-007-01-biometric-provider-and-identity.md).

## Dedicated attendance frontend — 3 November 2026

5 November refinement (SPORTS-FR-014/036): add online **New session** in the Next.js attendance app. Reuse native session creation and eligible roster snapshots, configured academy timezone, friendly permitted programs/groups and server creation permissions. Preserve a stable request UUID/payload across uncertain failures and tab reload; offline creation stays disabled. Cancellation/finalization remain in Boost.

Console entry refinement: Sports App contributes **Sports → Attendance App**, with an explicit new-tab link to `/sports-attendance`, through its own optional provider manifest and asset. Only authorized Sports player-management staff receive the entry. ERP Boost remains generic; no host code/role/schema change is required.

SPORTS-FR-036: Sports-owned Next.js attendance PWA reuses authenticated Sports sessions/rosters and native attendance saves. Explicit trusted-device download enables offline manual marking into a user/company-scoped IndexedDB queue. Pending choices survive reload and remain provisional until explicit online sync under the same account/company. Preserve original server versions, idempotent same-result retries, visible durable conflict review and reasoned corrections. Cache only the public shell in the service worker; never tokens or API responses. Offline identity expires after seven days without deleting pending work. No biometric identity, auto-absence or offline admission/accounting is implied. [US-006-04](backlog/user-stories/us-006-04-attendance-pwa.md), [guide](attendance-app-guide.md).

Scope clarification (3 November 2026): enrollment remains the existing HTML website. The experimental Next.js enrollment requirement `SPORTS-FR-035` is withdrawn; retain its ID for audit history. The requested Next.js app is for attendance, with scope to be refined against SPORTS-FR-014/015. [Reversal evidence](build-logs/2026-11-03-us-001-04-revert-enrollment-pwa.md).

Current user decisions as of 2026-11-03 (Africa/Lagos). The [original brief](requirements.txt) is preserved. The [requirement baseline](concepts/requirement-baseline.md) lists all stable IDs and story links; the [PRD](PRD.md) describes the wider product and release gates. This document records current acceptance rules, not a claim that all planned functionality is complete.

| Requirement | Current rule | Evidence / delivery |
|---|---|---|
| SPORTS-FR-001 | Configure academy/company, sports programs/groups, currency/timezone, numbering and defaults without client-specific code. Enforce Company scope on UI and direct writes. | US-001-01, accepted into local develop |
| SPORTS-FR-002 | Public website prototype uses an app-owned content file and native Frappe www template; branded responsive pages with submittable private registration and staff review. Full CMS/publishing and production rollout remain future work. | US-001-02, prototype slice |
| SPORTS-FR-003 | Public POST creates a private Sports Registration and reference, with original timestamp, allowlisted required fields, rate limit and retry safety. Authorized Company-scoped staff review possible matches and accept exactly once into Player/Customer/User/enrollment, or reject with a reason. No guest list/read or automatic account reuse. | US-003-01, PoC workflow |
| SPORTS-FR-004 / SPORTS-FR-006 | Permanent player ID and dated program/group enrollments; same-name people remain separate; corrections retain identity and history. | US-003-02, private slice in progress |
| SPORTS-FR-026 | One save creates one player, their own Individual ERPNext Customer/contact and the first enrollment. Copy supplied player name/email/phone. No payer chooser or shared-family account. All enrollments derive the player's Customer. | US-003-02 |
| SPORTS-FR-027 | Create/reuse a Customer Group whose name is the initial program's friendly name. Assign it to the newly created Customer. Use a valid existing tree root; never overwrite an incompatible existing group. Later enrollments do not silently reclassify an existing Customer. | US-003-02 |
| SPORTS-FR-028 | Expose Sports requirements, PRD, epics, stories, ADRs, build logs and guides in an app-owned Development Tools view (read-only documents, narrowly editable story metadata) of the shared console, matching Boost cards/counters/tabs with documents in modal popups. Management roles only; no Finance role required. | US-002-04 |
| SPORTS-FR-029 | New players require a valid unique email and receive an automatically linked, disabled Website User with only the non-Desk Sports Player role. No welcome email, password or activation; future self-service access is a separate workflow. Existing accounts are never silently reused. | US-003-02 |
| SPORTS-FR-030 | Shared enrollment/registration details: split names, birth date, gender, position, school, medical notes, player and guardian contacts/address, emergency contact and independent consent choices. Extend Sports Player; every new app-owned DocType must start with Sports. Preserve automatic Customer/User creation and unique player email. Public form saves Sports Registration for authorized review; Make Payment creates a prospective Customer/draft Sales Invoice, and acceptance reuses that Customer for the Player/User/enrollment. | US-001-02, US-003-02 |
| SPORTS-FR-031 | Multi-step enrollment shows configured fees/bank details. Make Payment creates one draft ERPNext Sales Invoice and uses its invoice-series number as the reference. Token-authorized payment claim moves the invoice to Pending Review (docstatus 0), without a receipt or ledger posting. An authorized Finance reviewer uses Confirm Payment in the invoice context menu (hidden after confirmation), or Complete Payment under View, to atomically submit the invoice and one fully allocated Payment Entry. Authorized enrollment acceptance may combine admission with that same invoice/receipt completion in one atomic action; draft/unclaimed invoices cannot be accepted. Show invoice reference/workflow in the enrollment queue. Reuse the application-owned Customer on staff acceptance. No general Guest/registrar finance permissions. Legacy Payment Entry references remain supported. | US-005-01, invoice-first enrollment PoC |
| SPORTS-FR-019 / SPORTS-FR-020 | One optional Boost console, with separate app ownership and a versioned provider interface. Finance-only/basic Sports users must not gain private player or management-document access. | US-002-01 accepted; US-002-02/03 planned |
| SPORTS-NFR-003 | Registration retries/concurrent requests create no duplicate player, User, Customer, contact or initial enrollment. Validation failures leave no partial records, including program-category creation. | US-003-02 |
| SPORTS-NFR-006 | Friendly program/group names in controls and profiles; usable desktop/phone workflows. Preserve internal IDs. | US-003-02 and later UI stories |
| SPORTS-NFR-009 | Every story delivery and every adjustment/fix/refinement receives its own dated, indexed build log with actual verification, data impact, limitations and cleanup. | Repository AGENTS.md; US-002-04 |

## Background creation and permissions

Registrar authority covers a narrow server operation that creates the player's disabled User, Customer, contact and program category. It does not grant general accounting, Customer Group, Customer or Contact write privileges. ERPNext validations still run. Preserve Company/User Permissions, immutable Customer linkage and stable registration IDs. Customer IDs derive from player IDs; display names are player names.

The program category is the initial registration classification because ERPNext has one Customer Group per Customer. Additional program enrollments retain it. Classification changes for existing accounting records require an explicit later workflow. Territory follows ERPNext Selling Settings, falling back to an existing territory matching the academy Company's country; missing master configuration raises a setup error.

## Remaining product scope

Production application hardening, full role boundaries, configurable publishing, fee plans/scholarships, player-attributed invoices/payments, attendance, biometric integrations and ERP launch acceptance remain the linked backlog. Ordinary direct registration creates no invoices or payments. The authorized enrollment Make Payment action creates a draft invoice; an applicant claim moves it to Pending Review without a receipt or ledger posting. Finance alone completes payment: invoice and allocated receipt submit together or roll back together. Recurring invoices, partial payments and production reconciliation remain separate scope. Do not treat installed apps or a working form as complete financial delivery.

## Club relations refinement — 2 November 2026

| Requirement | Rule | Delivery |
|---|---|---|
| SPORTS-FR-032 | Company-scoped generic Sports organisations, opportunities and internal correspondence logs in the shared console. Native permissions apply; no automatic finance parties, sending or player-profile sharing. | US-009-01 |
| SPORTS-FR-033 | Source-attributed Nigerian and international football directory with Unrated/1–5 staff relationship-priority assessment, required rationale and server-attributed assessor/date. Idempotent imports preserve staff changes; no invented performance score or contacts. | US-009-01 |

Club relations UI refinement: SPORTS-FR-032/033 use searchable paginated tables with optional email-only filtering. Public contact enrichment must record publication purpose/source/review date, preserve staff contacts and distinguish supporter/general inboxes from recruitment contacts. No messages or mailbox probes are sent by enrichment.

## Column sorting and combined filters — 2 November 2026

Organizations have a clearly labelled Organization or email search, Country, Priority and Relationship filters, plus With email only. Filters combine; Clear filters resets them. Click Organization or Country (or another sortable column) to toggle ascending/descending ordering; arrows and accessible header state show the direction. Sorting runs on the server across the full Company-scoped result set before 30-row pagination, with a stable record-ID tie-break. Changing a filter or sort returns to page one. Switching tabs clears tab-specific filters and sorting. Opportunities and Correspondence support sorting of their own text/status/date columns; the linked organization label there is not sortable. This avoids sorting by opaque linked IDs.

## Payment review notifications — 3 November 2026

| Requirement | Rule | Delivery |
|---|---|---|
| SPORTS-FR-034 | Sports Academy Settings provides a comma-separated payment review email list. Validate/normalize/deduplicate addresses; blank disables notifications. The first token-authorized website payment claim queues one linked review email in the same transaction as Pending Review, including legacy receipt references. Retries send no duplicates; rollback leaves no notification. Messages describe an unverified transfer claim and grant no approval rights. | US-005-01 |

## Registration table and context actions — 3 November 2026

SPORTS-FR-003 refinement: Sports Registrations follows the invoice table presentation with sortable columns, status badges and a reference dropdown. View opens a modal without leaving the list. Pending registrations expose Accept/Reject only with document write permission; actions fetch the latest record before opening confirmation. Accept retains possible-match review and enrollment choices; Reject requires a reason. Accepted/rejected/read-only rows expose View only. Existing admission/finance permissions and server validations remain authoritative.

## Enrollment naming and profile layout — 3 November 2026

SPORTS-FR-003 refinement: rename the staff application queue and its user-facing controls from Registrations to Enrollments. Use Enrollment application to distinguish the incoming application from the dated program membership created on acceptance. View is a grouped, responsive profile with summary/status, admission controls/matches, billing/payment, player, guardian/emergency and consent sections. Preserve IDs, existing application/program-membership records, permissions and finance provenance; this terminology refinement requires no DocType rename or data migration.

## Manual attendance prototype — 3 November 2026

SPORTS-FR-014/015: Sports → Attendance provides same-day scheduled sessions with academy timezone, creator/operator and a fixed roster from Active date-eligible enrollments in the chosen program/group. One player/session record is enforced even with overlapping enrollments. Staff explicitly save Present/Late/Absent/Excused; remaining Unmarked entries become Absent only on confirmed finalization. Corrections require a reason and preserve native audit history. Repeated requests are idempotent and stale changes are rejected; a batch failure rolls back the batch. Cancelled sessions are read-only.

Prototype access uses existing Sports Registrar/Academy Administrator/System Manager roles with Company/document permissions. Group-restricted coach assignments, roster exceptions, cross-session reports/rates and biometric integration remain open. No biometric data or financial posting is introduced. [Guide](attendance-guide.md).

## Player list and profile layout — 3 November 2026

SPORTS-FR-005 refinement: Players follows the Enrollments table/reference-menu pattern, with a grouped responsive private profile modal that preserves list/search context. Sort identity/company/date columns server-side; expose New program enrollment only with player-write and enrollment-create permission. Show existing account links, paginated memberships, contact details and explicit consent choices. No finance/attendance history completion is implied by this presentation slice (US-003-03).

## BA questionnaire discovery — 6 November 2026

[BA-QNR-001 source register](discovery/README.md) and [question-by-question reconciliation](discovery/BA-QNR-001-reconciliation.md) preserve exact responses and classify overlap/new scope. These are proposed refinements; current implemented fees, IDs, role permissions, disabled Users and admission/payment behavior remain authoritative until a recorded decision changes them. Original-only scope is not removed.

| Requirement | Proposed discovery addition | Origin / delivery |
|---|---|---|
| SPORTS-FR-038 | Player performance assessments | Questionnaire only; [US-003-04](backlog/user-stories/us-003-04-player-performance-assessments.md), Proposed |
| SPORTS-FR-039 | Procurement and player kit distribution | Both; [US-008-04](backlog/user-stories/us-008-04-procurement-and-player-kit-distribution.md), Proposed |
| SPORTS-FR-040 | Arrival, departure and absence review | Both; [US-006-05](backlog/user-stories/us-006-05-arrival-departure-and-absence-review.md), Proposed |
| SPORTS-FR-041 | Parent reminders and receipt delivery | Questionnaire only; [US-005-04](backlog/user-stories/us-005-04-parent-reminders-and-receipt-delivery.md), Proposed |
| SPORTS-FR-042 | Payment gateway discovery and reconciliation | Questionnaire only; [US-005-05](backlog/user-stories/us-005-05-payment-gateway-discovery-and-reconciliation.md), Proposed |

## Story review controls — 6 November 2026

SPORTS-FR-028 refinement: management-authorized Sports Development Tools provides MoSCoW and status edits in the story table and reader modal, plus Mark Done while reading. Only allowlisted individual story metadata is writable; other document content remains read-only. Preserve narrative, provenance and partial-delivery qualifiers unless status is explicitly changed. Require source-revision matching, serialize edits, synchronize epic/backlog rows, and create an indexed reviewer/time/change build log for each actual edit. Mark Done is a human review decision and does not run tests or certify hardware/implementation. No general file editing or new finance permissions.

SPORTS-FR-028 / SPORTS-NFR-006 presentation refinement (6 November 2026): use Boost-style separated table columns and header/content hierarchy, status-tinted rows and independently coloured MoSCoW badges/selectors. Retain text labels, readable widths, horizontal table scroll and stacked mobile reader controls. No status, priority or authorization behavior change.

SPORTS-FR-028 interaction refinement (6 November 2026): status and MoSCoW dropdown selections autosave in the story table and reader; remove Save buttons and duplicate priority labels/badges above dropdowns. Retain accessible labels, table heading, colour distinction, audit/revision checks and Mark Done. Failed saves restore the confirmed selection and show an error.

SPORTS-FR-028 presentation refinement (6 November 2026): remove duplicate status badges/visible labels above status selectors, preserving accessible names and the table heading; place Mark Done immediately beside Open in each row, with feedback below. Keep autosave, colours and reader quick completion unchanged.

SPORTS-FR-028 / SPORTS-NFR-006 viewport refinement (6 November 2026): increase the Sports Development Tools table scroll cap from 70vh to 110vh so long lists extend beyond the navigation area; retain sticky headings, internal vertical/horizontal scrolling and natural height for short lists.

SPORTS-FR-019 / SPORTS-NFR-001/006 navigation refinement (6 November 2026): where authorized Sports views appear in the shared console, show the Sports group before Boost groups. Use green Sports and blue Boost group headings, with visibly indented child items and clear active/focus states. Sports owns the presentation enhancement; preserve host routing, permissions, search and collapse behavior. Without Sports entries, native-only navigation is unchanged.

SPORTS-FR-019 / SPORTS-NFR-006 hierarchy refinement (6 November 2026): consolidate native Boost sections beneath one collapsible blue Boost parent below Sports. Nested finance section labels use lighter styling and retain their own collapse controls; do not present each as an independent app group. Preserve permissions, routes and other provider identities. Native-only navigation remains unchanged when no Sports menu is present.

SPORTS-FR-028 / SPORTS-NFR-006 stability refinement (6 November 2026): keep Status/MoSCoW controls mounted and enabled while autosaving; do not rebuild the table or reader on save completion. Queue consecutive changed fields using confirmed revisions, update other visible copies in place, retain focus/scroll and preserve failure restoration.

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

## EPIC-004 accepted prototype policy — 6 November 2026

User authorized the Sports-only scholarship/fee-plan/manual monthly billing slice. Academy management approves/revokes restricted effective-dated decisions; an unassigned Sports Finance role can read them and run billing alongside existing native permissions. Coaches gain no scholarship access. Keep category/benefit records separate from routine financial payloads and Customer Groups. Approved records retain actor/time, no overlap or history deletion, and no silent rewrite of issued invoices.

Full monthly fee is due for current Active memberships eligible at the start of the calendar month. Mid-month joiners are not charged that month; suspended records and mid-month concession changes require review. Plans require explicit service item, income ledger, cost center, company currency, effective dates and due day. Month-aligned enabled plans cannot overlap. Partial coverage remains available as a dated concession, not an invented player category. No automatic expiry, payment-free admission, refund, grace/notice or historical suspension policy is inferred from TBD/blank answers.

Retain current NGN250,000 public enrollment charges and configurable NGN40,000 monthly default; the earlier questionnaire fee ambiguity does not override that explicit user answer. Manual preview/generation creates one immutable enrollment/month obligation and at most one draft Sales Invoice; zero-due obligations create no invoice or receipt. Stable keys, revision checks, serialization and row-level rollback protect retries. Routine previews exclude scholarship reasons, status, benefit flags and decision IDs. Native invoice approval/payment controls remain; no automatic posting, scheduler or email. See [billing guide](billing-guide.md) and [build evidence](build-logs/2026-11-06-epic-004-scholarships-and-monthly-billing.md).

Academy Settings tab refinement (6 November 2026, SPORTS-FR-001 / SPORTS-NFR-006): organize the existing controls into General, Player IDs, Enrollment defaults, Monthly fees, Website payments and Programs & groups. Save remains global; switching tabs preserves unsaved values and existing validation, permissions and data semantics. [Build evidence](build-logs/2026-11-06-us-001-01-tabbed-academy-settings.md).

## Item-based enrollment and subscription pricing — 7 November 2026

Accepted user refinement of SPORTS-FR-001/009/010/031, supplementary to BA-QNR-001 rather than a change to its original responses. Academy Settings → Website payments contains an invoice-style **Enrollment charges** table: select existing enabled sales Items, quantity and rate; the server calculates amounts. Configure 1–30 rows with a positive total. Item names and quantities appear on the public payment page and become invoice lines. Stock Items can be charged without stock issuance; procurement/distribution remains separate. No hardcoded registration/jersey Item creation remains.

The additive migration copies saved legacy charges once, preserving the current NGN250,000 total. Existing invoices, immutable fee snapshots, references and legacy receipts are retained. Removing all rows after migration cannot resurrect legacy fees. New settings edits supersede the fixed two-charge model for future applications only.

Sports Fee Plan may select an existing **ERPNext Subscription Plan** for one Month, interval count 1, Fixed Rate and the company currency. Its enabled non-stock sales Item and current native rate override manual Item/amount inputs. Native Plan/Item read permissions are required. A plan-price change requires a fresh preview for ungenerated charges; generated obligations retain their original invoice. Manual Item/rate plans remain supported when no Subscription Plan is linked. Native Subscription records, automatic scheduled invoicing/posting and prorating are not enabled; this avoids competing lifecycles with the manual scholarship-safe generation process. The website monthly amount remains explicitly informational.

[Adjustment evidence](build-logs/2026-11-07-us-001-01-configurable-enrollment-items-and-subscription-pricing.md).

## PDF receipts and manual delivery — 7 November 2026

User-approved refinement: invoice/receipt references in the player financial history and enrollment review open native PDF downloads in a new tab. Links use an underline, link colour and visible PDF ↗ indicator. The final **Elapsed** column shows minutes/hours/days since finance-record creation or application submission; labels update every 30 seconds while connected, without editing source dates or balances.

Posted positive Customer Receive receipts expose **Email receipt** in the player receipt menu and, for the linked accepted application, its context menu. Require native receipt read/print/email, player access and matching Company/Customer. A dialog defaults the permitted guardian email (or player email) and requires explicit confirmation of one recipient. Server rechecks eligibility and attaches the native receipt print format as PDF. A receipt lock and stable per-dialog request key prevent lost-response duplicates; changed-recipient retries are rejected. Native Communication and Email Queue provide audit and delivery status; queued does not mean delivered. Default outgoing Email Account and working PDF generation are required. No scheduled reminder or automatic acceptance email is enabled.

The transactional email may reach disabled future player/guardian Website Users without activating their accounts. No financial posting, new role grant or Boost change. [Build evidence](build-logs/2026-11-07-us-003-03-pdf-receipts-email-and-elapsed-time.md).

## Main-table document actions and branded PDF modals — 7 November 2026

Subsequent user refinement supersedes the normal new-tab PDF interaction above: ordinary clicks open an in-console **PDF preview** modal with an Open / download fallback. Ctrl/Cmd-click still supports the browser’s normal new-tab behaviour. Main **Players** adds **Latest invoice**, **Latest receipt** and final **Elapsed** columns, plus View invoice PDF / View receipt PDF / Email receipt in the player menu when permitted. Latest refers to newest creation time; the player profile retains access to older documents. Main **Enrollments** has linked invoice and posted receipt columns and matching context actions, without opening the inner profile first.

Financial references use native permission-filtered Company/Customer queries. Sports-only staff without finance access receive no finance IDs. Email retains posted Receive/read/print/email checks and explicit recipient confirmation. No accounting states or dates change.

Backend Print Formats **Sports Academy Invoice** and **Sports Academy Receipt** provide green/gold branding, existing website crest on Moyours, clear reference/date/party/line-item/total sections and draft/cancelled indicators. The receipt shows only its recorded amount and allocations; it does not claim all customer invoices are settled. Sports PDF preview/download and receipt email explicitly choose these formats. They do not replace ERPNext global print defaults. **Academy Settings → General → Document logo** configures the Sports PDF logo; another academy can use its own image, falling back to its Company logo. This deployment reuses Moyours’ existing public crest and leaves Company branding unchanged.

[Build evidence](build-logs/2026-11-07-us-003-03-main-table-finance-and-branded-pdf-modal.md).

Player profile presentation refinement (7 November 2026): show each label with a colon and its bold value on the same row, including linked accounts. Give cards clearer green accents, section dividers and spacing; retain desktop two-column/phone single-column layout and wrap long value text. Native account links, tab/history behaviour and all data/finance permissions are unchanged. [Build evidence](build-logs/2026-11-07-us-003-03-inline-player-profile-details.md).

## Automatic monthly receivables — 7 November 2026

Explicit user direction supersedes the earlier manual/draft-only monthly policy: eligible Active enrollments are billed automatically each calendar month and positive charges are submitted to native ERPNext accounting, producing outstanding receivables. The first-day/full-fee eligibility rule and approved concessions remain unchanged; mid-month joiners begin the following month. No payment/receipt or bank clearance is inferred.

Academy Settings → Monthly fees now controls automatic submission, an explicit earliest billing month (first-day date) and the enabled System User that executes billing. A daily Sports scheduler processes the current month and retries missed months from that start date only, evaluated in academy timezone. Months before the start are not backfilled. Disabled monthly fees or automatic billing stops the job. Native Company/Player/Enrollment/accounting scope, invoice read/create/submit, workflow conditions and configured approver checks remain mandatory. No user roles are granted.

Deterministic enrollment/month keys, shared settings and enrollment locks, immutable snapshots and per-row rollback prevent duplicate obligations/invoices/ledger posting. Existing submitted invoices remain unchanged; legacy drafts resume under the same reference. Cancelled invoices require reviewed correction. Full concessions create zero obligations without invoices or receipts. Failures do not stop other rows: failed enrollment/month keys enter native Error Log and staff can inspect the Monthly billing preview. An unreadable or invalid execution user fails the native scheduled job; jobs and errors are visible in Desk Scheduled Job Type / Error Log.

The Sports-owned invoice workflow gains a conditional Submit monthly fee transition for existing invoice-approval roles, applicable only to a valid Sports monthly obligation without enrollment-application provenance. Ordinary invoices and enrollment payment review retain their existing paths. Custom third-party workflows are not rewritten; if no permitted synchronous submitted transition exists, the charge fails safely. No Boost code/global settings or native Subscription scheduler is changed. No automatic parent invoice/reminder email is introduced; normal installed native notification hooks retain their configured behavior.

Manual Preview and Generate and submit invoices remain available for authorized recovery, with the same posting behavior and native permissions. Source changes require a new preview for ungenerated charges. This adjustment does not complete installment/refund/grace/returning-player or automatic reminder policy scope.

[Automatic monthly receivables](build-logs/2026-11-07-us-004-03-automatic-monthly-receivables.md).

## Subscription overview and checkbox payments — 7 November 2026

User requested the Community App Membership Admin Overview and Payments pattern for Sports subscriptions. Community source was inspected read-only; Sports owns its independent implementation with no Community runtime dependency or Boost source changes.

Sports → Scholarships & Billing opens an Overview with scoped enrollment/active counts and submitted annual/monthly billed, settled and outstanding totals. Settled includes allocations/credits and is explicitly not reported as cash receipts. Payments provides a paginated player/program-by-month grid, year and player-name filters, explicit unpaid/partial/paid/no-charge/unbilled/review/future/cancelled states, overdue indication and source invoice/receipt PDF modals. Financial status comes from native submitted invoices and outstanding amounts; no checkbox directly toggles accounting state. Fully exempt months do not produce false payments.

Authorized Finance selects up to 20 payable cells, an enabled same-company/currency Bank or Cash account, payment date and bank/cash reference, then explicitly confirms funds received. One action generates/submits an eligible missing monthly invoice if necessary and creates/submits a fully allocated Payment Entry for the remaining balance. Each cell has a separate Customer-attributed receipt, so reversal does not affect other months or players. Partial balances can be fully settled; arbitrary installment scheduling is not implemented. Native accounting, Company/Player permissions, workflow and configured approver checks remain mandatory. There are no new role grants or general finance bypasses.

A stable request key and payload hash return the same receipt on retries; changed retry inputs are rejected. Shared settings/enrollment/invoice locks serialize requests. Failure at receipt submission rolls back that cell's obligation, invoice and ledger as well as its receipt; successful independent cells are reported separately. Existing invoices retain original billing snapshots and already-paid cells are not collected again.

Activate reversal exposes selectors for submitted receipts created by this grid only. A reason, native receipt read/cancel and an allowed cancellation workflow are required. Cancellation reopens the invoice's native outstanding balance while retaining the charge and audit trail. Repeating cancellation is safe; retrying the old payment request after reversal returns Cancelled instead of creating a replacement. A new explicit confirmation may settle the reopened balance. Enrollment receipts, unrelated multi-invoice receipts, credit notes, bank reconciliations and actual cash refunds stay in their own reviewed native processes.

Automatic monthly invoice posting remains a separate implemented feature whose development activation still awaits an explicitly approved execution account. This manual checkbox collection interface does not enable it or assign Administrator. No real development balances were changed by QA; no production deployment, commit, PR or merge requested.

[Build evidence](build-logs/2026-11-07-us-005-01-subscription-overview-payment-grid.md).

## Checkbox invoice-only and delivery refinement — 7 November 2026

Payments month checkboxes now support **Generate invoices** (receivables only, including historical eligible months) separately from **Save payments** (confirmed receipt collection). Invoice-only generation does not require bank details or post a receipt. Future months are rejected here. Payment references are optional and generated deterministically if blank; a configured receiving ledger is preselected only when permitted/valid. Billing exceptions show their reason. This supersedes the earlier mandatory-reference UI requirement; native finance controls and effective fee-plan snapshots remain authoritative.

Sports release URLs now ensure complete, web-readable versioned assets are published before advertisement; old hashes remain available. No Boost change. [Historical test evidence](build-logs/2026-11-07-us-004-03-january-test-and-checkbox-invoices.md) · [Asset recovery](build-logs/2026-11-07-us-005-01-extension-asset-recovery.md).

## Completed-month automation and payment-only checkboxes — 7 November 2026

Explicit user correction supersedes the earlier month-start issuance, automation-start floor and checkbox invoice-generation interactions. **Submit monthly invoices automatically after their calendar month ends**, catching up from each currently Active enrollment's start date. Keep the approved full-fee eligibility at the first day of each billed month, dated fee-plan rates, concessions and native accounting mappings. A January-1 enrollment is eligible for January–October invoices on 7 November; November becomes eligible on 1 December. Midmonth joiners still begin with the following full month. Existing invoices/receipts remain authoritative and are not silently cancelled/repriced.

The Sports daily task now derives completed periods from each enrollment, so the deprecated global start-date value cannot hide historical obligations. Native settings retain that value for compatibility but hide its editor. Automation enablement and the enabled, deliberately selected execution User remain required, with native Company/read/create/submit/workflow/approver controls and no role grants. Enrollment, fee-plan and Academy Settings updates request a deduplicated catch-up after commit; the daily job provides ongoing month-boundary generation and failure retries. Install/migrate registers the Sports daily Scheduled Job Type. Opening a grid does not post accounting.

**Payments checkboxes mean receipt collection only.** Unpaid/partial cells are unchecked, paid cells are checked with a green background; unbilled/not-due/future/review/no-charge cells have no payable checkbox. Check the received months and Save payments, with explicit funds confirmation. The payment API refuses a missing or unsubmitted invoice and never creates its charge. The Generate invoices button is removed from Payments and the Generate and submit invoices button is removed from Monthly billing; that tab is a read-only status/exception view. Native accountant recovery services are not the ordinary workflow. The compact yearly grid keeps amounts/status in tooltips and invoice/receipt PDF links under a documents menu. Activate reversal selects permitted grid receipts, requires a reason and restores the native outstanding balance without deleting the charge.

The first corrected run registered the missing daily task and posted nine missing completed-month invoices for the retained January test enrollment. January–October now each have a submitted native invoice. No payment or email was created, and existing invoices/receipts were preserved, including an already-posted November test invoice from the earlier manual flow. New automatic runs exclude current/future months. Existing selected execution account, automation switch, saved fee plans and global scheduler configuration were not changed.

[Build evidence](build-logs/2026-11-07-us-004-03-completed-month-automation-payment-only-grid.md).


## Payments summary cards — 7 November 2026

SPORTS-FR-011 / SPORTS-FR-012 / SPORTS-FR-023, US-005-02: Payments also displays the Overview's Program enrollments, Active enrollments, Billed this year and Outstanding cards above the payment controls. The same permission-scoped Overview API supplies selected-year totals across all visible enrollments, independently of grid pagination/player search; this scope is stated beside the cards. Refresh, year changes and completed payment/reversal actions reload totals. Enrollment counts retain the Overview's current enrollment semantics. No billing/payment, permission or schema change.

[Build evidence](build-logs/2026-11-07-us-005-02-payment-summary-cards.md).


## Summary card colours — 7 November 2026

US-005-02 / SPORTS-FR-011, SPORTS-FR-012, SPORTS-FR-023: Overview and Payments share coloured summary cards: blue enrollments, teal active enrollments, green billed amounts, red positive outstanding balances and green cleared balances. Soft matching backgrounds, accent borders and bold values follow the Community App visual direction; text labels retain meaning independently of colour. This is a visual refinement with unchanged financial totals and scope. [Build evidence](build-logs/2026-11-07-us-005-02-summary-card-colours.md).


## Sports Academy landing dashboard — 7 November 2026

SPORTS-FR-023 / SPORTS-NFR-002 / SPORTS-NFR-005, US-008-02: replace the Sports Academy introductory text with a read-only dashboard. Coloured cards show visible player counts, current Active program memberships, Pending applications and non-cancelled sessions in the academy's current month. The next five Scheduled sessions from today show title, date/time and venue with native record links. Active memberships are enrollment counts, not unique active players or reconstructed historical eligibility.

Authorized finance users also see selected-year monthly subscription Billed, Settled and Outstanding totals with a twelve-month billed/outstanding chart. Reuse the existing permission-scoped subscription Overview service: submitted monthly invoices only, not enrollment fees/all ERP revenue; Settled includes accounting credits and is not cash receipts. The year filter affects financial totals only. Operational counts remain current. Missing native permissions show Restricted, not zero; no scholarship, biometric or player contact data is included.

Role-scoped shortcuts use the existing host dashboard navigation to Players, Enrollments, Attendance, Scholarships & Billing and Academy Settings. Refresh, year changes and host data-change watchers update the dashboard, with loading, empty, restricted, retry and unmount protection. Desktop and phone layouts use the same coloured summary style. This delivers the landing-dashboard slice; broader date/program filters, exports, attendance outcome reporting and production p95 acceptance remain open. [Build evidence](build-logs/2026-11-07-us-008-02-academy-landing-dashboard.md).
