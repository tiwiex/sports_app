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
