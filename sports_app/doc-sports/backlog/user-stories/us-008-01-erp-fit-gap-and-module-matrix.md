# US-008-01: Define ERP coverage and launch-required modules

## Header

- Epic: [EPIC-008](../epics/EPIC-008-erp-readiness-reporting-and-rollout.md)
- State: Proposed
- Priority: Must
- Delivery owner / affected apps: ERPNext configuration + Sports App

## Story statement

**As a** academy director, **I want** to agree the full ERP module matrix and implementation boundary **so that** ERP expectations become verifiable delivery scope.

## Traceability

- Requirements: `SPORTS-FR-022`
- Dependencies: None
- Planned branch: `story/us-008-01-erp-fit-gap-and-module-matrix`
- Planned build log: `YYYY-MM-DD-us-008-01-erp-fit-gap-and-module-matrix.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given academy workflows, when the fit-gap workshop ends, then Finance, purchasing, inventory, assets, HR/payroll and reporting each have an owner, release phase, native/Boost coverage and acceptance examples.
2. Given the target installation, when dependencies are reviewed, then app versions, required HR/payroll apps, Company, tax, bank, cost-center and accounting master decisions are recorded.
3. Given a gap in Boost navigation or workflow for a launch-required module, when scope is agreed, then a linked delivery task and acceptance criteria are created; installation alone is never marked module completion.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: Not started.
- Verification summary: Not implemented or verified.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.
