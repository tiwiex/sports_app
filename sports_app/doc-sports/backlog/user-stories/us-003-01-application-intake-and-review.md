# US-003-01: Capture and review player registrations

## Header

- Epic: [EPIC-003](../epics/EPIC-003-registration-and-player-record.md)
- State: In progress — PoC workflow
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** registrar, **I want** to capture direct registrations and review submitted applications **so that** each accepted applicant has an accurate private record.

## Traceability

- Requirements: `SPORTS-FR-003`, `SPORTS-NFR-003`
- Dependencies: [US-001-03](../../backlog/user-stories/us-001-03-sports-role-and-data-boundaries.md)
- Planned branch: `story/us-003-01-application-intake-and-review`
- Planned build log: `YYYY-MM-DD-us-003-01-application-intake-and-review.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given a valid direct registration or public application, when submitted, then required fields validate and a reference plus original submission timestamp are recorded; review edits retain that timestamp.
2. Given potential duplicate contact/identity details, when intake is reviewed, then possible matches are shown without rejecting different people who share a name.
3. Given repeated acceptance requests, when an application is accepted, then exactly one linked player is produced; public submission is rate-limited and does not allow listing applications.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Public submission and review](../../build-logs/2026-11-01-us-003-01-public-submission-and-review.md).
- Verification summary: Public submission/reference, private review, possible matches, accept/reject, immutable timestamp, strict fields, guest/role denial, rate limit, retry/concurrency, rollback and desktop/phone flow verified on the development site; see build evidence.
- Remaining decisions / follow-up work: Production acceptance/hardening, verified communications, full consent/contract versioning, portal activation and payments remain separate scope. This slice completes the requested PoC intake workflow.

New user refinement: [multi-step enrollment and draft Payment Entry review](../../build-logs/2026-11-01-us-005-01-enrollment-payment-review.md). This supersedes the previous no-payment PoC boundary; finance submission, invoice allocation and production acceptance remain separate.

## Registration context menu refinement — 3 November 2026

- Present the queue using the shared invoice table styling, status badges and allowlisted server sorting before pagination.
- Reference dropdown offers View in a modal; Pending rows with native write permission additionally offer Accept registration and Reject registration. Read-only or completed rows offer View only.
- Fetch current state/permissions before review confirmation. Accept shows possible player matches and enrollment controls; Reject requires a reason. Refresh the list and displayed profile after completion.
- Preserve all server authorization, admission idempotency and financial boundaries.
- [Build evidence](../../build-logs/2026-11-03-us-003-01-registration-context-menu.md).

## Enrollment naming and modal formatting — 3 November 2026

- Label the application queue **Enrollments** and its actions Accept/Reject enrollment. Use Enrollment application in the profile to distinguish intake from accepted program membership.
- Group the profile into readable summary, admission/match, billing/payment, player, guardian/emergency and consent sections; use responsive label/value columns with safe multiline wrapping.
- Preserve existing application IDs, program membership links, admission and Finance permissions. No DocType rename or migration.
- [Build evidence](../../build-logs/2026-11-03-us-003-01-enrollment-review-layout.md).
