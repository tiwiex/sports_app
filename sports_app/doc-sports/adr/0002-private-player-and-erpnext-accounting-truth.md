# ADR-0002: Private player aggregate and ERPNext accounting truth

- Status: Proposed
- Date: 2026-11-01
- Related stories: sports_app:US-003-02, US-003-03, US-004-01, US-004-03, US-005-03, US-007-01
- Requirements: SPORTS-FR-004, SPORTS-FR-005, SPORTS-FR-008, SPORTS-FR-010, SPORTS-FR-013, SPORTS-NFR-007

## Context

Primero's Player is publicly readable and named by full name, with football-specific fields. The new app needs a private central record, confidential exemptions, reliable monthly payments and biometric identity. Reusing that schema directly would conflict with private operations and create naming collisions if both apps were installed.

## Proposed decision

Use namespaced Sports DocTypes and immutable registration IDs, with same-name players allowed. Aggregate linked enrollment, obligation, attendance and restricted identity records through the private player page. Publish only explicit approved projections. Keep scholarship decisions separate and management-only, including API/export/search paths. Store opaque provider biometric IDs where possible, with live enrollment gated on the chosen provider and agreed retention/consent process.

Use ERPNext Sales Invoice, Payment Entry and authorized credit/refund/reversal flows as financial truth. Sports stores idempotent period obligations, player attribution and document links; summary statuses derive from submitted documents and allocations. For MVP, one player's obligation per invoice avoids ambiguous shared-payer attribution. Zero-due exemption periods are obligations, not pretend receipts.

## Alternatives and consequences

A single public/private Player DocType reduces initial schemas but risks disclosure. Name-based identity fails for duplicates and renames. A separate Sports payment ledger creates reconciliation drift. Proposed separation adds linking and derived-view work but keeps ownership and audit boundaries clear. Confirm payer model, zero-charge treatment, retention and correction behavior through stories before acceptance.
