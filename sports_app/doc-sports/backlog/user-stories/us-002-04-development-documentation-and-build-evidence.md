# US-002-04: Expose Sports development documentation and build evidence

- Epic: EPIC-002
- State: In review
- Requirements: SPORTS-FR-028, SPORTS-NFR-002, SPORTS-NFR-009
- Branch: `story/us-003-02-player-numbering-and-enrollment` (current uncommitted review slice alongside the requested registration adjustment)

As a project administrator, I want requirements, delivery documents and build evidence in Sports Development Tools so that implementation and refinements are reviewable from the shared console.

## Acceptance criteria

1. System Manager / Sports Academy Administrator can discover and read requirements, PRD, epics, stories, ADRs, logs and guides without a Finance role. Basic Sports, registrar-only, Finance-only and Guest users cannot access the menu or APIs.
2. Files remain owned by Sports. The viewer is read-only, sanitizes Markdown, resolves local documentation links safely and rejects traversal, arbitrary files and symlinks outside its documentation root.
3. Repository guardrails require a dated indexed log for each story and each subsequent adjustment. Current requirements and logs reflect the requested automatic Customer and program-category changes.

## Verification and evidence

See [guardrails, docs and categorization adjustment](../../build-logs/2026-11-01-us-002-04-guardrails-docs-and-program-categories.md). Unit/site/browser checks are recorded there. Broad editable requirement tracking and Boost's finance documentation are outside this slice.

Verification: 57 unit checks and site/browser checks passed. Native Customer-field hiding, automatic program category rollback/reuse, management-only document access, relative links and traversal denial are recorded in the log. All temporary QA accounts/data were removed.

Follow-up: [asset cache refresh and Boost-style documentation modals](../../build-logs/2026-11-01-us-002-04-asset-cache-and-modal-layout.md). Content-fingerprinted assets must load after migration and browser reload; documentation uses the host card/tab styles with Frappe modal readers.
