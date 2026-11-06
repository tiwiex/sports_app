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

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q02-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-01), [BA-QNR-001-Q02-09](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-09).
- Impact: Expanded.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q02-01: Online and staff intake; payment confirms admission subject to approved scholarship/part-payment exceptions. No automatic bank clearance from a claim.
  - BA-QNR-001-Q02-09: Online and staff intake; payment confirms admission subject to approved scholarship/part-payment exceptions. No automatic bank clearance from a claim.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-003-registration-and-player-record.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Accepted enrollment refinement — 6 November 2026

This explicit user refinement supersedes the earlier separate admission/payment-confirmation step for applications with a linked Sales Invoice. Origin: **Both** (existing workflow and BA-QNR-001-Q02-01/Q02-09), with the specific UI/series/image direction supplied by the user on 6 November.

4. The public HTML form accepts an optional player portrait (JPEG/PNG/WebP up to 2 MB), previews it, stores a sanitized private image and carries it to the accepted player. Arbitrary file URLs, SVG, animated/corrupt/oversized content are rejected. Portrait collection does not grant public media consent.
5. New application references use `SPORTS-APP-YYYY-#####`. Existing application references and invoice transfer references remain unchanged. The application and accepted program membership remain separate linked records.
6. Make Payment creates one draft invoice; closing or abandoning the payment step leaves it draft. I've made payment requests **Pending Review**, without posting a receipt or confirming bank clearance. Retries do not duplicate applications/invoices/images.
7. The enrollment queue shows the linked invoice number and invoice workflow state. Pending applications offer acceptance only when the reviewer can also complete linked finance, and the invoice is awaiting review or already validly settled. Draft/unclaimed invoices cannot be accepted through this combined flow.
8. After checking the bank transfer, an authorized reviewer accepts the enrollment in one action: submit the linked invoice and fully allocated receipt, create player/customer/user/enrollment links and record acceptance atomically. Preserve native financial permissions and configured Boost approval controls. An error rolls back the entire operation; retries create no duplicate player or payment. Applications without an invoice retain ordinary admission review.
9. Rejection does not post financial documents. Cancelled, inconsistent or otherwise unsupported invoice states fail safely; historical accepted records are not silently recharged.

Scholarship/part-payment exceptions, production acceptance and consent-version policy remain open discovery scope; this refinement does not implement those exceptions or change configured fees/bank details. State remains In progress.

Build evidence: [Enrollment image and combined acceptance](../../build-logs/2026-11-06-us-003-01-enrollment-image-and-invoice-acceptance.md).

## Enrollment series setting — 6 November 2026

AC-5 refinement: expose Enrollment naming series in native Academy Settings and the Sports console. Default `MSA-ENR-.YYYY.-.#####`; support a validated uppercase prefix, optional year and 4–10 counter digits. Subsequent new applications use the saved series; existing IDs and invoice numbering are preserved. This supersedes the fixed SPORTS-APP prefix above. [Build evidence](../../build-logs/2026-11-06-us-003-01-configurable-enrollment-series.md).

## Confirmed player numbering and public age rule — 6 November 2026

User clarification confirms BA-QNR-001-Q02-07/Q02-08: **MSA + two-digit creation year + hyphen + two-digit creation month + continuous serial**, e.g. `MSA26-08005` followed by `MSA26-09006`. The sequence also continues across year boundaries. The backend uses the academy timezone and a locked Company-scoped counter whose key excludes month, year, editable prefix and application series. Minimum sequence width defaults to three digits and expands naturally; prefix/width remain management settings. On first initialization, seed after the highest existing matching player reference in that Company. Existing prototype IDs of another format stay unchanged and are not interpreted as legacy serials. Existing IDs are immutable; no identity, Customer or finance references are renamed.

The player reference is independent of the configurable **enrollment application** series (`MSA-ENR-.YYYY.-.#####`), accepted Sports Enrollment membership IDs and ERPNext invoice numbering. Current development player defaults are MSA / 3 digits. This supersedes the old prefix-plus-counter-only player ID format for new players.

Public HTML enrollment accepts ages **4 through 18 inclusive**, calculated from calendar birthdays against the academy-local date. Show an inline age error and enforce date bounds in the browser; reject invalid ages in the server-owned public application controller before creating a successful application/invoice. Under-4, 19-or-older and future DOBs are rejected. A February 29 birthday reaches the next age on March 1 in a non-leap year. Enforce on new applications/DOB corrections, without retroactively blocking unchanged historical applications or imposing this public intake policy on ordinary updates to existing player records. Private staff intake policy is not broadened by this web-form refinement.

Provenance: numbering is **Both** (baseline plus questionnaire, now user-confirmed); the explicit 4–18 public restriction is user direction informed by the supplied web-form screenshot, not a claim that the questionnaire stated those exact limits.

Acceptance refinement: verify August-to-September and December-to-January continuity; separate application/player counters; existing-reference preservation; concurrent allocation under settings/native-series locks; inclusive birthday bounds, leap birthdays, browser validation and direct-service age rejection. Story remains In progress for wider discovery scope.

[Build evidence](../../build-logs/2026-11-06-us-003-02-player-series-and-public-age-policy.md).

## Player email preflight and shared guardian identity — 6 November 2026

User refinement: a player email must be unique before public enrollment is submitted, not only when staff accepts it. Normalize player email; reject addresses already used by a User (including email-field aliases such as Administrator), Sports Player or another Pending Sports Registration. Rejected applications release their pending reservation. Browser preflight runs on leaving the player-email field and again before Make Payment/Submit, returning only availability; server validation remains authoritative under the existing settings lock. Preserve token-bound unchanged retries. Show a specific inline error and retain entered details. Review older applications again before financial completion, so a known conflicting email does not start the posting process.

At authorized acceptance/direct player registration, create the player's separate disabled Website User and create or reuse the guardian User. A server-owned **guardian_user** link on Sports Player supports many players to one guardian. Siblings retain separate player emails, Users, Customers and enrollment/finance histories. Player and guardian email on one form must differ. New guardian accounts are disabled Website Users without Desk roles or welcome mail; existing guardian accounts retain their original type, enabled state, roles and profile. Guardian email repetition is permitted; it never becomes a shared payer Customer. Account creation/linkage participates in the same admission transaction and rolls back on failure.

A supplied guardian email is an unverified identity reference, not proof of guardianship or permission to access children. This change does not activate accounts, grant guardian portal permissions, send invitations or implement the parent portal. Existing records are not bulk-backfilled or automatically merged; existing duplicate applications require staff/Finance correction. This user-approved account preparation refines the earlier player-only provisioning decision while leaving portal activation/access as separate scope.

Acceptance refinement: existing User/player/pending email conflicts must block public submission before an application/invoice is written; token retries remain idempotent; distinct sibling emails reuse one guardian User without changing it; fresh player/guardian Users and account links roll back on failure. Verify desktop/phone inline correction, same-email rejection, server denial and pre-finance checks. State remains In progress for wider backlog scope.

[Build evidence](../../build-logs/2026-11-06-us-003-01-email-preflight-and-guardian-users.md).

## Live operational tables — 6 November 2026

The installed Boost host now offers an optional mounted-table watcher. Sports Enrollments, Players, Attendance sessions and Clubs & Partners declare their own relevant DocTypes and retain their authorized APIs, filters, sorting, page offsets and generation guards. Committed native notifications coalesce into a background reread; a 15-second fallback catches missed notifications or writes without events. Only matching records on the current filtered/sorted page appear. Equal responses keep the existing DOM.

Updates pause while a filter/input/select, context menu or dialog is in use, then catch up. Hidden tabs do not poll; resuming/reconnecting triggers a reread. Host abort/unmount removes timers/listeners; responses recheck signal/generation/application safety. Explicit Refresh remains supported. The compatibility hook is generic and does not hardcode Sports into Boost. On an older host without the hook, manual refresh remains available. This slice updates operational queue tables; editable documentation/settings forms and the separate Next attendance application are not remounted by it.

No permissions, financial state, record identity, schema or website enrollment behavior changes. No production edits/deployment.

Acceptance refinement: matching new/updated/removed queue rows become visible without manual refresh; preserve query/page/scroll, open interactions and read permissions; verify unchanged DOM, stale result rejection, visibility/socket/poll catch-up and abort cleanup. Existing wider story status remains unchanged.

[Build evidence](../../build-logs/2026-11-06-us-002-01-live-console-tables.md).
