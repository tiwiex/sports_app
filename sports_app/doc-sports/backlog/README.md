# Sports App product backlog

The 8 epics contain 25 implementation stories: **21 Proposed**, **US-003-02 In progress**, **US-002-04 In review**, and **US-001-01 / US-002-01 Done**. Priority is **Must** for the first complete release. “Must” includes user-requested outcomes and proposed controls necessary to operate them; refine details against the PRD decisions before committing estimates. US-002-01 has a verified console prototype and US-001-01 has verified academy settings; both were accepted by the user for local merge into develop.

```text
Original brief / user direction → SPORTS-FR / SPORTS-NFR → PRD → Epic → Story → App PR(s) → Build log → Release evidence
```

## Epic roadmap

| Epic | Outcome | Indicative gate |
|---|---|---|
| [EPIC-001](epics/EPIC-001-academy-configuration-and-access.md) | Academy configuration and access — A reusable academy setup and private operating boundary. | G1 |
| [EPIC-002](epics/EPIC-002-shared-console-integration.md) | Shared console integration — Sports and Finance run in one console while remaining separate apps. | G0–G1 |
| [EPIC-003](epics/EPIC-003-registration-and-player-record.md) | Registration and player record — Each player has a stable private identity and a central history. | G1 |
| [EPIC-004](epics/EPIC-004-scholarships-and-monthly-billing.md) | Scholarships and monthly billing — Approved concessions and fee rules produce correct monthly obligations. | G2 |
| [EPIC-005](epics/EPIC-005-payments-and-financial-history.md) | Payments and financial history — Player payment records reconcile to ERPNext accounting. | G2 |
| [EPIC-006](epics/EPIC-006-sessions-and-attendance.md) | Sessions and attendance — Operators record and review reliable session attendance. | G2 |
| [EPIC-007](epics/EPIC-007-biometric-identity-and-device-events.md) | Biometric identity and device events — One chosen provider connects securely to traceable attendance. | G3 |
| [EPIC-008](epics/EPIC-008-erp-readiness-reporting-and-rollout.md) | ERP readiness, reporting and rollout — The academy launches with reconciled data and an explicit ERP boundary. | G0 and G3–G4 |

## Delivery order and critical dependencies

1. Start `US-008-01` (ERP fit-gap) and `US-002-01` (console integration spike). Resolve target installation, provider support and academy policy/device discovery early; do not wait for the biometric epic to contact the supplier.
2. Deliver `EPIC-001` configuration and access, then `EPIC-003` registration/identity. Add the real Sports provider through `US-002-02` and validate login/finance regression through `US-002-03`.
3. Deliver `EPIC-004` fees and exemptions, `EPIC-005` payment/reconciliation and `EPIC-006` manual attendance against player IDs. These depend on the shared access and enrollment foundation.
4. Complete `EPIC-007` for the selected provider, and `US-008-02` reporting after source workflows reconcile.
5. Complete outstanding tasks from the ERP module matrix, then `US-008-03` migration, module acceptance, recovery, training and production pilot. Website publishing must also pass before the first complete release.

The dependency links in each story govern implementation order; numeric epic order is a grouping, not a schedule. Split stories further during refinement if they cannot be reviewed as one coherent slice. Fit-gap discoveries need new linked stories with requirement IDs before delivery commitment; the initial 24 do not pretend to define unknown ERP module gaps.

## Story states

| State | Meaning |
|---|---|
| Proposed | Captured, awaiting policy/dependency refinement |
| Ready | Meets Definition of Ready |
| In progress | Implementation started and build log opened |
| In review | Implementation and evidence under review |
| Done | Acceptance and Definition of Done satisfied |
| Blocked | Specific named dependency prevents progress |
| Retrospective | Historical delivery reconstructed from evidence; unused here |

## Story files

- [US-001-01](../backlog/user-stories/us-001-01-academy-and-program-settings.md)
- [US-001-02](../backlog/user-stories/us-001-02-configurable-public-website.md)
- [US-001-03](../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md)
- [US-002-01](../backlog/user-stories/us-002-01-console-extension-spike.md)
- [US-002-02](../backlog/user-stories/us-002-02-sports-console-provider.md)
- [US-002-03](../backlog/user-stories/us-002-03-console-login-and-finance-regression.md)
- [US-003-01](../backlog/user-stories/us-003-01-application-intake-and-review.md)
- [US-003-02](../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md)
- [US-003-03](../backlog/user-stories/us-003-03-central-player-profile.md)
- [US-004-01](../backlog/user-stories/us-004-01-restricted-scholarship-decisions.md)
- [US-004-02](../backlog/user-stories/us-004-02-fee-plans-and-policy.md)
- [US-004-03](../backlog/user-stories/us-004-03-monthly-obligations-and-invoices.md)
- [US-005-01](../backlog/user-stories/us-005-01-player-receipts-and-allocations.md)
- [US-005-02](../backlog/user-stories/us-005-02-monthly-status-and-history.md)
- [US-005-03](../backlog/user-stories/us-005-03-corrections-and-reconciliation.md)
- [US-006-01](../backlog/user-stories/us-006-01-sessions-and-rosters.md)
- [US-006-02](../backlog/user-stories/us-006-02-manual-attendance-and-corrections.md)
- [US-006-03](../backlog/user-stories/us-006-03-attendance-history-and-summary.md)
- [US-007-01](../backlog/user-stories/us-007-01-biometric-provider-and-identity.md)
- [US-007-02](../backlog/user-stories/us-007-02-authenticated-device-ingestion.md)
- [US-007-03](../backlog/user-stories/us-007-03-device-replay-and-exception-review.md)
- [US-008-01](../backlog/user-stories/us-008-01-erp-fit-gap-and-module-matrix.md)
- [US-008-02](../backlog/user-stories/us-008-02-operational-dashboard-and-exports.md)
- [US-008-03](../backlog/user-stories/us-008-03-migration-pilot-and-production-readiness.md)

Use the [story template](user-stories/STORY_TEMPLATE.md) and [development process](../DEVELOPMENT_PROCESS.md). In ERP Boost issues/PRs qualify IDs as `sports_app:US-002-01` to distinguish local Boost story IDs.

- [US-002-04: Development documentation and build evidence](user-stories/us-002-04-development-documentation-and-build-evidence.md)
