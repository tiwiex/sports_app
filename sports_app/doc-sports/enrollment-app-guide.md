# Withdrawn enrollment app prototype

**Withdrawn on 3 November 2026.** Enrollment remains in the original [HTML academy website](https://moyours.ideltatech.com/academy). The instructions below describe the retired prototype only. Next.js is intended for attendance. See the [reversal log](build-logs/2026-11-03-us-001-04-revert-enrollment-pwa.md).


Open [Enrollment app](https://moyours.ideltatech.com/sports-enroll) on the development site. This uncached entry redirects to the current version of the static frontend. The existing academy website and Boost staff console remain available.

1. Start enrollment or resume a draft saved on this device.
2. Choose a pathway and complete player/guardian/emergency details. Record only supplied consent choices. Each new player requires a unique email.
3. Optionally choose **Save draft on this device**. Saving includes personal, contact and medical details; avoid shared devices. **Clear saved draft** removes it. Drafts expire after seven days when accessed. Initial online loading is required before offline form use.
4. With internet access, choose **Make Payment**. The server creates the application and draft invoice and returns the reference, fees and bank instructions. Use that invoice number in the transfer narration.
5. After transferring, choose **I’ve made payment**. This requests Finance review; it does not confirm bank clearance or admission. Staff use the existing Boost finance/admission workflows.
6. Keep the reference, then choose **Finish & clear this tab**. Tab recovery holds the pending submission details until successful preparation; afterward only its token/reference/payment instructions remain until finishing.

If a network failure leaves the result uncertain, details are locked. Retry the same request; it retains its identity after reload. A known validation failure permits corrections. Browser storage must be available to preserve retry identity. Do not clear storage while a request outcome is uncertain; contact the academy with any known reference.

The browser may offer **Install enrollment app**. Installation availability depends on browser/platform. Offline support currently covers form preparation/device drafts only. No offline server submission, invoice numbering or account creation is promised. Closing a tab/clearing browser data can remove recovery information; browser storage is not guaranteed durable storage.

Biometrics are not implemented in this slice. Staff can already mark attendance in Boost without a scanner. A future QR flow could avoid biometric hardware; shared-device thumb identification requires selecting and validating a suitable scanner/terminal integration. Phone passkeys authenticate a device credential and do not expose fingerprints to Sports App.

Developer build/run instructions live in `sports_app/enrollment_app/README.md`. Rebuild/publish the static export after frontend changes; migration does not compile it.

## Enrollment review refinement (6 November 2026)

The HTML form now offers an optional private player photograph (JPEG/PNG/WebP, 2 MB maximum). New application references follow SPORTS-APP-YYYY-#####; the invoice number remains the bank transfer narration. Existing references are retained.

Make Payment prepares a draft invoice. I've made payment requests Pending Review without posting funds. The Enrollments table displays Invoice and Invoice workflow. After independently verifying the bank transfer, a reviewer with admission and Finance/Boost approval permissions selects Accept enrollment, checks the program/group/start/status and confirms **Accept and confirm payment**. The invoice and allocated receipt are submitted together with player admission. Failed acceptance rolls everything back; a retry does not duplicate payment. Unclaimed drafts cannot be accepted. Rejection remains separate and posts nothing. Previously accepted applications are not automatically charged again.

[Build evidence](build-logs/2026-11-06-us-003-01-enrollment-image-and-invoice-acceptance.md).

## Configurable enrollment references — 6 November 2026

Academy Settings exposes **Enrollment naming series**, default `MSA-ENR-.YYYY.-.#####` (example `MSA-ENR-2026-00001`). A literal uppercase prefix, optional year and 4–10 counter digits are supported, for example `CLUB-ENR-.######`. This supersedes the earlier fixed `SPORTS-APP-YYYY-#####` choice. Only new enrollment applications use the configured series; existing application references, accepted program membership IDs, player IDs and invoice transfer references remain unchanged. Native Frappe series counters allocate references. [Build evidence](build-logs/2026-11-06-us-003-01-configurable-enrollment-series.md).

## Confirmed player numbering and public age rule — 6 November 2026

User clarification confirms BA-QNR-001-Q02-07/Q02-08: **MSA + two-digit creation year + hyphen + two-digit creation month + continuous serial**, e.g. `MSA26-08005` followed by `MSA26-09006`. The sequence also continues across year boundaries. The backend uses the academy timezone and a locked Company-scoped counter whose key excludes month, year, editable prefix and application series. Minimum sequence width defaults to three digits and expands naturally; prefix/width remain management settings. On first initialization, seed after the highest existing matching player reference in that Company. Existing prototype IDs of another format stay unchanged and are not interpreted as legacy serials. Existing IDs are immutable; no identity, Customer or finance references are renamed.

The player reference is independent of the configurable **enrollment application** series (`MSA-ENR-.YYYY.-.#####`), accepted Sports Enrollment membership IDs and ERPNext invoice numbering. Current development player defaults are MSA / 3 digits. This supersedes the old prefix-plus-counter-only player ID format for new players.

Public HTML enrollment accepts ages **4 through 18 inclusive**, calculated from calendar birthdays against the academy-local date. Show an inline age error and enforce date bounds in the browser; reject invalid ages in the server-owned public application controller before creating a successful application/invoice. Under-4, 19-or-older and future DOBs are rejected. A February 29 birthday reaches the next age on March 1 in a non-leap year. Enforce on new applications/DOB corrections, without retroactively blocking unchanged historical applications or imposing this public intake policy on ordinary updates to existing player records. Private staff intake policy is not broadened by this web-form refinement.

Provenance: numbering is **Both** (baseline plus questionnaire, now user-confirmed); the explicit 4–18 public restriction is user direction informed by the supplied web-form screenshot, not a claim that the questionnaire stated those exact limits.

[Build evidence](build-logs/2026-11-06-us-003-02-player-series-and-public-age-policy.md).

## Player email preflight and shared guardian identity — 6 November 2026

User refinement: a player email must be unique before public enrollment is submitted, not only when staff accepts it. Normalize player email; reject addresses already used by a User (including email-field aliases such as Administrator), Sports Player or another Pending Sports Registration. Rejected applications release their pending reservation. Browser preflight runs on leaving the player-email field and again before Make Payment/Submit, returning only availability; server validation remains authoritative under the existing settings lock. Preserve token-bound unchanged retries. Show a specific inline error and retain entered details. Review older applications again before financial completion, so a known conflicting email does not start the posting process.

At authorized acceptance/direct player registration, create the player's separate disabled Website User and create or reuse the guardian User. A server-owned **guardian_user** link on Sports Player supports many players to one guardian. Siblings retain separate player emails, Users, Customers and enrollment/finance histories. Player and guardian email on one form must differ. New guardian accounts are disabled Website Users without Desk roles or welcome mail; existing guardian accounts retain their original type, enabled state, roles and profile. Guardian email repetition is permitted; it never becomes a shared payer Customer. Account creation/linkage participates in the same admission transaction and rolls back on failure.

A supplied guardian email is an unverified identity reference, not proof of guardianship or permission to access children. This change does not activate accounts, grant guardian portal permissions, send invitations or implement the parent portal. Existing records are not bulk-backfilled or automatically merged; existing duplicate applications require staff/Finance correction. This user-approved account preparation refines the earlier player-only provisioning decision while leaving portal activation/access as separate scope.

[Build evidence](build-logs/2026-11-06-us-003-01-email-preflight-and-guardian-users.md).
