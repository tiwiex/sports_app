# US-003-02: Assign stable player IDs and enrollment dates

## Header

- Epic: [EPIC-003](../epics/EPIC-003-registration-and-player-record.md)
- State: Proposed
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
2. Given acceptance or direct registration, when enrollment is confirmed, then program/group, payer link, start/end dates and active status are validated.
3. Given withdrawal, suspension or a same-name player, when records are updated, then existing history remains linked to the correct immutable ID and future eligibility follows effective dates.

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
