# Sports App agent guardrails

## Scope and ownership

- Read `sports_app/doc-sports/DEVELOPMENT_PROCESS.md`, `REQUIREMENTS.md`, the relevant story and its build log before implementation.
- Keep Sports models, APIs, business rules, documentation and console assets in Sports App. Boost owns the reusable console shell; use its provider contract. Do not copy the shell or import Primero at runtime.
- Use the independent development bench and designated `moyours.ideltatech.com` test site. Never edit the live Boost checkout as a shortcut to a development change.
- Preserve existing work and business data. Do not commit, merge, push or deploy to production unless authorized in the conversation. Existing authorization remains valid; do not ask repeatedly.

## Required build evidence

- Every completed story implementation AND every subsequent adjustment/fix/refinement must have a dated Markdown build log before reporting completion, even when no commit is requested.
- For each distinct adjustment, create a separate `sports_app/doc-sports/build-logs/YYYY-MM-DD-<story-id>-<adjustment>.md`; link it from `build-logs/index.md` and the affected story. Record client-local date (Africa/Lagos for this academy).
- Include request/outcome, story and requirement IDs, affected apps/branch, files/behavior changed, actual verification and results, data/schema changes, cleanup, limitations and release impact. Never invent a test result or claim a whole story Done for a partial slice.
- Keep requirements, PRD, story acceptance criteria and user guides aligned with accepted user refinements. Preserve historical evidence; clearly identify superseded decisions.
- Use `build-logs/TEMPLATE.md`. Build logs and current requirements must be discoverable through Sports Development Tools.

## DocType naming

- Prefix every new app-owned DocType, including registration/application and child-table types, with `Sports`. Reuse Sports Player/Sports Enrollment where suitable; do not rename ERPNext core DocTypes.

## Player and finance invariants

- Each player has one automatically created Customer, with the player's supplied name/contact details. Create player, Customer/contact and initial enrollment atomically; retries must not duplicate them.
- No manual payer selection or shared-family Customer model. Customer links are server-owned. Preserve immutable player IDs and registration provenance; same-name people remain separate players/accounts.
- Categorize a new Customer under a Customer Group named for the initial registration program. Further enrollments do not silently move existing accounting classifications.
- Show program/group names to operators while retaining stable internal IDs.
- Enforce roles, Company/User Permissions and validation in APIs and native controllers. Narrow background Customer/Contact/Customer Group creation does not grant general finance write privileges.
- ERPNext is the accounting source of truth. Ordinary registration creates no invoices/payments. The explicitly authorized enrollment Make Payment service creates an application-owned draft Sales Invoice and prospective Customer; an applicant claim moves the invoice to Pending Review without a Payment Entry or ledger posting. Only authorised Finance may complete payment, atomically submitting the invoice and its fully allocated receipt. Preserve legacy receipt references. Do not infer bank clearance from an applicant claim. Watch for upstream hooks that commit inside a supposed atomic operation.

## Verification and documentation access

- Run meaningful checks for privacy, Company scope, rollback, idempotency/concurrency and ERP linkage when changed. UI changes need browser checks at desktop and phone widths as appropriate.
- Use authorized temporary QA accounts only; revoke sessions and delete test accounts/data in guaranteed cleanup, restore temporary settings, and record the result without credentials or player PII.
- Documentation endpoints require an explicit management role, remain read-only, and serve only allowlisted app documentation. Reject path traversal/symlinks outside that root; sanitize rendered Markdown and handle links safely.
- Follow session permissions and approvals. These guardrails add no separate approval step for already authorized work.
