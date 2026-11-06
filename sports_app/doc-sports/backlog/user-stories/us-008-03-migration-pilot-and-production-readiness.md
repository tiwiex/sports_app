# US-008-03: Rehearse migration and validate production readiness

## Header

- Epic: [EPIC-008](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** implementation lead, **I want** to import verified opening data and complete a controlled pilot **so that** the academy can adopt the system with support evidence.

## Traceability

- Requirements: `SPORTS-FR-022`, `SPORTS-FR-024`, `SPORTS-FR-025`, `SPORTS-NFR-008`
- Dependencies: [US-001-02](../../backlog/user-stories/us-001-02-configurable-public-website.md), [US-002-03](../../backlog/user-stories/us-002-03-console-login-and-finance-regression.md), [US-005-03](../../backlog/user-stories/us-005-03-corrections-and-reconciliation.md), [US-006-03](../../backlog/user-stories/us-006-03-attendance-history-and-summary.md), [US-007-03](../../backlog/user-stories/us-007-03-device-replay-and-exception-review.md), [US-008-01](../../backlog/user-stories/us-008-01-erp-fit-gap-and-module-matrix.md), [US-008-02](../../backlog/user-stories/us-008-02-operational-dashboard-and-exports.md)
- Planned branch: `story/us-008-03-migration-pilot-and-production-readiness`
- Planned build log: `YYYY-MM-DD-us-008-03-migration-pilot-and-production-readiness.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given legacy roster, balances and attendance sources, when a dry run and rerun execute, then external IDs, rejected rows and opening totals reconcile; unverifiable history is labeled rather than fabricated.
2. Given all launch-required ERP modules and the selected biometric provider, when business owners run agreed scenarios, then configuration, permissions, accounting, manual/device attendance and end-to-end player journeys have signed evidence; any outstanding ERP delivery task blocks its module acceptance.
3. Given a backup and cutover rehearsal, when restore/replay and rollback steps are exercised, then identities and balances remain consistent and the release has trained operators, runbook, support owners, recovery targets and management sign-off.

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

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q01-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-03), [BA-QNR-001-Q01-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-06), [BA-QNR-001-Q01-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-07), [BA-QNR-001-Q01-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-08), [BA-QNR-001-Q01-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-09), [BA-QNR-001-Q02-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-02), [BA-QNR-001-Q04-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-05), [BA-QNR-001-Q04-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-08), [BA-QNR-001-Q05-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-08), [BA-QNR-001-Q06-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-06), [BA-QNR-001-Q08-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-01), [BA-QNR-001-Q08-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-05), [BA-QNR-001-Q09-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q09-01), [BA-QNR-001-Q09-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q09-02), [BA-QNR-001-Q09-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q09-03), [BA-QNR-001-Q09-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q09-04).
- Impact: Changed; Context / needs clarification; Expanded; Expanded / needs clarification; Needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q01-03: Approximately 75 players in Excel/Zoho; obtain sample, mapping, quality checks and opening balance reconciliation. No import performed.
  - BA-QNR-001-Q01-06: Stakeholder decision and commercial dates/budget need sign-off; TBD does not replace existing eight-week/NGN7M proposal assumptions.
  - BA-QNR-001-Q01-07: Approximately 75 players in Excel/Zoho; obtain sample, mapping, quality checks and opening balance reconciliation. No import performed.
  - BA-QNR-001-Q01-08: Stakeholder decision and commercial dates/budget need sign-off; TBD does not replace existing eight-week/NGN7M proposal assumptions.
  - BA-QNR-001-Q01-09: Stakeholder decision and commercial dates/budget need sign-off; TBD does not replace existing eight-week/NGN7M proposal assumptions.
  - BA-QNR-001-Q02-02: Approximately 75 players in Excel/Zoho; obtain sample, mapping, quality checks and opening balance reconciliation. No import performed.
  - BA-QNR-001-Q04-05: Approximately 75 players in Excel/Zoho; obtain sample, mapping, quality checks and opening balance reconciliation. No import performed.
  - BA-QNR-001-Q04-08: Approximately 75 players in Excel/Zoho; obtain sample, mapping, quality checks and opening balance reconciliation. No import performed.
  - BA-QNR-001-Q05-08: N/A does not establish reliable power/network; confirm venue conditions and portable-device/offline recovery acceptance. Keep existing offline prototype scope.
  - BA-QNR-001-Q06-06: Approximately 75 players in Excel/Zoho; obtain sample, mapping, quality checks and opening balance reconciliation. No import performed.
  - BA-QNR-001-Q08-01: Approximately 75 players in Excel/Zoho; obtain sample, mapping, quality checks and opening balance reconciliation. No import performed.
  - BA-QNR-001-Q08-05: Training for five staff; phone/virtual support and Idelta maintenance discussed. SLA, ownership, recurring fees and coverage TBD; not an agreed support contract.
  - BA-QNR-001-Q09-01: Phases accepted; attendance and biometrics highest priority alongside payments/reporting. Replan within existing proposal assumptions after device discovery; no implied production deadline.
  - BA-QNR-001-Q09-02: Training for five staff; phone/virtual support and Idelta maintenance discussed. SLA, ownership, recurring fees and coverage TBD; not an agreed support contract.
  - BA-QNR-001-Q09-03: Training for five staff; phone/virtual support and Idelta maintenance discussed. SLA, ownership, recurring fees and coverage TBD; not an agreed support contract.
  - BA-QNR-001-Q09-04: Stakeholder decision and commercial dates/budget need sign-off; TBD does not replace existing eight-week/NGN7M proposal assumptions.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
