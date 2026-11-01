# EPIC-003: Registration and player record

## Outcome

Each player has a stable private identity and a central history.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-003-01](../user-stories/us-003-01-application-intake-and-review.md) | Capture and review player registrations | Must | Proposed | US-001-03 |
| [US-003-02](../user-stories/us-003-02-player-numbering-and-enrollment.md) | Assign stable player IDs and enrollment dates | Must | Proposed | US-003-01, US-001-01 |
| [US-003-03](../user-stories/us-003-03-central-player-profile.md) | Present the private central player record | Must | Proposed | US-003-02 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
