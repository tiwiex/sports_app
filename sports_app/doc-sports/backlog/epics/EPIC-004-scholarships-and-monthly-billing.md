# EPIC-004: Scholarships and monthly billing

## Outcome

Approved concessions and fee rules produce correct monthly obligations.

## Scope and success

- Merge scholarship/non-scholarship categories, full fee coverage and kit/trip/trial/tournament benefits with existing restricted decisions.
- Extend proposed fee policies for installments, discounts, grace/notice and refund eligibility; monthly obligations still reconcile to ERPNext.
- Treat automatic Customer classification and scholarship eligibility as separate concerns; benefits must not expose confidential status to stock operators.

## Stories

This is the complete current epic inventory, including proposed additions and withdrawn history. State is copied from each story as of 6 November 2026; a prototype does not establish full acceptance.

| Story | State | Origin | Priority |
|---|---|---|---|
| [US-004-01: Manage effective-dated scholarship and exemption decisions](../user-stories/us-004-01-restricted-scholarship-decisions.md) | Proposed | Both | Must |
| [US-004-02: Configure fee plans and concession-safe charge calculation](../user-stories/us-004-02-fee-plans-and-policy.md) | Proposed | Both | Must |
| [US-004-03: Generate monthly obligations and ERPNext invoices safely](../user-stories/us-004-03-monthly-obligations-and-invoices.md) | Proposed | Both | Must |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
## Consolidated discovery decisions

- Resolve fee breakdown conflict with the current NGN250,000 PoC and ambiguous billing-cadence Yes response.
- Confirm coach recommendation versus admin approval, payment-free admission, review/expiry and exact visibility roles.

- Epic origin: **Both**. Individual rows distinguish questionnaire-only additions from overlapping scope.
- Source responses: [BA-QNR-001-Q02-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-06), [BA-QNR-001-Q03-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-01), [BA-QNR-001-Q03-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-02), [BA-QNR-001-Q03-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-03), [BA-QNR-001-Q03-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-04), [BA-QNR-001-Q03-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-05), [BA-QNR-001-Q03-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-06), [BA-QNR-001-Q03-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-07), [BA-QNR-001-Q03-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-08), [BA-QNR-001-Q04-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-01), [BA-QNR-001-Q04-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-06), [BA-QNR-001-Q04-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-07), [BA-QNR-001-Q04-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-09), [BA-QNR-001-Q04-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-10).
- [Question-level reconciliation](../../discovery/BA-QNR-001-reconciliation.md); [consolidation evidence](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
- Open decisions are proposed refinements, not permission, pricing, delivery-state or commercial changes. Resolve them before affected work becomes Ready.
