# US-006-02: Capture manual attendance and reviewed corrections

Dedicated frontend follow-up: [US-006-04](us-006-04-attendance-pwa.md) and [Next.js attendance build evidence](../../build-logs/2026-11-03-us-006-04-attendance-pwa.md). The new app uses these same manual marking/correction services; production/device acceptance remains open.

## Header

- Epic: [EPIC-006](../epics/EPIC-006-sessions-and-attendance.md)
- State: In progress — manual attendance prototype
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** attendance operator, **I want** to record session statuses on a phone **so that** training can continue during device outages.

## Traceability

- Requirements: `SPORTS-FR-015`, `SPORTS-NFR-004`, `SPORTS-NFR-006`
- Dependencies: [US-006-01](../../backlog/user-stories/us-006-01-sessions-and-rosters.md)
- Planned branch: `story/us-006-02-manual-attendance-and-corrections`
- Planned build log: `YYYY-MM-DD-us-006-02-manual-attendance-and-corrections.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a roster, when marking Present, Late, Absent or Excused and finalizing, then one logical record exists per player/session and missing scans become absences only through the finalization policy.
2. Given concurrent edits or repeated saves, when attendance is recorded, then duplicate logical records are prevented and conflicts are visible.
3. Given a reviewed correction, when an authorized operator supplies a reason, then old/new status, actor, time and source remain auditable; phone-width and keyboard entry are usable.

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

## Manual prototype — 3 November 2026

Implemented development slice: session scheduling with timezone/operator, fixed date-eligible Active roster, unique player/session identity, manual marking, explicit finalization, reasoned corrections and audit history. Native Company/document restrictions and batch conflict/rollback controls apply. [Build evidence](../../build-logs/2026-11-03-us-006-01-manual-attendance-prototype.md). Full coach/group authorization, roster exceptions and production acceptance remain open; this story is not marked Done.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q05-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-09).
- Impact: Confirmed.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q05-09: Manual system attendance is the fallback when fingerprints fail; maintain operator, reason and correction history.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-006-sessions-and-attendance.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
