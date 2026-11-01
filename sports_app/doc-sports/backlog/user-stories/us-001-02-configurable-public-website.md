# US-001-02: Configure and publish academy website content

## Header

- Epic: [EPIC-001](../epics/EPIC-001-academy-configuration-and-access.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** website editor, **I want** to manage branding, page sections and approved public content **so that** the academy has its own website using reusable templates.

## Traceability

- Requirements: `SPORTS-FR-002`, `SPORTS-NFR-006`
- Dependencies: [US-001-01](../../backlog/user-stories/us-001-01-academy-and-program-settings.md)
- Planned branch: `story/us-001-02-configurable-public-website`
- Planned build log: `YYYY-MM-DD-us-001-02-configurable-public-website.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given changed branding and program content, when an authorized editor publishes, then public pages reflect settings without source changes.
2. Given an unpublished player, when a guest requests a profile or lists public content, then private player fields are absent and no operational player endpoint becomes public.
3. Given phone-width and keyboard navigation, when an applicant browses configured pages, then core content, labels and application navigation remain usable; stored content is safely rendered.

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
