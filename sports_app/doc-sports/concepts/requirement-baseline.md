# Sports requirement baseline

2026-11-05 addition: `SPORTS-FR-037`, administrator-only fingerprint consent/preparation metadata without hardware capture, templates, device mapping or biometric attendance. [US-007-01](../backlog/user-stories/us-007-01-biometric-provider-and-identity.md); live provider acceptance remains pending.

2026-11-03 addition: `SPORTS-FR-036`, dedicated Next.js attendance frontend with trusted-device roster download, offline manual capture and explicit authenticated conflict-aware sync. [US-006-04](../backlog/user-stories/us-006-04-attendance-pwa.md). This is separate from withdrawn enrollment PWA requirement `SPORTS-FR-035`; HTML enrollment remains unchanged.

Captured 2026-11-01. Initial planning status for the original rows: **Proposed**; current delivery state is recorded by the linked stories and build logs. Requirement IDs are prefixed `SPORTS-` to avoid ambiguity with ERP Boost's separate `FR-*` and `NFR-*` register. Epic/story IDs are local to this folder; qualify them as `sports_app:US-...` in cross-app issues.

The [original brief](../requirements.txt) remains unchanged. “Client brief” identifies directly requested outcomes; “User direction” identifies the accompanying IDE request; “Proposed” identifies analysis or design detail requiring refinement. This table is a documentation register, not a live Frappe DocType. Requirement behavior and release tests are developed in the [PRD](../PRD.md) and linked stories.

| Requirement | Need / capability | Provenance | Delivery stories |
|---|---|---|---|
| SPORTS-FR-001 | Academy and program configuration | User direction + proposed detail | [US-001-01](../backlog/user-stories/us-001-01-academy-and-program-settings.md) |
| SPORTS-FR-002 | Configurable public website and explicit profile publication | User direction + proposed detail | [US-001-02](../backlog/user-stories/us-001-02-configurable-public-website.md) |
| SPORTS-FR-003 | Registration and application review | Client brief | [US-003-01](../backlog/user-stories/us-003-01-application-intake-and-review.md) |
| SPORTS-FR-004 | Immutable unique player registration number | Client brief | [US-003-02](../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md) |
| SPORTS-FR-005 | Central private player information and linked histories | Client brief | [US-003-03](../backlog/user-stories/us-003-03-central-player-profile.md) |
| SPORTS-FR-006 | Enrollment, grouping and effective lifecycle dates | Proposed detail | [US-001-01](../backlog/user-stories/us-001-01-academy-and-program-settings.md), [US-003-02](../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md) |
| SPORTS-FR-007 | Management-approved scholarship/exemption lifecycle | Client brief + proposed detail | [US-004-01](../backlog/user-stories/us-004-01-restricted-scholarship-decisions.md) |
| SPORTS-FR-008 | Management-only scholarship/exemption confidentiality | Client brief | [US-001-03](../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md), [US-004-01](../backlog/user-stories/us-004-01-restricted-scholarship-decisions.md), [US-004-02](../backlog/user-stories/us-004-02-fee-plans-and-policy.md) |
| SPORTS-FR-009 | Effective-dated monthly fee plans and ERP mappings | Proposed detail | [US-004-02](../backlog/user-stories/us-004-02-fee-plans-and-policy.md) |
| SPORTS-FR-010 | Idempotent monthly obligations and ERPNext invoices | Proposed detail supporting monthly payments | [US-004-03](../backlog/user-stories/us-004-03-monthly-obligations-and-invoices.md) |
| SPORTS-FR-011 | Player-attributed receipts and payment allocations | Client brief + proposed detail | [US-005-01](../backlog/user-stories/us-005-01-player-receipts-and-allocations.md) |
| SPORTS-FR-012 | Monthly payment status and complete history | Client brief | [US-005-02](../backlog/user-stories/us-005-02-monthly-status-and-history.md) |
| SPORTS-FR-013 | Traceable credits, refunds, cancellations and reconciliation | Proposed detail | [US-005-03](../backlog/user-stories/us-005-03-corrections-and-reconciliation.md) |
| SPORTS-FR-014 | Sessions and eligible attendance rosters | Proposed detail | [US-006-01](../backlog/user-stories/us-006-01-sessions-and-rosters.md) |
| SPORTS-FR-015 | Manual attendance and player attendance history | Client brief + proposed detail | [US-006-02](../backlog/user-stories/us-006-02-manual-attendance-and-corrections.md), [US-006-03](../backlog/user-stories/us-006-03-attendance-history-and-summary.md) |
| SPORTS-FR-016 | Biometric identity binding and revocation | Client brief + proposed detail | [US-007-01](../backlog/user-stories/us-007-01-biometric-provider-and-identity.md) |
| SPORTS-FR-017 | Authenticated device event ingestion and deduplication | Proposed detail supporting biometric attendance | [US-007-02](../backlog/user-stories/us-007-02-authenticated-device-ingestion.md) |
| SPORTS-FR-018 | Device exceptions, replay and reviewed corrections | Proposed detail | [US-007-03](../backlog/user-stories/us-007-03-device-replay-and-exception-review.md) |
| SPORTS-FR-019 | One role-aware staff console for Sports and Finance | User direction | [US-002-02](../backlog/user-stories/us-002-02-sports-console-provider.md), [US-002-03](../backlog/user-stories/us-002-03-console-login-and-finance-regression.md) |
| SPORTS-FR-020 | Versioned installed-app console provider interface | Proposed integration detail | [US-002-01](../backlog/user-stories/us-002-01-console-extension-spike.md), [US-002-02](../backlog/user-stories/us-002-02-sports-console-provider.md) |
| SPORTS-FR-021 | Server-enforced sports and finance permissions | Proposed detail | [US-001-03](../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md), [US-002-03](../backlog/user-stories/us-002-03-console-login-and-finance-regression.md) |
| SPORTS-FR-022 | ERP fit-gap, configuration and launch-module acceptance | User direction + proposed detail | [US-008-01](../backlog/user-stories/us-008-01-erp-fit-gap-and-module-matrix.md), [US-008-03](../backlog/user-stories/us-008-03-migration-pilot-and-production-readiness.md) |
| SPORTS-FR-023 | Operational dashboards, filters and authorized exports | Proposed detail | [US-006-03](../backlog/user-stories/us-006-03-attendance-history-and-summary.md), [US-008-02](../backlog/user-stories/us-008-02-operational-dashboard-and-exports.md) |
| SPORTS-FR-024 | Controlled import and opening balance reconciliation | Proposed detail | [US-008-03](../backlog/user-stories/us-008-03-migration-pilot-and-production-readiness.md) |
| SPORTS-FR-025 | Pilot, training, support and release evidence | Proposed detail | [US-008-03](../backlog/user-stories/us-008-03-migration-pilot-and-production-readiness.md) |
| SPORTS-NFR-001 | Separate app ownership and compatibility; Boost independent of Sports | User direction + proposed detail | [US-002-01](../backlog/user-stories/us-002-01-console-extension-spike.md), [US-002-02](../backlog/user-stories/us-002-02-sports-console-provider.md), [US-002-03](../backlog/user-stories/us-002-03-console-login-and-finance-regression.md) |
| SPORTS-NFR-002 | Least privilege across UI, API, export, search and cache | Proposed detail supporting management-only scope | [US-001-03](../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md), [US-002-03](../backlog/user-stories/us-002-03-console-login-and-finance-regression.md), [US-004-01](../backlog/user-stories/us-004-01-restricted-scholarship-decisions.md), [US-008-02](../backlog/user-stories/us-008-02-operational-dashboard-and-exports.md) |
| SPORTS-NFR-003 | Idempotency, concurrency safety and event reliability | Proposed detail | [US-003-01](../backlog/user-stories/us-003-01-application-intake-and-review.md), [US-003-02](../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md), [US-004-03](../backlog/user-stories/us-004-03-monthly-obligations-and-invoices.md), [US-005-01](../backlog/user-stories/us-005-01-player-receipts-and-allocations.md), [US-007-02](../backlog/user-stories/us-007-02-authenticated-device-ingestion.md), [US-007-03](../backlog/user-stories/us-007-03-device-replay-and-exception-review.md) |
| SPORTS-NFR-004 | Attributable audit and correction history | Proposed detail | [US-004-01](../backlog/user-stories/us-004-01-restricted-scholarship-decisions.md), [US-005-03](../backlog/user-stories/us-005-03-corrections-and-reconciliation.md), [US-006-02](../backlog/user-stories/us-006-02-manual-attendance-and-corrections.md), [US-007-03](../backlog/user-stories/us-007-03-device-replay-and-exception-review.md) |
| SPORTS-NFR-005 | Paginated history and agreed response-time targets | Proposed target | [US-003-03](../backlog/user-stories/us-003-03-central-player-profile.md), [US-008-02](../backlog/user-stories/us-008-02-operational-dashboard-and-exports.md) |
| SPORTS-NFR-006 | Responsive, keyboard-usable guided workflows | User direction + proposed target | [US-001-02](../backlog/user-stories/us-001-02-configurable-public-website.md), [US-002-02](../backlog/user-stories/us-002-02-sports-console-provider.md), [US-006-02](../backlog/user-stories/us-006-02-manual-attendance-and-corrections.md) |
| SPORTS-NFR-007 | Private attachments, minimal biometric data and retention controls | Proposed detail | [US-001-03](../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md), [US-003-03](../backlog/user-stories/us-003-03-central-player-profile.md), [US-007-01](../backlog/user-stories/us-007-01-biometric-provider-and-identity.md) |
| SPORTS-NFR-008 | Rehearsed backup, restore, migration and recovery | Proposed target | [US-007-03](../backlog/user-stories/us-007-03-device-replay-and-exception-review.md), [US-008-03](../backlog/user-stories/us-008-03-migration-pilot-and-production-readiness.md) |

## Original client outcome coverage

| Brief item | Requirement IDs |
|---|---|
| Registration | SPORTS-FR-003 |
| Player ID / registration number | SPORTS-FR-004 |
| Player information / central record | SPORTS-FR-005 |
| Management-only scholarship/exemption status | SPORTS-FR-007, SPORTS-FR-008 |
| Monthly payment records | SPORTS-FR-009, SPORTS-FR-010, SPORTS-FR-011 |
| Payment status/history | SPORTS-FR-012, SPORTS-FR-013 |
| Biometric identity | SPORTS-FR-016, SPORTS-FR-017, SPORTS-FR-018 |
| Attendance history | SPORTS-FR-014, SPORTS-FR-015 |

25 functional and 8 non-functional requirements are planning decomposition, not additional promises from the client. First-release requirements are Must unless a story explicitly identifies later work; release sequencing does not reduce the importance of biometrics or the agreed ERP scope.


## Accepted user refinements (2026-11-01)

| Requirement | Current rule | Delivery |
|---|---|---|
| SPORTS-FR-026 | Background, atomic creation of one Customer per player from registration details; no manual/shared payer selection | US-003-02 |
| SPORTS-FR-027 | Customer Group named for the initial program, created/reused during registration | US-003-02 |
| SPORTS-FR-028 | Management-only Sports Development Tools documentation hub; audited status/MoSCoW story controls | US-002-04 |
| SPORTS-FR-029 | Require unique player email; automatically provision a disabled non-Desk Website User for future self-service, without invitation or staff/finance roles | US-003-02 |
| SPORTS-FR-030 | Shared public-demo/staff registration fields based on reference enrollment; new DocTypes prefixed Sports | US-001-02, US-003-02 |
| SPORTS-FR-031 | Enrollment draft invoice with invoice-series transfer reference; applicant claim sends invoice to unposted review; Finance completes invoice and allocated receipt atomically | US-005-01 |
| SPORTS-NFR-009 | A separate dated, indexed build log after every story implementation or adjustment | US-002-04 and all subsequent work |

See [current requirements](../REQUIREMENTS.md) for the governing rules and [adjustment evidence](../build-logs/2026-11-01-us-002-04-guardrails-docs-and-program-categories.md).

## Club relations addition — 2 November 2026

SPORTS-FR-032: generic Company-scoped organisation/opportunity/correspondence workspace. SPORTS-FR-033: sourced directory and attributable staff relationship-priority assessment. Both map to EPIC-009 / US-009-01.

## Website payment review notifications — 3 November 2026

| ID | Requirement | Story |
|---|---|---|
| SPORTS-FR-034 | Configurable comma-separated review email list; transactional, duplicate-safe notification on first website payment claim; preserve Finance authorization | US-005-01 |

## BA questionnaire discovery — 6 November 2026

[BA-QNR-001 source register](../discovery/README.md) and [question-by-question reconciliation](../discovery/BA-QNR-001-reconciliation.md) preserve exact responses and classify overlap/new scope. These are proposed refinements; current implemented fees, IDs, role permissions, disabled Users and admission/payment behavior remain authoritative until a recorded decision changes them. Original-only scope is not removed.

| Requirement | Proposed discovery addition | Origin / delivery |
|---|---|---|
| SPORTS-FR-038 | Player performance assessments | Questionnaire only; [US-003-04](../backlog/user-stories/us-003-04-player-performance-assessments.md), Proposed |
| SPORTS-FR-039 | Procurement and player kit distribution | Both; [US-008-04](../backlog/user-stories/us-008-04-procurement-and-player-kit-distribution.md), Proposed |
| SPORTS-FR-040 | Arrival, departure and absence review | Both; [US-006-05](../backlog/user-stories/us-006-05-arrival-departure-and-absence-review.md), Proposed |
| SPORTS-FR-041 | Parent reminders and receipt delivery | Questionnaire only; [US-005-04](../backlog/user-stories/us-005-04-parent-reminders-and-receipt-delivery.md), Proposed |
| SPORTS-FR-042 | Payment gateway discovery and reconciliation | Questionnaire only; [US-005-05](../backlog/user-stories/us-005-05-payment-gateway-discovery-and-reconciliation.md), Proposed |

6 November 2026 refinement to SPORTS-FR-028: [story review controls](../story-review-guide.md) add narrowly editable status/MoSCoW and Mark Done, revision checks and indexed reviewer audit. Story narrative and other documents remain read-only.
