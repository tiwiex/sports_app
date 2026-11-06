# Build log: central player record and protected linked histories

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: sports_app:US-003-03 / EPIC-003
- Requirements: SPORTS-FR-005; SPORTS-NFR-005/007; questionnaire BA-QNR-001 Q02-03/04/05 and Q06-02
- App / branch: Sports App / story/us-003-03-central-player-record
- Pull requests: None for this work yet.
- Status: Verified development slice; whole story remains In progress

## Intended outcome and starting context

User approved the next Sports-only central profile implementation after merging enrollment/identity refinements. Existing profile has memberships/contact details but not full histories. Shared Boost must not be edited without prior explicit approval; this work changes only Sports.

## Policy decisions and plan

Keep existing player/profile identity and enrollment actions. Add independently paginated permission-scoped invoices, receipts, attendance and management-only fingerprint preparation; use native ERPNext balances grouped by currency, never convert or hardcode currency. No accounting actions or biometric capture. Add optional preferred foot and append-only dated height(cm)/weight(kg) measurements. Supporting documents are private, management-only, attached to their own protected Sports record, not a broadly readable Player. Native permission/Company checks apply to lists, direct writes and file downloads; no new core finance rights.

## Work performed

- Added `player_profile.py` for permission-scoped overview, currency-separated submitted-invoice outstanding, independently paginated native source histories, preferred-foot revision checks and append-only measurement creation. All lists use native permissions and configured Company/player/account scope; no finance posting APIs or grants.
- Added `player_documents.py` and two prefixed DocTypes: **Sports Player Measurement** and **Sports Player Document**. Management-only supporting files use protected private parents, native read/write/Company checks and narrow server-owned File insertion. Stable UUID/payload hashes make unchanged retries idempotent and reject changed requests.
- Documents auto-submit as immutable archives with `protect_attached_files`; this is an internal document lifecycle, not a financial workflow. Added pre-validation File guards for privacy/attachment changes and a File-list condition based on native permitted document parents. Unrelated attachments retain native behavior.
- Added Sports-owned `player_profile.js` to the Players provider assets and integrated it into the existing modal, including independent pagination, nested-dialog cleanup, native links, role-restricted sections, private file picker and responsive tables. Public enrollment is unchanged.
- Extended Sports Player with optional preferred foot. Updated requirements, PRD, guide, story, backlog/epic inventory and reconciliation provenance. Wider scholarship decisions, injury absence rules, returning-player undertakings and parent portal remain outside this slice.

## Commands and observations

- Starting checkout: clean Sports `develop` after PR #2 at `9c8efed1ee28ce6f3afacc9978be94e8e4f8fa10`; new branch `story/us-003-03-central-player-record`.
- `env/bin/python -m unittest discover -s sports_app/tests -p 'test_*.py'`: **196 passed** (179 prior + 17 profile checks).
- `test_central_profile_browser.cjs` and `test_players_browser.cjs`: passed actual-source Chromium fixtures at desktop/phone widths; APIs/Dialogs are synthetic, not authenticated end-to-end site testing.
- Pinned pre-commit checks: syntax/JSON/imports/Ruff/format/Prettier/ESLint passed, explicitly including untracked feature files. Frappe Semgrep rules: **0 findings**. Mechanical constructor/format findings were corrected before final passes.
- Development native scripts `/tmp/sports-central-profile-schema.py` and `/tmp/sports-central-profile-qa.py`: synchronized only Sports metadata, then verified real Frappe controllers/permissions under blocked commits and rolled back test fixtures. Authorized native roles used disabled, no-password QA accounts, no mail/invitations/sessions.
- At approximately 75 provisional players, five combined list/overview/attendance/measurement reads measured median **88.0 ms**, maximum **96.4 ms**. This is a native server sample, not HTTP/browser p95 or production performance certification. Initial normal fixture creation reached Frappe's interactive User-creation throttle; the complete attempt rolled back. The successful bulk sample used native Importer under its intended request-local import flags; no persistent throttle/configuration changes.
- A final small native run after attachment hardening confirmed private file deletion/public-move attempts are denied for management and Administrator **before bytes disappear**, with native File lists/direct reads denied for nonmanagement.
- Published immutable Sports assets and checked provider asset files, cleared only development cache and restarted only `frappe-bench-dev-web:frappe-bench-dev-frappe-web`. Live services were untouched.
- HTTPS smoke check: content-addressed profile asset returned 200 and matched source; unauthenticated profile API returned 403. Updated Markdown relative links verified.
- Boost worktrees remain clean and unchanged: development `899afa62964927468bba6372254d7946bd5d27be`; live `30aba92a8c6ea5433d04223813833c30fa32648b`.

## Verification evidence

| Criterion | Check / artifact | Result |
|---|---|---|
| AC-2/3/4: scoped histories and finance privacy | Unit filters/field checks + native Sports/mixed/management/Guest access | Passed; no finance rights granted. Existing native Accounts User configuration lacks Sales Invoice read on this site; respected rather than repaired. |
| AC-5/6: measurements, preferences and private files | Native stale revision, unchanged/changed retry, immutable history, private parent/File denial; unit invalid numbers/date/PDF checks | Passed; archive files retained after denied deletion/public conversion. |
| AC-1/2: desktop/phone and modal lifecycle | Both actual-source browser fixtures | Passed; list/search retained, currency separation and independent pagination, no restricted requests/URLs or outer overflow. |
| AC-3: pilot-volume native latency | 75 provisional players; five combined read samples | Median 88.0 ms / max 96.4 ms; all fixtures rolled back. |

## Decisions, deviations and recovery

No Boost code or role changes. Financial reads use native roles, User Permissions, Company and field permissions. Restricted records must not leak totals, content or file URLs. A controller `File.on_trash` hook would run after Frappe physically removes a file; it was replaced before release by native submitted-parent attachment protection. Supporting archive submission has no invoice/payment effect. Files remain audit-retained in this prototype until an approved retention process is defined.

Guaranteed rollback compared before/after counts for Player, Enrollment, Session, Attendance, Biometric Enrollment, Measurement, Document, Customer, Contact, User, Sales Invoice, Payment Entry and File; counts restored. QA user caches cleared and physical private test files absent after cleanup. No real players edited, no persistent QA accounts, no mail or financial postings. General concurrent writer serialization reuses the existing settings/Player locks; verification covers retries and stale revision, not a parallel load test.

## Remaining work and release impact

Development is ready for review at **Sports → Players → Player ID → View** on `moyours.ideltatech.com`. Reload the console to get the new immutable provider manifest. Two new Sports DocTypes and the preferred-foot field were synchronized on this site; later releases require normal Sports migration and asset publication.

Whole US-003-03 remains In progress for expanded injury/absence, returning-player and final retention policy scope. No production deployment, actual document imports, real player changes, commits or merges. Changes remain reviewable on the new Sports branch. Sensitive document retention and operational sign-off are required before production use; no newly imposed approval flow or Boost change.
