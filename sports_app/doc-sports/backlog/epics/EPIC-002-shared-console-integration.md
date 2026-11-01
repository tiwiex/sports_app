# EPIC-002: Shared console integration

## Outcome

Sports and Finance run in one console while remaining separate apps.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-002-01](../user-stories/us-002-01-console-extension-spike.md) | Validate and specify the console provider contract | Must | Done | None |
| [US-002-02](../user-stories/us-002-02-sports-console-provider.md) | Mount Sports views in the shared console | Must | Proposed | US-002-01, US-001-03 |
| [US-002-03](../user-stories/us-002-03-console-login-and-finance-regression.md) | Unify console entry and protect existing Finance behavior | Must | Proposed | US-002-02 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
