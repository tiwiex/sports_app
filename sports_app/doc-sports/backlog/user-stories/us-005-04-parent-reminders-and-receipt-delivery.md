# US-005-04: Parent reminders and receipt delivery

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: Proposed
- Priority: Proposed launch candidate; estimate and sequence pending clarification
- Delivery owner / affected apps: Sports App / native ERPNext where applicable

## Story statement

**As an** authorized academy operator, **I want to** send controlled email fee reminders and provide downloadable receipts from posted accounting records.

## Traceability

- Requirements: SPORTS-FR-041
- Dependencies: US-005-01 US-005-02
- Origin: Questionnaire only
- Source references: [BA-QNR-001-Q04-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-12), [BA-QNR-001-Q10-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-01)
- PRD: [Product requirements](../../PRD.md)
- Reconciliation: [BA-QNR-001 register](../../discovery/BA-QNR-001-reconciliation.md)
- Planned branch: `story/us-005-04-parent-reminders-and-receipt-delivery`

## Notes and scope

Recipient authority, schedule, opt-out/delivery handling and private access need refinement. WhatsApp is discovery only, provider/cost/template approval pending.

This is proposed scope, not implementation or commercial acceptance. Use generic sport configuration and Sports-prefixed owned DocTypes; preserve ERPNext accounting and backend authorization.

## Acceptance criteria — proposed

1. Given agreed recipient/schedule rules, send an email reminder using current reconciled outstanding amount and log delivery without disclosing another player’s finances.
2. Retrying the same billing/reminder event does not duplicate notifications; failed deliveries are visible for authorized review.
3. Authorized receipt download matches a submitted allocated receipt; applicant payment claims never produce a false cleared-payment receipt.

## Verification plan

Verify authorized/denied roles, Company isolation, retries, correction history and relevant native ERP reconciliation. Agree fixtures, missing policies and failure cases before marking Ready.

## Completion evidence

- Discovery build log: [Questionnaire reconciliation](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Implementation: Not started; no delivery or hardware claims.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-005-payments-and-financial-history.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
