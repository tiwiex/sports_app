# Build log: Story row colours and Boost-style layout

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-002-04 / EPIC-002
- Requirements: SPORTS-FR-028, SPORTS-NFR-006
- App / branch: Sports App / `story/us-007-01-fingerprint-preparation`
- Asset: `development_tools.d9ab3a29c8abf2e3.js`
- Pull requests: None; no commit, merge or push requested
- Status: Verified development presentation adjustment

## Intended outcome and starting context

User requested colour-coded story rows, distinct MoSCoW colours and Boost’s header/content system because the prior controls were squashed together. Inspected development Boost’s story table, status-row classes and activity/document layout. Sports previously combined status and priority in one table cell.

## Policy decisions and plan

Use the host’s existing status-row classes and activity/table conventions; keep all additional styling scoped to Sports. Distinguish priority independently from status and retain text labels rather than relying only on colour. Preserve review APIs, provenance, revisions, audit and permissions.

## Work performed

- Replaced combined document/tracking cells with Story, Epic, Title, Origin, Status, MoSCoW and Action columns. Fixed column minimums and horizontal table scrolling prevent compressed controls.
- Applied Boost’s status row colours to normalized status prefixes, including qualified prototype states; added local UAT/withdrawn/unclassified styles. State labels and selectors retain the exact stored text.
- Added MoSCoW badge/selector colours: Must red, Should amber, Could blue, Won’t slate; unknown priorities remain neutral. Badge/selector preview changes on selection; Save still controls persistence.
- Added a distinct page header, card/activity/search spacing, sticky table headings, padded rows and visible priority legend.
- Separated reader review controls into a padded header panel; desktop grid/mobile stacking, dedicated actions area and spaced document headings/paragraphs/lists/tables improve readability.
- Updated user guide, requirements, affected story and indexed adjustment evidence. Backend/Boost app code unchanged.

## Commands and observations

- JS syntax check and `git diff --check` passed.
- Extended Chromium fixture passed at 1440/390px with actual Sports JS and Boost stylesheet. Verified seven distinct headers, amber In progress and green Done row colours, four unique labelled MoSCoW badge colours, padded reader/grid spacing and no page-level overflow. Existing save, stale-error, Mark Done, list/reader refresh and cleanup checks still pass.
- Browser API responses synthetic; no real story metadata, role or ERP records changed.
- Visually inspected desktop table and phone reader screenshots.
- Published content-addressed console assets; verified HTTPS response on Moyours development matches the source. No migration or worker restart required for this frontend-only change.

## Verification evidence

| Criterion | Evidence | Result |
|---|---|---|
| Status row colours and separate columns | [Desktop table](assets/2026-11-06-story-table-layout-1440.png), browser computed styles | Passed |
| Distinct MoSCoW colours with labels | Four badge colour assertions; selector previews | Passed |
| Spaced reader header/content | [Desktop reader](assets/2026-11-06-story-tracking-layout-1440.png), [phone reader](assets/2026-11-06-story-tracking-layout-390.png) | Passed |
| Phone table remains scrollable | [Phone table](assets/2026-11-06-story-table-layout-390.png), overflow check | Passed |
| Existing review flow retained | Synthetic API desktop/phone regression fixture | Passed |

## Decisions, deviations and recovery

No schema, backend service, finance, role or actual backlog-state changes. No QA accounts or business records created; fixture browser contexts closed. Existing unrelated work and older hashed assets preserved. New styles belong to Sports App and reuse host conventions without copying the console shell.

## Remaining work and release impact

Refresh Sports Development Tools on Moyours development to load the new asset. Horizontal scrolling is intentional when the available width cannot fit readable columns. No production release or Git commit/push performed.
