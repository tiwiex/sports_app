# Build log: tabbed Academy Settings

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-001-01 / EPIC-001
- Requirements: SPORTS-FR-001, SPORTS-NFR-006
- Affected apps / branch: Sports App / story/epic-004-scholarships-and-monthly-billing
- Pull requests: None for this refinement yet.
- Status: Verified development refinement

## Intended outcome and starting context

User requested tabs in Academy Settings after reviewing the player profile and starting EPIC-004. Existing settings are a long FieldGroup followed by program/group lists. Preserve the current settings validation, revision checks and save behavior.

## Policy decisions and plan

Six tabs: General; Player IDs; Enrollment defaults; Monthly fees; Website payments; Programs & groups. Save Settings remains outside the panels and saves all controls. Tab changes must preserve unsaved values; master-list refresh retains the selected tab and unsaved settings. The numbering example belongs in Player IDs.

## Work performed

Added Sports-owned accessible tab/tabpanel navigation to `academy_settings.js`, with selected state, roving focus, arrow/Home/End navigation and a horizontally scrolling phone tab strip. Existing native control wrappers move into the panels while remaining inside the same FieldGroup wrapper, retaining native change/dependency/validation handlers and cross-field queries. No field values or objects are recreated on tab selection. If validation fails on a required field, select its tab before focusing it. Program/group management continues to use the existing dialogs/APIs.

## Commands and observations

- Actual `academy_settings.js` browser fixture passed at 1440px and 390px using synthetic API/native-control wrappers: six tabs, one visible panel, cross-tab unsaved values, original revision in save payload, Player IDs preview, payment-review addresses/monthly-fee/general values saved together, keyboard arrow/Home/End navigation and no outer overflow/page errors.
- Program creation through the existing dialog refreshed the lists while retaining Programs & groups selection and unsaved numbering values. A required-field failure on a hidden tab selected General and made no save request. No real site settings or masters were edited by browser tests.
- Pinned trailing-whitespace/merge-conflict/Prettier/ESLint checks passed. No backend changes, so existing native settings permission/validation tests were not unnecessarily repeated.
- Published Sports immutable assets and cleared only development cache with no Boost import/call, role synchronization or DB commit. HTTPS Academy Settings asset returned 200 and exactly matched source. No service restart or migration needed.
- Updated academy setup guide, requirement/PRD refinement, affected Done story and build-log index. Existing EPIC-004 implementation remains intact.

## Verification evidence

| Acceptance criterion | Check | Result |
|---|---|---|
| Six groups and visible active panel, keyboard and phone layout | Actual-source browser fixture | Passed |
| Preserve numbering/other unsaved values and cross-tab save payload | Actual-source browser fixture | Passed |
| Preserve native settings validation/permissions | No backend/API/schema changes | Unchanged |

## Decisions, deviations and recovery

No Boost changes, host-role synchronization, schema/data/permission changes, financial operations or temporary site accounts. Existing EPIC-004 work remains on this branch and is preserved. Native FieldGroup continues to own controls and validation; tabs are only presentation.

## Remaining work and release impact

Available on Moyours development after reloading the console. Sports immutable assets published and development cache cleared. The existing Done status of US-001-01 is retained with this linked adjustment evidence. No production deployment, commit or merge.
