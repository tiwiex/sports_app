# US-003-03: Present the private central player record

## Header

- Epic: [EPIC-003](../epics/EPIC-003-registration-and-player-record.md)
- State: In progress — profile presentation slice
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

- Pull request(s): Not opened.
- Build log: [Player list and profile layout](../../build-logs/2026-11-03-us-003-03-player-profile-layout.md).
- Verification summary: Invoice-style reference menu, sortable list and grouped responsive profile verified with automated desktop/phone browser fixtures and protected native read APIs. Full linked histories remain outstanding.
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
