# ADR-0001: Shared Boost console with separate app ownership

- Status: Proposed
- Date: 2026-11-01
- Related stories: sports_app:US-002-01, US-002-02, US-002-03
- Requirements: SPORTS-FR-019, SPORTS-FR-020, SPORTS-FR-021, SPORTS-NFR-001

## Context

The academy needs sports operations and full ERP in one staff console while retaining generic independent apps. Boost has an existing finance console, fixed view definitions, finance initialization and a Boost-role entry allowlist. The reviewed source has not established a supported third-party provider contract. Sports is currently a scaffold; Primero's brand-specific public website is reference material.

## Proposed decision

Use `/app/boost-console` as the staff host. Add a generic versioned installed-app provider interface in ERP Boost, and implement Sports navigation, lazy assets, views, context handlers and permission callbacks in Sports App. Keep finance/domain endpoints in their existing owner apps. Shell permission is composed from permitted installed modules; it does not grant financial access. Validate company selection and skip Finance initialization for Sports-only users.

Install the selected compatible apps on the same target site. Boost must run independently without Sports. No runtime dependency on Primero, hardcoded cross-bench paths, copied Boost shell, arbitrary admin-injected JavaScript, or second production console is proposed.

## Alternatives considered

- Separate Sports console: simpler initial isolation, but adds two staff entry points and duplicates navigation/context work.
- Copy or fork the Boost shell into Sports: quick reuse but creates divergent ownership and repeated maintenance.
- Merge Sports into Boost: one repository, but sacrifices the requested app separation and generic finance scope.
- Extract a new platform shell app immediately: viable future option if several providers justify it; premature for this first integration.

## Consequences and validation

Requires coordinated PRs, a compatibility contract, page-role/login changes and regression coverage. Provider errors must be isolated; disabling a provider should leave finance usable. Prototype the contract and validate Boost-only, combined, Sports-only and mixed-role journeys in US-002-01 before treating this decision as Accepted. Decide Sports' standalone installation support explicitly; this proposal commits only to the combined academy deployment profile.
