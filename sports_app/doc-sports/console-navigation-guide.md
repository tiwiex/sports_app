# Sports and Boost navigation

On sites with Sports App, authorized Sports menu groups appear above the native Boost groups in the shared console sidebar. The Sports heading is green; a single blue Boost heading contains the native finance sections (Dashboard, Sales and others). These nested section labels use lighter styling rather than separate coloured cards. Expand/collapse Boost as a whole or its individual sections. Child menu items are indented below their group headings, and the selected Sports item has a light-green highlight. Group names, item labels and keyboard focus remain visible.

The presentation follows the existing authorized menu entries; it grants no additional access. Search/collapse and menu refresh continue to use Boost. If no Sports items are available to the current user or search, the native menu keeps its existing appearance and order. The enhancement is shipped only by Sports App; no Sports-specific code is added to Boost or Boost-only sites.

After an update, reload the whole Desk page to load the Sports navigation asset. The existing sidebar show/hide behavior on phones remains controlled by Boost.

The Boost parent keeps its expanded/collapsed state across menu rebuilds within the current Desk page. Other installed-app provider groups are not classified as Boost merely because they appear in the same menu.

## Live operational tables — 6 November 2026

The installed Boost host now offers an optional mounted-table watcher. Sports Enrollments, Players, Attendance sessions and Clubs & Partners declare their own relevant DocTypes and retain their authorized APIs, filters, sorting, page offsets and generation guards. Committed native notifications coalesce into a background reread; a 15-second fallback catches missed notifications or writes without events. Only matching records on the current filtered/sorted page appear. Equal responses keep the existing DOM.

Updates pause while a filter/input/select, context menu or dialog is in use, then catch up. Hidden tabs do not poll; resuming/reconnecting triggers a reread. Host abort/unmount removes timers/listeners; responses recheck signal/generation/application safety. Explicit Refresh remains supported. The compatibility hook is generic and does not hardcode Sports into Boost. On an older host without the hook, manual refresh remains available. This slice updates operational queue tables; editable documentation/settings forms and the separate Next attendance application are not remounted by it.

No permissions, financial state, record identity, schema or website enrollment behavior changes. No production edits/deployment.

[Build evidence](build-logs/2026-11-06-us-002-01-live-console-tables.md).


## Sports menu counts — 6 November 2026

Sports-owned menu badges show pending enrollment applications, total players, attendance sessions and clubs/partners in the configured academy. Counts use native permission-filtered aggregate reads, independent of Finance access; unauthorized entries are omitted. Zero is displayed explicitly. Badges refresh on relevant received native notifications, window focus and a 15-second visible-console fallback, survive sidebar redraws, and clear after failed reads. Settings, documents and the attendance-app shortcut have no artificial record total. No Sports dependency is added to Boost.

SPORTS-FR-019/020; SPORTS-NFR-006. [Build evidence](build-logs/2026-11-06-us-002-01-sports-menu-badges.md). Existing wider story status is unchanged.
