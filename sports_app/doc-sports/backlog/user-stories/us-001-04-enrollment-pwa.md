# US-001-04: Dedicated enrollment PWA

- Epic: EPIC-001
- State: Withdrawn — user clarified Next.js is for attendance
- Requirements: SPORTS-FR-003, SPORTS-FR-030, SPORTS-FR-035, SPORTS-NFR-006
- Branch: `story/us-001-04-enrollment-pwa`
- Dependencies: US-003-01 application intake; US-005-01 invoice/review services

As an applicant/guardian, I want a focused installable enrollment experience that preserves a draft during connectivity loss, so I can prepare an application and submit it when connected.

## Acceptance criteria

1. Use shared required player/guardian/emergency/consent definitions, configurable academy identity and existing application pathways. Consent starts unchecked.
2. Save/restore an optional device draft with clear privacy/expiry controls. After a prior online visit, reopen the app offline and edit the saved draft; final submission and payment claims remain disabled offline.
3. Make Payment reuses the existing server-owned draft Sales Invoice and immutable retry identity. Ambiguous failures survive tab reload without issuing a second request identity. Applicant claims request review without financial posting; admission remains separate.
4. Protect session tokens from persistent configuration caching; service worker caches only the public app shell. Preserve existing server validation, permissions and idempotency.
5. Verify desktop and phone layouts. Publish development entry point, reproducible build instructions and limitations.

## Evidence and follow-up

[Build log](../../build-logs/2026-11-03-us-001-04-enrollment-pwa.md). [Frontend guide](../../enrollment-app-guide.md).

Production browser/device coverage, broader accessibility, encrypted/managed-device policy, conflict-handled attendance synchronization and validated biometric hardware integration remain separate work. A phone authenticator must not be presented as a shared-player fingerprint scanner.

## Scope correction — 3 November 2026

The user requested restoring the existing HTML enrollment. This Next.js enrollment slice and SPORTS-FR-035 are withdrawn, not completed requirements. The Next.js frontend is intended for attendance instead. Runtime/source removed from active Sports tree; historical evidence retained. [Reversal build log](../../build-logs/2026-11-03-us-001-04-revert-enrollment-pwa.md).

## Discovery provenance — 6 November 2026

- Origin: **Original baseline only** (including subsequent user direction); no direct questionnaire response establishes this story’s specific scope. Preserve existing state and acceptance evidence.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-001-academy-configuration-and-access.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
