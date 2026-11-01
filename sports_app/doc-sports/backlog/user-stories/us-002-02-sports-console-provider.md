# US-002-02: Mount Sports views in the shared console

## Header

- Epic: [EPIC-002](../epics/EPIC-002-shared-console-integration.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERP Boost + Sports App

## Story statement

**As a** academy operator, **I want** to open Sports views through Boost navigation **so that** daily work uses one staff entry point.

## Traceability

- Requirements: `SPORTS-FR-019`, `SPORTS-FR-020`, `SPORTS-NFR-001`, `SPORTS-NFR-006`
- Dependencies: [US-002-01](../../backlog/user-stories/us-002-01-console-extension-spike.md), [US-001-03](../../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md)
- Planned branch: `story/us-002-02-sports-console-provider`
- Planned build log: `YYYY-MM-DD-us-002-02-sports-console-provider.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given permitted Sports views, when the console loads, then app-owned Sports modules appear with namespaced IDs and lazy-loaded assets alongside allowed Finance views.
2. Given player and academy context, when switching to a permitted billing view and back, then player, company, filters and return location are retained and validated.
3. Given a disabled Sports module or a user with no access, when navigation is rebuilt, then unavailable entries and cached data are removed; branding has no administrator-supplied executable script.

## Verification plan

- Target-site installed-app combinations, Sports-only/Finance-only/mixed roles, lifecycle and financial regression checks.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: Not started.
- Verification summary: Not implemented or verified.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.
