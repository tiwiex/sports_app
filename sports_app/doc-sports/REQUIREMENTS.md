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
| SPORTS-FR-031 | Multi-step enrollment shows configured fees/bank details. Make Payment creates one draft ERPNext Sales Invoice and uses its invoice-series number as the reference. Token-authorized payment claim moves the invoice to Pending Review (docstatus 0), without a receipt or ledger posting. An authorized Finance reviewer uses Confirm Payment in the invoice context menu (hidden after confirmation), or Complete Payment under View, to atomically submit the invoice and one fully allocated Payment Entry. Reuse the application-owned Customer on staff acceptance. No general Guest/registrar finance permissions. Legacy Payment Entry references remain supported. | US-005-01, invoice-first enrollment PoC |
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
