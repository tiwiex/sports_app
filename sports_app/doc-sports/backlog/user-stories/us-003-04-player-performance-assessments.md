# US-003-04: Player performance assessments

## Header

- Epic: [EPIC-003](../epics/EPIC-003-registration-and-player-record.md)
- State: Proposed
- Priority: Proposed launch candidate; estimate and sequence pending clarification
- Delivery owner / affected apps: Sports App / native ERPNext where applicable

## Story statement

**As an** authorized academy operator, **I want to** record dated player performance assessments and quarterly summaries using agreed metrics.

## Traceability

- Requirements: SPORTS-FR-038
- Dependencies: US-003-03 US-001-03
- Origin: Questionnaire only
- Source references: [BA-QNR-001-Q01-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-02), [BA-QNR-001-Q02-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-06), [BA-QNR-001-Q06-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-01), [BA-QNR-001-Q10-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-04)
- PRD: [Product requirements](../../PRD.md)
- Reconciliation: [BA-QNR-001 register](../../discovery/BA-QNR-001-reconciliation.md)
- Planned branch: `story/us-003-04-player-performance-assessments`

## Notes and scope

Metric definitions, age/sport applicability, scoring/aggregation, assessors and report sign-off remain unresolved. No invented scoring formula.

This is proposed scope, not implementation or commercial acceptance. Use generic sport configuration and Sports-prefixed owned DocTypes; preserve ERPNext accounting and backend authorization.

## Acceptance criteria — proposed

1. Given an agreed versioned metric set, an authorized assessor records a dated assessment against an immutable player ID with units, scale and contextual notes.
2. Changes retain assessor/time and prior values; unauthorized users cannot read private assessments or exports.
3. Monthly/quarterly summaries use the agreed aggregation version and show missing data; exports reconcile to underlying assessments.

## Verification plan

Verify authorized/denied roles, Company isolation, retries, correction history and relevant native ERP reconciliation. Agree fixtures, missing policies and failure cases before marking Ready.

## Completion evidence

- Discovery build log: [Questionnaire reconciliation](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Implementation: Not started; no delivery or hardware claims.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-003-registration-and-player-record.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
