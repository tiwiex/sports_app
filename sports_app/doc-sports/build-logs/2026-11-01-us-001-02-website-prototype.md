# Build log: Moyours public website proof of concept

- Date: 2026-11-01 (Africa/Lagos)
- Story / epic: US-001-02 / EPIC-001 (prototype slice)
- Requirements: SPORTS-FR-002, SPORTS-NFR-002, SPORTS-NFR-006, SPORTS-NFR-009
- Apps / branch: Sports App / `story/us-001-02-configurable-public-website`
- Pull requests: Not opened; local work only.
- Status: Verified prototype / In review

## Intended outcome and starting context

Pause private-console development and build a public website PoC before preparing a proposal. First commit and merge the completed player/documentation work and generic development Boost role-editor repair. User supplied https://www.moyoursacademy.com/ and its homepage screenshot as the reference.

## Policy decisions and plan

Native Frappe `www/academy` route on the designated development site. Keep production website, site homepage setting, live Boost and operational records unchanged. Public content comes only from an app-owned JSON file. This is presentation work; the full authorized CMS/publishing workflow remains unimplemented. Enrollment is explicitly a browser-only demonstration using sample details, with no submission, storage or account creation.

## Work performed

- Sports prior work committed as `16e737f`, merged into local develop as `e87702c`.
- Development Boost standard role-editor correction committed as `b5a4011`, merged into local develop as `2df09b8`. No remote pushes or production changes.
- New public template, scoped CSS/JS and JSON content. Green/gold visual identity, existing crest and two locally hosted academy images; asset sources recorded.
- Academy story, interactive three-stage pathway with keyboard tab navigation, manually controlled hero photographs, gallery lightbox, training/contact information and demo enrollment dialog.
- Responsive navigation, native modal focus/Escape handling, reduced-motion support, escaped content, fingerprinted styles/scripts and no-index/sitemap exclusion for the prototype.

## Commands and observations

- Reviewed public source homepage, About, Programs and Contact pages; retrieved the existing crest and two academy photographs and served them locally (no third-party image calls at runtime).
- Development web worker restarted to load the new Python page controller. No migration/schema/settings/role changes or fixture accounts needed.
- `node --check public/js/academy.js` and `git diff --check`: passed.
- Public JSON/template render check with malicious sample identity/program HTML: escaped rather than executed; passed. Content comes from the app-owned public configuration, with no database imports in its loader/controller.
- Playwright Guest checks against `https://moyours.ideltatech.com/academy`: passed at 1440px desktop and 390px/320px phone widths. All visible images decode; HTTP route/assets return successfully; no page errors, failed responses, horizontal overflow, browser local-storage entries or non-GET/HEAD requests.
- Verified keyboard program selection (arrows/End), matching selected program in modal, demo confirmation/reset/reopen, photo previous/next, gallery lightbox/Escape, mobile menu open/close and phone modal sizing. Final run used reduced-motion preference. Screenshots visually reviewed; all browser contexts closed.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Public template/configuration prototype | Native Guest HTTP route, JSON render/escaping and local assets | Passed for prototype; editor/publishing still deferred |
| No private player exposure or write requests | Database-free public content loader; browser request/storage checks and demo flow | Passed; no accounts/data created |
| Desktop, phone and keyboard use | 1440px, 390px, 320px guest browser checks, keyboard tabs/modal Escape | Passed |

Screenshots: [desktop](assets/2026-11-01-website-desktop.png), [full desktop](assets/2026-11-01-website-full-desktop.png), [phone](assets/2026-11-01-website-mobile.png).

## Decisions, deviations and recovery

Live source website reviewed using browsing and public asset inspection. Prototype copy is adapted, avoiding unverified new statistics, fees, fixtures or staff/player profiles. Full publishing/editor permissions and public applications remain future stories.

Initial browser image checks included deliberately lazy/hidden lightbox content; the harness was corrected to check visible loaded images. Mobile menu assertions now use its stable selector because the accessible label changes when opened. Native dialog focus now avoids scrolling the confirmation, and background scroll is locked while a modal is open. With reduced motion, the driver's locator stability heuristic timed out on the confirmation close button despite repeated identical measured bounds; a real pointer click at the button's measured center closed it successfully. The final suite uses that pointer interaction plus keyboard Escape checks. Initial-state screenshots are captured after a fresh route load to avoid smooth-scroll/focus artifacts.

## Remaining work and release impact

Prototype only; no proposal, production publication or public intake integration. Site root remains unchanged; preview uses `/academy`. CMS, content approval, complete accessibility review, production media permissions and account/application workflows remain later work. New website changes remain on their story branch for review.
