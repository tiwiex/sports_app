# US-009-01: Club and partner directory, opportunities and correspondence

- Epic: EPIC-009
- Requirements: SPORTS-FR-032, SPORTS-FR-033
- Status: In Review — development slice
- Date: 2 November 2026 (Africa/Lagos)

As an academy administrator, I want a sourced directory with staff-assessed relationship priority, opportunities and internal correspondence history so that club follow-ups and player opportunities have a visible record.

## Acceptance criteria

1. Sports Organization, Sports Opportunity and Sports Interaction use generic sport/type fields and Company scope. Management roles only; no Guest/player/ordinary registrar access is granted.
2. Native writes and direct APIs enforce the same restrictions and cross-company/link consistency.
3. Priority is Unrated or1–5 with rationale, current staff assessor and date. Imported records are Unrated; retry imports preserve staff fields and create no duplicates.
4. Source-attributed public Nigerian/international clubs populate a private prospect directory, without guessed contacts, partnerships or performance ratings.
5. Shared console offers Organizations, Opportunities and Correspondence tabs, filters and native modal forms. Recording an interaction does not send a message.
6. No automatic Customer/Supplier/User, invoice or external profile disclosure. A player nomination remains an internal link only.

[Build evidence](../../build-logs/2026-11-02-us-009-01-club-partner-relations.md). Live outreach, consent-controlled player submissions, club portal and partnership lifecycle remain later slices.

## Table and contact enrichment — 2 November 2026

Use table layouts for organisations, opportunities and correspondence. Retain name/country/priority filters and pagination; allow email search/email-only filtering. Published public role contacts retain their purpose, source and review date. Never imply a general/supporter email is a recruitment address, overwrite staff contacts or send messages during enrichment. [Adjustment evidence](../../build-logs/2026-11-02-us-009-01-table-and-public-emails.md).

## Column sorting and combined filters — 2 November 2026

Organizations have a clearly labelled Organization or email search, Country, Priority and Relationship filters, plus With email only. Filters combine; Clear filters resets them. Click Organization or Country (or another sortable column) to toggle ascending/descending ordering; arrows and accessible header state show the direction. Sorting runs on the server across the full Company-scoped result set before 30-row pagination, with a stable record-ID tie-break. Changing a filter or sort returns to page one. Switching tabs clears tab-specific filters and sorting. Opportunities and Correspondence support sorting of their own text/status/date columns; the linked organization label there is not sortable. This avoids sorting by opaque linked IDs.

Acceptance evidence: [Column filters and sorting](../../build-logs/2026-11-02-us-009-01-column-filters-and-sorting.md).

## Discovery provenance — 6 November 2026

- Origin: **Original baseline only** (including subsequent user direction); no direct questionnaire response establishes this story’s specific scope. Preserve existing state and acceptance evidence.
- Reconciliation: [BA-QNR-001](../../discovery/BA-QNR-001-reconciliation.md).
- Adjustment evidence: [Discovery build log](../../build-logs/2026-11-06-discovery-questionnaire-reconciliation.md).
- Existing delivery state and acceptance criteria remain unchanged; proposed changes require refinement before implementation.

Epic consolidation (6 November 2026): the [complete epic inventory](../epics/EPIC-009-club-and-partner-relations.md) now includes this story alongside baseline and questionnaire additions. State and acceptance evidence unchanged. [Build log](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
