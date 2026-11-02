# EPIC-003: Registration and player record

## Outcome

Each player has a stable private identity and a central history.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-003-01](../user-stories/us-003-01-application-intake-and-review.md) | Capture and review player registrations | Must | Proposed | US-001-03 |
| [US-003-02](../user-stories/us-003-02-player-numbering-and-enrollment.md) | Assign stable player IDs and enrollment dates | Must | In progress | US-003-01, US-001-01 |
| [US-003-03](../user-stories/us-003-03-central-player-profile.md) | Present the private central player record | Must | Proposed | US-003-02 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.

US-003-01 now includes a submittable public PoC and private registration review, linked to the existing US-003-02 identity service. [Build evidence](../../build-logs/2026-11-01-us-003-01-public-submission-and-review.md) distinguishes this workflow from remaining production acceptance.
