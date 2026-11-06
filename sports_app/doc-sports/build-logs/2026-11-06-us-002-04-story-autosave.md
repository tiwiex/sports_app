# Build log: Story dropdown autosave and label cleanup

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-002-04 / EPIC-002
- Requirements: SPORTS-FR-028, SPORTS-NFR-006
- App / branch: Sports App / `story/us-007-01-fingerprint-preparation`
- Asset: `development_tools.94ed8af9fb4a53ff.js`
- Pull requests: None; no commit, merge or push requested
- Status: Verified development interaction adjustment

## Intended outcome and starting context

User requested automatic saving on dropdown selection, no Save buttons and no redundant MoSCoW text above dropdowns. Prior layout required an explicit Save and repeated priority as a badge above its selector.

## Policy decisions and plan

Trigger the existing protected, revision-checked, audited update service on each changed selection. Preserve colour distinction, accessible labels, table heading and Mark Done. No backend, permission or persistence-model change.

## Work performed

- Status and MoSCoW selections autosave in both the table and reader. Controls disable during a request to prevent overlapping edits; unchanged selections remain no-ops.
- Removed Save buttons, repeated priority badges inside rows and visible MoSCoW label above reader dropdowns. The table heading, accessible selector names, coloured dropdowns and legend remain.
- Failed saves restore the last confirmed status/priority and priority colour, with visible reopen/retry guidance. Success refreshes list/reader from the existing service; Mark Done still works.
- Updated guide, requirement refinement, story and indexed adjustment evidence. Review notes should be entered before making the autosaved change.

## Commands and observations

- Extended desktop/phone Chromium fixture passed at 1440/390px: priority selections persist without button clicks, table status selection autosaves, reader priority autosaves, no Save button, no row priority badge, reader priority label visually hidden but accessible, four selector colours, failed status change restores confirmed selection, Mark Done and synchronized row colour remain functional.
- Synthetic API fixture only; no actual story or ERP record changed. Browser contexts closed normally.
- JS syntax and `git diff --check` passed. Backend unchanged; previous backend regression evidence remains applicable.
- Published hashed console asset and verified HTTPS bytes match source on Moyours development. No migration/restart required.

## Verification evidence

| Criterion | Check / artifact | Result |
|---|---|---|
| Autosave from list and reader | Browser selection / fixture persistence assertions | Passed |
| No Save or redundant priority text | DOM/visibility assertions; [desktop table](assets/2026-11-06-story-table-autosave-1440.png) | Passed |
| Responsive reader / coloured priority | [Phone reader](assets/2026-11-06-story-tracking-autosave-390.png), colour assertions | Passed |
| Safe failed autosave / quick completion | Failure restoration, Mark Done and list refresh checks | Passed |

## Decisions, deviations and recovery

No role/schema/backend/business-data or real backlog-state changes. No QA accounts or cleanup needed. Existing review audit and file safeguards retained; unrelated pending work and historical assets/logs preserved.

## Remaining work and release impact

Refresh Sports Development Tools to load the new asset. Changes persist immediately on selection; editing the optional note alone does not save a story. No production deployment, commit or push performed.
