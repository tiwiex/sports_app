# Build log: Restore HTML enrollment and withdraw Next.js enrollment

- Date: 2026-11-03 (Africa/Lagos)
- Story / epic: US-001-04 / EPIC-001 (withdrawn)
- Requirements: SPORTS-FR-003/030 retained; SPORTS-FR-035 withdrawn
- Affected apps / branches / versions: Sports App, `story/us-001-04-enrollment-pwa`, committed baseline `a9aabf8`
- Pull requests: None; no commit, merge or push performed for this reversal.
- Status: Verified reversal on development

## Intended outcome and starting context

User clarified the Next.js request concerned attendance and explicitly requested reverting enrollment. The existing HTML enrollment had not been replaced or modified; the new enrollment frontend had been added alongside it.

## Policy decisions and plan

Withdraw the additional frontend, preserve committed Sports work and original HTML/application/finance behavior. Preserve historical build evidence with explicit withdrawn status. Keep narrow retirement endpoints so bookmarked/installed prototype copies do not strand users in a stale offline application. Next.js attendance remains the intended subsequent frontend; it is not implemented by this reversal.

## Work performed

- Moved only the new uncommitted Next.js enrollment package, generated bundle, bootstrap API and prototype-specific tests into a reversible local `/tmp` archive, outside the active app. The archive is temporary recovery material, not a retained product dependency.
- Restored documentation baseline where it advertised the new enrollment frontend. Added scope-correction notes, marked US-001-04 and SPORTS-FR-035 withdrawn, and retained the original build log/screenshots as historical evidence.
- `/sports-enroll` now temporarily redirects to `/academy`. Old static entry also returns visitors to the original academy website.
- Retained a small worker at the former worker URL that unregisters itself and deletes only `sports-enrollment-shell-*` caches; it redirects open prototype clients to the HTML academy website. No browser drafts, other worker registrations, unrelated caches or business records are deleted.
- Restarted development web workers to unload the retired API. No live bench or database/schema changes.

## Commands and observations

- Compared original `www/academy.html`, `www/academy.py`, `public/js/academy.js`, `public/css/academy.css`, application API and both invoice/payment services byte-for-byte with `git show HEAD:<path>`: all match committed baseline.
- Python unittest discovery: 116 tests passed after removing the prototype-only bootstrap test.
- `git diff --check`: passed.
- HTTPS Chromium checks at 1440px and 390px: retired entry returns to `/academy`; original HTML enrollment dialog and step markers present. No form submissions.
- Fresh isolated browser cache fixture: retirement removes enrollment shell cache and its registration while retaining an unrelated synthetic cache. Browser contexts closed afterward.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Original HTML enrollment preserved | Byte comparison of HTML/controller/JS/CSS and existing application/payment services | Passed |
| Original browser workflow accessible | Desktop/phone dialog opening and old-link redirect | Passed |
| Installed prototype safely retired | Scope-specific worker/cache checks | Passed |
| Committed Sports features retained | Existing 116-test suite | Passed |

## Decisions, deviations and recovery

Deleting the old worker URL alone would leave previously installed copies controlling cached pages. Retirement code therefore remains at that exact URL; it contains no enrollment functionality or Next.js dependency. Browser-local saved drafts are preserved because they may contain user-entered information. Historical prototype guide is clearly marked withdrawn.

## Remaining work and release impact

Enrollment continues on the original HTML academy website. The dedicated Next.js attendance app is future work; existing Boost attendance remains available. Old offline installations must reconnect before receiving the retirement worker. No application, player, customer, invoice, payment or role records were created/deleted by this reversal. No migration required.
