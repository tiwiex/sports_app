# Build log: Enrollment terminology and review modal layout

- Date: 2026-11-03 (Africa/Lagos)
- Story / epic: US-003-01 / EPIC-003
- Requirements: SPORTS-FR-003, SPORTS-NFR-002, SPORTS-NFR-003
- Affected apps / branch / versions: Sports App / story/us-003-01-enrollment-review-layout; base HEAD 48fb0a2 plus preserved pending work
- Pull requests: None; changes uncommitted
- Status: Verified development refinement / In review

## Intended outcome and starting context

The user reported poor modal formatting and asked whether the registration queue represents enrollment. It contains incoming applications to enroll; acceptance creates the player and their dated program membership. The prior modal used a flat definition list with headings and review/payment paragraphs mixed together.

## Policy decisions and plan

Use Enrollments for the console queue, its status filter, menu actions and modal title. Use Enrollment application inside the profile to clarify the admission stage. Keep existing application and program-membership models, identifiers, provider key and API links stable; this avoids conflating an intake application with its accepted membership or changing financial provenance. No DocType rename or migration is needed.

## Work performed

- Replaced the flat profile with scoped, responsive cards: application summary, status/name header, admission review and possible matches, accepted player/rejection reason when applicable, billing/payment, player details, parent/guardian, emergency contact and consent choices.
- Consistent label/value styling, two-column desktop grids, one-column phone grids, full-width multiline fields and wrapping for long contact/address/medical text. Explicit Yes/No consent values remain intact.
- Admission buttons are grouped with spacing. Linked invoices/receipts have labelled references and separate review/posting/payment states. Empty billing is explained; cancelled invoices are labelled cancelled.
- Renamed the provider label and visible queue/filter/menu/modal/pagination text to Enrollments. Overview guidance now distinguishes enrollment applications, admitted players/program memberships and separate Finance review.
- Updated current requirements, PRD, story acceptance notes and enrollment/player guides. Historical logs and technical identifiers retain their original names.

## Commands and observations

- Full Sports unit suite: 101 tests passed. Existing admission/finance/notification checks remain passing.
- Node syntax checks for registrations.js and console_overview.js and git diff whitespace checks passed.
- Chromium fixture uses actual Sports view, registration field definitions and Boost CSS at 1440px/390px. Confirmed grouped sections, desktop two-column/phone single-column fields, no profile horizontal overflow, long text wrapping and explicit negative consent rendering. Prior menu/permission/stale-state/confirmation/reason/sort/cleanup checks also passed after label changes. Dialog/API are controlled fixtures; no real applicant was accepted or rejected.
- Inspected synthetic desktop/phone screenshots: [desktop](assets/2026-11-03-enrollment-review-1440.png), [phone](assets/2026-11-03-enrollment-review-390.png). Native Frappe Dialog chrome/control styling is not represented by this fixture; the profile structure and scoped styles are actual implementation code.
- Native provider check on Moyours returns Enrollments under the existing stable view key. Published registrations.35b1aae53d9872e7.js and console_overview.d008502e3ef74e4b.js, cleared caches and restarted only the development web process.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Clear enrollment wording | Provider assertion, renamed controls/browser regression | Passed |
| Readable grouped modal | Actual field schema, DOM sections and inspected previews | Passed |
| Responsive layout and values | Two/one-column assertions, overflow and consent checks | Passed |
| Preserve admission actions and safeguards | Existing unit suite and browser action cases | Passed |

## Decisions, deviations and recovery

No record/DocType/provider-key/API rename, financial changes or permission changes. Enrollments describes the admission application queue; accepted program memberships remain accessible under Players. Existing pending club-directory, notification and context-menu work remains intact.

## Remaining work and release impact

Available on moyours.ideltatech.com development after reloading the console. No database migration, production deployment, commit/merge/push, QA account creation or external email. All preview data is synthetic. Authenticated native Dialog acceptance/posting is outside the layout fixture verification; underlying server guards are unchanged.
