# US-005-04: Parent reminders and receipt delivery

## Header

- Epic: [EPIC-005](../epics/EPIC-005-payments-and-financial-history.md)
- State: In progress
- Priority: Proposed launch candidate; estimate and sequence pending clarification
- Delivery owner / affected apps: Sports App / native ERPNext where applicable

## Story statement

**As an** authorized academy operator, **I want to** send controlled email fee reminders and provide downloadable receipts from posted accounting records.

## Traceability

- Requirements: SPORTS-FR-041
- Dependencies: US-005-01 US-005-02
- Origin: Both
- Source references: [BA-QNR-001-Q04-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q04-12), [BA-QNR-001-Q10-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q10-01)
- PRD: [Product requirements](../../PRD.md)
- Reconciliation: [BA-QNR-001 register](../../discovery/BA-QNR-001-reconciliation.md)
- Planned branch: `story/us-005-04-parent-reminders-and-receipt-delivery`

## Notes and scope

Recipient authority, schedule, opt-out/delivery handling and private access need refinement. WhatsApp is discovery only, provider/cost/template approval pending.

This is proposed scope, not implementation or commercial acceptance. Use generic sport configuration and Sports-prefixed owned DocTypes; preserve ERPNext accounting and backend authorization.

## Acceptance criteria — proposed

1. Given agreed recipient/schedule rules, send an email reminder using current reconciled outstanding amount and log delivery without disclosing another player’s finances.
2. Retrying the same billing/reminder event does not duplicate notifications; failed deliveries are visible for authorized review.
3. Authorized receipt download matches a submitted allocated receipt; applicant payment claims never produce a false cleared-payment receipt.

## Verification plan

Verify authorized/denied roles, Company isolation, retries, correction history and relevant native ERP reconciliation. Agree fixtures, missing policies and failure cases before marking Ready.

## Completion evidence

- Discovery build log: [Questionnaire reconciliation](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Implementation: Manual posted-receipt delivery slice under the explicit 7 November user refinement; scheduled reminders and broader delivery policies remain outstanding.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-005-payments-and-financial-history.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

## Accepted PDF/manual-delivery refinement — 7 November 2026

Invoice/receipt links open clearly styled native PDFs. Add elapsed-time columns using finance creation/application submission timestamps. The operator-confirmed Email receipt action is restricted to posted positive Receive receipts and native read/print/email plus scoped player/Company/Customer access. Preserve source records, zero financial posting and duplicate-safe queued delivery. This is subsequent user direction supplementing BA-QNR-001-Q04-12. Automatic reminders, schedules, WhatsApp and broader delivery acceptance are not complete.

[Build evidence](../../build-logs/2026-11-07-us-003-03-pdf-receipts-email-and-elapsed-time.md) · [Operator guide](../../players-guide.md).

## Main-table PDF refinement — 7 November 2026

Main Players/Enrollments expose permission-scoped document links/actions and elapsed age. PDF links open a modal with download fallback and use selectable Sports Academy Invoice / Sports Academy Receipt backend Print Formats. The Settings document logo is configurable; Moyours reuses its website crest. Native Company/Customer/document permissions and deliberate receipt-email confirmation remain authoritative. Do not change global print defaults or broader story acceptance state.

[Build evidence](../../build-logs/2026-11-07-us-003-03-main-table-finance-and-branded-pdf-modal.md) · [Operator guide](../../players-guide.md).
