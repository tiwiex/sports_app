# US-003-02: Assign stable player IDs and enrollment dates

## Header

- Epic: [EPIC-003](../epics/EPIC-003-registration-and-player-record.md)
- State: In progress
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** registrar, **I want** to maintain unique player IDs and effective enrollments **so that** all downstream records identify the correct player.

## Traceability

- Requirements: `SPORTS-FR-004`, `SPORTS-FR-006`, `SPORTS-NFR-003`
- Dependencies: [US-003-01](../../backlog/user-stories/us-003-01-application-intake-and-review.md), [US-001-01](../../backlog/user-stories/us-001-01-academy-and-program-settings.md)
- Planned branch: `story/us-003-02-player-numbering-and-enrollment`
- Planned build log: `YYYY-MM-DD-us-003-02-player-numbering-and-enrollment.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given simultaneous new registrations, when IDs are assigned, then each academy-scoped registration number is unique, immutable and independent of player name or public slug.
2. Given acceptance or direct registration, when enrollment is confirmed, then program/group, automatically created per-player Customer link, start/end dates and active status are validated.
3. Given withdrawal, suspension or a same-name player, when records are updated, then existing history remains linked to the correct immutable ID and future eligibility follows effective dates.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Private registration slice](../../build-logs/2026-11-01-us-003-02-player-numbering-and-enrollment.md).
- Verification summary: Direct private registration, stable IDs, enrollment, automatic per-player Customer creation, concurrent retries and three browser role profiles verified on the development site. See the build log.
- Remaining decisions / follow-up work: Public application acceptance integration depends on US-003-01; full identity/contact duplicate policy, broader role boundaries and downstream eligibility integration remain open. This private slice is not a completed public intake workflow.

## Current delivery slice

User requested player management and ERPNext Customer linkage after accepting settings. Start with private direct registration, an immutable Sports Player identity and Sports Enrollment Customer/date/status records. Public intake can later call this foundation; US-003-01 is still Proposed. Sports Registrar is the initial restricted operator role. Player-attributed invoicing and receipt history remain EPIC-004/005. See the [usage guide](../../players-guide.md).

User refinement (2026-11-01): registration must create one Customer per player from the supplied details in one save. No shared family Customer or payer selector. Customer/contact/player/enrollment writes must roll back together, and retries must not duplicate any record. Program/group controls and profile rows show friendly names while retaining stable IDs internally.

Program categorization and hidden native Customer-field refinement: [separate adjustment log](../../build-logs/2026-11-01-us-002-04-guardrails-docs-and-program-categories.md). New Customers belong to a program-named group based on their immutable initial registration program; future enrollments retain that classification.

Follow-up: [asset cache refresh and Boost-style documentation modals](../../build-logs/2026-11-01-us-002-04-asset-cache-and-modal-layout.md). Content-fingerprinted assets must load after migration and browser reload; documentation uses the host card/tab styles with Frappe modal readers.

Follow-up: [Player Users and User role editor](../../build-logs/2026-11-01-us-003-02-player-users-and-role-editor.md). New players require a unique email and receive a disabled Website User; activation remains deferred. Standard System Manager User role-editor access is restored without new Boost Admin powers.

User refinement: [Full menu and shared registration fields](../../build-logs/2026-11-01-us-001-02-menu-and-registration-fields.md). Share the reference enrollment details with staff registration, retain unique player email and automatic Customer/User provisioning, and prefix any new DocTypes with Sports. Public intake remains demo-only.

Superseding refinement: public enrollment now submits Sports Registration for staff review/acceptance, documented in [US-003-01 evidence](../../build-logs/2026-11-01-us-003-01-public-submission-and-review.md). Earlier demo-only submission scope is historical; wider publishing/production scope remains open.

Presentation follow-up: [Player reference menu and grouped profile modal](../../build-logs/2026-11-03-us-003-03-player-profile-layout.md). Existing program-membership creation and automatic account linkage are retained.
