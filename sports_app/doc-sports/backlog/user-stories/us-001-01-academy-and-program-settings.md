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
