# Build log: Sports story status, MoSCoW and quick completion

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-002-04 / EPIC-002
- Requirements: SPORTS-FR-028, SPORTS-NFR-002/004/009
- App / branch: Sports App / `story/us-007-01-fingerprint-preparation`
- Asset: `development_tools.ed1523966b7228a4.js`
- Pull requests: None; no commit, merge or push requested
- Status: Verified development refinement

## Intended outcome and starting context

User requested the editable story status/MoSCoW and quick completion experience visible in Boost. Inspected development Boost's story status API, list controls and Mark Done reader interaction. Sports previously offered protected read-only Markdown documentation without story controls.

## Policy decisions and plan

Keep Sports backlog ownership and authorization in Sports App. The explicit request extends the prior read-only rule only for individual story status/priority metadata; no arbitrary narrative editor, broad requirement editing or finance privilege is added. Mark Done is a human reviewer action, not execution of acceptance tests. Record each actual edit with actor, Lagos timestamp, before/after and optional note; retain source provenance and prior build evidence.

## Work performed

- `story_tracking.py`: allowlisted Sports story paths, current status/priority/origin/revision metadata; recognized legacy Status headers and qualified partial-delivery values. Enumerated MoSCoW and status choices, including Withdrawn.
- `development_api.py`: protected list/reader metadata and POST-only `update_story`, retaining existing management role and path restrictions.
- Serialized edits with a stable local file lock and mandatory SHA-256 revision comparison. Atomic file replacements and handled-error rollback across story, audit/index, epic/master rows and derived state snapshot. Unchanged edits are no-ops. Rejected invalid fields, stale content, unsupported paths and symlink escape.
- Updated primary epic/master rows and delivery-state snapshot in the same locked edit; appended an indexed per-change review build log and story backlink. Preserved original narrative/qualifiers except when status explicitly replaced.
- Sports-owned JS adds Status/MoSCoW/Save and Mark Done to the story list and reader, optional reader review note, in-place list/reader refresh and stale-save feedback. Already Done disables quick completion. Labels and controls wrap on phones.
- Updated guardrails, current requirement/baseline, PRD, story criteria, process and [review guide](../story-review-guide.md). Prior read-only historical logs remain unchanged. No Boost checkout modifications.

## Commands and observations

- Python `test_story_tracking` plus existing `test_development_docs`: 14 tests passed. Includes authorization, allowed paths/values, stale edits, legacy/qualified state preservation, no-op, audit/index synchronization and injected multi-file failure recovery.
- JS syntax check and `git diff --check` passed.
- Chromium fixture passed at 1440/390px using the actual Sports asset and Boost stylesheet: MoSCoW save, qualified status display, reader review note, failed/stale save without false completion, Mark Done, synchronized list and disabled Already Done, modal cleanup and no page-level horizontal overflow. APIs synthetic; no actual story state or business writes.
- Visually inspected phone screenshot. [Desktop](assets/2026-11-06-story-tracking-1440.png), [phone](assets/2026-11-06-story-tracking-390.png).
- Development-site read-only check as Administrator: 33 story metadata records, matching list/reader revisions and POST-only editor registration. DB connection rolled back/destroyed; no story edits made.
- Published content-addressed console assets and restarted only `frappe-bench-dev-web:frappe-bench-dev-frappe-web`; verified HTTPS asset bytes match source on moyours.ideltatech.com. No live bench changes, migration or permission reset.

## Verification evidence

| Criterion | Check | Result |
|---|---|---|
| MoSCoW and status controls in list/reader | Browser fixture at desktop/phone sizes | Passed |
| Complete while reading | Mark Done → Already Done; list/reader refresh | Passed |
| Restricted/audited writes | Backend authorization/path/revision/audit tests | Passed |
| Inventory consistency and failure recovery | Native temporary-file unit fixtures | Passed |
| Development availability | Site metadata and HTTPS hashed asset verification | Passed |

## Decisions, deviations and recovery

No schema, financial/business-data, role or real story-state changes made during verification; test files live only in automatically cleaned temporary directories. No QA accounts created. Stable lock/temp files ignored in doc-sports Git rules. User-authorized narrow editor is the exception to earlier read-only documentation guardrails; it does not expose arbitrary filesystem writes. All unrelated pending work preserved.

## Remaining work and release impact

Refresh the Boost console on Moyours development. Management users can now review Sports stories without opening files manually. Review-generated Markdown remains pending Git work for the usual commit process. Handler rollback covers ordinary write errors; abrupt process/power loss during a multi-file update still requires operational backup/reconciliation. No claim of crash-atomic filesystem transactions or authenticated end-to-end browser editing on real stories. No production release, commit or push performed.
