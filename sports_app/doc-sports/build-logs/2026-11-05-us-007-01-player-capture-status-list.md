# Build log: Player list with fingerprint capture preparation status

- Date: 2026-11-05 (Africa/Lagos)
- Story / epic: US-007-01 / EPIC-007
- Requirements: SPORTS-FR-037, SPORTS-NFR-007
- Affected apps / branch: Sports App, `story/us-007-01-fingerprint-preparation`; prior pending work preserved
- Pull requests: None; no commit/merge/push
- Status: Verified development adjustment

## Intended outcome and starting context

User requested a player list showing fingerprint capture status. Previously administrators searched and selected a player before seeing individual request history.

## Policy decisions and plan

Show preparation status accurately: Not prepared if no permitted request exists, otherwise the latest request's Pending capture or Withdrawn. No Captured/Enrolled status is fabricated while hardware is unavailable. Reuse existing administrator-only access and Company/player/document scope; no role changes.

## Work performed

- `biometric_preparation.list_player_statuses`: bounded 20-player pages plus has-more lookahead, name/ID search and stable full_name/name order. Query only the configured Company and permitted players; fetch latest permitted request per returned player in creation/name descending order. Return identity, status, finger, reference and prepared timestamp only, without consent-person/reference details.
- Fingerprint registration dialog loads the directory on open. Table shows name/ID, capture preparation status, finger/request reference and View / prepare. Search and previous/next navigation retained; selected player's identity remains explicit even when changing directory pages. Replaced the redundant player dropdown.
- Preparation/history refresh reloads the directory so pending/withdrawn transitions appear immediately. Phone tables scroll within their wrapper.
- Added latest-status/unprepared-player privacy coverage and extended desktop/phone browser checks. Updated guide, requirement clarification, story and this indexed adjustment log.

## Commands and observations

- Python unittest discovery: 128 tests passed. New test proves latest Pending capture takes precedence over an older Withdrawn request, missing history remains Not prepared, withdrawn-only history is shown and directory payload excludes consent-person details; Company query scope retained.
- Production Next build passed. Real-export browser fixture at 1440/390px passed directory presence, View / prepare selection and immediate Pending capture/Withdrawn row updates, plus existing session/offline/consent/privacy regressions. APIs synthetic; no ERP writes.
- Native read-only Moyours check passed allowed status values, exact narrow payload keys and Guest denial. No player data printed or changed.
- Published development version `18de6bd96e00165c`; restarted development web workers to load the new endpoint. No schema migration, role grants or ERP Boost edits.
- `git diff --check` passed.

## Verification evidence

| Criterion | Check | Result |
|---|---|---|
| Latest status and unprepared players | Focused Python test and actual read-only endpoint | Passed |
| Interactive status refresh | Browser prepare → Pending capture → Withdrawn assertions in table | Passed |
| Privacy/ownership | Administrator guard, configured Company/native get_list, narrow directory fields | Passed changed scope |
| Desktop/phone display | Actual-export fixture at both widths; scoped horizontal table scrolling | Passed |

## Decisions, deviations and recovery

Statuses represent preparation metadata, never evidence of a captured fingerprint. No new persistence, account, scanner identity or attendance mutation introduced. Browser contexts closed; native checks read-only and rolled back. Existing preparation/withdrawal history unchanged.

## Remaining work and release impact

Refresh/reopen the attendance app, then Fingerprint registration. Actual capture/matching and live hardware acceptance remain pending US-007-01 work. No additional migration; deploy Python changes and rebuild/publish the frontend normally.
