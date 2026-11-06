# US-007-01: Validate the provider and bind biometric identities

## Header

- Epic: [EPIC-007](../epics/EPIC-007-biometric-identity-and-device-events.md)
- State: In progress — preparation metadata only; hardware/provider validation pending
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** integration administrator, **I want** to map approved external biometric identities to players **so that** scans resolve to the correct academy record.

## Traceability

- Requirements: `SPORTS-FR-016`, `SPORTS-NFR-007`
- Dependencies: [US-003-02](../../backlog/user-stories/us-003-02-player-numbering-and-enrollment.md), [US-001-03](../../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md)
- Planned branch: `story/us-007-01-biometric-provider-and-identity`
- Planned build log: `YYYY-MM-DD-us-007-01-biometric-provider-and-identity.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

Directory separation refinement: **Fingerprint enrollments** is a standalone table; row actions and enrollment references open the selected player’s registration form. The form retains player/request references and returns to the same table search/page. Existing capture preparation and simulation remain unchanged. [Adjustment log](../../build-logs/2026-11-05-us-007-01-separate-enrollment-table.md).

Visual demo refinement: fixed SVG fingerprint preview, simulated scanning animation and server-confirmed completion, with permanent simulation label and reduced-motion support. No biometric collection or backend state changes. [Adjustment log](../../build-logs/2026-11-05-us-007-01-fingerprint-demo-animation.md).

Demo refinement: an explicit Demo capture generates a stable random DEMO-prefixed numeric identifier and CODE128 graphic for an existing pending request. Simulated metadata remains separate from real Pending capture/Withdrawn status, with actor/time and immutable reference. No barcode authentication or attendance ingestion. [Adjustment log](../../build-logs/2026-11-05-us-007-01-demo-capture-barcode.md).

Player-directory refinement: searchable paginated player table shows Not prepared or the latest request's Pending capture/Withdrawn status, finger and reference, with View / prepare action. No captured-state claim. [Adjustment log](../../build-logs/2026-11-05-us-007-01-player-capture-status-list.md).

5 November refinement: provide a preparation-only workflow without a scanner, using Sports Biometric Enrollment. Only Pending capture and Withdrawn are supported; no actual enrolled state, raw templates, device identity binding or scan-based attendance. [Guide](../../fingerprint-preparation-guide.md). Requirement SPORTS-FR-037 covers this slice separately from live provider validation.

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given the selected hardware/provider, when discovery is completed, then model/API, authentication, identifiers, timezone, offline behavior, template boundary and consent/guardian and retention decisions are recorded before live enrollment.
2. Given a valid player and external identity, when binding, then duplicate/conflicting mappings are rejected and only authorized administrators can enroll or revoke identities.
3. Given revocation or retention expiry, when cleanup runs, then configured local/provider actions and failures are tracked; no raw templates are exposed in ordinary APIs, profile pages or logs.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Pending fingerprint capture preparation](../../build-logs/2026-11-05-us-007-01-fingerprint-preparation.md).
- Verification summary: Administrator-only player/consent preparation, duplicate prevention, pending/withdrawn lifecycle and blocked native edits verified. No fingerprints or external identities captured/bound; full story acceptance remains open.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q05-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-05), [BA-QNR-001-Q05-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-06), [BA-QNR-001-Q05-07](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-07), [BA-QNR-001-Q05-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-10), [BA-QNR-001-Q09-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q09-01).
- Impact: Changed; Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q05-05: Fingerprint for identity/attendance; ZK-9500 named by academy, portable setup. Treat model as a candidate; SDK/browser/OS compatibility and procurement remain unverified.
  - BA-QNR-001-Q05-06: Fingerprint for identity/attendance; ZK-9500 named by academy, portable setup. Treat model as a candidate; SDK/browser/OS compatibility and procurement remain unverified.
  - BA-QNR-001-Q05-07: Fingerprint for identity/attendance; ZK-9500 named by academy, portable setup. Treat model as a candidate; SDK/browser/OS compatibility and procurement remain unverified.
  - BA-QNR-001-Q05-10: Parents sign consent at registration; obtain actual form and confirm biometric-specific scope, guardian authority, withdrawal and retention before real capture.
  - BA-QNR-001-Q09-01: Phases accepted; attendance and biometrics highest priority alongside payments/reporting. Replan within existing proposal assumptions after device discovery; no implied production deadline.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-007-biometric-identity-and-device-events.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
