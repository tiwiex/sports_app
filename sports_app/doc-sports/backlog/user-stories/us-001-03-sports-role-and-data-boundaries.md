# US-001-03: Define and enforce sports permissions

## Header

- Epic: [EPIC-001](../epics/EPIC-001-academy-configuration-and-access.md)
- State: Proposed
- Priority: Must
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
