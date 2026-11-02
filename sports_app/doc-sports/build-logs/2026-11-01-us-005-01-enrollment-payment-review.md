# Build log: Multi-step enrollment and draft payment review

- Date: 2026-11-01 (Africa/Lagos)
- Stories: US-001-02, US-003-01, US-005-01 (enrollment advance-receipt PoC slice)
- Requirements: SPORTS-FR-003, SPORTS-FR-011, SPORTS-FR-026, SPORTS-NFR-002, SPORTS-NFR-003, SPORTS-NFR-009
- App / branch: Sports App / story/us-005-01-enrollment-payment-review; preserves earlier uncommitted PoC work
- Status: Verified PoC / In review
- PRs: Not opened

## Request and decisions

User requested a multi-page enrollment form with bank details and an actual Payment Entry naming-series reference. Make Payment creates a draft; I've made payment moves it to a review workflow state. User explicitly confirmed NGN 220,000 registration + NGN 30,000 jerseys and Optimus Bank account 1000112942, beneficiary Moyours Sports Academy. NGN 40,000 monthly subscription from the reference is informational and excluded from the initial receipt.

Existing site has an NGN bank/receivable ledger, no Bank Account master and no active Payment Entry workflow. Academy Settings currency is USD; enrollment payment currency is configured independently as NGN, matching the company/account currency, without silently changing academy-wide defaults.

## Implementation

Welcome → Player details → Payment → Confirmation. Draft Payment Entry number is the transfer reference. Token-authorized repeated make/claim calls are idempotent; anonymous users get no general finance/record access. A prospective Customer is created at Make Payment because ERPNext requires the party; staff acceptance reuses that exact application-owned Customer through server-scoped provenance. No Customer picker/shared family account. Identity/program freeze after draft prevents reassignment. Player/User/enrollment still require staff acceptance.

A default Sports Payment Entry Review workflow is installed only when no active Payment Entry workflow exists; compatible existing workflows are preserved. Draft and Pending Review remain docstatus 0; Finance submission alone posts. Public claim performs a fixed audited state update after token/provenance/financial snapshot checks, with no Guest workflow permissions, finance role assignment, approval email or submission. Sports hooks protect linked receipt party/company/amount/currency/accounts on native saves/submission. The receipt is an unallocated advance; invoices/allocation remain later scope.

## Verification

- 86 focused Sports/Boost tests passed plus two additional Boost approver-schema tests, including fixed receipt amount/currency/accounts/provenance, forged service-flag rejection, unrelated PE isolation, private response allowlist and request-scoped Customer reuse. JS syntax and diff whitespace checks passed.
- Development backup completed; settings/application schema and additive Payment Entry fields installed. Confirmed bank master and enrollment fees enabled against the existing NGN bank/receivable ledgers. New review workflow installed because none was active; no existing workflow replaced. Console assets published and development worker restarted.
- Real draft creation used ERPNext naming series and server-selected Company/Customer/accounts/currency/NGN 250,000. No Player or User existed before acceptance. Make Payment retries returned one PE; wrong reference/token claims were denied.
- I’ve made payment changed Draft → Pending Review, retaining docstatus 0. Repeated/concurrent claims did not duplicate documents/transitions. GL Entry and Payment Ledger Entry counts remained zero for tested receipts. No financial posting was tested or performed.
- Staff acceptance reused the exact prospective Customer and attached the checked player email before creating the disabled Website User. Real browser acceptance with no player phone exercised creation of the previously absent contact under bounded permissions. Registrar still had no general PE write/submit rights.
- Native amount tampering was rejected. Forced ERPNext payment validation failure rolled back application, prospective Customer/Contact and draft. Concurrent preparations created one draft per request.
- Desktop and 390px/320px wizard checks passed: Welcome, details, Make Payment, bank/fee/PE-series reference, lost-response retry, read-only return to details, payment claim, confirmation and mobile layout. Guest PE list/read denied. Sports registration profile showed the linked PE/state; a registrar completed admission acceptance without finance privileges.
- All temporary applications, draft receipts, prospective Customers/Contacts, Players/enrollments, staff/generated Users/sessions and test master/category data were removed. Original academy defaults restored, preserving the explicitly confirmed bank/fee/workflow setup. Test credential files removed. Draft numbering cleanup follows ERPNext’s standard deletion behavior; no custom series-reset command was used.

Screenshots: [payment page](assets/2026-11-01-enrollment-payment-page.png), [review confirmation](assets/2026-11-01-payment-review-confirmation.png), [phone wizard](assets/2026-11-01-enrollment-wizard-phone.png), [staff payment state](assets/2026-11-01-registration-payment-state.png).

## Decisions and recovery

ERPNext’s UI account-details helper checks Payment Entry read permission even during ignore-permissions insertion. Initial integration failed and rolled back cleanly. A service-only in-memory subclass now populates metadata/balances for only the server-configured accounts and new Customer, then retains all other ERPNext validation and document hooks. This is not a globally registered controller override and grants no Guest/registrar finance rights. Subsequent Finance edits use ERPNext’s ordinary controller.

Contact.validate automatically binds an existing User by email. The prospective Customer therefore receives no email until acceptance checks player email uniqueness; private application data retains it. The same Customer then receives the contact/User linkage in the existing atomic acceptance flow. Zero-player-phone and nonempty-phone paths both passed.

The first phone test attempted to start a new registration twice while already on its details step; correcting the test navigation made both phone widths pass. No product failure was hidden. The workflow represents an unallocated advance; invoice allocation is not implemented. Applicant claims use a token-checked audited DB state change, not Guest workflow privileges or finance approval. No approval emails are sent by that action.

A final native Finance readiness check found Boost’s approval hook installed without its `custom_selected_approver` field. The independent development Boost checkout now has an idempotent install/migrate schema helper that creates only that missing field and preserves workflows/roles. Two schema tests passed. On a temporary Pending Review receipt, the native Approve transition was available and the existing selected-approver guard assigned Administrator successfully while the receipt remained docstatus 0 and GL count zero. The receipt and related fixtures were removed. No submission or email occurred. This requires the paired development Boost helper change/migration; live Boost was not edited.

## Data and release impact

Enrollment fee/bank/account settings, private application payment links/snapshot, additive Sports links on Payment Entry and a conditional workflow are deployed on development. This is an explicit exception to the earlier no-payment registration PoC; ordinary direct registration still creates no receipt. The default workflow affects native Payment Entries globally when enabled, while Sports financial locks apply only to linked enrollment receipts. Bank/receivable master read was added only for settings roles; no financial write/submit authority was added. No live Boost edits, production publication, remote push, automatic payment submission or account activation. Public claims are not proof of cleared funds. Receipt upload/bank reconciliation remain separate work.
