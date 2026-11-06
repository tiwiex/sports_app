# US-003-03: Present the private central player record

## Header

- Epic: [EPIC-003](../epics/EPIC-003-registration-and-player-record.md)
- State: In progress — central record slice verified
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** registrar, **I want** to search one player and view permitted linked histories **so that** registration, payments and attendance are accessible together.

## Traceability

- Requirements: `SPORTS-FR-005`, `SPORTS-NFR-005`, `SPORTS-NFR-007`
- Dependencies: [US-003-02](../../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md)
- Planned branch: `story/us-003-03-central-player-profile`
- Planned build log: `YYYY-MM-DD-us-003-03-central-player-profile.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a registration number or name, when searching, then authorized results distinguish same-name players and show only permitted identity fields.
2. Given a player with history, when opening the profile, then enrollment, payment and attendance sections use paginated linked records and show source references; empty modules are identified clearly.
3. Given a non-management operator and private attachments, when profile payloads are inspected, then scholarship details and unauthorized files are absent; measure search/profile latency at the agreed pilot volume.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): [Sports PR #3](https://github.com/tiwiex/sports_app/pull/3); GitHub state is authoritative for merge status.
- Build log: [Player list and profile layout](../../build-logs/2026-11-03-us-003-03-player-profile-layout.md).
- Verification summary: Invoice-style reference menu, sortable list and grouped responsive profile verified with automated desktop/phone browser fixtures and protected native read APIs. Central linked histories are now implemented; see the additional delivery evidence below.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

## Presentation refinement — 3 November 2026

Match the Enrollments queue: bordered sortable table, Player ID context menu, View modal and permission-scoped New program enrollment action. Keep the search/list beneath the modal; show friendly program/group names and explicit consent choices. This completes the presentation slice only. Payment/attendance histories, broader role/privacy verification and pilot-volume latency remain acceptance work before the whole story can be Done.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q02-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-03), [BA-QNR-001-Q02-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-04), [BA-QNR-001-Q02-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-05), [BA-QNR-001-Q02-11](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-11), [BA-QNR-001-Q02-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-13), [BA-QNR-001-Q06-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-02).
- Impact: Expanded; Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q02-03: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
  - BA-QNR-001-Q02-04: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
  - BA-QNR-001-Q02-05: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
  - BA-QNR-001-Q02-11: Returning player undertaking and reassessment history; subscription continuation; penalty and retention timeline TBD. Do not delete lifetime history or silently merge returning players.
  - BA-QNR-001-Q02-13: Returning player undertaking and reassessment history; subscription continuation; penalty and retention timeline TBD. Do not delete lifetime history or silently merge returning players.
  - BA-QNR-001-Q06-02: Add height/weight with units and assessment date, preferred foot, private photo/birth/medical documents and injuries. Derive age from DOB; injury may excuse attendance. Biometric capture remains separate.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-003-registration-and-player-record.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Central record delivery — 6 November 2026

User authorized the recommended Sports-only central record slice. Original presentation evidence above remains historical. Branch: `story/us-003-03-central-player-record`. [Build log](../../build-logs/2026-11-06-us-003-03-central-player-record.md).

Additional acceptance for this slice:

4. Invoices, receipts, attendance/session references, measurements and management-only document/fingerprint histories paginate independently and enforce native read/field/Company access. Restricted modules reveal no totals or file URLs. Submitted-invoice outstanding amounts remain separate per currency; this is not a full GL/advance balance.
5. Authorized staff can update preferred foot with a current revision and append dated height(cm)/weight(kg) observations; invalid/future/before-birth/nonfinite values and history overwrites are denied. Stable request keys make retries idempotent.
6. Management can create a private supporting-document archive with title/type/date. Files stay private and protected from replacement, reassignment or deletion; nonmanagement users cannot access parent, direct private file or File-list metadata. Native document submission protects the archive and never posts finance.

Evidence: 196 Python checks passed; actual-module browser fixtures passed at desktop and phone widths. Native development checks covered Sports/mixed/management/Guest permissions, private-file deletion/public-move denial, lost-response retries and rollback. A provisional 75-player native read sample recorded median 88.0 ms and maximum 96.4 ms across five combined list/summary/attendance/measurement calls; this is not browser p95 evidence. All provisional records/accounts/files were removed by rollback.

Story remains In progress: injury/attendance excusal, returning-player undertaking/reassessment policy and final sensitive-document retention are not claimed complete. Scholarship details remain absent. No Boost changes, new finance rights or production deployment.

## Tabbed profile refinement — 6 November 2026

User requested distinct tabs for details and histories. Group the modal into Player details, Program enrollments, Invoices & receipts, Attendance & fingerprint, Measurements and Documents, with common actions always available. Preserve active section on same-player refresh/pagination, accessible keyboard navigation and mobile scrolling. Existing access controls and independent history pagination remain unchanged. [Build log](../../build-logs/2026-11-06-us-003-03-tabbed-player-profile.md).

Header-photo refinement (6 November 2026): move the authorized private portrait beside the name, above the tabs, so it remains immediately visible while switching sections. [Build log](../../build-logs/2026-11-06-us-003-03-profile-header-photo.md).

User-authorized develop integration (6 November 2026): [integration evidence](../../build-logs/2026-11-06-us-003-03-develop-integration.md). Merge status follows the linked GitHub PR; broader story remains In progress.

Backlog review (6 November 2026): the console reads this story and the synchronized epic/inventory. Central profile, histories, tabs and header photo are verified. Keep the whole story In progress for the explicitly outstanding injury/absence, returning-player and retention-policy refinements; do not label those complete. Future complete stories should be marked Done with linked acceptance evidence. Recommended next refinement: US-004-02 fee plans, then US-004-03 monthly obligations/invoices after cadence, proration and arrears decisions.
