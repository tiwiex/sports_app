# US-004-02: Configure fee plans and concession-safe charge calculation

## Header

- Epic: [EPIC-004](../epics/EPIC-004-scholarships-and-monthly-billing.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** finance administrator, **I want** to configure effective monthly plans and calculate authorized amounts **so that** billing uses agreed academy policy.

## Traceability

- Requirements: `SPORTS-FR-008`, `SPORTS-FR-009`
- Dependencies: [US-001-01](../../backlog/user-stories/us-001-01-academy-and-program-settings.md), [US-004-01](../../backlog/user-stories/us-004-01-restricted-scholarship-decisions.md)
- Planned branch: `story/us-004-02-fee-plans-and-policy`
- Planned build log: `YYYY-MM-DD-us-004-02-fee-plans-and-policy.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given an active plan, when saved, then effective dates, currency, company, service item, income account and due-date rule are valid.
2. Given full and partial concessions, when finance previews a charge, then the final amount is correct and scholarship reasons/status are absent from routine finance payloads.
3. Given mid-month enrollment, suspension, overlapping rules or missing mappings, when previewing, then an explicitly selected policy is applied or billing stops with a clear exception; capture approved examples before implementation.

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
- Source references: [BA-QNR-001-Q03-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-01), [BA-QNR-001-Q03-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-03), [BA-QNR-001-Q03-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-05), [BA-QNR-001-Q03-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-08), [BA-QNR-001-Q04-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-01), [BA-QNR-001-Q04-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-06), [BA-QNR-001-Q04-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-07), [BA-QNR-001-Q04-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-09).
- Impact: Conflicting / needs clarification; Expanded; Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q03-01: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
  - BA-QNR-001-Q03-03: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
  - BA-QNR-001-Q03-05: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
  - BA-QNR-001-Q03-08: Scholarship/non-scholarship; full scholarship includes kits, trips/trials/tournaments. Separate fee coverage and benefits; no forced extra categories. About half current players are beneficiaries.
  - BA-QNR-001-Q04-01: Source mentions 150k/220k including 30k kit and 40k subscription; PoC uses 220k registration +30k kit =250k excluding monthly40k. Obtain approved itemized fee schedule before changes.
  - BA-QNR-001-Q04-06: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-07: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-09: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-004-scholarships-and-monthly-billing.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
