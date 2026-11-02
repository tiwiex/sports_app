# Sports App development process

## Delivery chain

```text
Brief / user direction → requirement baseline → PRD → epic → story → app branch(es) → checks → build log → release
```

Use stable `SPORTS-FR-*` and `SPORTS-NFR-*` requirement IDs. Sports epic/story IDs are local to `doc-sports`; prefix cross-app references with `sports_app:`. Do not reuse ERP Boost's live requirement register IDs as if they described Sports work.

## Definition of Ready

A story has an outcome, requirements, observable acceptance criteria, affected apps, named dependencies and a verification plan. Resolve relevant PRD questions, identify required hardware/test fixtures and agree policy examples. For a cross-app story, identify the host contract/version and rollout order. Refine scope until one reviewable delivery slice is clear. Do not mark the initial draft stories Ready solely because files exist.

## Implementation workflow

1. Update requirement baseline, PRD and story when scope changes.
2. Use `story/<story-id-lowercase>-<description>` branches in affected app repositories.
3. Start an indexed build log and reference the Sports-qualified ID in every related PR.
4. Build the smallest vertical slice; keep business logic, server authorization and fixtures in the app owning the domain.
5. Verify positive and failure paths at a scope appropriate to the change. Financial retries/reconciliation, management-only access and device deduplication need meaningful automated checks. Layout/content-only changes can use manual review.
6. Update help/runbooks and ADRs for durable design choices. Record actual commands, site/app versions and observed results without secrets or private player data.
7. Add acceptance evidence and review references before changing story state.

## Cross-app changes

ERP Boost changes must be generic console capability. Sports owns the provider and sports APIs, with no runtime import of Primero. Validate Boost-only and combined installations and Sports-only/Finance-only/mixed permission profiles. Ship a compatible Boost extension contract first, then the Sports provider, then enable configured modules. Record version compatibility and provider-disable rollback; disabling UI does not reverse invoices or delete business records.

Use a designated development/test site for schema, permissions and integration checks. The reviewed apps are in different benches; installation on a common test site is future implementation work, not accomplished by this documentation baseline. Preserve existing app changes and data.

## Definition of Done

All acceptance criteria have evidence; appropriate checks pass; source references and balances reconcile; UI and direct endpoints enforce the intended boundaries; relevant documentation and ADRs are current. Link affected app PRs, build log and verification details. State limitations and any newly scoped work. For cross-app stories, both app changes and compatibility checks must be complete before closure.

## Release gates

Use PRD G0–G4. Complete biometric provider validation before claiming complete client scope. Require module-owner acceptance for every launch-required ERP module, plus migration/recovery rehearsal and trained operators. Capture sign-off evidence; do not infer it from installation or a successful screenshot.

## Mandatory adjustment logs

Every story implementation and every subsequent fix, adjustment or user refinement must have a separate dated build log before completion is reported. Use `YYYY-MM-DD-<story-id>-<adjustment>.md`, index it in `build-logs/index.md`, and link it from each affected story. This applies even when changes are uncommitted or documentation-only. Record actual checks, changed behavior, schema/data impact, cleanup and limitations; never overwrite prior evidence to disguise a changed decision. Repository-root `AGENTS.md` makes this an agent guardrail. Sports Development Tools discovers these files automatically.

One requested adjustment and the fixes needed to verify it share one adjustment log; a later requested change gets a new log. Individual file edits and test iterations do not each need their own log.

## DocType naming

All new app-owned DocTypes, including registration/application and child-table types, must start with `Sports`. Extend existing Sports Player/Sports Enrollment where appropriate. Do not rename ERPNext core Customer, User, Contact or other installed-app DocTypes.
