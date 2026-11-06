# US-002-01: Validate and specify the console provider contract

## Header

- Epic: [EPIC-002](../epics/EPIC-002-shared-console-integration.md)
- State: Done
- Priority: Must
- Delivery owner / affected apps: ERP Boost + Sports App

## Story statement

**As a** platform maintainer, **I want** to validate an installed-app provider seam in Boost **so that** Sports can integrate without copying the console.

## Traceability

- Requirements: `SPORTS-FR-020`, `SPORTS-NFR-001`
- Dependencies: None
- Planned branch: `story/us-002-01-console-extension-spike`
- Planned build log: `YYYY-MM-DD-us-002-01-console-extension-spike.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given the reviewed Boost shell and target app versions, when the spike is complete, then a documented contract specifies provider discovery, manifest version, permissions, context, assets, lifecycle and error handling.
2. Given a minimal provider in the test site, when a permitted Sports-only user opens the shell, then a sample Sports view loads without a finance role or finance initialization request.
3. Given Boost without Sports and a failing or unsupported provider, when the console loads, then finance remains usable and the provider failure has an explicit diagnostic; record evidence and resolve ADR-0001 before production integration.

## Verification plan

- Target-site installed-app combinations, Sports-only/Finance-only/mixed roles, lifecycle and financial regression checks.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [2026-11-01 delivery evidence](../../build-logs/2026-11-01-us-002-01-console-extension-spike.md).
- Verification summary: 31 Python checks and both JavaScript suites pass. Real Sports-only, Finance-only and mixed-role browser/permission checks passed on `moyours.ideltatech.com`; temporary accounts/sessions removed. See the build log for limits.
- Remaining decisions / follow-up work: User accepted local commit and merge into develop. Full Sports views, richer context, finance workflow configuration and broader regression remain US-002-02/03 and later stories.

## Discovery provenance — 6 November 2026

- Origin: **Original baseline only** (including subsequent user direction); no direct questionnaire response establishes this story’s specific scope. Preserve existing state and acceptance evidence.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-002-shared-console-integration.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Live operational tables — 6 November 2026

The installed Boost host now offers an optional mounted-table watcher. Sports Enrollments, Players, Attendance sessions and Clubs & Partners declare their own relevant DocTypes and retain their authorized APIs, filters, sorting, page offsets and generation guards. Committed native notifications coalesce into a background reread; a 15-second fallback catches missed notifications or writes without events. Only matching records on the current filtered/sorted page appear. Equal responses keep the existing DOM.

Updates pause while a filter/input/select, context menu or dialog is in use, then catch up. Hidden tabs do not poll; resuming/reconnecting triggers a reread. Host abort/unmount removes timers/listeners; responses recheck signal/generation/application safety. Explicit Refresh remains supported. The compatibility hook is generic and does not hardcode Sports into Boost. On an older host without the hook, manual refresh remains available. This slice updates operational queue tables; editable documentation/settings forms and the separate Next attendance application are not remounted by it.

No permissions, financial state, record identity, schema or website enrollment behavior changes. No production edits/deployment.

Acceptance refinement: matching new/updated/removed queue rows become visible without manual refresh; preserve query/page/scroll, open interactions and read permissions; verify unchanged DOM, stale result rejection, visibility/socket/poll catch-up and abort cleanup. Existing wider story status remains unchanged.

[Build evidence](../../build-logs/2026-11-06-us-002-01-live-console-tables.md).


## Sports menu counts — 6 November 2026

Sports-owned menu badges show pending enrollment applications, total players, attendance sessions and clubs/partners in the configured academy. Counts use native permission-filtered aggregate reads, independent of Finance access; unauthorized entries are omitted. Zero is displayed explicitly. Badges refresh on relevant received native notifications, window focus and a 15-second visible-console fallback, survive sidebar redraws, and clear after failed reads. Settings, documents and the attendance-app shortcut have no artificial record total. No Sports dependency is added to Boost.

SPORTS-FR-019/020; SPORTS-NFR-006. [Build evidence](../../build-logs/2026-11-06-us-002-01-sports-menu-badges.md). Existing wider story status is unchanged.
