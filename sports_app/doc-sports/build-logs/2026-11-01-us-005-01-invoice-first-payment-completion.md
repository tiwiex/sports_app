# Build log: Invoice-first enrolment and one-click payment completion

- Date: 2026-11-01 (Africa/Lagos)
- Stories / epics: US-005-01 / EPIC-005; related US-001-02 and US-003-01
- Requirements: SPORTS-FR-003, SPORTS-FR-011, SPORTS-FR-026, SPORTS-FR-030, SPORTS-FR-031, SPORTS-NFR-002, SPORTS-NFR-003, SPORTS-NFR-009
- App / branch: Sports App / story/us-005-01-enrollment-payment-review; existing uncommitted work preserved
- Site: moyours.ideltatech.com, development bench
- Pull requests: None
- Status: Verified PoC / In review

## Intended outcome and starting context

The user changed the enrollment design: Make Payment should create a draft invoice instead of a receipt; the applicant's payment claim should move that invoice to review; Finance should complete payment with one action without opening Payment Entry separately. This supersedes the earlier receipt-first PoC for new enrollments. Initial fees and bank instructions remain the user-confirmed NGN setup.

## Policy decisions and plan

Make Payment creates a private application, prospective Customer and unsubmitted Sales Invoice. Use the actual invoice number as transfer reference. I've made payment records Pending Review on the invoice only, with docstatus 0 and no receipt/ledger posting. Finance verifies the bank credit before using Complete Payment. The invoice and a fully allocated receipt submit in one transaction; any failure rolls back both, including GL and Payment Ledger entries.

The user supplied a named existing finance account after being asked who should approve. Enable that account through the existing Boost Sales Invoice/payment approver configuration and its required Boost Invoice Approver role. Preserve all pre-existing native roles and Company/User Permissions. Do not make Administrator an invoice approver or send invitations/messages. Other approvers still need normal native invoice/payment rights, valid Boost approval configuration and allowed workflow transitions.

## Work performed

- Added `enrollment_invoices.py` for snapshot-based draft creation, fixed token-authorised claims, finance checks, idempotent completion and native invoice submission hooks.
- Public API URLs remain compatible; new preparations create invoices, while legacy Payment Entry reference claims retain the previous route. No existing receipt was converted/deleted.
- Added a unique, server-owned Sales Invoice link on Sports Registration and additive registration/claim fields on Sales Invoice. Existing Customer reuse and later Player/User acceptance remain intact.
- Added configurable fee Item links to Academy Settings. Setup creates compatible missing Sports Registration Fee / Sports Jersey Fee non-stock Items. Use company income/cost-center defaults and the existing enrollment receivable/bank accounts. Fee snapshots lock identity, amounts, currency, accounts and fee lines. Links cannot be detached to evade validation. New receipts must allocate the full initial amount to the linked invoice.
- Added a conditional default Sports Enrollment Invoice Review workflow because no Sales Invoice workflow was active. Existing compatible customer workflows are preserved; incompatible ones raise setup guidance instead of being replaced. Ordinary non-Sports invoices have their normal Complete/Approve paths and do not create Sports receipts. Default workflow scope is document-wide, as required by Frappe; completion conditions isolate Sports invoices.
- Kept the existing Payment Entry workflow and selected-approver guards. The receipt is created/submitted through native validations and allowed Approve transition, without extra Guest/registrar permissions or opening a Payment Entry form.
- Added the Complete Payment action and bank-verification reminder on the native Sales Invoice. Registration review shows the invoice reference/state and a permission-controlled invoice link. Updated the public wizard to display invoice references and settlement wording.
- Updated requirements, PRD, requirement baseline, player/website guides, story/epic, and AGENTS guardrail. Earlier dated build logs remain historical.

## Commands and observations

- `python -m unittest discover -s sports_app/tests -p 'test_*.py' -q`: 76 tests passed. Added invoice financial/provenance/line guards, role/approval checks, unrelated-invoice isolation and existing-workflow preservation/rejection checks. Existing receipt, registration, Customer/User and console tests remain passing. Invalid claim tokens return the same denial for missing and existing invoice references.
- Python compile checks and Node syntax checks for the changed wizard, settings, registration review and invoice scripts passed. `git diff --check` passed.
- Site schema/setup performed through native DocType reload/custom-field/workflow APIs. Repeated setup succeeded without replacing workflows or duplicating fee items. Published content-addressed console assets and refreshed only the development web worker.
- Real Guest preparation: actual ACC-SINV series, NGN 250,000 draft, one prospective Customer, no Payment Entry and no ledger entries. Unchanged retry returned the same invoice; wrong claim token was denied; repeated valid claims stayed Pending Review/docstatus 0. Guest invoice read/list and completion were denied.
- A temporary finance-only QA user with the required native/Boost approval rights, but no Sports Registration read permission, completed the invoice. Both invoice and receipt had docstatus 1; the receipt allocated NGN 250,000 to that exact invoice, with zero unallocated amount and zero invoice outstanding. Repeating completion returned the same receipt.
- Forced failure before receipt insertion rolled back the invoice posting and state. Forced failure after native receipt submission rolled back both documents' posting, application payment link, GL Entry and Payment Ledger Entry effects. Counts returned to their pre-QA values.
- An ordinary non-Sports invoice was created, sent for review and approved in real site QA; it remained unpaid and created no Sports receipt. The final regression run stubs outbound approval email.
- The selected real finance account was verified eligible without posting a transaction under its identity. Existing roles were preserved; only the required approval role and per-user approval configuration were added. No password, account-type, company-scope or notification changes.
- Real development browser checks passed: four-step public wizard, lost-response retry, actual invoice-series reference, bank/fee display, Pending Review confirmation, private invoice denial and 390px/320px layouts. Native Sales Invoice displayed Complete Payment for a finance-only QA account. Its click invoked the intended endpoint and reload. That browser completion response was deliberately stubbed; real posting/allocation was tested separately in rollback-controlled site QA above.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Draft invoice at Make Payment, no draft receipt | Native Guest preparation, browser lost-response retry | Passed |
| Payment claim marks invoice for unposted review | Token checks, repeat claim, ledger counts | Passed |
| One-click Finance completion and allocation | Native workflow submission + receipt, zero outstanding, retry | Passed |
| Failure does not leave partial financial effects | Before-receipt and after-receipt injected failures | Passed |
| Preserve role boundaries and existing workflows | Unit guards, real finance-only user, Guest denials, named-user eligibility | Passed |
| Usable public and invoice review controls | Desktop and phone browser checks; native invoice action | Passed |

Screenshots: [invoice payment reference](assets/2026-11-01-invoice-payment-page.png), [review confirmation](assets/2026-11-01-invoice-review-confirmation.png), [Finance invoice action](assets/2026-11-01-invoice-finance-review.png). All contain synthetic QA information only.

## Decisions, deviations and recovery

Initial real draft creation identified a mandatory Remarks property on this site; the service now supplies an enrollment-reference remark. Initial isolated unit failures were due to translation/site setup and dict test doubles colliding with `.items`; corrected the test harness and reran successfully. Neither was hidden as a passing check. An ordinary-invoice regression initially entered the pre-existing approval-email hook and logged a mail-server failure; no QA email queue record remained. The final regression run explicitly stubs that email callback. The applicant enrollment claim path does not invoke that hook.

User approver configuration is applied additively. Saving Boost Settings wholesale would run its managed-role sync and could remove unrelated native roles; this adjustment updates only the selected user's approval metadata/required role and clears its cached access. Existing selected-approver restrictions remain enforced at submission.

## Data impact and cleanup

Persistent development changes: additive application/invoice fields, two configured fee Items, a default invoice workflow and the user-approved finance assignment. Existing NGN fees/bank settings and receipt workflow are retained. No invoice/payment/GL posting from QA remains. Real posting tests ran inside a transaction that was rolled back; browser fixtures were unposted and removed afterward. Temporary finance users, approver rows, passwords/files, sessions, applications, prospective Customers/Contacts and any QA-created program category were removed. No applicant/player/User was created as a side effect of finance completion; admission still requires its existing staff action.

## Remaining work and release impact

This PoC supports full settlement of the initial fees, using manual bank verification. Partial/overpayments, fees/refunds, recurring monthly billing, proof upload, automatic reconciliation, lost-token recovery and production hardening remain separately scoped. Parallel completion load testing is not claimed; this slice uses shared lock ordering, locked application/invoice records, unique links and retry checks. No live Boost checkout edits, production publication, commit, merge or push occurred. The development code changes remain uncommitted alongside the preserved earlier work. Reload Desk to obtain current invoice scripts and approver access.
