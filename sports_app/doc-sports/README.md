# Sports App product and delivery documents

Planning baseline for the generic `sports_app`, with Moyours Sports Academy as the first proposed implementation. Created 2026-11-01. The source request spells the academy “Moyours”; confirm the trading name before publishing branding.

| Document | Purpose |
|---|---|
| [Original requirements](requirements.txt) | Unmodified client brief |
| [PRD](PRD.md) | Product scope, workflows, permissions, architecture, and release gates |
| [Requirement baseline](concepts/requirement-baseline.md) | Stable requirements, provenance, and story traceability |
| [Backlog](backlog/README.md) | Ordered epics and individually actionable stories |
| [Development process](DEVELOPMENT_PROCESS.md) | Readiness, completion, and cross-app delivery rules |
| [Architecture decisions](adr/index.md) | Proposed choices that need validation during implementation |
| [Build logs](build-logs/index.md) | Planning evidence and future implementation verification |

This follows ERP Boost's PRD → requirement baseline → epic → story → ADR → build-log structure. All implementation stories start **Proposed**. Existing Primero and Boost functionality is reuse evidence, not evidence that Sports features are delivered. No live requirement register has been created; the baseline Markdown table is the planning source of truth until a later, explicitly recorded migration.

Only documentation is introduced by this baseline. No app, database, role, route, device, accounting configuration, or deployment is changed.
