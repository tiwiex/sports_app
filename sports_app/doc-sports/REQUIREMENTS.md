# Sports App requirements

Current user decisions as of 2026-11-01 (Africa/Lagos). The [original brief](requirements.txt) is preserved. The [requirement baseline](concepts/requirement-baseline.md) lists all stable IDs and story links; the [PRD](PRD.md) describes the wider product and release gates. This document records current acceptance rules, not a claim that all planned functionality is complete.

| Requirement | Current rule | Evidence / delivery |
|---|---|---|
| SPORTS-FR-001 | Configure academy/company, sports programs/groups, currency/timezone, numbering and defaults without client-specific code. Enforce Company scope on UI and direct writes. | US-001-01, accepted into local develop |
| SPORTS-FR-004 / SPORTS-FR-006 | Permanent player ID and dated program/group enrollments; same-name people remain separate; corrections retain identity and history. | US-003-02, private slice in progress |
| SPORTS-FR-026 | One save creates one player, their own Individual ERPNext Customer/contact and the first enrollment. Copy supplied player name/email/phone. No payer chooser or shared-family account. All enrollments derive the player's Customer. | US-003-02 |
| SPORTS-FR-027 | Create/reuse a Customer Group whose name is the initial program's friendly name. Assign it to the newly created Customer. Use a valid existing tree root; never overwrite an incompatible existing group. Later enrollments do not silently reclassify an existing Customer. | US-003-02 |
| SPORTS-FR-028 | Expose Sports requirements, PRD, epics, stories, ADRs, build logs and guides in an app-owned, read-only Development Tools view of the shared console, matching Boost cards/counters/tabs with documents in modal popups. Management roles only; no Finance role required. | US-002-04 |
| SPORTS-FR-029 | New players require a valid unique email and receive an automatically linked, disabled Website User with only the non-Desk Sports Player role. No welcome email, password or activation; future self-service access is a separate workflow. Existing accounts are never silently reused. | US-003-02 |
| SPORTS-FR-019 / SPORTS-FR-020 | One optional Boost console, with separate app ownership and a versioned provider interface. Finance-only/basic Sports users must not gain private player or management-document access. | US-002-01 accepted; US-002-02/03 planned |
| SPORTS-NFR-003 | Registration retries/concurrent requests create no duplicate player, User, Customer, contact or initial enrollment. Validation failures leave no partial records, including program-category creation. | US-003-02 |
| SPORTS-NFR-006 | Friendly program/group names in controls and profiles; usable desktop/phone workflows. Preserve internal IDs. | US-003-02 and later UI stories |
| SPORTS-NFR-009 | Every story delivery and every adjustment/fix/refinement receives its own dated, indexed build log with actual verification, data impact, limitations and cleanup. | Repository AGENTS.md; US-002-04 |

## Background creation and permissions

Registrar authority covers a narrow server operation that creates the player's disabled User, Customer, contact and program category. It does not grant general accounting, Customer Group, Customer or Contact write privileges. ERPNext validations still run. Preserve Company/User Permissions, immutable Customer linkage and stable registration IDs. Customer IDs derive from player IDs; display names are player names.

The program category is the initial registration classification because ERPNext has one Customer Group per Customer. Additional program enrollments retain it. Classification changes for existing accounting records require an explicit later workflow. Territory follows ERPNext Selling Settings, falling back to an existing territory matching the academy Company's country; missing master configuration raises a setup error.

## Remaining product scope

Public applications, full role boundaries, configurable publishing, fee plans/scholarships, player-attributed invoices/payments, attendance, biometric integrations and ERP launch acceptance remain the linked backlog. Registration creates no invoices, payments or ledger balances. Do not treat installed apps or a working form as complete financial delivery.
