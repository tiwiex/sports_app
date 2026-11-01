# EPIC-008: ERP readiness, reporting and rollout

## Outcome

The academy launches with reconciled data and an explicit ERP boundary.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-008-01](../user-stories/us-008-01-erp-fit-gap-and-module-matrix.md) | Define ERP coverage and launch-required modules | Must | Proposed | None |
| [US-008-02](../user-stories/us-008-02-operational-dashboard-and-exports.md) | Provide authorized academy dashboards and exports | Must | Proposed | US-005-02, US-006-03, US-002-02 |
| [US-008-03](../user-stories/us-008-03-migration-pilot-and-production-readiness.md) | Rehearse migration and validate production readiness | Must | Proposed | US-001-02, US-002-03, US-005-03, US-006-03, US-007-03, US-008-01, US-008-02 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
