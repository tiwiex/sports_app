# US-008-04: Procurement and player kit distribution

## Header

- Epic: [EPIC-008](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md)
- State: Proposed
- Priority: Proposed launch candidate; estimate and sequence pending clarification
- Delivery owner / affected apps: Sports App / native ERPNext where applicable

## Story statement

**As an** authorized academy operator, **I want to** procure academy stock and record accountable kit distribution to individual players.

## Traceability

- Requirements: SPORTS-FR-039
- Dependencies: US-008-01 US-003-03
- Origin: Both
- Source references: [BA-QNR-001-Q03-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-05), [BA-QNR-001-Q10-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-04)
- PRD: [Product requirements](../../PRD.md)
- Reconciliation: [BA-QNR-001 register](../../discovery/BA-QNR-001-reconciliation.md)
- Planned branch: `story/us-008-04-procurement-and-player-kit-distribution`

## Notes and scope

Inventory is explicit now; procurement/distribution already existed in proposal direction. Confirm sizes, kit entitlements, stock costing, scholarship privacy and launch warehouses.

This is proposed scope, not implementation or commercial acceptance. Use generic sport configuration and Sports-prefixed owned DocTypes; preserve ERPNext accounting and backend authorization.

## Acceptance criteria — proposed

1. Given authorized procurement, use native ERPNext supplier, purchase order/receipt/invoice and warehouse controls; receiving stock updates quantities once.
2. An authorized operator issues the selected kit/size/quantity to a stable player reference with native stock movement and attributable issue history; retries do not duplicate issues.
3. Returns/corrections retain the original issue link; stock/issue reports reconcile and ordinary kit operators cannot infer scholarship status.

## Verification plan

Verify authorized/denied roles, Company isolation, retries, correction history and relevant native ERP reconciliation. Agree fixtures, missing policies and failure cases before marking Ready.

## Completion evidence

- Discovery build log: [Questionnaire reconciliation](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Implementation: Not started; no delivery or hardware claims.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
