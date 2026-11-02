# Build log: Confirm Payment in the invoice context menu

- Date: 2026-11-01 (Africa/Lagos)
- Story / epic: US-005-01 / EPIC-005
- Requirements: SPORTS-FR-031
- Affected app / branch: Sports App / story/us-005-01-enrollment-payment-review; optional development Boost host unchanged
- Pull requests: None; no commit or push requested
- Status: Verified

## Intended outcome and starting context

Finance should confirm enrollment payments from the invoice context menu without opening View. Keep the existing action under View and remove the shortcut after confirmation.

## Policy decisions and work performed

Added Sports-owned Desk script `public/js/invoice_context_payment.js` through `hooks.py`. Opening a Sales Invoice menu requests current eligibility, then inserts Confirm Payment after View. Eligibility is fetched again on every opening; completed invoices never retain a cached action. Stale async responses and duplicate clicks are guarded. Successful completion removes the item and refreshes the console list. View remains unchanged.

Strengthened `enrollment_invoices.completion_access` to require a draft Sports invoice in Pending Review, a non-rejected application, existing finance/selected-approver permissions, Company access and an available Complete Payment workflow transition. The existing complete_payment service still revalidates and settles atomically. Generic invoice/payment behavior and the Boost checkout are unchanged. The operator must verify bank credit before confirming, as in the existing View action.

## Commands and observations

- `python -m unittest discover -s sports_app/tests -p 'test_*.py' -q`: 77 tests passed. Added eligibility coverage for authorised Pending Review, submitted/cancelled/draft/unrelated invoices, missing finance access, rejected application and missing workflow transition.
- `node --check sports_app/public/js/invoice_context_payment.js`: passed.
- Chromium UI fixture: passed eligibility insertion, calling existing completion service, refreshing list, removing confirmed action and excluding Purchase Invoice. Responses were mocked; no new financial posting is claimed. Async timing in the fixture was corrected to model a network response.
- Actual development-site Desk hooks include the new script; its public asset returned HTTPS 200 with normal certificate verification.
- Moyours cache cleared and only development web process refreshed successfully. Initial verification commands used an unavailable env-local Bench path and the wrong Frappe working directory; corrected to installed Bench and sites directory, then passed.

## Data, cleanup, limitations and release impact

No schema migration, finance permissions, approval settings or business records changed. No QA users, invoices or payments were created. Native View completion remains available. Existing backend financial posting/rollback tests and controls are reused; this adjustment verifies the shortcut with mocked completion rather than posting a real bank transaction. No live Boost changes or production deployment. Reload Desk to load the new asset. Temporary browser fixture resides under /tmp/test_sports_context.cjs.
