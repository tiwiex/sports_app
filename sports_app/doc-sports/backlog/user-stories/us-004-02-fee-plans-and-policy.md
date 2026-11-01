# US-004-02: Configure fee plans and concession-safe charge calculation

## Header

- Epic: [EPIC-004](../epics/EPIC-004-scholarships-and-monthly-billing.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** finance administrator, **I want** to configure effective monthly plans and calculate authorized amounts **so that** billing uses agreed academy policy.

## Traceability

- Requirements: `SPORTS-FR-008`, `SPORTS-FR-009`
- Dependencies: [US-001-01](../../backlog/user-stories/us-001-01-academy-and-program-settings.md), [US-004-01](../../backlog/user-stories/us-004-01-restricted-scholarship-decisions.md)
- Planned branch: `story/us-004-02-fee-plans-and-policy`
- Planned build log: `YYYY-MM-DD-us-004-02-fee-plans-and-policy.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given an active plan, when saved, then effective dates, currency, company, service item, income account and due-date rule are valid.
2. Given full and partial concessions, when finance previews a charge, then the final amount is correct and scholarship reasons/status are absent from routine finance payloads.
3. Given mid-month enrollment, suspension, overlapping rules or missing mappings, when previewing, then an explicitly selected policy is applied or billing stops with a clear exception; capture approved examples before implementation.

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
