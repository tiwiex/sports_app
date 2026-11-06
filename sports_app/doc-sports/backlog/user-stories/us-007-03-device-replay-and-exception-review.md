# US-007-03: Resolve device exceptions and recover from outages

## Header

- Epic: [EPIC-007](../epics/EPIC-007-biometric-identity-and-device-events.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** integration administrator, **I want** to review and replay unmatched or delayed device events **so that** attendance is recoverable without losing corrections.

## Traceability

- Requirements: `SPORTS-FR-018`, `SPORTS-NFR-003`, `SPORTS-NFR-004`, `SPORTS-NFR-008`
- Dependencies: [US-007-02](../../backlog/user-stories/us-007-02-authenticated-device-ingestion.md)
- Planned branch: `story/us-007-03-device-replay-and-exception-review`
- Planned build log: `YYYY-MM-DD-us-007-03-device-replay-and-exception-review.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given an unmatched event, when an authorized reviewer fixes mapping or session selection, then reprocessing links the existing event and records the actor and result.
2. Given manually corrected attendance and later device replay, when processing resumes, then reviewed status is preserved or a review conflict is raised; no silent overwrite occurs.
3. Given a simulated provider outage and recovery, when queued events replay, then no duplicate attendance is created and visible failed/retry counts support recovery; record restore/replay evidence.

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

## Discovery provenance — 6 November 2026

- Origin: **Original baseline only** (including subsequent user direction); no direct questionnaire response establishes this story’s specific scope. Preserve existing state and acceptance evidence.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-007-biometric-identity-and-device-events.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
