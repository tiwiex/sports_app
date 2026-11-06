# US-006-05: Arrival, departure and absence review

## Header

- Epic: [EPIC-006](../epics/EPIC-006-sessions-and-attendance.md)
- State: Proposed
- Priority: Proposed launch candidate; estimate and sequence pending clarification
- Delivery owner / affected apps: Sports App / native ERPNext where applicable

## Story statement

**As an** authorized academy operator, **I want to** track arrival and departure and help administrators review absences without assuming unmarked players are absent.

## Traceability

- Requirements: SPORTS-FR-040
- Dependencies: US-006-01 US-006-02 US-007-02
- Origin: Both
- Source references: [BA-QNR-001-Q05-11](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-11), [BA-QNR-001-Q05-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-12), [BA-QNR-001-Q05-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-13), [BA-QNR-001-Q06-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-02)
- PRD: [Product requirements](../../PRD.md)
- Reconciliation: [BA-QNR-001 register](../../discovery/BA-QNR-001-reconciliation.md)
- Planned branch: `story/us-006-05-arrival-departure-and-absence-review`

## Notes and scope

Existing attendance covers manual status; paired timestamps and midday alert are additional scope. Confirm cutoff/timezone, late threshold, duplicates, missing departure, injuries and offline event ordering.

This is proposed scope, not implementation or commercial acceptance. Use generic sport configuration and Sports-prefixed owned DocTypes; preserve ERPNext accounting and backend authorization.

## Acceptance criteria — proposed

1. Given a session/player, arrival and departure events retain source, timezone-aware occurrence time and received time; duplicates do not multiply events.
2. Missing departure, reversed event order and offline conflicts require review; no attendance status is inferred solely from a scan failure.
3. At an agreed session-relative cutoff, alert only authorized admins about eligible unmarked players; admin records excused absence/injury reason with audit; parent contact remains manual.

## Verification plan

Verify authorized/denied roles, Company isolation, retries, correction history and relevant native ERP reconciliation. Agree fixtures, missing policies and failure cases before marking Ready.

## Completion evidence

- Discovery build log: [Questionnaire reconciliation](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Implementation: Not started; no delivery or hardware claims.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-006-sessions-and-attendance.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
