# US-005-03: Reconcile credits, refunds and payment corrections

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** finance manager, **I want** to correct transactions through approved ERPNext paths **so that** player history stays consistent with the ledger.

## Traceability

- Requirements: `SPORTS-FR-013`, `SPORTS-NFR-004`
- Dependencies: [US-005-02](../../backlog/user-stories/us-005-02-monthly-status-and-history.md)
- Planned branch: `story/us-005-03-corrections-and-reconciliation`
- Planned build log: `YYYY-MM-DD-us-005-03-corrections-and-reconciliation.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a cancelled receipt, return or credit note, when an authorized correction completes, then affected obligations and player balances recompute from submitted source documents.
2. Given an attempted correction by an unauthorized cashier, when called directly, then financial approval/permission rules deny the action.
3. Given a reconciliation run, when comparing obligations, invoices and allocations, then mismatches are reported by source reference, correction actors are auditable and no duplicate Sports ledger is introduced.

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
- Source references: [BA-QNR-001-Q04-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-06), [BA-QNR-001-Q04-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-07), [BA-QNR-001-Q04-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-09).
- Impact: Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q04-06: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-07: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
  - BA-QNR-001-Q04-09: About70% late; installments/discounts and non-subscription refunds; part payment may confirm registration with notice period. Approval, thresholds, due dates and refund policy need definition; existing complete-payment PoC stays unchanged.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-005-payments-and-financial-history.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
