# Sports App requirements

Current user decisions as of 2026-11-03 (Africa/Lagos). The [original brief](requirements.txt) is preserved. The [requirement baseline](concepts/requirement-baseline.md) lists all stable IDs and story links; the [PRD](PRD.md) describes the wider product and release gates. This document records current acceptance rules, not a claim that all planned functionality is complete.

| Requirement | Current rule | Evidence / delivery |
|---|---|---|
| SPORTS-FR-001 | Configure academy/company, sports programs/groups, currency/timezone, numbering and defaults without client-specific code. Enforce Company scope on UI and direct writes. | US-001-01, accepted into local develop |
| SPORTS-FR-002 | Public website prototype uses an app-owned content file and native Frappe www template; branded responsive pages with submittable private registration and staff review. Full CMS/publishing and production rollout remain future work. | US-001-02, prototype slice |
| SPORTS-FR-003 | Public POST creates a private Sports Registration and reference, with original timestamp, allowlisted required fields, rate limit and retry safety. Authorized Company-scoped staff review possible matches and accept exactly once into Player/Customer/User/enrollment, or reject with a reason. No guest list/read or automatic account reuse. | US-003-01, PoC workflow |
| SPORTS-FR-004 / SPORTS-FR-006 | Permanent player ID and dated program/group enrollments; same-name people remain separate; corrections retain identity and history. | US-003-02, private slice in progress |
| SPORTS-FR-026 | One save creates one player, their own Individual ERPNext Customer/contact and the first enrollment. Copy supplied player name/email/phone. No payer chooser or shared-family account. All enrollments derive the player's Customer. | US-003-02 |
| SPORTS-FR-027 | Create/reuse a Customer Group whose name is the initial program's friendly name. Assign it to the newly created Customer. Use a valid existing tree root; never overwrite an incompatible existing group. Later enrollments do not silently reclassify an existing Customer. | US-003-02 |
| SPORTS-FR-028 | Expose Sports requirements, PRD, epics, stories, ADRs, build logs and guides in an app-owned, read-only Development Tools view of the shared console, matching Boost cards/counters/tabs with documents in modal popups. Management roles only; no Finance role required. | US-002-04 |
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
