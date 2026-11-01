# US-007-02: Ingest device events with deduplication and session matching

## Header

- Epic: [EPIC-007](../epics/EPIC-007-biometric-identity-and-device-events.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** attendance operator, **I want** to turn authenticated scans into attendance evidence **so that** device events produce reliable session records.

## Traceability

- Requirements: `SPORTS-FR-017`, `SPORTS-NFR-003`
- Dependencies: [US-007-01](../../backlog/user-stories/us-007-01-biometric-provider-and-identity.md), [US-006-02](../../backlog/user-stories/us-006-02-manual-attendance-and-corrections.md)
- Planned branch: `story/us-007-02-authenticated-device-ingestion`
- Planned build log: `YYYY-MM-DD-us-007-02-authenticated-device-ingestion.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a request with invalid credentials or a device outside its academy scope, when posted, then it is rejected and does not create attendance.
2. Given valid, repeated, concurrent or out-of-order events, when processed, then a stable provider/device/event key deduplicates ingestion and each player/session retains one logical attendance record.
3. Given occurrence/receive timestamps, unknown identities or multiple session matches, when processed, then timezone rules are applied and unresolved events queue with an explicit reason rather than inventing a player/session.

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
