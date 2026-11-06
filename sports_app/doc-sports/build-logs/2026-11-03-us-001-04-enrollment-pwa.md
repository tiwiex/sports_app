# Build log: Dedicated Next.js enrollment prototype

- Date: 2026-11-03 (Africa/Lagos)
- Story / epic: US-001-04 / EPIC-001; related US-003-01 and US-005-01
- Requirements: SPORTS-FR-003, SPORTS-FR-030, SPORTS-FR-035, SPORTS-NFR-006
- Affected apps / branches / versions: Sports App; `story/us-001-04-enrollment-pwa`; Next.js 16.4.5, React/React DOM 19.3.1, isolated Node 22 runtime. Existing Frappe/ERPNext/Boost unchanged.
- Pull requests: None. Prior pending Sports work committed as `a9aabf8` before starting this branch. No merge/push requested or performed; new PWA work remains uncommitted for review.
- Status: Historical verified prototype; withdrawn at user request on 2026-11-03. See [reversal log](2026-11-03-us-001-04-revert-enrollment-pwa.md).

## Intended outcome and starting context

User requested committing existing work and commencing a Next.js enrollment app, with clarification about whether phone fingerprint hardware replaces an external device. Existing shared application, invoice and review services already provide the backend. Pharmacy's checked PWA assets supplied architectural reference only; no pharmacy code or dependency was copied.

## Policy decisions and plan

Keep a separately built frontend package inside Sports App, statically hosted on the same Frappe origin. No second backend/ledger, Boost coupling or duplicated admission/account creation logic. First slice: online enrollment and optional offline device drafts. Attendance synchronization and biometric capture are not included. Phone passkeys authenticate a credential without exposing fingerprint data; shared-player thumb identification needs a separately validated scanner/terminal integration. Manual attendance needs no scanner; QR check-in remains a future alternative.

## Work performed

- `enrollment_app/`: pinned Next/React dependencies and lockfile, static export, responsive four-step wizard, app manifest/icon, scoped service worker, prepare/publish scripts and build guide.
- Fields come from the shared registration definitions. Academy name/payment enablement come from settings; pathways come from existing website content. No unchecked consent is silently granted.
- `enrollment_app_api.py`: narrow public bootstrap returning field/pathway configuration and fresh session token. Real `no-store, private` and `Vary: Cookie` response headers; no settings dump, finance records or reviewer emails exposed.
- Make Payment calls existing idempotent invoice service; payment claim calls existing review service. Payment-disabled sites use existing private application submission. No new mutation endpoint.
- Optional localStorage drafts include privacy disclosure, clear control and seven-day expiry on access. Only public configuration is cached automatically without token. Submit payload/key stored in sessionStorage before a mutation; ambiguous failures lock details and retry the same identity after reload. Successful preparation removes retained player payload and device draft. Finish clears tab recovery.
- Worker precaches the public shell and 19 generated JS/CSS files; APIs and submission responses excluded. Worker upgrades retain the existing client until it closes; old hashed chunks are retained by publication.
- `www/sports-enroll.html` / `sports_enroll.py`: uncached temporary redirect to content-versioned static entry, avoiding bench's long-lived static HTML cache. Manifest uses explicit index.html because development Nginx does not serve directory indexes. Worker navigation revalidates HTML; worker registration bypasses its HTTP cache.
- Added dedicated story, requirement baseline/PRD updates and usage guide. No schema migration, roles or finance configuration changed.

## Commands and observations

- Existing suite before commit: 116 tests passed; `git diff --check` passed. Committed existing 82-file Sports change as `a9aabf8`.
- Checked npm registry: Next 16.4.5 requires Node >=20.9. Installed Node 22 under `/tmp/sports-enrollment-runtime`; no bench/system runtime changes. Installed pinned dependencies and generated lockfile.
- `npm run build` with isolated runtime: production static export passed. Prepare script emitted versioned offline shell with 19 assets. `npm run publish`: development export `e384cacc8398256c` published.
- Python unittest discovery: 117 tests passed, including bootstrap allowlist/no-store-header coverage.
- Real-export Chromium fixture at 1440/390px: passed first-visit offline shell reload, device draft restore, offline-submit disabling, ambiguous 503 retry identity, tab reload recovery, invoice/reference rendering, review claim, PII cleanup, no API Cache Storage entries and no page overflow/errors.
- HTTPS read-only checks: actual bootstrap 200 with no-store headers; correct allowlisted keys; all 19 public shell assets available. Moyours browser checks passed friendly redirect, real bootstrap, worker installation and offline form reload at both widths. No actual enrollment/invoice/payment submissions.
- Restarted development web workers for the new bootstrap and cleared development cache for new www route. No live bench/service edits.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| AC-1 shared fields and consent | Actual field JSON in browser fixture, required controls, unchecked consents | Passed |
| AC-2 offline drafts | First online visit then offline reload; save/restore and disabled final submit | Passed |
| AC-3 existing financial API/retries | Synthetic API transport with ambiguous 503; UUID stable after reload; Pending Review claim | Passed fixture; unchanged server finance behavior remains covered by existing suite |
| AC-4 token/data caching | Python response allowlist/no-store; token excluded from persisted configuration; no API entries in worker caches | Passed |
| AC-5 responsive release | [Desktop](assets/2026-11-03-enrollment-app-1440.png), [Phone](assets/2026-11-03-enrollment-app-390.png); HTTPS checks on Moyours | Passed; screenshots use synthetic data |

## Decisions, deviations and recovery

Publication checks found static directory URLs return 404 and the first redirect controller used a hyphenated filename, which Frappe does not load. Corrected the manifest/worker to index.html, added content-versioned entry and renamed the Python controller to underscores; repeated actual entry/offline checks passed. Precaching generated chunks makes cold offline reload possible after the first worker installation, rather than relying on a prior controlled reload.

No QA accounts or persistent business records created. Browser contexts isolated/closed; synthetic data only. Build artifacts remain ignored; source/lockfile/scripts are reviewable. Offline browser storage is neither encrypted storage nor a guaranteed backup.

## Remaining work and release impact

Development entry: https://moyours.ideltatech.com/sports-enroll . Existing academy website and staff console retained. Rebuild/publish frontend when deploying source; migration does not compile Next.js. Only the new public bootstrap/entry controller needs normal Python code rollout.

Broader browser/device installation/accessibility, retention/managed-device policy, CMS branding and production hardening remain future work. No proof-file upload, phone fingerprint login, biometric enrollment, offline server submission or offline attendance synchronization was implemented or claimed. Real finance posting was deliberately not exercised against academy data for this UI slice.
