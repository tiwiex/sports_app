# Build log: administrator-only player ID correction

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: sports_app:US-003-02 and migration preparation US-008-03 / EPIC-003/008
- Requirements: SPORTS-FR-004/024; SPORTS-NFR-003
- Affected app / branch: Sports App / story/us-003-01-enrollment-image-and-invoice-acceptance
- Pull requests: Not opened for this refinement.
- Status: Verified on development

## Intended outcome and starting context

User explicitly approved an audited administrator-only Change Player ID action after discussing import-first setup. Earlier blanket immutability is superseded only for this narrow service; ordinary rename and merges remain prohibited.

## Policy decisions and plan

Check management capability, native Player write access, configured Company, fresh modified revision, safe ID syntax and unused/non-retired target. Use native link/attachment rename with standard write checks, controlled by a server ContextVar rather than client flags. Require reason and UUID request key. Preserve Customer/User/guardian/accounting identities. Keep a read-only Sports Player ID Change record; old/new Data fields retain historical text across later corrections, current Player Link follows the identity.

## Work performed

- Added transactional correction service, strict controller rename gate, append-only audit DocType and retired-ID checks in new-player validation. Reserve matching old/new suffixes through existing Company counter without resetting it.
- Native rename updates Links/Dynamic Links/attachments. Repair derived attendance identities and modification versions. Lock sessions/rows before native link updates; enrollment and fingerprint-preparation writes serialize using the existing settings lock. No attendance result/consent/demo/financial state is changed.
- Added shared Sports dialog and entry points in player reference menu, profile and native Player form; server capability flags drive visibility. History link in the profile opens native protected audit list. Generic Boost remains untouched.
- Added permission/input/retry/context/audit/rollback/lock-order unit checks and extended actual-source desktop/phone browser fixture.
- Updated agent guardrail, requirements, PRD, stories and player guide to record the user-authorized exception and offline implications.

## Commands and observations

- Final full Sports suite: 179 tests passed, including retired automatic candidate skipping after prefix/date changes.
- Actual Players/dialog source in Chromium passed at 1440/390px including correction request/revision/reason and changed profile refresh; controls/API are synthetic.
- Final pinned formatting/lint checks passed for all affected runtime/test files, including new untracked files explicitly.
- Final Frappe Semgrep scanned eight runtime Python/JS files with zero findings.
- Synchronized only the new Sports Player ID Change metadata on Moyours development; no actual player IDs changed.

- Final native rollback QA passed through real registration, session/roster, fingerprint preparation, nomination and private remote attachment metadata. Native correction preserved account IDs and updated all tested links; attendance hash/version repaired; stale offline status change rejected; structured audit actor/reason retained; same-request retry produced one record; direct native rename, retired-ID reuse and audit edit denied.
- Injected failure after native rename rolled the player, enrollment, attendance identity and audit state back. Commit was blocked during QA; original Player/Enrollment/Session/Attendance/Biometric/Opportunity/Customer/Contact/User/Invoice/Payment/File/audit counts restored afterward. No test sessions/login credentials were created and no financial documents were posted.
- Search rebuild is explicitly queued after commit; failed operations discard scoped callbacks. No pre-commit global-search job is enqueued by native rename. Old/new numeric suffixes are reserved case-insensitively; automatic allocation skips retired IDs even if a future prefix/date combination reaches one.
- Browser fixture also exercised the actual native Player form refresh handler: authorized button present, capability denial hides it. Browser controls/API remain synthetic; native integration uses direct server services.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Management, scope, stale/duplicate and direct-native/merge guards | Unit suite | Passed |
| Transaction, audit, safe retry and counter/link safety | Real Frappe services/native rename with guarded commits and rollback | Passed |
| Responsive menu/profile correction | Actual-source desktop/phone fixture | Passed |
| Final pinned/static checks | Pinned hooks, Semgrep and 179 Python tests | Passed |

## Decisions, deviations and recovery

The installed public frappe.rename_doc wrapper does not expose ignore_permissions; use its supported signature, which retains native write-permission checks. Native integration first found an invalid synthetic consent choice; corrected the QA fixture to Parent / Guardian. All failed QA attempts rolled back their temporary records. No permanent real-player correction was attempted.

## Remaining work and release impact

Native link/audit/offline/rollback checks completed. Sports assets published/verified and development cache cleared; only the development web process restarted successfully. Reload open console tabs. New audit metadata must be synchronized before runtime code elsewhere. No live Boost edits, production deployment, commits/merges, real roster changes or financial posting. Offline caches are not rewritten remotely; operators must refresh rosters and preserve pending work for conflict review. Raw biometric capture/device integration remains separate scope.
