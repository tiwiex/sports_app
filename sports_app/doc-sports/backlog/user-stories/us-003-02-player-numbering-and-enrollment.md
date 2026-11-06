# US-003-02: Assign stable player IDs and enrollment dates

## Header

- Epic: [EPIC-003](../epics/EPIC-003-registration-and-player-record.md)
- State: In progress
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** registrar, **I want** to maintain unique player IDs and effective enrollments **so that** all downstream records identify the correct player.

## Traceability

- Requirements: `SPORTS-FR-004`, `SPORTS-FR-006`, `SPORTS-NFR-003`
- Dependencies: [US-003-01](../../backlog/user-stories/us-003-01-application-intake-and-review.md), [US-001-01](../../backlog/user-stories/us-001-01-academy-and-program-settings.md)
- Planned branch: `story/us-003-02-player-numbering-and-enrollment`
- Planned build log: `YYYY-MM-DD-us-003-02-player-numbering-and-enrollment.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given simultaneous new registrations, when IDs are assigned, then each academy-scoped registration number is unique, immutable and independent of player name or public slug.
2. Given acceptance or direct registration, when enrollment is confirmed, then program/group, automatically created per-player Customer link, start/end dates and active status are validated.
3. Given withdrawal, suspension or a same-name player, when records are updated, then existing history remains linked to the correct immutable ID and future eligibility follows effective dates.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Private registration slice](../../build-logs/2026-11-01-us-003-02-player-numbering-and-enrollment.md).
- Verification summary: Direct private registration, stable IDs, enrollment, automatic per-player Customer creation, concurrent retries and three browser role profiles verified on the development site. See the build log.
- Remaining decisions / follow-up work: Public application acceptance integration depends on US-003-01; full identity/contact duplicate policy, broader role boundaries and downstream eligibility integration remain open. This private slice is not a completed public intake workflow.

## Current delivery slice

User requested player management and ERPNext Customer linkage after accepting settings. Start with private direct registration, an immutable Sports Player identity and Sports Enrollment Customer/date/status records. Public intake can later call this foundation; US-003-01 is still Proposed. Sports Registrar is the initial restricted operator role. Player-attributed invoicing and receipt history remain EPIC-004/005. See the [usage guide](../../players-guide.md).

User refinement (2026-11-01): registration must create one Customer per player from the supplied details in one save. No shared family Customer or payer selector. Customer/contact/player/enrollment writes must roll back together, and retries must not duplicate any record. Program/group controls and profile rows show friendly names while retaining stable IDs internally.

Program categorization and hidden native Customer-field refinement: [separate adjustment log](../../build-logs/2026-11-01-us-002-04-guardrails-docs-and-program-categories.md). New Customers belong to a program-named group based on their immutable initial registration program; future enrollments retain that classification.

Follow-up: [asset cache refresh and Boost-style documentation modals](../../build-logs/2026-11-01-us-002-04-asset-cache-and-modal-layout.md). Content-fingerprinted assets must load after migration and browser reload; documentation uses the host card/tab styles with Frappe modal readers.

Follow-up: [Player Users and User role editor](../../build-logs/2026-11-01-us-003-02-player-users-and-role-editor.md). New players require a unique email and receive a disabled Website User; activation remains deferred. Standard System Manager User role-editor access is restored without new Boost Admin powers.

User refinement: [Full menu and shared registration fields](../../build-logs/2026-11-01-us-001-02-menu-and-registration-fields.md). Share the reference enrollment details with staff registration, retain unique player email and automatic Customer/User provisioning, and prefix any new DocTypes with Sports. Public intake remains demo-only.

Superseding refinement: public enrollment now submits Sports Registration for staff review/acceptance, documented in [US-003-01 evidence](../../build-logs/2026-11-01-us-003-01-public-submission-and-review.md). Earlier demo-only submission scope is historical; wider publishing/production scope remains open.

Presentation follow-up: [Player reference menu and grouped profile modal](../../build-logs/2026-11-03-us-003-03-player-profile-layout.md). Existing program-membership creation and automatic account linkage are retained.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q01-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-04), [BA-QNR-001-Q02-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-03), [BA-QNR-001-Q02-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-04), [BA-QNR-001-Q02-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-05), [BA-QNR-001-Q02-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-07), [BA-QNR-001-Q02-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-08), [BA-QNR-001-Q02-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-10), [BA-QNR-001-Q02-11](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-11), [BA-QNR-001-Q02-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-12), [BA-QNR-001-Q02-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-13), [BA-QNR-001-Q04-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-13), [BA-QNR-001-Q06-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-02), [BA-QNR-001-Q07-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-05).
- Impact: Changed; Changed / needs clarification; Conflicting / needs clarification; Expanded; Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q01-04: One current location; age bands U6/U8/U10/U13/U15/U17. Confirm progression criteria and shared-session grouping; do not hardcode football bands.
  - BA-QNR-001-Q02-03: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
  - BA-QNR-001-Q02-04: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
  - BA-QNR-001-Q02-05: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
  - BA-QNR-001-Q02-07: Source example MSA17-08001 and name+year-month+continuous serial description are ambiguous. Confirm exact format; preserve immutable existing IDs and import legacy references.
  - BA-QNR-001-Q02-08: Source example MSA17-08001 and name+year-month+continuous serial description are ambiguous. Confirm exact format; preserve immutable existing IDs and import legacy references.
  - BA-QNR-001-Q02-10: Parent portal is TBD in 2.10 and No in 7.5. Retain disabled future player Users; no parent login/activation or shared-family Customer inferred.
  - BA-QNR-001-Q02-11: Returning player undertaking and reassessment history; subscription continuation; penalty and retention timeline TBD. Do not delete lifetime history or silently merge returning players.
  - BA-QNR-001-Q02-12: One current location; age bands U6/U8/U10/U13/U15/U17. Confirm progression criteria and shared-session grouping; do not hardcode football bands.
  - BA-QNR-001-Q02-13: Returning player undertaking and reassessment history; subscription continuation; penalty and retention timeline TBD. Do not delete lifetime history or silently merge returning players.
  - BA-QNR-001-Q04-13: No automatic unpaid-fee suspension; misconduct suspension/dismissal is reviewed. Display arrears without automatic exclusion; preserve any manual disciplinary audit.
  - BA-QNR-001-Q06-02: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
  - BA-QNR-001-Q07-05: Parent portal is TBD in 2.10 and No in 7.5. Retain disabled future player Users; no parent login/activation or shared-family Customer inferred.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-003-registration-and-player-record.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Confirmed player numbering and public age rule — 6 November 2026

User clarification confirms BA-QNR-001-Q02-07/Q02-08: **MSA + two-digit creation year + hyphen + two-digit creation month + continuous serial**, e.g. `MSA26-08005` followed by `MSA26-09006`. The sequence also continues across year boundaries. The backend uses the academy timezone and a locked Company-scoped counter whose key excludes month, year, editable prefix and application series. Minimum sequence width defaults to three digits and expands naturally; prefix/width remain management settings. On first initialization, seed after the highest existing matching player reference in that Company. Existing prototype IDs of another format stay unchanged and are not interpreted as legacy serials. Existing IDs are immutable; no identity, Customer or finance references are renamed.

The player reference is independent of the configurable **enrollment application** series (`MSA-ENR-.YYYY.-.#####`), accepted Sports Enrollment membership IDs and ERPNext invoice numbering. Current development player defaults are MSA / 3 digits. This supersedes the old prefix-plus-counter-only player ID format for new players.

Public HTML enrollment accepts ages **4 through 18 inclusive**, calculated from calendar birthdays against the academy-local date. Show an inline age error and enforce date bounds in the browser; reject invalid ages in the server-owned public application controller before creating a successful application/invoice. Under-4, 19-or-older and future DOBs are rejected. A February 29 birthday reaches the next age on March 1 in a non-leap year. Enforce on new applications/DOB corrections, without retroactively blocking unchanged historical applications or imposing this public intake policy on ordinary updates to existing player records. Private staff intake policy is not broadened by this web-form refinement.

Provenance: numbering is **Both** (baseline plus questionnaire, now user-confirmed); the explicit 4–18 public restriction is user direction informed by the supplied web-form screenshot, not a claim that the questionnaire stated those exact limits.

Acceptance refinement: verify August-to-September and December-to-January continuity; separate application/player counters; existing-reference preservation; concurrent allocation under settings/native-series locks; inclusive birthday bounds, leap birthdays, browser validation and direct-service age rejection. Story remains In progress for wider discovery scope.

[Build evidence](../../build-logs/2026-11-06-us-003-02-player-series-and-public-age-policy.md).

## Player email preflight and shared guardian identity — 6 November 2026

User refinement: a player email must be unique before public enrollment is submitted, not only when staff accepts it. Normalize player email; reject addresses already used by a User (including email-field aliases such as Administrator), Sports Player or another Pending Sports Registration. Rejected applications release their pending reservation. Browser preflight runs on leaving the player-email field and again before Make Payment/Submit, returning only availability; server validation remains authoritative under the existing settings lock. Preserve token-bound unchanged retries. Show a specific inline error and retain entered details. Review older applications again before financial completion, so a known conflicting email does not start the posting process.

At authorized acceptance/direct player registration, create the player's separate disabled Website User and create or reuse the guardian User. A server-owned **guardian_user** link on Sports Player supports many players to one guardian. Siblings retain separate player emails, Users, Customers and enrollment/finance histories. Player and guardian email on one form must differ. New guardian accounts are disabled Website Users without Desk roles or welcome mail; existing guardian accounts retain their original type, enabled state, roles and profile. Guardian email repetition is permitted; it never becomes a shared payer Customer. Account creation/linkage participates in the same admission transaction and rolls back on failure.

A supplied guardian email is an unverified identity reference, not proof of guardianship or permission to access children. This change does not activate accounts, grant guardian portal permissions, send invitations or implement the parent portal. Existing records are not bulk-backfilled or automatically merged; existing duplicate applications require staff/Finance correction. This user-approved account preparation refines the earlier player-only provisioning decision while leaving portal activation/access as separate scope.

Acceptance refinement: existing User/player/pending email conflicts must block public submission before an application/invoice is written; token retries remain idempotent; distinct sibling emails reuse one guardian User without changing it; fresh player/guardian Users and account links roll back on failure. Verify desktop/phone inline correction, same-email rejection, server denial and pre-finance checks. State remains In progress for wider backlog scope.

[Build evidence](../../build-logs/2026-11-06-us-003-01-email-preflight-and-guardian-users.md).

## Live operational tables — 6 November 2026

The installed Boost host now offers an optional mounted-table watcher. Sports Enrollments, Players, Attendance sessions and Clubs & Partners declare their own relevant DocTypes and retain their authorized APIs, filters, sorting, page offsets and generation guards. Committed native notifications coalesce into a background reread; a 15-second fallback catches missed notifications or writes without events. Only matching records on the current filtered/sorted page appear. Equal responses keep the existing DOM.

Updates pause while a filter/input/select, context menu or dialog is in use, then catch up. Hidden tabs do not poll; resuming/reconnecting triggers a reread. Host abort/unmount removes timers/listeners; responses recheck signal/generation/application safety. Explicit Refresh remains supported. The compatibility hook is generic and does not hardcode Sports into Boost. On an older host without the hook, manual refresh remains available. This slice updates operational queue tables; editable documentation/settings forms and the separate Next attendance application are not remounted by it.

No permissions, financial state, record identity, schema or website enrollment behavior changes. No production edits/deployment.

Acceptance refinement: matching new/updated/removed queue rows become visible without manual refresh; preserve query/page/scroll, open interactions and read permissions; verify unchanged DOM, stale result rejection, visibility/socket/poll catch-up and abort cleanup. Existing wider story status remains unchanged.

[Build evidence](../../build-logs/2026-11-06-us-002-01-live-console-tables.md).


## Legacy player import and numbering setup — 6 November 2026

Player setup refinement: Academy Settings exposes the existing player prefix/digit width plus **Player starting sequence**, a positive whole-number minimum (default 1). Set 126 to continue after legacy sequence 125. The Company counter uses the highest of the configured minimum minus one, existing issued counter and matching imported player suffixes. Changing prefix/month/year or lowering the minimum never resets numbering; existing player IDs and links remain unchanged. Enrollment application and invoice series remain independent.

Native Data Import is enabled for Sports Player, with import permission restricted to System Manager/Sports Academy Administrator roles and management checks enforced in the controller. Native Company/User Permissions still apply; imported Company must match the configured academy. Use Insert New Records with each legacy player number in the **ID** column. Preserve historical IDs verbatim; after successful insertion reserve the matching continuous suffix under the same settings/Series locks, including imports after the counter was already initialized. Nonmatching legacy formats are preserved without guessing their suffix; set the starting sequence explicitly after reconciliation. Blank IDs use automatic numbering. Do not merge duplicates or rewrite existing identities.

Player email/account validation and automatic separate Customer/disabled player User/shared guardian account preparation remain in force for imports. Imports create no invoices, receipts, balances or attendance history; create program memberships separately using staff tools. Missing/duplicate emails require source-data correction rather than placeholders or silent existing-account reuse. Obtain and review the real roster before an actual import; this adjustment prepares tooling and does not complete the migration/pilot story.

SPORTS-FR-001/004/024; SPORTS-NFR-003. User refinement of existing numbering and BA-QNR-001 legacy-roster discovery, not new questionnaire wording. [Build evidence](../../build-logs/2026-11-06-us-003-02-legacy-import-and-sequence-floor.md). Wider delivery states remain unchanged.


## Audited player ID correction — 6 November 2026

Authorized exception to the earlier immutable-ID rule: Administrator, System Manager or Sports Academy Administrator with native Player write access and permitted configured Company may use **Change Player ID** from the Players reference menu/profile or native Player form. Require a new unique 2–140-character ID (letters/digits/hyphens/underscores), a reason and current source revision. No general native rename or merge permission is granted; direct renames and all merges remain blocked by the controller.

Use native Frappe rename to update Link/Dynamic Link records and attachment ownership while preserving the same Customer, User, guardian, enrollment identities and accounting documents/amounts. Reserve old/new matching player suffixes without resetting the Company sequence. Keep append-only **Sports Player ID Change** records with old/new IDs as historical Data fields, current Player link, Company, reason, operator/time and request identity. Lost-response retries are idempotent and must match actor/payload/current scope. Existing/retired IDs cannot be reused by correction or new intake/import.

Repair derived Sports Attendance identity hashes and row modification versions atomically. Session and roster-row locks precede native link updates; enrollment and fingerprint-preparation writes share the settings lock to serialize identity changes. Unchanged attendance results remain idempotent; changed stale offline marks require fresh roster/conflict review. Operators must refresh downloaded rosters without deleting pending offline work. Existing preparation consent/demo references and request provenance stay intact; uncertain old-ID preparation retries require review rather than creating another preparation.

Any rename, derived-key, counter or audit failure rolls the operation back. This corrects the Player identifier only; no invoice submission/payment, account activation, customer/user renaming, bulk renumber or production roster cleanup is included. It supersedes the earlier blanket prohibition only through this management service.

SPORTS-FR-004/024; SPORTS-NFR-003. User-authorized refinement; questionnaire transcript unchanged. [Build evidence](../../build-logs/2026-11-06-us-003-02-audited-player-id-correction.md). Wider story states remain unchanged.
