# Sports attendance frontend

Next.js static-export PWA owned by Sports App. Frappe remains the authenticated backend and accounting is untouched. Enrollment remains the HTML academy website.

Use Node 22+ and npm from this directory:

```sh
npm ci
npm run build
npm run publish
```

The export is published to `sports_app/public/attendance`, with content-versioned shell cache and public JS/CSS precaching. Generated assets/dependencies are ignored; source and lockfile are versioned. Keep old hashed chunks for open clients. Migration does not build Next.js; rebuild/publish as a deployment step. No new long-running Node service is required. `/sports-attendance` is the uncached friendly route and redirects to the current static HTML version. Same-origin hosting is required for Frappe session/CSRF controls. Local `next dev` needs a same-origin proxy for the Frappe API.

## Data and authorization

- Public shell/manifest contain no roster data. `attendance_mobile_api.bootstrap` returns no private data/token for Guest, and checks Sports staff + Company access for logged-in users; it sets real `no-store, private` headers.
- Reads/writes use the existing `attendance_api` services. The roster capability is advisory; native session/row permissions, Company scope, dates, cancellation and correction validation remain authoritative on every save.
- App captures manual choices only: Present, Late, Absent, Excused. Unmarked remains Unmarked until staff finalizes in Boost. Online New session uses existing configuration/create_session APIs, friendly program/group controls and a per-user/company tab recovery key. The same creation UUID/payload is retried after an ambiguous response or reload; validation failures unlock corrections. Cancellation/finalization remain in the console.
- Trust-device enablement is explicit. IndexedDB stores a user/company-scoped session snapshot, downloaded roster (names, IDs, status, version only), queued choices/reasons and last verified identity. No passwords, CSRF tokens, medical/contact data or biometric templates are persisted. Local storage is not encrypted by this app.
- Offline identity expires seven days after its last online verification; offline activity never extends it. Pending marks are not automatically deleted. A device with physical/browser access can see local data; use only trusted devices. Revocation can only be checked after reconnecting.
- Every choice is durably queued before showing success. Sync is explicit and rechecks the signed-in account/company using fresh bootstrap/CSRF data. No silent upload or background financial actions.
- Queued choices retain their original server modified value. Batches reuse existing transaction/version checks; retries of the same resulting status are native no-ops. Conflicts/errors remain queued, including after reload. Staff may explicitly discard a local choice with Use server status, or review the current server state and supply a correction reason before rebasing/requeueing. Cancelled/read-only sessions cannot be rebased.
- Queue acknowledgments compare per-intent UUIDs before deletion, preserving a newer edit from another tab. Web Locks coordinate concurrent sync tabs where supported; server version checks remain necessary.
- Browser capture timestamp is local metadata. Server audit/source/actor/time reflect the authenticated manual save at sync time, not a verified offline/device scan time.
- Forget device refuses unresolved marks and removes only this account/company's downloaded data. Changing accounts does not transfer another account's queue. Sign in as the original operator to resolve it. Browser eviction/deleting site data can lose unsynced work; this prototype is not a guaranteed durable kiosk.

## Verification

`tests/js/test_attendance_app_browser.cjs` serves the real export, service worker and IndexedDB with synthetic APIs. It covers desktop/phone, offline reload/mark recovery, retries, conflicts, account changes and permission failure. Python coverage checks bootstrap privacy and roster capabilities; native rollback fixture evidence is in the story build log. Full native browser sign-in/device management, biometric SDKs and production sync hardening remain future work.
