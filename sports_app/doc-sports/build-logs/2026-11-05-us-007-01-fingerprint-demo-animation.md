# Build log: Decorative fingerprint demo and scanning animation

- Date: 2026-11-05 (Africa/Lagos)
- Story / epic: US-007-01 / EPIC-007
- Requirements: SPORTS-FR-037, SPORTS-NFR-006/007
- Affected apps / branch: Sports App, `story/us-007-01-fingerprint-preparation`; existing pending work preserved
- Pull requests: None; no commit, merge or push
- Status: Verified development visual adjustment

## Intended outcome and starting context

User accepted adding a fingerprint illustration/scanning animation to the dummy capture flow, with simulated completion and the random demo code underneath. Existing backend generates a stable demo barcode but has no real scanner.

## Policy decisions and plan

Use a fixed code-native SVG drawing, identical for every player. Keep a permanent SIMULATED — NO SCANNER label and explicit no-collection explanation. Animate only the demo UI; completion requires the existing server demo request and record refresh. Do not introduce camera/device permissions, random biometric templates, actual capture status or new backend writes.

## Work performed

- Added `attendance_app/app/demo-fingerprint.js`: fixed decorative ridge paths, ready/scanning/complete phases, scan-line overlay, completed check indicator and live status text.
- Fingerprint registration shows the ready preview before Demo capture, disables repeated actions during the request and animates a short simulated scan. Reduced-motion preference removes both moving line and intentional animation delay. Error/uncertain response exits scanning without false success; retry behavior remains the existing backend's stable demo reference.
- Existing DemoBarcode renders the completed illustration above the same barcode/reference. Withdrawn requests continue to show withdrawn history rather than active demo display.
- Scoped responsive styling; no new dependencies, schema, permission or backend code changes. Updated guide, requirements, related story and this indexed log.

## Commands and observations

- Python unittest discovery: 130 tests passed. `git diff --check` passed.
- Next production build passed, with version `9897b7446c79d962` and 20 public assets; published to Moyours development. No web-worker restart or migration required for this frontend-only adjustment.
- Extended real-export Chromium fixture passed at 1440/390px: decorative illustration present, failed demo request never shows completion, retry enters scanning with disabled action, reduced-motion CSS has no animation, then server-confirmed demo completion and original barcode appear. Existing consent/withdrawal/list/session/offline/privacy regressions passed. Browser APIs synthetic; no ERP records written.
- Visually inspected the phone completion screenshot. Published HTTPS entry matches the current static export.

## Verification evidence

| Criterion | Check / artifact | Result |
|---|---|---|
| Scanning/complete illustration | [Phone scan](assets/2026-11-05-demo-fingerprint-scanning-390.png), [Phone completion](assets/2026-11-05-demo-fingerprint-complete-390.png), desktop fixture | Passed |
| Honest success/failure | Simulated 503 then retry; no success before confirmation | Passed |
| Accessibility/motion | Live status, decorative simulation label, reduced-motion computed CSS | Passed changed scope |
| Existing behavior | Barcode/reference, pending real status and broader fixture/unit suite | Passed |

## Decisions, deviations and recovery

The SVG is a decorative asset drawn in source, not an actual or generated player fingerprint. No image generation/capture service is used. There is no persisted fingerprint image and no modification to the demo code, real status or attendance. Tests use isolated synthetic browser contexts; no QA accounts or business records created.

## Remaining work and release impact

Refresh/reopen the Attendance App → Fingerprint registration → View / prepare a pending request → Demo capture. Existing demo-completed requests show the completed illustration automatically. Hardware matching/capture and broader production acceptance remain pending. Rebuild/publish frontend for other environments; no schema migration or ERP Boost changes.
