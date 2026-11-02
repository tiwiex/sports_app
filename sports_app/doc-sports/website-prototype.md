# Moyours website and enrollment PoC

The development demonstration is `/academy` on `moyours.ideltatech.com`. It is separate from the academy's current public website. Production publishing/CMS, payment gateways and self-service activation remain separate scope.

## Current applicant journey — invoice first

1. Choose Enroll or Find your place, then proceed through Welcome and Player Details.
2. **Make Payment** saves one private Sports Registration, its prospective Customer and one **draft Sales Invoice**. Its actual ERPNext invoice-series number is the bank-transfer reference. The draft has no ledger impact and creates no Payment Entry.
3. The Payment page displays the configured NGN 220,000 registration fee plus NGN 30,000 jerseys, total NGN 250,000; the NGN 40,000 monthly subscription is informational and excluded from this invoice. Bank: Optimus Bank, account 1000112942, beneficiary Moyours Sports Academy. These are academy collection instructions, not implementation-fee instructions.
4. After making a transfer through their own bank, the applicant clicks **I've made payment**. A token-authorised claim moves the invoice to **Pending Review**, retaining docstatus 0. No invoice/payment ledger posting, email, Player or User is created by the claim.
5. Finance verifies the full bank credit, then uses **Complete Payment** on the Sales Invoice. One action submits the invoice, creates and submits its allocated ERPNext Payment Entry, and checks that the invoice balance is zero. No separate Payment Entry form is required. Failure rolls back both documents' financial effects.

Player details become read-only after preparation. Closing/reopening within the same page retains the current reference; Start another registration resets the in-memory form. Reloading loses the private token; contact the academy with the invoice reference if interrupted. Tokens and private player data are not placed in browser storage or URLs. Public invoice list/read access is denied.

No proof-file upload or automated bank verification is included. The reviewer must verify the actual bank credit before completing payment. Applicant confirmation alone does not establish payment clearance or admission.

## Staff review and admission

Open Sports → Registrations, select the application and review its details and possible matches. Accepting creates one Player, disabled Website User and enrollment, reusing the exact prospective Customer. Admission remains separate from finance approval. A registrar can review the invoice state but gains no general invoice/payment creation or submission rights. Finance users can open the invoice directly from the standard Sales Invoice list; registration reviewers with financial read access also receive an invoice link.

## Finance permissions and action

The selected PoC approver is the user supplied by the academy in this session. Use the existing Boost Sales Invoice approver and payment-approver configuration, together with native invoice read/write/submit and Payment Entry read/create/submit permissions, Company/User Permissions and allowed workflow transitions. No Sports-only role receives those rights. An existing selected approver remains binding.

Pending Review invoices display **Complete Payment** and a reminder to verify the full bank credit. The same action is available through the native workflow. Submitted invoice state is Approved; its financial status becomes Paid when the receipt is allocated. Receipt state is Submitted. Repeated calls to the service return the same completed result, without another receipt. Cancelled, rejected or inconsistent records require normal controlled Finance correction; this button does not create a refund or override approval restrictions.

The PoC supports full settlement of the fixed initial fees only. Partial/overpayments, bank fees, refunds, recurring monthly invoice runs and bank reconciliation require their own reviewed workflows.

## Configuration and deployment

Academy Settings owns enrollment currency, fees, Bank Account, receivable account and two non-stock fee Item links. Invoice income and cost center use the existing company defaults. There are two fee lines and no stock movement or automatic extra taxes/discounts. Tax, stock or account configuration that changes the agreed total is rejected for correction.

Setup creates missing compatible Sports Registration Fee / Sports Jersey Fee Items only when no explicit item is selected. It adds immutable application links to Sales Invoice and Payment Entry. The Sports Enrollment Invoice Review workflow is created only when no Sales Invoice workflow is active; an existing workflow must have compatible Draft/Pending Review draft states and an authorised Complete Payment transition to a submitted state. Existing workflows are never silently replaced. Non-Sports invoices retain a standard Approve path and do not create Sports receipts.

The earlier Sports Payment Entry Review workflow remains for receipt submission and any legacy applications. Older Payment Entry references continue through their original token-authorised claim path; new Make Payment requests create invoices. Earlier Payment Entry-first documentation/build evidence is historical and superseded for new enrollments.

## Verification and limits

See the [invoice-first implementation build log](build-logs/2026-11-01-us-005-01-invoice-first-payment-completion.md) for real native accounting, failure rollback, access and browser evidence. The prototype does not activate user accounts, send welcome/approval emails from applicant claims or establish production acceptance. Device integration, monthly billing and full production reconciliation remain in the backlog.

Finance can also use **Confirm Payment** directly in the Boost invoice context menu. It appears only for eligible Pending Review enrollment invoices and authorised reviewers, and disappears after confirmation. The existing **Complete Payment** action under View remains available. Both actions use the same financial completion service.
