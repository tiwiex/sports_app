# EPIC-006: Sessions and attendance

## Outcome

Operators record and review reliable session attendance.

## Scope and success

- Keep existing session rosters, audited manual marking/history and the dedicated Next.js attendance PWA/offline sync.
- Merge training/matches/camps/trials, per-player and monthly coach reporting, and manual fallback for scanner failure.
- Add paired arrival/departure, reviewed injury/excused absences and midday admin alert as proposed work; manual parent notification remains explicit.

## Stories

This is the complete current epic inventory, including proposed additions and withdrawn history. State is copied from each story as of 6 November 2026; a prototype does not establish full acceptance.

| Story | State | Origin | Priority |
|---|---|---|---|
| [US-006-01: Create sessions and eligible player rosters](../user-stories/us-006-01-sessions-and-rosters.md) | In progress — manual attendance prototype | Both | Must |
| [US-006-02: Capture manual attendance and reviewed corrections](../user-stories/us-006-02-manual-attendance-and-corrections.md) | In progress — manual attendance prototype | Both | Must |
| [US-006-03: Review attendance history and filtered summaries](../user-stories/us-006-03-attendance-history-and-summary.md) | Proposed | Both | Must |
| [US-006-04: Dedicated Next.js offline attendance app](../user-stories/us-006-04-attendance-pwa.md) | In progress — first development prototype | Both | Must for the requested dedicated attendance frontend; production acceptance pending |
| [US-006-05: Arrival, departure and absence review](../user-stories/us-006-05-arrival-departure-and-absence-review.md) | Proposed | Both | Proposed launch candidate; estimate and sequence pending clarification |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
## Consolidated discovery decisions

- Define cutoff/timezone, lateness, missing departures, session finalization and event ordering.
- Clarify actual power/network conditions; N/A is not an offline reliability guarantee. No automatic absence from unmarked events.

- Epic origin: **Both**. Individual rows distinguish questionnaire-only additions from overlapping scope.
- Source responses: [BA-QNR-001-Q01-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-01), [BA-QNR-001-Q01-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-02), [BA-QNR-001-Q05-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-01), [BA-QNR-001-Q05-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-02), [BA-QNR-001-Q05-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-03), [BA-QNR-001-Q05-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-04), [BA-QNR-001-Q05-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-08), [BA-QNR-001-Q05-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-09), [BA-QNR-001-Q05-11](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-11), [BA-QNR-001-Q05-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-12), [BA-QNR-001-Q05-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-13), [BA-QNR-001-Q05-14](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-14), [BA-QNR-001-Q06-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-01), [BA-QNR-001-Q06-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-02), [BA-QNR-001-Q08-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-02), [BA-QNR-001-Q08-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-03), [BA-QNR-001-Q10-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-02), [BA-QNR-001-Q10-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-03).
- [Question-level reconciliation](../../discovery/BA-QNR-001-reconciliation.md); [consolidation evidence](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
- Open decisions are proposed refinements, not permission, pricing, delivery-state or commercial changes. Resolve them before affected work becomes Ready.
