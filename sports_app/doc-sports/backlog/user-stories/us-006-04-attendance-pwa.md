# US-006-04: Dedicated Next.js offline attendance app

- Epic: EPIC-006
- State: In progress — first development prototype
- Priority: Must for the requested dedicated attendance frontend; production acceptance pending
- Requirements: SPORTS-FR-014, SPORTS-FR-015, SPORTS-FR-036, SPORTS-NFR-004, SPORTS-NFR-006
- Branch: `story/us-006-04-attendance-pwa`
- Dependencies: US-006-01 rosters; US-006-02 marking/corrections; existing Sports staff/Company permissions

As an authorized attendance operator, I want a dedicated phone-friendly app with downloaded rosters and a durable local queue, so I can capture manual attendance during connectivity loss and reconcile it when online.

## Acceptance criteria

1. Staff sign-in is required for private data; Guest gets only public shell/sign-in. Existing native roles, Company and document permission checks remain authoritative. No new broad role grants.
2. Explicit trusted-device enablement and online roster download precede offline capture. Cache minimal player identity/status/version fields only. Seven-day offline identity expiry does not delete pending work or renew while offline.
3. Present/Late/Absent/Excused capture persists before UI success and survives offline reload. Pending counts differ from server acceptance. No automatic finalization/absence or biometric claims.
4. Explicit sync verifies current account/company, uses server CSRF and version checks, and handles lost responses without duplicate marks/audit. Acknowledgments cannot delete a newer queued intent from another tab.
5. Concurrent/server validation conflicts remain visible and queued after reload. Staff either explicitly discard the local choice or review fresh server status and provide a correction reason before requeueing. Read-only/cancelled/future sessions stay protected.
6. Desktop/phone layout, privacy, storage failure and account/permission denial are verified. Forget-device control cannot discard unresolved marks. Existing HTML enrollment remains unchanged.
7. Online New session creates a scheduled session and eligible roster through existing server services, with permitted friendly program/group controls, academy-local dates/times, creation capability checks and tab-persisted same-key retry after lost responses. Cancellation/finalization remain in Boost. [Adjustment evidence](../../build-logs/2026-11-05-us-006-04-new-session.md).

## Evidence and limits

[Usage guide](../../attendance-app-guide.md). [Build log](../../build-logs/2026-11-03-us-006-04-attendance-pwa.md).

Console refinement: [Sports-owned Attendance App menu launcher](../../build-logs/2026-11-03-us-006-04-sports-console-link.md). Registered through the optional provider contract only for authorized Sports player-management staff; no ERP Boost code or Sports dependency added to the host.

Dedicated kiosk provisioning/encryption, assigned-coach scope, device biometrics/QR, large pilot performance, broader platform installation, retention/recovery rehearsal and production acceptance remain open. This story remains In progress for those controls and field acceptance.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q05-08](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-08), [BA-QNR-001-Q08-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-02), [BA-QNR-001-Q08-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-03).
- Impact: Confirmed / needs clarification; Needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q05-08: N/A does not establish reliable power/network; confirm venue conditions and portable-device/offline recovery acceptance. Keep existing offline prototype scope.
  - BA-QNR-001-Q08-02: Web delivery requested; No integrations answer does not remove the existing website or HTML enrollment direction. Confirm website migration/integration boundary; no native app implied.
  - BA-QNR-001-Q08-03: Web delivery requested; No integrations answer does not remove the existing website or HTML enrollment direction. Confirm website migration/integration boundary; no native app implied.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-006-sessions-and-attendance.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
