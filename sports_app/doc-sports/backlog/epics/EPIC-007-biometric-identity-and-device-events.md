# EPIC-007: Biometric identity and device events

## Outcome

One chosen provider connects securely to traceable attendance.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-007-01](../user-stories/us-007-01-biometric-provider-and-identity.md) | Validate the provider and bind biometric identities | Must | Proposed | US-003-02, US-001-03 |
| [US-007-02](../user-stories/us-007-02-authenticated-device-ingestion.md) | Ingest device events with deduplication and session matching | Must | Proposed | US-007-01, US-006-02 |
| [US-007-03](../user-stories/us-007-03-device-replay-and-exception-review.md) | Resolve device exceptions and recover from outages | Must | Proposed | US-007-02 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
