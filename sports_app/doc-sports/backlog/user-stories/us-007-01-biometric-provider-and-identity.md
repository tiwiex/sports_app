# US-007-01: Validate the provider and bind biometric identities

## Header

- Epic: [EPIC-007](../epics/EPIC-007-biometric-identity-and-device-events.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** integration administrator, **I want** to map approved external biometric identities to players **so that** scans resolve to the correct academy record.

## Traceability

- Requirements: `SPORTS-FR-016`, `SPORTS-NFR-007`
- Dependencies: [US-003-02](../../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md), [US-001-03](../../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md)
- Planned branch: `story/us-007-01-biometric-provider-and-identity`
- Planned build log: `YYYY-MM-DD-us-007-01-biometric-provider-and-identity.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given the selected hardware/provider, when discovery is completed, then model/API, authentication, identifiers, timezone, offline behavior, template boundary and consent/guardian and retention decisions are recorded before live enrollment.
2. Given a valid player and external identity, when binding, then duplicate/conflicting mappings are rejected and only authorized administrators can enroll or revoke identities.
3. Given revocation or retention expiry, when cleanup runs, then configured local/provider actions and failures are tracked; no raw templates are exposed in ordinary APIs, profile pages or logs.

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
