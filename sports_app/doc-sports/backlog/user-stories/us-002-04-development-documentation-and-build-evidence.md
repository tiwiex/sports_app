# US-002-04: Expose Sports development documentation and build evidence

- Epic: EPIC-002
- State: In review
- Requirements: SPORTS-FR-028, SPORTS-NFR-002, SPORTS-NFR-009
- Branch: `story/us-003-02-player-numbering-and-enrollment` (current uncommitted review slice alongside the requested registration adjustment)

As a project administrator, I want requirements, delivery documents and build evidence in Sports Development Tools so that implementation and refinements are reviewable from the shared console.

## Acceptance criteria

1. System Manager / Sports Academy Administrator can discover and read requirements, PRD, epics, stories, ADRs, logs and guides without a Finance role. Basic Sports, registrar-only, Finance-only and Guest users cannot access the menu or APIs.
2. Files remain owned by Sports. The document viewer sanitizes Markdown; story status and MoSCoW have a narrowly authorized audited editor; other content stays read-only. It, resolves local documentation links safely and rejects traversal, arbitrary files and symlinks outside its documentation root.
3. Repository guardrails require a dated indexed log for each story and each subsequent adjustment. Current requirements and logs reflect the requested automatic Customer and program-category changes.

## Verification and evidence

See [guardrails, docs and categorization adjustment](../../build-logs/2026-11-01-us-002-04-guardrails-docs-and-program-categories.md). Unit/site/browser checks are recorded there. Broad editable requirement tracking and Boost's finance documentation remain outside this slice.

Verification: 57 unit checks and site/browser checks passed. Native Customer-field hiding, automatic program category rollback/reuse, management-only document access, relative links and traversal denial are recorded in the log. All temporary QA accounts/data were removed.

Follow-up: [asset cache refresh and Boost-style documentation modals](../../build-logs/2026-11-01-us-002-04-asset-cache-and-modal-layout.md). Content-fingerprinted assets must load after migration and browser reload; documentation uses the host card/tab styles with Frappe modal readers.

## Discovery provenance — 6 November 2026

- Origin: **Original baseline only** (including subsequent user direction); no direct questionnaire response establishes this story’s specific scope. Preserve existing state and acceptance evidence.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-002-shared-console-integration.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Story review controls — 6 November 2026

Management users can edit story status and MoSCoW in the list or document reader and use Mark Done without leaving the reader. Stale versions and invalid/arbitrary paths are rejected; every changed review records actor/time, before/after and note in an indexed build log. Narrative and source provenance remain unchanged; epic/master rows synchronize. Mark Done records a human decision rather than automatic acceptance verification. [Adjustment evidence](../../build-logs/2026-11-06-us-002-04-story-review-controls.md).

## Colour and layout refinement — 6 November 2026

Story rows use Boost status colours and separate Story/Epic/Title/Origin/Status/MoSCoW/Action columns. Independent priority badges/selectors distinguish Must/Should/Could/Won’t, retaining visible text. Reader header controls and content have responsive spacing and clear heading hierarchy. Existing review/audit APIs are unchanged. [Adjustment evidence](../../build-logs/2026-11-06-us-002-04-story-colours-and-layout.md).

## Autosave simplification — 6 November 2026

Status/MoSCoW dropdown changes now autosave in the list and reader. Save buttons and redundant priority text/badges above dropdowns are removed; accessible labels, table heading and coloured selectors remain. Failed saves restore confirmed values; Mark Done and indexed review audit remain unchanged. [Adjustment evidence](../../build-logs/2026-11-06-us-002-04-story-autosave.md).

Status-label/action refinement (6 November 2026): no repeated status text above selectors; Open and Mark Done are adjacent row actions. Accessible names and autosave remain. [Adjustment evidence](../../build-logs/2026-11-06-us-002-04-status-label-and-actions.md).

Table viewport refinement (6 November 2026): increased table scroll height to 110vh, retaining sticky headers and scroll behavior. [Adjustment evidence](../../build-logs/2026-11-06-us-002-04-taller-scroll-viewport.md).

Dropdown stability fix (6 November 2026): autosaves now update existing controls instead of replacing the table/reader. Dropdowns remain enabled; rapid changes serialize against confirmed revisions, and visible copies synchronize in place. [Build evidence](../../build-logs/2026-11-06-us-002-04-stable-dropdowns.md).
