# Build log: Keep story dropdowns stable during autosave

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-002-04 / EPIC-002
- Requirements: SPORTS-FR-028, SPORTS-NFR-006
- App / branch: Sports App / `story/us-007-01-fingerprint-preparation`
- Asset: `development_tools.4c07249203f97e43.js`
- Pull requests: None; no commit, merge or push requested
- Status: Verified development fix

## Intended outcome and starting context

User reported Status/MoSCoW dropdowns closing before a selection could be made. Code inspection found autosave disabled both selects, then replaced the entire table and reloaded the reader after each response. A response arriving during another selection could detach or disable that control. This is a concrete interruption path; no authenticated reproduction of the user's exact browser session was performed.

## Policy decisions and plan

Keep mounted controls enabled and update only confirmed metadata in place. Serialize consecutive field edits using the revision returned by the prior successful write. Preserve existing authorization, audit, stale-write rejection, failure recovery, colours and Mark Done.

## Work performed

- Replaced save-triggered renderIndex/openDocument calls with in-place editor synchronization; table/reader control nodes and scroll context remain intact.
- Added pending-field queue per editor. Edits made during a request are saved after it using the confirmed revision; only changed/requested fields are sent.
- Selectors stay enabled during requests; Mark Done remains guarded. Focused or pending fields are not overwritten by another editor's save response. Status row colour, button text and document metadata text update without reconstructing the reader.
- Background document discovery refreshes audit-log data without rerendering controls. Failed writes clear pending work, restore confirmed selections and retain reopen guidance. Editor references clean up when detached or unmounted.
- Updated guide, requirement refinement, affected story and build-log index. Backend unchanged.

## Commands and observations

- Extended Chromium fixture passed at desktop/phone widths: delayed saves leave selectors enabled and connected; rapid Could→Should changes produce two serialized writes and retain the final choice; opening Status while those writes finish retains focus. List and reader select nodes remain identical before/after saves.
- Existing autosave, qualified status, colours, failure restoration, Mark Done, adjacent buttons, long viewport, list/reader synchronization and cleanup checks still pass with synthetic APIs. No real story or business writes.
- JS syntax and git diff whitespace checks passed. Backend unchanged, so earlier backend evidence remains applicable.
- Published content-addressed asset; HTTPS bytes match source on Moyours development. No migration, restart or permissions change required.

## Verification evidence

| Criterion | Check | Result |
|---|---|---|
| Control survives delayed autosave | Same-node and enabled-state assertions | Passed |
| Another open dropdown is not replaced | Focus retained while queued saves finish | Passed |
| Consecutive edits persist in order | Delayed synthetic requests and final-value assertions | Passed |
| Existing review safeguards remain | Desktop/phone regression fixture | Passed |

## Decisions, deviations and recovery

No schema, role, backend, actual story-state or business-data changes. No QA accounts/records; browser contexts closed and fixture state discarded. Existing unrelated work and historical assets/logs retained. Requests are serialized per visible editor; concurrent independent reviewers remain protected by server revision checks.

## Remaining work and release impact

Refresh Sports Development Tools on Moyours development. Native dropdown rendering remains browser-controlled, but autosaves no longer remove or disable the control. An explicit refresh/navigation can still replace the current view. No production release, commit or push performed.
