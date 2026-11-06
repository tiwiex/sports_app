# EPIC-007: Biometric identity and device events

## Outcome

One chosen provider connects securely to traceable attendance.

## Scope and success

- Retain protected consent/preparation records and clearly simulated fingerprint/barcode UI; these do not establish real capture.
- Merge client-nominated ZK-9500 portable fingerprint/identity requirement into provider discovery and authenticated event ingestion.
- Keep event deduplication, exception review, withdrawal and recovery boundaries; link paired-event requirements to EPIC-006.

## Stories

This is the complete current epic inventory, including proposed additions and withdrawn history. State is copied from each story as of 6 November 2026; a prototype does not establish full acceptance.

| Story | State | Origin | Priority |
|---|---|---|---|
| [US-007-01: Validate the provider and bind biometric identities](../user-stories/us-007-01-biometric-provider-and-identity.md) | In progress — preparation metadata only; hardware/provider validation pending | Both | Must |
| [US-007-02: Ingest device events with deduplication and session matching](../user-stories/us-007-02-authenticated-device-ingestion.md) | Proposed | Both | Must |
| [US-007-03: Resolve device exceptions and recover from outages](../user-stories/us-007-03-device-replay-and-exception-review.md) | Proposed | Original baseline only | Must |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
## Consolidated discovery decisions

- Validate supplier SDK, operating system/browser bridge, physical device, portability and event identity before choosing integration.
- Obtain actual consent form, guardian authority, retention/deletion and failure policy; no real biometric capture until validated.

- Epic origin: **Both**. Individual rows distinguish questionnaire-only additions from overlapping scope.
- Source responses: [BA-QNR-001-Q05-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-05), [BA-QNR-001-Q05-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-06), [BA-QNR-001-Q05-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-07), [BA-QNR-001-Q05-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-10), [BA-QNR-001-Q09-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q09-01).
- [Question-level reconciliation](../../discovery/BA-QNR-001-reconciliation.md); [consolidation evidence](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
- Open decisions are proposed refinements, not permission, pricing, delivery-state or commercial changes. Resolve them before affected work becomes Ready.
