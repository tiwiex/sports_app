# EPIC-005: Payments and financial history

## Outcome

Player payment records reconcile to ERPNext accounting.

## Scope and success

- Retain invoice-first Make Payment, applicant Pending Review claim and authorized one-click invoice/receipt completion.
- Merge partial-payment admission and correction/reconciliation needs into existing fee/payment stories; current full-payment PoC is unchanged.
- Integrate proposed email reminders/downloadable receipts and payment-gateway discovery into the main story table.

## Stories

This is the complete current epic inventory, including proposed additions and withdrawn history. State is copied from each story as of 6 November 2026; a prototype does not establish full acceptance.

| Story | State | Origin | Priority |
|---|---|---|---|
| [US-005-01: Record player-attributed payments using ERPNext](../user-stories/us-005-01-player-receipts-and-allocations.md) | In review | Both | Must |
| [US-005-02: Show monthly payment status and source history](../user-stories/us-005-02-monthly-status-and-history.md) | In progress | Both | Must |
| [US-005-03: Reconcile credits, refunds and payment corrections](../user-stories/us-005-03-corrections-and-reconciliation.md) | In progress | Both | Must |
| [US-005-04: Parent reminders and receipt delivery](../user-stories/us-005-04-parent-reminders-and-receipt-delivery.md) | In progress | Both | Proposed launch candidate; estimate and sequence pending clarification |
| [US-005-05: Payment gateway discovery and reconciliation](../user-stories/us-005-05-payment-gateway-discovery-and-reconciliation.md) | Proposed | Questionnaire only | Proposed launch candidate; estimate and sequence pending clarification |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
## Consolidated discovery decisions

- Approve amounts, thresholds, authorized admin/finance confirmation and refund rules before behavior changes.
- Select gateway/provider/methods and notification schedule/recipients; WhatsApp remains investigation only.

- Epic origin: **Both**. Individual rows distinguish questionnaire-only additions from overlapping scope.
- Source responses: [BA-QNR-001-Q01-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-01), [BA-QNR-001-Q01-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-02), [BA-QNR-001-Q02-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-01), [BA-QNR-001-Q02-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-09), [BA-QNR-001-Q04-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-01), [BA-QNR-001-Q04-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-02), [BA-QNR-001-Q04-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-03), [BA-QNR-001-Q04-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-04), [BA-QNR-001-Q04-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-06), [BA-QNR-001-Q04-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-07), [BA-QNR-001-Q04-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-09), [BA-QNR-001-Q04-11](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-11), [BA-QNR-001-Q04-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-12), [BA-QNR-001-Q04-13](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-13), [BA-QNR-001-Q06-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-01), [BA-QNR-001-Q10-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-01), [BA-QNR-001-Q10-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-02), [BA-QNR-001-Q10-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-03).
- [Question-level reconciliation](../../discovery/BA-QNR-001-reconciliation.md); [consolidation evidence](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
- Open decisions are proposed refinements, not permission, pricing, delivery-state or commercial changes. Resolve them before affected work becomes Ready.
