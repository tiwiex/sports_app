# Build log: Simulated capture with random barcode reference

- Date: 2026-11-05 (Africa/Lagos)
- Story / epic: US-007-01 / EPIC-007
- Requirements: SPORTS-FR-037, SPORTS-NFR-007
- Affected apps / branch: Sports App, `story/us-007-01-fingerprint-preparation`; previous pending work preserved
- Pull requests: None; no commit, merge or push
- Status: Verified development demo adjustment

## Intended outcome and starting context

User requested a dummy capture button or random barcode-like numbers while no fingerprint scanner is available. Add a usable, labelled demo barcode to existing pending preparation records without claiming a fingerprint was captured.

## Policy decisions and plan

Keep real status Pending capture. Generate a separate DEMO-prefixed 20-digit random identifier server-side, unique in the database and stable on retry. Administrator-only, online-only, pending-consent requests only. Do not add barcode authentication, player matching or attendance writes.

## Work performed

- Sports Biometric Enrollment: added read-only unique demo_reference and generation actor/time fields. Existing preparation/consent metadata unchanged; no captured/enrolled state or templates.
- `biometric_preparation.demo_capture`: native write permission, administrator/player/Company guards and row lock; reject withdrawn records. First call saves random reference and audit comment; unchanged retry returns the same code without another write/audit. Once set, controller forbids editing/removing the code/audit metadata. Withdrawal retains historical code.
- Directory/history responses include the separate demo reference. App shows Demo captured (simulated) in the player list, while real status stays Pending capture. Selected active request renders CODE128 graphic and explicit simulation notice; withdrawn history labels the code withdrawn and does not render an active barcode.
- Added pinned local renderer `jsbarcode` 3.12.3 and lockfile, using SVG. No external CDN/runtime request, scanner/SDK, biometric data or financial calls.
- Updated requirement/PRD/story/guide and this indexed build log.

## Commands and observations

- npm registry version check and primary JsBarcode documentation reviewed for SVG/CODE128 rendering. Installed pinned dependency; production Next build passed with 20 public shell assets.
- Python unittest discovery: **130 tests passed**, including stable code generation, unchanged real status, single write/audit on retry and withdrawn rejection.
- Loaded only simulation fields into the existing development DocType with reload_doc; no full migration, roles or other app schemas changed.
- Native rollback fixture: generated properly formatted random code, repeated calls returned it with unchanged modified timestamp, list reflected it while real status remained Pending capture, withdrawal blocked further simulation, Guest denied. All temporary metadata/player/attendance/Customer/invoice/Payment Entry counts restored; no real demo records retained.
- Extended real-export browser fixture at 1440/390px: clicked demo capture, verified CODE128 SVG bars/reference, simulated list badge and unchanged underlying status; existing withdrawal/consent, offline, session and privacy tests passed. Browser APIs synthetic.
- Published development version `eca142ea9b201015`, restarted development web workers only. No ERP Boost edits.
- `git diff --check` passed. Physical scanner decoding was not tested; this is a standard-format graphical demo barcode, not a hardware integration claim.

## Verification evidence

| Criterion | Check | Result |
|---|---|---|
| Random stable reference / no false capture | Native format and repeat/no-op checks; unit test | Passed |
| Scope and withdrawn denial | Existing admin/Company/native controls; native Guest/withdraw checks | Passed changed scope |
| Display and demo labelling | Desktop/phone real-export SVG and list-badge checks | Passed |
| No attendance/finance changes | Native fixture rollback/count restoration; no new ingestion endpoint | Passed |

## Decisions, deviations and recovery

Reference is intentionally identifiable as DEMO and is not an authentication secret. No raw fingerprint or fake template was created. Status separates demo completion from actual capture; withdrawn codes cannot be recaptured. No regeneration action exists. Existing browser/DB fixtures cleaned up; temporary records rolled back, generated schema retained.

## Remaining work and release impact

Refresh/reopen the attendance app → Fingerprint registration → View / prepare a pending request → Demo capture — generate barcode. No attendance is recorded by generating or scanning the code. Real biometric capture/matching and any future barcode check-in require separate implementation and validation. Deploy added fields via migration/reload and rebuild/publish frontend elsewhere.
