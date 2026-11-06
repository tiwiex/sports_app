# Build log: Next.js attendance app with offline manual queue

- Date: 2026-11-03 (Africa/Lagos)
- Story / epic: US-006-04 / EPIC-006; related US-006-01/02
- Requirements: SPORTS-FR-014/015/036, SPORTS-NFR-004/006
- Affected apps / branches / versions: Sports App, `story/us-006-04-attendance-pwa`, based on `a9aabf8`; Next.js 16.4.5, React 19.3.1, isolated Node 22 runtime. Existing enrollment reversal preserved.
- Pull requests: None. New work uncommitted; no merge/push or live Boost changes.
- Status: Verified first development prototype; field/production acceptance remains open

## Intended outcome and starting context

User clarified Next.js is for attendance, with enrollment retained as HTML, then authorized proceeding. Existing Sports Session/Attendance services already provide roster snapshots, native role/Company checks, transaction rollback, conflict detection, explicit finalization and auditable corrections. Reuse that backend instead of introducing a second attendance ledger.

## Policy decisions and plan

Build a Sports-owned static Next.js PWA on the Frappe origin. Staff explicitly enable a trusted device and download selected rosters before offline marking. Persist local intent before showing success; synchronize only on explicit request under the original account/company. Keep conflicts pending for review and never infer absence from an unsynced/unmarked player. Session creation, cancellation and finalization stay in Boost. Biometrics, QR and coach assignment scope are separate future work.

## Work performed

- `attendance_app/`: independent pinned frontend package/lockfile, responsive session cards, downloaded roster, player name/ID search, status/pending filter, provisional counts, Present/Late/Absent/Excused choices, correction reason and explicit sync/review controls.
- IndexedDB stores minimal user/company-scoped roster snapshots and intent queue with original server status/version, UUID and local capture timestamp. No passwords, CSRF tokens, medical/guardian/contact details or biometric templates enter device storage.
- Offline identity expires seven days after online verification; offline marking never extends it. Pending intents are retained. Forget-device rejects unresolved intents and removes only the current account/company's state.
- Sync requests refresh bootstrap/CSRF and compare the current account/company before posting. Existing native service owns validation/audit; same-result retries are no-ops. Failed batches retain intents and persistent review messages. Explicit reviewed corrections rebase to downloaded server version and require a reason. Queue acknowledgments compare UUIDs before deletion; Web Locks coordinate sync tabs where available.
- `attendance_mobile_api.py`: narrow no-store bootstrap; Guest receives authenticated=false only. Authorized staff require existing Sports role and configured Company access.
- `attendance_api.roster`: advisory can_mark capability checks session/attendance write rights, cancellation and academy-local date. Server save guards remain authoritative for each row.
- `www/sports-attendance.html` / `sports_attendance.py`: uncached versioned static entry at `/sports-attendance`. Service worker caches only the public shell/static assets inside its narrow scope; APIs never enter Cache Storage.
- `public/js/attendance.js`: Open attendance app link from the existing console toolbar. Source and build scripts live in Sports App; no Boost dependency or new Node service.
- Updated PRD, requirement baseline, EPIC-006, related story, usage guides and this indexed build evidence. No new DocTypes, schema, roles, accounting transactions or enrollment logic.

## Commands and observations

- `npm ci`, `npm run build`: production Next static export passed using the isolated Node runtime; shell prepared with 19 public JS/CSS assets. No bench/system Node runtime changed.
- Published development HTML version `d8bfedeb2bd68fec`; attendance console asset `attendance.9d32cc06e94f839d.js`. Cleared development cache and restarted development web workers only.
- Python unittest discovery: 120 tests passed, including new Guest/staff/bootstrap role/Company/privacy checks and roster capability cases for write denial, cancellation and future dates.
- New real-export Chromium fixture at 1440/390px: trusted roster download, actual IndexedDB/worker, offline mark/reload, player filtering, explicit sync, server-applied/lost-response retry without a duplicate mark, concurrent correction and review after reload, wrong-account/no-POST, permission denial with retained queue, storage failure without a false save, no persisted CSRF/API-cache entries, Guest sign-in and forget-device protection all passed. Synthetic API records only.
- Existing console attendance browser fixture passed at desktop/phone after adding the new app link: create, roster/save/finalization/correction/cancel and cleanup unchanged.
- Native Moyours rollback fixture: temporary session created through the real API using configured program and eligible roster. Advisory can_mark=true; real first mark and repeated old-version same-result request preserved modified timestamp (no duplicate update). Rolled back, then verified original counts for sessions, attendance, players, Customers, invoices and Payment Entries. Guest bootstrap returned no private data and Guest list access was denied. CLI bootstrap token alone was stubbed because a CLI context has no browser session object; native roles/data/services remained real.
- Published HTTPS browser checks at both widths passed friendly route, real Guest bootstrap/no-store headers, worker installation and offline public-shell reopening. No actual public/staff enrollment or payment submission.
- Existing HTML academy HTML/controller/JS/CSS, application API and invoice/payment services match `git show HEAD:<path>` byte-for-byte. `node --check` for console JS and `git diff --check` passed.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| AC-1 private staff data and native permissions | Bootstrap tests, Guest HTTPS, native role/Company services | Passed changed scope; full native browser role matrix remains pilot work |
| AC-2 trusted device/minimal cache | Explicit enablement, minimal roster allowlist, token/cache privacy and fixed verification timestamp | Passed design/fixture checks |
| AC-3 durable offline intent | Actual worker/IndexedDB offline reload and marking tests | Passed |
| AC-4 safe explicit sync | Same-result retry fixture/native no-op, wrong-account preflight, versioned service saves | Passed; UUID acknowledgment guard implemented, full multi-device field testing pending |
| AC-5 reviewed conflicts | Concurrent server change, reload-retained review state and reasoned rebase | Passed |
| AC-6 responsive/storage/enrollment preservation | [Desktop](assets/2026-11-03-attendance-app-1440.png), [Phone](assets/2026-11-03-attendance-app-390.png); storage-failure test and baseline comparison | Passed prototype checks |

## Decisions, deviations and recovery

Browser API responses were synthetic to avoid changing academy attendance for presentation tests. A separate native temporary session exercised real roster/save/retry and was fully rolled back. No QA accounts were required. CLI bootstrap initially lacked a browser session object; test-only token stub resolved that harness limitation. A browser fixture initially matched an empty transient alert before the save finished; it now waits for the specific completed failure response. Durable sync review messages were added so conflicts remain visible after reload.

Browser capture time is local metadata, not verified scan time. Server audit actor/time/source reflect the authenticated manual sync operation. A physical/browser user on a trusted device can access its local data; no encryption or remote wipe is claimed. Offline permissions may be stale until reconnection. Browser eviction/clear-data can lose unsynced work; sync promptly.

## Remaining work and release impact

Development URL: https://moyours.ideltatech.com/sports-attendance . Sign in, create a session in Boost if needed, enable a trusted device, download a roster, then mark and sync. No persistent demo session was left behind. Rebuild/publish static frontend as part of deployment; Frappe migration alone does not compile Next.js. Native database/schema is unchanged.

The broader story remains In progress: managed kiosk/device provisioning, encryption/recovery/retention policy, coach-assigned-group authorization, multi-device field trials, platform installation/accessibility/performance testing and production acceptance remain open. No biometric enrollment/scanner or QR attendance was implemented. Enrollment remains HTML and finance behavior is unchanged.
