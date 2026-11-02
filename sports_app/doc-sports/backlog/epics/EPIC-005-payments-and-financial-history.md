# EPIC-005: Payments and financial history

## Outcome

Player payment records reconcile to ERPNext accounting.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-005-01](../user-stories/us-005-01-player-receipts-and-allocations.md) | Record player-attributed payments using ERPNext | Must | In progress — invoice-first PoC | US-004-03, US-002-03 |
| [US-005-02](../user-stories/us-005-02-monthly-status-and-history.md) | Show monthly payment status and source history | Must | Proposed | US-005-01, US-003-03 |
| [US-005-03](../user-stories/us-005-03-corrections-and-reconciliation.md) | Reconcile credits, refunds and payment corrections | Must | Proposed | US-005-02 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
