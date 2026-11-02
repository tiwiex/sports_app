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


## Current implementation

[US-002-01](backlog/user-stories/us-002-01-console-extension-spike.md) is Done with a working provider prototype on `moyours.ideltatech.com`. [Delivery evidence](build-logs/2026-11-01-us-002-01-console-extension-spike.md) records the independent dev checkout, role/browser checks, temporary-account cleanup and remaining Finance setup. US-003-01/US-003-02 are In progress and US-002-04 is In review; US-001-02 now has a public website prototype slice; other implementation stories remain Proposed.


[Academy setup guide](academy-setup.md) explains the Sports settings menu, administrator role, programs/groups and validation rules.

[US-001-01](backlog/user-stories/us-001-01-academy-and-program-settings.md) adds Academy Settings, programs/groups and configuration access; it is Done. Both stories were accepted for local merge into develop; no remote push or production release is included.

[Players guide](players-guide.md) covers private registration, enrollment status/dates and automatic per-player ERPNext Customer creation. [US-003-02 evidence](build-logs/2026-11-01-us-003-02-player-numbering-and-enrollment.md) records the development slice and outstanding public-intake integration.

[Current requirements](REQUIREMENTS.md) records accepted refinements. Management users can browse requirements, PRD, stories, ADRs and logs through **Sports → Development Tools**. Repository-root `AGENTS.md` and the [development process](DEVELOPMENT_PROCESS.md) require a new indexed log after each story or adjustment.

Development Tools now follows the Boost card/counter/tab layout and opens documents in Frappe modals. [Asset refresh and modal evidence](build-logs/2026-11-01-us-002-04-asset-cache-and-modal-layout.md) records the content-fingerprint fix for stale registration forms.

[Website prototype guide](website-prototype.md) covers the `/academy` preview, app-owned public content, demo interactions and limits. [PoC build evidence](build-logs/2026-11-01-us-001-02-website-prototype.md) records verification and the preceding local merges.

Public enrollment is now submittable: [Sports Registration review workflow](website-prototype.md), with [submission/acceptance evidence](build-logs/2026-11-01-us-003-01-public-submission-and-review.md). Earlier demo-only submission notes are historical.

[Enrollment payment wizard](website-prototype.md) now creates draft invoices, uses actual invoice references and sends claims for unposted Finance review. One Complete Payment action submits the invoice and its allocated receipt together. [Current build evidence](build-logs/2026-11-01-us-005-01-invoice-first-payment-completion.md) supersedes the earlier receipt-first PoC for new enrollments.
