# US-002-03: Unify console entry and protect existing Finance behavior

## Header

- Epic: [EPIC-002](../epics/EPIC-002-shared-console-integration.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERP Boost + Sports App

## Story statement

**As a** platform maintainer, **I want** to compose shell access and login routing across apps **so that** sports staff enter safely and finance users keep existing workflows.

## Traceability

- Requirements: `SPORTS-FR-019`, `SPORTS-FR-021`, `SPORTS-NFR-001`, `SPORTS-NFR-002`
- Dependencies: [US-002-02](../../backlog/user-stories/us-002-02-sports-console-provider.md)
- Planned branch: `story/us-002-03-console-login-and-finance-regression`
- Planned build log: `YYYY-MM-DD-us-002-03-console-login-and-finance-regression.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given Sports-only, Finance-only and mixed users, when logging in or following authorized deep links, then each reaches the shared route and only permitted modules; unauthorized deep links are denied.
2. Given a Sports-only role, when opening the shell or calling invoice APIs directly, then finance prefetch is skipped and accounting access remains denied without granting broad Boost/Accounts roles.
3. Given Boost alone and a combined installation, when representative invoice, payment, approval, role guard and explicit-login-redirect journeys run, then existing authorized behavior passes; permission/company changes invalidate scoped caches.

## Verification plan

- Target-site installed-app combinations, Sports-only/Finance-only/mixed roles, lifecycle and financial regression checks.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: Not started.
- Verification summary: Not implemented or verified.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.

## Discovery provenance — 6 November 2026

- Origin: **Original baseline only** (including subsequent user direction); no direct questionnaire response establishes this story’s specific scope. Preserve existing state and acceptance evidence.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-002-shared-console-integration.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
