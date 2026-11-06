# EPIC-003: Registration and player record

## Outcome

Each player has a stable private identity and a central history.

## Scope and success

- Merge online/staff admission with existing player ID, automatic Customer/User creation and private central profile workflows.
- Expand proposed profile scope for height/weight, preferred foot, private documents, injury/reassessment and returning-player history.
- Include new performance-assessment story in the primary story table, with versioned metrics and monthly/quarterly summaries.

## Stories

This is the complete current epic inventory, including proposed additions and withdrawn history. State is copied from each story as of 6 November 2026; a prototype does not establish full acceptance.

| Story | State | Origin | Priority |
|---|---|---|---|
| [US-003-01: Capture and review player registrations](../user-stories/us-003-01-application-intake-and-review.md) | In progress — PoC workflow | Both | Must |
| [US-003-02: Assign stable player IDs and enrollment dates](../user-stories/us-003-02-player-numbering-and-enrollment.md) | In progress | Both | Must |
| [US-003-03: Present the private central player record](../user-stories/us-003-03-central-player-profile.md) | In progress — central record slice verified | Both | Must |
| [US-003-04: Player performance assessments](../user-stories/us-003-04-player-performance-assessments.md) | Proposed | Questionnaire only | Proposed launch candidate; estimate and sequence pending clarification |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.

US-003-01 now includes a submittable public PoC and private registration review, linked to the existing US-003-02 identity service. [Build evidence](../../build-logs/2026-11-01-us-003-01-public-submission-and-review.md) distinguishes this workflow from remaining production acceptance.
## Consolidated discovery decisions

- Confirm legacy ID grammar without renumbering existing players; returning-player undertaking, penalty and retention policy remain open.
- Agree performance metrics/aggregation and private document access; resolve admission/payment exceptions jointly with EPIC-004/005.

- Epic origin: **Both**. Individual rows distinguish questionnaire-only additions from overlapping scope.
- Source responses: [BA-QNR-001-Q01-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-02), [BA-QNR-001-Q01-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-04), [BA-QNR-001-Q02-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-01), [BA-QNR-001-Q02-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-03), [BA-QNR-001-Q02-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-04), [BA-QNR-001-Q02-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-05), [BA-QNR-001-Q02-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-06), [BA-QNR-001-Q02-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-07), [BA-QNR-001-Q02-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-08), [BA-QNR-001-Q02-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-09), [BA-QNR-001-Q02-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-10), [BA-QNR-001-Q02-11](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-11), [BA-QNR-001-Q02-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-12), [BA-QNR-001-Q02-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-13), [BA-QNR-001-Q04-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-13), [BA-QNR-001-Q06-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-01), [BA-QNR-001-Q06-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-02), [BA-QNR-001-Q07-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-05), [BA-QNR-001-Q10-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-04).
- [Question-level reconciliation](../../discovery/BA-QNR-001-reconciliation.md); [consolidation evidence](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
- Open decisions are proposed refinements, not permission, pricing, delivery-state or commercial changes. Resolve them before affected work becomes Ready.
