# EPIC-006: Sessions and attendance

## Outcome

Operators record and review reliable session attendance.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. A manual attendance prototype is available on development; remaining stories and acceptance scope stay open. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-006-01](../user-stories/us-006-01-sessions-and-rosters.md) | Create sessions and eligible player rosters | Must | In progress — prototype | US-003-02, US-001-03 |
| [US-006-02](../user-stories/us-006-02-manual-attendance-and-corrections.md) | Capture manual attendance and reviewed corrections | Must | In progress — prototype | US-006-01 |
| [US-006-03](../user-stories/us-006-03-attendance-history-and-summary.md) | Review attendance history and filtered summaries | Must | Proposed | US-006-02, US-003-03 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
