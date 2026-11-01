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
