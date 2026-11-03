# US-006-01: Create sessions and eligible player rosters

## Header

- Epic: [EPIC-006](../epics/EPIC-006-sessions-and-attendance.md)
- State: In progress — manual attendance prototype
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** coach, **I want** to schedule group sessions with dated rosters **so that** attendance is recorded against the right event.

## Traceability

- Requirements: `SPORTS-FR-014`
- Dependencies: [US-003-02](../../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md), [US-001-03](../../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md)
- Planned branch: `story/us-006-01-sessions-and-rosters`
- Planned build log: `YYYY-MM-DD-us-006-01-sessions-and-rosters.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a group and date/time, when a session is created, then academy timezone, responsible operator and enrollment-based roster are explicit.
2. Given overlapping or cancelled sessions, when selecting an attendance target, then operators see clear status and ambiguous matches require selection.
3. Given withdrawn or not-yet-enrolled players, when generating a roster, then eligibility follows effective enrollment dates and any manual exception requires a reason.

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
