# Build log: Fingerprint registration preparation without a scanner

- Date: 2026-11-05 (Africa/Lagos)
- Story / epic: US-007-01 / EPIC-007
- Requirements: SPORTS-FR-016/037, SPORTS-NFR-007
- Affected apps / branches / versions: Sports App, `story/us-007-01-fingerprint-preparation`; existing pending attendance/reversal work preserved
- Pull requests: None; no commit, merge or push
- Status: Verified development preparation slice; hardware/provider acceptance incomplete

## Intended outcome and starting context

User requested a fingerprint registration system before a scanner is available. Implement a real preparation/consent workflow without pretending to capture, verify or enroll fingerprints. Existing players and the Next.js attendance app are reused.

## Policy decisions and plan

Only Sports Academy Administrator/System Manager can prepare or withdraw requests, with native Company/player/document access. Ordinary registrars receive no new powers. Require actual supplied consent metadata and explicit confirmation; do not reuse medical/media consent as biometric permission. Selected finger is a future capture instruction only.

No scanner/device mapping, fingerprint image/template, Enrolled/Captured state or biometric attendance is implemented. Actual provider/SDK, identity validation, guardian authority and retention/deletion policy remain full-story prerequisites before live capture. This slice is not legal/compliance acceptance.

## Work performed

- Added app-owned DocType **Sports Biometric Enrollment**, track_changes enabled, immutable preparation/consent identity, unique request UUID and server-created actor/time. Only Pending capture and Withdrawn status options exist. Native deletion and ordinary native edits are blocked; consent corrections require withdrawal/new preparation. Metadata retained for audit.
- `biometric_preparation.py`: administrator/Company/player guards; bounded player search and history; strict consent-field allowlist, finger/relationship/date validation and no future consent dates. Player row lock serializes preparation and prevents duplicate pending records. Same UUID/hash retry returns the same record, including its withdrawn state; changed payload or a second pending request is rejected. Withdrawal requires a reason and preserves native audit history.
- `attendance_mobile_api.py`: authenticated advisory administrator capability; Guest remains authenticated=false only. No new role grants.
- `attendance_app/app/fingerprint-registration.js`: online administrator-only dialog with player search/ID selection, pending/withdrawn history, finger choice, consent name/relationship/reference/date, unchecked confirmation and reasoned withdrawal. Prominent scanner-not-connected explanation; no Capture/Enrolled action. In-memory UUID protects unchanged retries; reload requires reviewing existing requests. Consent choices reset on player change and withdrawal.
- Consent details are not persisted to the offline attendance store or public service-worker cache. Existing manual attendance and HTML enrollment/finance logic unchanged.
- Added focused Python tests, extended actual-export browser fixture, updated requirements/PRD/story and usage documentation. Story remains In progress.

## Commands and observations

- Python unittest discovery: **127 tests passed**. Checks include unauthorized capability denial, missing consent, forbidden extra/template field, invalid finger/date, forged service flag, schema lacking capture/template state, narrow response and cross-company player rejection.
- Next production build passed; published development version `0426e19c6a594eef` with 19 public assets. Loaded only the new DocType via `frappe.reload_doc`, then committed schema. No full migration or existing permission reset. Cleared development cache and restarted development web workers only.
- Native rollback fixture used an existing configured-company player and synthetic consent: prepare, identical retry, duplicate pending rejection, direct native edit denial, history read, withdrawal, old-key withdrawn retry and new-key reprepare all passed. Rolled back every record; original biometric metadata/player/attendance/Customer/invoice/Payment Entry counts restored. Guest player search denied. No real consent or fingerprints retained.
- Real-export Chromium fixture at desktop/phone passed player selection, unchecked/required consent, Pending capture response, mandatory withdrawal reason, Withdrawn state, confirmation reset and hidden controls for registrar/Guest. Existing session creation/retry, offline queue/sync/conflict/storage checks passed. APIs synthetic in browser; no live ERP writes.
- HTTPS friendly entry version and bytes matched published export. Real Guest bootstrap exposes no private metadata. `git diff --check` passed.

## Verification evidence

| Criterion / slice | Check / artifact | Result |
|---|---|---|
| Admin/Company/player boundaries | Python guards, native Guest denial and existing native permissions | Passed changed scope |
| Preparation and consent accuracy | Strict allowlist, explicit unchecked confirmation, date/finger validation | Passed |
| Duplicate/retry/lifecycle integrity | Native same-key/duplicate/withdraw/reprepare rollback fixture | Passed; concurrent service calls serialized by player lock, load testing not performed |
| Native state bypass prevention | Native edit rejected; only pending/withdrawn schema and no templates | Passed |
| Responsive interface | [Desktop](assets/2026-11-05-fingerprint-preparation-1440.png), [Phone](assets/2026-11-05-fingerprint-preparation-390.png) | Passed synthetic fixture |
| Full US-007-01 hardware/provider acceptance | Scanner identity binding, actual capture and provider deletion | Not implemented; pending hardware validation |

## Decisions, deviations and recovery

Calling the metadata DocType Enrollment does not mean enrollment happened; its visible state remains Pending capture until a future verified hardware implementation exists. Withdrawal is a request withdrawal, not proof of provider deletion. No legacy medical/media consent was copied or checked automatically. Browser tests and native synthetic records were isolated; native records fully rolled back and browser contexts closed. New schema remains installed with zero QA rows.

## Remaining work and release impact

Refresh/reopen https://moyours.ideltatech.com/sports-attendance as an academy administrator and choose Fingerprint registration. Native record is discoverable under Sports Biometric Enrollment. Deployment elsewhere requires migration/reload for the new DocType plus frontend rebuild/publish. No ERP Boost edits or finance/schema changes beyond this one Sports DocType.

No biometric capture, external identity mapping, matching, biometric attendance, device simulation or biometric deletion claim. Guardian authority, actual approved consent notice, retention and hardware/provider validation remain prerequisites before real capture. Preparation metadata retention/deletion and production privacy acceptance remain open; this is a prototype slice only.
