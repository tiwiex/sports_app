# Build log: EPIC-004 scholarships and monthly billing

- Date: 2026-11-06 (Africa/Lagos)
- Story / epic: US-004-01/02/03 / EPIC-004
- Requirements: SPORTS-FR-007/008/009/010; SPORTS-NFR-002/003/004/007
- Affected apps / branch: Sports App only / story/epic-004-scholarships-and-monthly-billing
- Status: Verified development slice; three stories In review, expanded epic not Done
- Pull requests: None for this implementation yet.

## Intended outcome and starting context

User authorized EPIC-004 after Sports PR #3. Explicit answers: academy administrators approve/revoke, unassigned Sports Finance reads scholarships and runs billing; coaches have no scholarship access. Full monthly fee for active-at-calendar-month-start memberships. Retain NGN250,000 public enrollment fees and configurable NGN40,000 monthly default. Generation is manual, draft-only, with no posting or automatic emailing.

## Policy decisions and plan

Separate restricted, effective-dated scholarship decisions and benefits from financial previews; reject overlapping approvals, preserve immutable issued charges, stop for mid-month concession changes and suspended membership exceptions. Fee plans require explicit native accounting mappings and month-aligned effective dates. Deterministic monthly enrollment keys, source-revision checks and per-row transaction rollback protect generation/retries. Zero-due obligations have no invoice or receipt. Native ERP permissions remain required; no automatic assignment or general finance grant.

## Work performed

- Added Sports Scholarship Decision, Sports Fee Plan and Sports Billing Obligation, plus the read-only/no-copy unique Sales Invoice monthly-obligation reference. Install/migrate hooks create the approved unassigned Sports Finance role before metadata synchronization. No user receives it automatically; no native finance rights are added.
- Added app-owned billing policy/access, scholarship, plan, preview/generation and console API modules. Restricted decision state follows native draft/submit/cancel with management actor/time and reasoned revocation. Approved records cannot overlap or be overwritten, deleted or renamed; ordinary sharing cannot grant access outside the explicit capability. Company/User Permissions and native field projections apply. Supporting attachments to decisions are disabled.
- Explicit monthly plans validate native program/company currency, non-stock service item, income ledger and cost center, due day and month-aligned validity. Final financial previews contain no decision IDs, scholarship reasons/status or benefit flags.
- Deterministic company/enrollment/month keys, preview revisions, settings/Player locks, immutable invoice snapshots and per-row rollback protect draft generation. Zero-due obligations create no invoice/receipt. Later decisions do not reprice an issued obligation. Native invoice submission/payment remains separate; no scheduler or app-triggered emailing is added. Unrelated invoices return immediately from new scoped hooks.
- Added the Sports-only Scholarships & Billing provider/view and content-addressed asset, with lists, modals, decision context actions, monthly preview, manual generation, independent paging and optional existing watcher integration. Existing host console roles remain unchanged.
- Added billing guide, requirement/PRD policy decisions and questionnaire reconciliation; synchronized the three stories, epic and consolidated inventory to In review with evidence. The original questionnaire transcript and earlier evidence are preserved.

## Commands and observations

- Full Python suite: **213 checks passed**, including 17 new billing checks beyond the prior 196. Covers calendar boundaries, eligibility, amounts/rounding, concession types/overlap, due dates, restricted read/share/approval boundaries, immutable provenance, native creation rights, disabled-monthly switch, Company currency and field projections.
- Actual `billing.js` Chromium fixture passed at **1440px and 390px**: explicit preview/generation (no automatic call), NGN display, zero-due/exception rows, explicit plan mapping, restricted decision view/approve/revoke, finance read-only controls and no outer overflow/page errors. APIs/Dialogs are synthetic, not authenticated end-to-end.
- Native Moyours QA used synthetic players/program/accounts, disabled no-password/no-mail users and **blocked commits**. Approved/revoked decisions recorded correctly; overlap denied. Full exemptions created no invoice. Positive rows created one draft invoice; unchanged retries reused it. Stale source and deliberately failed invoice insertion left no orphan obligation. Invoice changes and later decision repricing were blocked; no Payment Entry/GL posting.
- Native registrar/finance/management/Guest access verified. A temporary finance-only User Permission scoped to one test player filtered previews and denied an out-of-scope generation request at native permissions. No real user permission was changed. A separate native DB connection remained blocked while the first held the common settings lock and acquired it only after rollback; this verifies serialization, not a broad parallel load benchmark.
- All tracked before/after counts restored after guaranteed rollback: program, Customer Group, Player, Enrollment, Customer, Contact, User, User Permission, scholarship, plan, obligation, Sales Invoice, Payment Entry, GL Entry and File. Temporary QA user caches cleared. No mail/password/login sessions, real player edits, persisted QA plans/decisions/charges or role assignments.
- Pinned pre-commit syntax/JSON/import/format/Prettier/ESLint passed. Frappe Semgrep feature scan: **0 findings** after adding typed endpoints and removing the functional-map style finding.
- New Sports metadata, unassigned role and invoice reference synchronized only on development. Published Sports assets and cleared development cache with **no Boost import/call, role sync or DB commit** in the publishing step. Restarted only the development web process. HTTPS asset returned 200 and matched source; Guest configuration API denied access.
- Native read-only smoke checks confirmed zero real plans/decisions/obligations/monthly invoices and zero Sports Finance assignments. Billing guide and all three updated stories are discoverable through Sports Development Tools. Development and live Boost worktrees remain clean.

## Verification evidence

| Acceptance criterion | Check | Result |
|---|---|---|
| Restricted scholarship approval/revoke/history | Native role/state/overlap and unit/field projection checks | Passed |
| Explicit validated fee plans and private charge preview | Unit/native/browser checks | Passed for accepted prototype policy |
| Retry/serialization/zero-due/rollback | Unit, native retry/failure and two-connection lock checks | Passed; no claim of parallel load testing |

## Decisions, deviations and recovery

Initial fixture validation required the program's existing sport; native draft creation also required preserving explicit posting date (`set_posting_time`) and the site's mandatory remarks. These were corrected and the native suite passed; no native validation was bypassed.

Automatic approval review rejected an optional call to the existing Boost page-role synchronization contract because Boost-related changes need separate prior approval. That action did not execute. The safer activation removed that call and retained all existing provider/host console roles; finance users require an existing Sports Console/Registrar capability in addition to Sports Finance and native scope. No blocked host change is required for the current Administrator review, and no extra approval is being requested for omitted work.

Scholarship eligibility, kit/trip/trial/tournament benefits do not automatically post stock or grant payment-free admission. Unanswered expiry and admission-exception policies remain explicit follow-ups. No periodic scheduler or automatic invoice submission/email.

## Remaining work and release impact

Available for review at **Sports → Scholarships & Billing** on Moyours development after reloading the console. Create an explicit fee plan (including due day and native mappings) before generating; no live billing plan or charges were seeded. Native accounting and player read/create permissions remain separate prerequisites.

Stories US-004-01/02/03 are In review with implementation evidence. Installments, grace/notice/refund rules, payment-free scholarship admission and benefit fulfillment remain explicit follow-ups; the full expanded epic is not marked Done. Public enrollment fees stay unchanged. No production deployment, commit, PR or merge was requested for this implementation turn. Normal Sports migration and asset publication are needed when releasing elsewhere.
