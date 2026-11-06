# US-005-05: Payment gateway discovery and reconciliation

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: Proposed
- Priority: Proposed launch candidate; estimate and sequence pending clarification
- Delivery owner / affected apps: Sports App / native ERPNext where applicable

## Story statement

**As an** authorized academy operator, **I want to** select and validate a payment gateway with reliable ERP reconciliation.

## Traceability

- Requirements: SPORTS-FR-042
- Dependencies: US-005-01 US-005-03
- Origin: Questionnaire only
- Source references: [BA-QNR-001-Q04-11](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-11)
- PRD: [Product requirements](../../PRD.md)
- Reconciliation: [BA-QNR-001 register](../../discovery/BA-QNR-001-reconciliation.md)
- Planned branch: `story/us-005-05-payment-gateway-discovery-and-reconciliation`

## Notes and scope

Provider, fees, methods, settlement timing, refunds and credentials are undecided. Begin sandbox discovery, not live payment enablement.

This is proposed scope, not implementation or commercial acceptance. Use generic sport configuration and Sports-prefixed owned DocTypes; preserve ERPNext accounting and backend authorization.

## Acceptance criteria — proposed

1. Record provider comparison and approved methods/fees, sandbox flow and accounting/settlement mappings before live integration.
2. A signed server callback with validated merchant, currency, amount and transaction identity may reconcile payment once; forged/replayed callbacks and client-only success screens cannot post funds.
3. Failures, partial payments, reversals and settlement differences enter an auditable review path; secrets remain server-owned.

## Verification plan

Verify authorized/denied roles, Company isolation, retries, correction history and relevant native ERP reconciliation. Agree fixtures, missing policies and failure cases before marking Ready.

## Completion evidence

- Discovery build log: [Questionnaire reconciliation](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Implementation: Not started; no delivery or hardware claims.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-005-payments-and-financial-history.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
