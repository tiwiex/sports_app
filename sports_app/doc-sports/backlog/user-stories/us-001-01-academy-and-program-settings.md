# US-001-01: Configure academy and program defaults

## Header

- Epic: [EPIC-001](../epics/EPIC-001-academy-configuration-and-access.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** academy administrator, **I want** to configure academy identity, company, programs, groups and enrollment defaults **so that** a second academy can adopt the app without editing code.

## Traceability

- Requirements: `SPORTS-FR-001`, `SPORTS-FR-006`
- Dependencies: None
- Planned branch: `story/us-001-01-academy-and-program-settings`
- Planned build log: `YYYY-MM-DD-us-001-01-academy-and-program-settings.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given two academy fixtures, when each is configured, then names, sports, groups, currency, timezone and numbering use their own settings without code changes.
2. Given a company outside the operator’s permission scope, when it is selected through UI or API, then the setting or action is rejected.
3. Given missing fee or program defaults, when setup is saved or dependent work is started, then validation identifies required configuration without silently selecting a client-specific company.

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
