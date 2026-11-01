# EPIC-001: Academy configuration and access

## Outcome

A reusable academy setup and private operating boundary.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-001-01](../user-stories/us-001-01-academy-and-program-settings.md) | Configure academy and program defaults | Must | Done | None |
| [US-001-02](../user-stories/us-001-02-configurable-public-website.md) | Configure and publish academy website content | Must | Proposed | US-001-01 |
| [US-001-03](../user-stories/us-001-03-sports-role-and-data-boundaries.md) | Define and enforce sports permissions | Must | Proposed | US-001-01 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
