# US-001-02: Configure and publish academy website content

## Header

- Epic: [EPIC-001](../epics/EPIC-001-academy-configuration-and-access.md)
- State: In progress — prototype slice
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** website editor, **I want** to manage branding, page sections and approved public content **so that** the academy has its own website using reusable templates.

## Traceability

- Requirements: `SPORTS-FR-002`, `SPORTS-NFR-006`
- Dependencies: [US-001-01](../../backlog/user-stories/us-001-01-academy-and-program-settings.md)
- Planned branch: `story/us-001-02-configurable-public-website`
- Planned build log: `YYYY-MM-DD-us-001-02-configurable-public-website.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given changed branding and program content, when an authorized editor publishes, then public pages reflect settings without source changes.
2. Given an unpublished player, when a guest requests a profile or lists public content, then private player fields are absent and no operational player endpoint becomes public.
3. Given phone-width and keyboard navigation, when an applicant browses configured pages, then core content, labels and application navigation remain usable; stored content is safely rendered.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Website PoC](../../build-logs/2026-11-01-us-001-02-website-prototype.md).
- Verification summary: Prototype verified as Guest on desktop, 390px and 320px; interactive pathway, gallery, demo enrollment and escaped public content pass. Full CMS/editor/publishing criteria remain open.
- Remaining decisions / follow-up work: Refine applicable [PRD open decisions](../../PRD.md#11-open-decisions-and-risks) before marking Ready.


## Accepted prototype scope (2026-11-01)

User requested a website PoC based on the current Moyours website before a later proposal, after merging prior Sports/Boost work. Build a native `www/academy` preview with app-owned branding/content, three program stages, academy images, training/contact information and responsive interactions. Use a clearly identified demo-only enrollment modal with sample details and no persistence, guest write endpoint, User/Customer creation or email. Site homepage and production remain unchanged.

This verifies a reusable public template/configuration slice, not the complete editor/publishing workflow. Guest content never reads private player, User, Customer or enrollment records. CMS authorization, publishing/approval, live applications and production acceptance remain outstanding.

User refinement: [Full menu and shared registration fields](../../build-logs/2026-11-01-us-001-02-menu-and-registration-fields.md). Share the reference enrollment details with staff registration, retain unique player email and automatic Customer/User provisioning, and prefix any new DocTypes with Sports. Public intake remains demo-only.

Superseding refinement: public enrollment now submits Sports Registration for staff review/acceptance, documented in [US-003-01 evidence](../../build-logs/2026-11-01-us-003-01-public-submission-and-review.md). Earlier demo-only submission scope is historical; wider publishing/production scope remains open.

New user refinement: [multi-step enrollment and draft Payment Entry review](../../build-logs/2026-11-01-us-005-01-enrollment-payment-review.md). This supersedes the previous no-payment PoC boundary; finance submission, invoice allocation and production acceptance remain separate.
