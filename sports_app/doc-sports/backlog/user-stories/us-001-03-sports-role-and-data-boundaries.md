# US-001-03: Define and enforce sports permissions

## Header

- Epic: [EPIC-001](../epics/EPIC-001-academy-configuration-and-access.md)
- State: In progress
- Priority: Could
- Delivery owner / affected apps: Sports App

## Story statement

**As a** academy manager, **I want** to assign registrar, coach, finance and management permissions **so that** sensitive records stay restricted.

## Traceability

- Requirements: `SPORTS-FR-008`, `SPORTS-FR-021`, `SPORTS-NFR-002`, `SPORTS-NFR-007`
- Dependencies: [US-001-01](../../backlog/user-stories/us-001-01-academy-and-program-settings.md)
- Planned branch: `story/us-001-03-sports-role-and-data-boundaries`
- Planned build log: `YYYY-MM-DD-us-001-03-sports-role-and-data-boundaries.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a registrar, coach or cashier, when requesting scholarship flags, reasons, files or decision history by API, export, report or search, then restricted data is not returned.
2. Given an operator outside an assigned academy/group, when they request another group’s private records, then server checks deny unauthorized access.
3. Given a public user or direct private-file URL, when private identity records or attachments are requested, then access is denied; the documented permission matrix includes administrator support access.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: Not started.
- Verification summary: Not implemented or verified.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

Role-editor correction: [Player Users and User role editor](../../build-logs/2026-11-01-us-003-02-player-users-and-role-editor.md). Restore only the standard System Manager User permission baseline. This does not complete the broader role-boundary story.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q01-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-05), [BA-QNR-001-Q03-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-06), [BA-QNR-001-Q05-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-10), [BA-QNR-001-Q06-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-03), [BA-QNR-001-Q06-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-05), [BA-QNR-001-Q07-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-01), [BA-QNR-001-Q07-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-02), [BA-QNR-001-Q07-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-03), [BA-QNR-001-Q07-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-04), [BA-QNR-001-Q08-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-04).
- Impact: Changed / needs clarification; Confirmed / expanded; Expanded / needs clarification; Needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q01-05: Role-authorized downloadable reports for manual external sharing; no automatic external disclosure.
  - BA-QNR-001-Q03-06: Explicit scholarship visibility: admin, director and finance only. Confirm exact role mapping; coach assessment does not imply access to scholarship status. No permission changes yet.
  - BA-QNR-001-Q05-10: Parents sign consent at registration; obtain actual form and confirm biometric-specific scope, guardian authority, withdrawal and retention before real capture.
  - BA-QNR-001-Q06-03: N/A leaves detailed role matrix unresolved; retain existing least-privilege controls and resolve explicit scholarship rule separately.
  - BA-QNR-001-Q06-05: Role-authorized downloadable reports for manual external sharing; no automatic external disclosure.
  - BA-QNR-001-Q07-01: Multiple admins and audit trail requested; admin edit/approval answers do not authorize destructive deletion or finance bypass. Clarify coach/admin scholarship recommendation/approval separation.
  - BA-QNR-001-Q07-02: Multiple admins and audit trail requested; admin edit/approval answers do not authorize destructive deletion or finance bypass. Clarify coach/admin scholarship recommendation/approval separation.
  - BA-QNR-001-Q07-03: Multiple admins and audit trail requested; admin edit/approval answers do not authorize destructive deletion or finance bypass. Clarify coach/admin scholarship recommendation/approval separation.
  - BA-QNR-001-Q07-04: Multiple admins and audit trail requested; admin edit/approval answers do not authorize destructive deletion or finance bypass. Clarify coach/admin scholarship recommendation/approval separation.
  - BA-QNR-001-Q08-04: Role-authorized downloadable reports for manual external sharing; no automatic external disclosure.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-001-academy-configuration-and-access.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-e0718377675c.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-9f150914b6c6.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-2fc76d7478fa.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-d84672085869.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-bb26f8228919.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-17e37ded010c.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-0e66190fbb8d.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-03-review-5b832b672cf9.md).
