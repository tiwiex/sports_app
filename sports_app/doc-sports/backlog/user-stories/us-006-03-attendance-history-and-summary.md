# US-006-03: Review attendance history and filtered summaries

## Header

- Epic: [EPIC-006](../epics/EPIC-006-sessions-and-attendance.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** coach, **I want** to review permitted player and group attendance **so that** participation can be followed over time.

## Traceability

- Requirements: `SPORTS-FR-015`, `SPORTS-FR-023`
- Dependencies: [US-006-02](../../backlog/user-stories/us-006-02-manual-attendance-and-corrections.md), [US-003-03](../../backlog/user-stories/us-003-03-central-player-profile.md)
- Planned branch: `story/us-006-03-attendance-history-and-summary`
- Planned build log: `YYYY-MM-DD-us-006-03-attendance-history-and-summary.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a player and date range, when viewing history, then session date/time, final status, source and authorized correction context are shown.
2. Given session totals, when calculating attendance rates, then the documented denominator excludes cancelled sessions and clearly states treatment of excused and late statuses.
3. Given a coach restricted to an assigned group, when filtering or exporting another group, then the request is denied and scholarship/payment details are absent from attendance output.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: Not started.
- Verification summary: Not implemented or verified.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

## Prototype dependency evidence — 3 November 2026

The manual prototype supplies saved session rosters, per-status counts and per-record comment/Version history. Cross-session player history, date-range reports, attendance rates and group-restricted coach access are not implemented; this story remains Proposed. [Related evidence](../../build-logs/2026-11-03-us-006-01-manual-attendance-prototype.md).

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q01-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-01), [BA-QNR-001-Q01-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-02), [BA-QNR-001-Q05-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-01), [BA-QNR-001-Q05-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-02), [BA-QNR-001-Q05-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-03), [BA-QNR-001-Q05-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-04), [BA-QNR-001-Q05-14](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-14), [BA-QNR-001-Q06-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-01), [BA-QNR-001-Q10-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-02), [BA-QNR-001-Q10-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-03).
- Impact: Confirmed / expanded; Expanded.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q01-01: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q01-02: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q05-01: Training/matches/camps/trials, per-player reporting and monthly coach report; define session frequency and reporting scope before release.
  - BA-QNR-001-Q05-02: Training/matches/camps/trials, per-player reporting and monthly coach report; define session frequency and reporting scope before release.
  - BA-QNR-001-Q05-03: Training/matches/camps/trials, per-player reporting and monthly coach report; define session frequency and reporting scope before release.
  - BA-QNR-001-Q05-04: Training/matches/camps/trials, per-player reporting and monthly coach report; define session frequency and reporting scope before release.
  - BA-QNR-001-Q05-14: Training/matches/camps/trials, per-player reporting and monthly coach report; define session frequency and reporting scope before release.
  - BA-QNR-001-Q06-01: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q10-02: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
  - BA-QNR-001-Q10-03: Payment, attendance and exportable reporting remain priorities; player performance is separately proposed under FR-038.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-006-sessions-and-attendance.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
