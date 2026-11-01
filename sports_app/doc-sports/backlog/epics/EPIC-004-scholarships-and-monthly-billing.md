# EPIC-004: Scholarships and monthly billing

## Outcome

Approved concessions and fee rules produce correct monthly obligations.

## Scope and success

Deliver the three independently specified stories below, including their permission, data-integrity and failure cases. All work is forward-looking. See the [PRD](../../PRD.md) and [requirement baseline](../../concepts/requirement-baseline.md) for shared rules and unresolved decisions.

## Stories

| Story | Outcome | Priority | State | Dependencies |
|---|---|---|---|---|
| [US-004-01](../user-stories/us-004-01-restricted-scholarship-decisions.md) | Manage effective-dated scholarship and exemption decisions | Must | Proposed | US-001-03, US-003-02 |
| [US-004-02](../user-stories/us-004-02-fee-plans-and-policy.md) | Configure fee plans and concession-safe charge calculation | Must | Proposed | US-001-01, US-004-01 |
| [US-004-03](../user-stories/us-004-03-monthly-obligations-and-invoices.md) | Generate monthly obligations and ERPNext invoices safely | Must | Proposed | US-004-02, US-003-02 |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.
