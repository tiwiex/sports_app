# US-004-01: Manage effective-dated scholarship and exemption decisions

## Header

- Epic: [EPIC-004](../epics/EPIC-004-scholarships-and-monthly-billing.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** academy manager, **I want** to approve full or partial concessions with dates and reasons **so that** eligible players receive authorized fee treatment.

## Traceability

- Requirements: `SPORTS-FR-007`, `SPORTS-FR-008`, `SPORTS-NFR-002`, `SPORTS-NFR-004`
- Dependencies: [US-001-03](../../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md), [US-003-02](../../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md)
- Planned branch: `story/us-004-01-restricted-scholarship-decisions`
- Planned build log: `YYYY-MM-DD-us-004-01-restricted-scholarship-decisions.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a management-authorized approver, when a full/partial decision is approved or revoked, then scope, amount/percentage, dates, reason and actor are recorded and invalid overlaps follow the agreed rule.
2. Given a non-management role, when accessing decision lists, player flags, notifications, exports or files, then the server does not disclose restricted content.
3. Given a retroactive change affecting an issued invoice, when the decision changes, then no submitted invoice is silently rewritten; a reviewed correction path is required.

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
