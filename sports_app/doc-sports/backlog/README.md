# Sports App consolidated product backlog

Updated 6 November 2026: **9 epics, 33 story records**, including the withdrawn enrollment PWA history. Original scope, accepted refinements and BA-QNR-001 discovery share one backlog; there is no duplicate questionnaire epic set. Existing IDs and delivery evidence are preserved. Proposed additions are not promises of delivery within the prior budget/timeline.

[Source register](../discovery/README.md) · [82-question reconciliation](../discovery/BA-QNR-001-reconciliation.md) · [Current requirements](../REQUIREMENTS.md) · [PRD](../PRD.md)

## How to read this backlog

- **Both:** original baseline/user direction and questionnaire evidence overlap. New details can remain proposed even in an implemented story.
- **Questionnaire only:** new story outcome introduced by the questionnaire.
- **Original baseline only:** retained existing scope without direct questionnaire confirmation.
- State is the current story header, not inferred from prototype screenshots or questionnaire responses. Proposed policies remain open until refined; Done stories are not automatically reopened.

## Complete epic roadmap

| Epic | Consolidated outcome | Story records | Source coverage | Key decision |
|---|---|---|---|---|
| [EPIC-001](epics/EPIC-001-academy-configuration-and-access.md) | Academy configuration and controlled access | 4 | Both | Confirm age-band progression rules and role mapping; coach assessment does not grant scholarship visibility. |
| [EPIC-002](epics/EPIC-002-shared-console-integration.md) | Shared console and development documentation | 4 | Original baseline only | Validate combined Sports/Finance/Boost-only permissions and compatible releases before rollout. |
| [EPIC-003](epics/EPIC-003-registration-and-player-record.md) | Registration, player lifecycle and performance | 4 | Both | Confirm legacy ID grammar without renumbering existing players; returning-player undertaking, penalty and retention policy remain open. |
| [EPIC-004](epics/EPIC-004-scholarships-and-monthly-billing.md) | Scholarships, fee policy and recurring billing | 3 | Both | Resolve fee breakdown conflict with the current NGN250,000 PoC and ambiguous billing-cadence Yes response. |
| [EPIC-005](epics/EPIC-005-payments-and-financial-history.md) | Payments, financial history and controlled communications | 5 | Both | Approve amounts, thresholds, authorized admin/finance confirmation and refund rules before behavior changes. |
| [EPIC-006](epics/EPIC-006-sessions-and-attendance.md) | Sessions, attendance and arrival/departure | 5 | Both | Define cutoff/timezone, lateness, missing departures, session finalization and event ordering. |
| [EPIC-007](epics/EPIC-007-biometric-identity-and-device-events.md) | Biometric identity, portable device integration and exceptions | 3 | Both | Validate supplier SDK, operating system/browser bridge, physical device, portability and event identity before choosing integration. |
| [EPIC-008](epics/EPIC-008-erp-readiness-reporting-and-rollout.md) | ERP operations, inventory, reporting and rollout | 4 | Both | Confirm kit sizes/entitlements, warehouse/stock costing and source import quality; performance reports depend on EPIC-003 metrics. |
| [EPIC-009](epics/EPIC-009-club-and-partner-relations.md) | Club and partner relationships | 1 | Original baseline only | Confirm priority against revised launch scope; questionnaire silence does not delete the club directory or approve future integrations. |

## Delivery sequencing for refinement

1. Resolve fee/admission/role decisions and start nominated-device discovery early. These are blockers to specific acceptance, not reasons to pause independent work.
2. Retain configuration/access and shared-console foundations; extend registration/private profile only with agreed fields/policies.
3. Prioritize attendance/biometrics, payments and reporting per BA responses; continue manual fallback and invoice review controls while hardware is validated.
4. Refine performance metrics and native inventory/kit distribution with their owners; estimate new stories before assigning release dates. Gateway and WhatsApp choices remain discovery.
5. Reconcile imports/stock/financial reports, train five staff, rehearse recovery and approve pilot/support terms. Review the eight-week/NGN7M proposal against agreed scope before changing commitments.

## Complete story inventory

### EPIC-001: Academy configuration and controlled access

| Story | Current state | Origin |
|---|---|---|
| [US-001-01: Configure academy and program defaults](user-stories/us-001-01-academy-and-program-settings.md) | Done | Both |
| [US-001-02: Configure and publish academy website content](user-stories/us-001-02-configurable-public-website.md) | In progress | Both |
| [US-001-03: Define and enforce sports permissions](user-stories/us-001-03-sports-role-and-data-boundaries.md) | In progress | Both |
| [US-001-04: Dedicated enrollment PWA](user-stories/us-001-04-enrollment-pwa.md) | Withdrawn — user clarified Next.js is for attendance | Original baseline only |

### EPIC-002: Shared console and development documentation

| Story | Current state | Origin |
|---|---|---|
| [US-002-01: Validate and specify the console provider contract](user-stories/us-002-01-console-extension-spike.md) | Done | Original baseline only |
| [US-002-02: Mount Sports views in the shared console](user-stories/us-002-02-sports-console-provider.md) | Proposed | Original baseline only |
| [US-002-03: Unify console entry and protect existing Finance behavior](user-stories/us-002-03-console-login-and-finance-regression.md) | Proposed | Original baseline only |
| [US-002-04: Expose Sports development documentation and build evidence](user-stories/us-002-04-development-documentation-and-build-evidence.md) | In review | Original baseline only |

### EPIC-003: Registration, player lifecycle and performance

| Story | Current state | Origin |
|---|---|---|
| [US-003-01: Capture and review player registrations](user-stories/us-003-01-application-intake-and-review.md) | In progress — PoC workflow | Both |
| [US-003-02: Assign stable player IDs and enrollment dates](user-stories/us-003-02-player-numbering-and-enrollment.md) | In progress | Both |
| [US-003-03: Present the private central player record](user-stories/us-003-03-central-player-profile.md) | In progress — central record slice verified | Both |
| [US-003-04: Player performance assessments](user-stories/us-003-04-player-performance-assessments.md) | Proposed | Questionnaire only |

### EPIC-004: Scholarships, fee policy and recurring billing

| Story | Current state | Origin |
|---|---|---|
| [US-004-01: Manage effective-dated scholarship and exemption decisions](user-stories/us-004-01-restricted-scholarship-decisions.md) | In review | Both |
| [US-004-02: Configure fee plans and concession-safe charge calculation](user-stories/us-004-02-fee-plans-and-policy.md) | In review | Both |
| [US-004-03: Generate monthly obligations and ERPNext invoices safely](user-stories/us-004-03-monthly-obligations-and-invoices.md) | In review | Both |

### EPIC-005: Payments, financial history and controlled communications

| Story | Current state | Origin |
|---|---|---|
| [US-005-01: Record player-attributed payments using ERPNext](user-stories/us-005-01-player-receipts-and-allocations.md) | In review | Both |
| [US-005-02: Show monthly payment status and source history](user-stories/us-005-02-monthly-status-and-history.md) | In progress | Both |
| [US-005-03: Reconcile credits, refunds and payment corrections](user-stories/us-005-03-corrections-and-reconciliation.md) | In progress | Both |
| [US-005-04: Parent reminders and receipt delivery](user-stories/us-005-04-parent-reminders-and-receipt-delivery.md) | In progress | Both |
| [US-005-05: Payment gateway discovery and reconciliation](user-stories/us-005-05-payment-gateway-discovery-and-reconciliation.md) | Proposed | Questionnaire only |

### EPIC-006: Sessions, attendance and arrival/departure

| Story | Current state | Origin |
|---|---|---|
| [US-006-01: Create sessions and eligible player rosters](user-stories/us-006-01-sessions-and-rosters.md) | In progress — manual attendance prototype | Both |
| [US-006-02: Capture manual attendance and reviewed corrections](user-stories/us-006-02-manual-attendance-and-corrections.md) | In progress — manual attendance prototype | Both |
| [US-006-03: Review attendance history and filtered summaries](user-stories/us-006-03-attendance-history-and-summary.md) | Proposed | Both |
| [US-006-04: Dedicated Next.js offline attendance app](user-stories/us-006-04-attendance-pwa.md) | In progress — first development prototype | Both |
| [US-006-05: Arrival, departure and absence review](user-stories/us-006-05-arrival-departure-and-absence-review.md) | Proposed | Both |

### EPIC-007: Biometric identity, portable device integration and exceptions

| Story | Current state | Origin |
|---|---|---|
| [US-007-01: Validate the provider and bind biometric identities](user-stories/us-007-01-biometric-provider-and-identity.md) | In progress — preparation metadata only; hardware/provider validation pending | Both |
| [US-007-02: Ingest device events with deduplication and session matching](user-stories/us-007-02-authenticated-device-ingestion.md) | Proposed | Both |
| [US-007-03: Resolve device exceptions and recover from outages](user-stories/us-007-03-device-replay-and-exception-review.md) | Proposed | Original baseline only |

### EPIC-008: ERP operations, inventory, reporting and rollout

| Story | Current state | Origin |
|---|---|---|
| [US-008-01: Define ERP coverage and launch-required modules](user-stories/us-008-01-erp-fit-gap-and-module-matrix.md) | Proposed | Both |
| [US-008-02: Provide authorized academy dashboards and exports](user-stories/us-008-02-operational-dashboard-and-exports.md) | Proposed | Both |
| [US-008-03: Rehearse migration and validate production readiness](user-stories/us-008-03-migration-pilot-and-production-readiness.md) | Proposed | Both |
| [US-008-04: Procurement and player kit distribution](user-stories/us-008-04-procurement-and-player-kit-distribution.md) | Proposed | Both |

### EPIC-009: Club and partner relationships

| Story | Current state | Origin |
|---|---|---|
| [US-009-01: Club and partner directory, opportunities and correspondence](user-stories/us-009-01-club-partner-relations.md) | See story | Original baseline only |

## Delivery-state snapshot

- Done: 2
- In Review — development slice: 1
- In progress: 3
- In progress — PoC workflow: 1
- In progress — first development prototype: 1
- In progress — invoice-first enrollment PoC: 1
- In progress — manual attendance prototype: 2
- In progress — preparation metadata only; hardware/provider validation pending: 1
- In progress — central record slice verified: 1
- In review: 4
- Proposed: 15
- Withdrawn — user clarified Next.js is for attendance: 1

[Consolidation build log](../build-logs/2026-11-06-backlog-consolidated-epics.md). This overview supersedes earlier baseline-only counts; historical build logs remain unchanged. Enrollment stays HTML; the withdrawn US-001-04 experiment remains traceable and Next.js is attendance only.
