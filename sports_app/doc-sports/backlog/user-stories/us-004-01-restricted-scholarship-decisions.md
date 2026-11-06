# US-004-01: Manage effective-dated scholarship and exemption decisions

## Header

- Epic: [EPIC-004](../epics/EPIC-004-scholarships-and-monthly-billing.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** academy manager, **I want** to approve full or partial concessions with dates and reasons **so that** eligible players receive authorized fee treatment.

## Traceability

- Requirements: `SPORTS-FR-007`, `SPORTS-FR-008`, `SPORTS-NFR-002`, `SPORTS-NFR-004`
- Dependencies: [US-001-03](../../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md), [US-003-02](../../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md)
- Planned branch: `story/us-004-01-restricted-scholarship-decisions`
- Planned build log: `YYYY-MM-DD-us-004-01-restricted-scholarship-decisions.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a management-authorized approver, when a full/partial decision is approved or revoked, then scope, amount/percentage, dates, reason and actor are recorded and invalid overlaps follow the agreed rule.
2. Given a non-management role, when accessing decision lists, player flags, notifications, exports or files, then the server does not disclose restricted content.
3. Given a retroactive change affecting an issued invoice, when the decision changes, then no submitted invoice is silently rewritten; a reviewed correction path is required.

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
- Source references: [BA-QNR-001-Q02-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-06), [BA-QNR-001-Q03-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-01), [BA-QNR-001-Q03-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-02), [BA-QNR-001-Q03-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-03), [BA-QNR-001-Q03-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-04), [BA-QNR-001-Q03-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-05), [BA-QNR-001-Q03-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-06), [BA-QNR-001-Q03-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-07), [BA-QNR-001-Q03-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-08).
- Impact: Changed / needs clarification; Expanded; Expanded / needs clarification; Needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q02-06: Coach/technical director assesses scholarship trials and financial need; criteria and final approval authority need confirmation against admin approval responses.
  - BA-QNR-001-Q03-01: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
  - BA-QNR-001-Q03-02: Coach/technical director assesses scholarship trials and financial need; criteria and final approval authority need confirmation against admin approval responses.
  - BA-QNR-001-Q03-03: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
  - BA-QNR-001-Q03-04: Review/expiry TBD and payment-free registration approval unanswered; do not invent approval or expiry rules.
  - BA-QNR-001-Q03-05: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
  - BA-QNR-001-Q03-06: Explicit scholarship visibility: admin, director and finance only. Confirm exact role mapping; coach assessment does not imply access to scholarship status. No permission changes yet.
  - BA-QNR-001-Q03-07: Review/expiry TBD and payment-free registration approval unanswered; do not invent approval or expiry rules.
  - BA-QNR-001-Q03-08: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-004-scholarships-and-monthly-billing.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
