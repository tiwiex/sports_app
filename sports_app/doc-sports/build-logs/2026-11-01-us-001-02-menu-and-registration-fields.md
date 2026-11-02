# Build log: Full academy menu and shared registration fields

- Date: 2026-11-01 (Africa/Lagos)
- Story / epic: US-001-02 / EPIC-001; US-003-02 / EPIC-003
- Requirements: SPORTS-FR-002, SPORTS-FR-026, SPORTS-FR-029, SPORTS-FR-030, SPORTS-NFR-002, SPORTS-NFR-006, SPORTS-NFR-009
- Apps / branch: Sports App / `story/us-001-02-configurable-public-website`
- Pull requests: Not opened.
- Status: Verified / In review

## Intended outcome and starting context

Match the supplied full academy menu and inspect the live client-rendered `/enroll` form. Align the prototype enrollment and private staff registration with its player, guardian, emergency and consent fields. User requires Sports-prefixed names for any new DocTypes, including registration-related records.

## Policy decisions and plan

Keep public enrollment a clearly labeled demo with no persistence, email, payment or file upload. Use shared field definitions for public rendering, staff dialog, and server validation. Extend existing Sports Player instead of creating duplicate identity/guardian models. Sports Enrollment continues to link the player's own automatic Customer; no ERPNext core rename or extra privileges.

Keep the previously accepted unique player email for future User creation and capture guardian email separately. Consent choices are unselected and independent; staff record only actual guardian choices. A complete versioned consent/contract workflow remains future work. Do not hardcode the reference site's 4–18 age boundary into a generic app without program age policy.

## Work performed

- Full menu order: Summer Camp, About, Programs, Squads, Coaches, Fixtures, Results, Gallery, News, Support us, Contact, Enroll. Existing prototype sections remain local; pages outside this slice link to the matching existing academy website in a new tab. Summer Camp highlighted gold; responsive drawer for narrower displays.
- Shared app-owned registration schema: separate names, birth date, gender, preferred position, school, medical notes, unique player email/phone, guardian name/relationship/phone/alternative phone/email/address, emergency contact and three consent records.
- Sports Player fields extended; no new DocType required. Structured names derive full display name. Server validates required structured-registration fields, enums, dates, lengths, emails, paired emergency details and consent flags. Existing full-name records/API integrations remain supported; no forced historical backfill. Legacy full-name-only callers retain the existing minimal contract.
- Public modal renders the same schema without reading operational data. Staff dialog consumes it from the authenticated defaults endpoint. Medical/address/consent details remain inside permission-protected Sports Player records and never appear on public pages.

## Commands and observations

Reference inspection used a read-only browser because enrollment content is client-rendered. No original-site form was submitted. Development database backed up and targeted Sports Player schema sync completed. Existing role setup and fingerprinted console publication ran; only the development web worker restarted.

- 72 focused Python tests passed across registration validation, players, academy settings, permissions, console, assets, documentation, Boost provider/dimensions and User role repair.
- Syntax checks passed for public/staff JS; `git diff --check` passed. Native metadata includes the new fields; no new DocType or permission rows introduced for this adjustment.
- Public Guest browser QA passed at 1440px desktop, 390px and 320px phone widths. Header overflow checks also passed at 1281px, 1280px and 1024px. Full menu labels/order, local anchors/external destinations, keyboard program tabs, gallery, expanded required fields, selected program, unchecked media choice, preview/reset/reopen and mobile menu/modal sizing verified. No failed assets, JavaScript errors, horizontal overflow, write requests or local-storage entries.
- Real private registration/browser QA passed for structured names, required player/guardian fields, gender, preferred position, medical notes, guardian email/address and medical/media choices. Saved API response and native form retain the new details. A separate Customer and disabled Website User are still created automatically with no payer field.
- Existing Sports-only and Finance-only denial checks, rollback, same/different-key concurrent retries, duplicate names, immutable identifiers/dates, legacy full-name correction and Contact/User linkage passed.
- Sports Development Tools card/tab/modal regressions passed at desktop/phone widths.
- All temporary staff/generated Users, sessions, players, enrollments, Customers, Contacts and fixture masters removed; academy settings restored. Browser contexts closed and credential files removed. No original-site enrollment submitted; no public prototype data saved.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Menu matches reference, responsive links work | Guest header labels, URL inspection, desktop/tablet/phone checks | Passed |
| Public/staff/native fields align and validate | Shared schema, 72-test suite, public form and real staff save/native read | Passed |
| Atomic Customer/User registration and privacy preserved | Real-site rollback/retry/concurrency, role denial, linkage and cleanup | Passed |

Screenshots: [full menu](assets/2026-11-01-full-academy-menu.png), [public player fields](assets/2026-11-01-public-enrollment-fields.png), [guardian/consent fields](assets/2026-11-01-public-guardian-consent-fields.png), [staff dialog](assets/2026-11-01-staff-registration-fields.png).

## Decisions, deviations and recovery

The reference form uses guardian email; the accepted Sports account model requires a unique player email. Both are retained with separate labels, avoiding silently binding a parent or shared account. Payment and proof-of-payment stages are outside the current presentation PoC. The first staff browser run found an ambiguous checkbox selector because Frappe also renders a disabled checkbox; cleanup passed, the selector was narrowed to the editable control, and the full rerun passed. Repository AGENTS.md and the development process now record the explicit Sports DocType prefix rule.

## Remaining work and release impact

No commit/merge/push requested for this adjustment. Requires targeted Sports Player schema sync and refreshed content-fingerprinted assets on development. Keep full publishing, live public application review, production acceptance and consent/contract versioning deferred. New DocTypes must start with Sports; ERPNext core Customer/User/Contact names are unchanged.
