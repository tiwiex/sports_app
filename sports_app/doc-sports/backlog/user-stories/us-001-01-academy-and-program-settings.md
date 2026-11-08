# US-001-01: Configure academy and program defaults

## Header

- Epic: [EPIC-001](../epics/EPIC-001-academy-configuration-and-access.md)
- State: Done
- Priority: Must
- Delivery owner / affected apps: Sports App

## Story statement

**As a** academy administrator, **I want** to configure academy identity, company, programs, groups and enrollment defaults **so that** a second academy can adopt the app without editing code.

## Traceability

- Requirements: `SPORTS-FR-001`, `SPORTS-FR-006`
- Dependencies: None
- Planned branch: `story/us-001-01-academy-and-program-settings`
- Planned build log: `YYYY-MM-DD-us-001-01-academy-and-program-settings.md`
- PRD: [Product requirements](../../PRD.md)

## Notes and scope

This story covers the outcome and acceptance criteria below. Resolve applicable PRD open decisions during refinement. Use app-owned models and existing ERPNext transaction behavior; no duplicated accounting ledger or copied staff console. Existing source patterns are reference material, not completion evidence.

## Acceptance criteria

1. Given two academy fixtures, when each is configured, then names, sports, groups, currency, timezone and numbering use their own settings without code changes.
2. Given a company outside the operator’s permission scope, when it is selected through UI or API, then the setting or action is rejected.
3. Given missing fee or program defaults, when setup is saved or dependent work is started, then validation identifies required configuration without silently selecting a client-specific company.

## Verification plan

- Positive path plus relevant denied-role, invalid-input, retry/concurrency and correction scenarios from the acceptance criteria.
- Use fixtures and a designated development/test site; record app versions and policy decisions used.
- Add meaningful automated coverage for financial integrity, confidentiality, identity and device processing as applicable; use manual review for content/layout where sufficient.
- Link evidence to each acceptance criterion, update the requirement baseline and record any ADR changes.

## Completion evidence

- Pull request(s): Not opened.
- Build log: [Delivery evidence](../../build-logs/2026-11-01-us-001-01-academy-and-program-settings.md).
- Verification summary: 45 combined Python checks and two existing JavaScript suites pass; real configuration roundtrips, company-scope validation, denied-role API/menu checks and browser save/read-back are recorded in the build log.
- Remaining decisions / follow-up work: User accepted local commit and merge into develop. Academy staff must choose real program/group and fee defaults; website publishing and fee-plan/billing rules remain later stories. The supported configuration is one academy per site.


## Refined delivery scope

- Three Sports-owned DocTypes: single Academy Settings plus company-scoped Program and Group masters.
- Sports → Academy Settings contains the setup form, registration preview and program/group create/edit dialogs.
- System Manager or Sports Academy Administrator can configure; basic Sports Console users cannot access settings. The configuration role can read company/currency masters and has no accounting transaction rights.
- Company scope is enforced server-side, including direct API/native form writes. Default program/group must be enabled, belong together and match the settings company.
- Required settings are enforced on Save. Monthly fees require a positive default amount unless explicitly disabled; saving does not implement pricing plans or create charges.
- Registration prefix/digits and enrollment status are defaults for later player/enrollment implementation. They do not allocate or renumber any existing player ID.
- Native forms remain available for authorized support. ERPNext is required for the linked masters; Boost remains optional outside the shared console deployment.

## Chart of Accounts compatibility adjustment — 1 November 2026

Restored missing native Account permissions in development ERP Boost while preserving Sports-only read restrictions and all existing custom rules. Administrator can create/edit child accounts after reloading Desk. [Repair, regression checks and cleanup evidence](../../build-logs/2026-11-01-us-001-01-coa-native-permissions.md). No Sports runtime/schema changes.

## CoA balance repair — 1 November 2026

[Diagnosis, applied repair and verification](../../build-logs/2026-11-01-us-001-01-coa-balance-diagnosis.md): missing native GL read rules hide balances for the finance user; an absent optional Purchase Invoice workflow column also breaks console lists. The user approved both repairs; missing native GL rules were restored, optional workflow columns/filters are handled, and browser balances plus console lists passed verification.

## TLS hosting readiness — 1 November 2026

[Certificate activation diagnosis and staged validation](../../build-logs/2026-11-01-us-001-01-moyours-tls-activation.md): certificate issuance succeeded, but active Nginx uses a stale copied configuration without Moyours. After explicit user approval, the active configuration was backed up and linked to the validated generated configuration, and shared Nginx was gracefully reloaded. Public TLS hostname/trust verification, HTTP-to-HTTPS redirection and Chromium academy loading passed; the certificate expires on 30 January 2027.
## Payment review recipient setting — 3 November 2026

Academy Settings now includes comma-separated Payment review email addresses for website payment claims. Blank disables notifications. See [US-005-01 notification build evidence](../../build-logs/2026-11-03-us-005-01-payment-review-emails.md); Finance permissions are unchanged.

## Discovery provenance — 6 November 2026

- Origin: **Both** — existing baseline/user direction and BA-QNR-001. Overlap does not imply every questionnaire detail is delivered.
- Source references: [BA-QNR-001-Q01-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-04), [BA-QNR-001-Q02-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-12).
- Impact: Expanded / needs clarification.
- Proposed refinements / open decisions:
  - BA-QNR-001-Q01-04: One current location; age bands U6/U8/U10/U13/U15/U17. Confirm progression criteria and shared-session grouping; do not hardcode football bands.
  - BA-QNR-001-Q02-12: One current location; age bands U6/U8/U10/U13/U15/U17. Confirm progression criteria and shared-session grouping; do not hardcode football bands.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-001-academy-configuration-and-access.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-107558b70445.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-5cb603210414.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-55f190ef493d.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-a7991ce0fe71.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-4c73ea708705.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-e47274efd0fb.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-9fbbe20dc4cb.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-9250c48b7f5c.md).

Review tracking: [2026-11-06 status / MoSCoW update](../../build-logs/2026-11-06-us-001-01-review-91b452feaae8.md).

Enrollment naming series refinement: native and console settings now expose the configurable application reference with default `MSA-ENR-.YYYY.-.#####`. [Build evidence](../../build-logs/2026-11-06-us-003-01-configurable-enrollment-series.md).


## Legacy player import and numbering setup — 6 November 2026

Player setup refinement: Academy Settings exposes the existing player prefix/digit width plus **Player starting sequence**, a positive whole-number minimum (default 1). Set 126 to continue after legacy sequence 125. The Company counter uses the highest of the configured minimum minus one, existing issued counter and matching imported player suffixes. Changing prefix/month/year or lowering the minimum never resets numbering; existing player IDs and links remain unchanged. Enrollment application and invoice series remain independent.

Native Data Import is enabled for Sports Player, with import permission restricted to System Manager/Sports Academy Administrator roles and management checks enforced in the controller. Native Company/User Permissions still apply; imported Company must match the configured academy. Use Insert New Records with each legacy player number in the **ID** column. Preserve historical IDs verbatim; after successful insertion reserve the matching continuous suffix under the same settings/Series locks, including imports after the counter was already initialized. Nonmatching legacy formats are preserved without guessing their suffix; set the starting sequence explicitly after reconciliation. Blank IDs use automatic numbering. Do not merge duplicates or rewrite existing identities.

Player email/account validation and automatic separate Customer/disabled player User/shared guardian account preparation remain in force for imports. Imports create no invoices, receipts, balances or attendance history; create program memberships separately using staff tools. Missing/duplicate emails require source-data correction rather than placeholders or silent existing-account reuse. Obtain and review the real roster before an actual import; this adjustment prepares tooling and does not complete the migration/pilot story.

SPORTS-FR-001/004/024; SPORTS-NFR-003. User refinement of existing numbering and BA-QNR-001 legacy-roster discovery, not new questionnaire wording. [Build evidence](../../build-logs/2026-11-06-us-003-02-legacy-import-and-sequence-floor.md). Wider delivery states remain unchanged.

## Tabbed Academy Settings — 6 November 2026

Group existing controls into General, Player IDs, Enrollment defaults, Monthly fees, Website payments and Programs & groups. Keep Save Settings available across tabs and preserve all unsaved values, numbering preview, native validation and master-management dialogs. Accessible keyboard navigation and phone scrolling are required. Existing Done state remains; [adjustment build log](../../build-logs/2026-11-06-us-001-01-tabbed-academy-settings.md).

## Accepted Item-pricing refinement — 7 November 2026

Enrollment charges are selected existing sales Items with quantity/rate rows in Academy Settings, driving public labels and native invoice lines. Monthly plans optionally reuse a one-month, company-currency Fixed Rate ERPNext Subscription Plan and its service Item/rate. Manual previews, immutable snapshots, scholarship privacy and native approval/payment controls remain in force. No native automatic Subscription is created. Migration preserves the current enrollment total; row edits affect new applications only. Verify arbitrary charge counts/quantities, unchanged retries, native Plan read permissions and stale-price rejection. This adjustment does not close unresolved EPIC-004 policy scope or change story review state.

[Build evidence](../../build-logs/2026-11-07-us-001-01-configurable-enrollment-items-and-subscription-pricing.md) · [Setup guide](../../academy-setup.md) · [Billing guide](../../billing-guide.md).

## Main-table PDF refinement — 7 November 2026

Main Players/Enrollments expose permission-scoped document links/actions and elapsed age. PDF links open a modal with download fallback and use selectable Sports Academy Invoice / Sports Academy Receipt backend Print Formats. The Settings document logo is configurable; Moyours reuses its website crest. Native Company/Customer/document permissions and deliberate receipt-email confirmation remain authoritative. Do not change global print defaults or broader story acceptance state.

[Build evidence](../../build-logs/2026-11-07-us-003-03-main-table-finance-and-branded-pdf-modal.md) · [Operator guide](../../players-guide.md).

7 November refinement: Monthly fees settings now expose automatic submitted receivables, explicit start month and execution user. No role grants or native Subscription activation. [Build evidence](../../build-logs/2026-11-07-us-004-03-automatic-monthly-receivables.md).
