# EPIC-002: Shared console integration

## Outcome

Sports and Finance run in one console while remaining separate apps.

## Scope and success

- Retain the optional Boost provider interface and separate app ownership; Sports remains usable without hardcoded football/client dependencies.
- Preserve role-aware finance regressions and protected modal documentation, including questionnaire provenance.
- The questionnaire does not independently establish the provider architecture; original technical direction remains valid.

## Stories

This is the complete current epic inventory, including proposed additions and withdrawn history. State is copied from each story as of 6 November 2026; a prototype does not establish full acceptance.

| Story | State | Origin | Priority |
|---|---|---|---|
| [US-002-01: Validate and specify the console provider contract](../user-stories/us-002-01-console-extension-spike.md) | Done | Original baseline only | Must |
| [US-002-02: Mount Sports views in the shared console](../user-stories/us-002-02-sports-console-provider.md) | Proposed | Original baseline only | Must |
| [US-002-03: Unify console entry and protect existing Finance behavior](../user-stories/us-002-03-console-login-and-finance-regression.md) | Proposed | Original baseline only | Must |
| [US-002-04: Expose Sports development documentation and build evidence](../user-stories/us-002-04-development-documentation-and-build-evidence.md) | In review | Original baseline only | See story |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
## Consolidated discovery decisions

- Validate combined Sports/Finance/Boost-only permissions and compatible releases before rollout.

- Epic origin: **Original baseline only**. Individual rows distinguish questionnaire-only additions from overlapping scope.
- [Question-level reconciliation](../../discovery/BA-QNR-001-reconciliation.md); [consolidation evidence](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
- Open decisions are proposed refinements, not permission, pricing, delivery-state or commercial changes. Resolve them before affected work becomes Ready.
