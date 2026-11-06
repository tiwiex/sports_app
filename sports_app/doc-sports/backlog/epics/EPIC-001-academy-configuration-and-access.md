# EPIC-001: Academy configuration and access

## Outcome

A reusable academy setup and private operating boundary.

## Scope and success

- Retain reusable academy/company/program settings and server-enforced role/Company restrictions.
- Merge one-location/age-band configuration and admin/director/finance scholarship visibility discovery into setup/access stories.
- Keep the configurable HTML website; the withdrawn Next.js enrollment experiment remains historical.

## Stories

This is the complete current epic inventory, including proposed additions and withdrawn history. State is copied from each story as of 6 November 2026; a prototype does not establish full acceptance.

| Story | State | Origin | Priority |
|---|---|---|---|
| [US-001-01: Configure academy and program defaults](../user-stories/us-001-01-academy-and-program-settings.md) | Done | Both | Must |
| [US-001-02: Configure and publish academy website content](../user-stories/us-001-02-configurable-public-website.md) | In progress | Both | Must |
| [US-001-03: Define and enforce sports permissions](../user-stories/us-001-03-sports-role-and-data-boundaries.md) | In progress | Both | Could |
| [US-001-04: Dedicated enrollment PWA](../user-stories/us-001-04-enrollment-pwa.md) | Withdrawn — user clarified Next.js is for attendance | Original baseline only | See story |

## Exit criteria

Every linked story is Done with acceptance evidence, affected app pull requests and build logs. Demonstrate the combined workflow on the agreed test-site versions. Record unresolved scope as explicit follow-up work; no missing client requirement can be hidden by closing this epic.

US-001-02 prototype checkpoint: native `/academy` public preview is verified on the development site; content editor/publishing and production acceptance remain open. See [website PoC log](../../build-logs/2026-11-01-us-001-02-website-prototype.md).
## Consolidated discovery decisions

- Confirm age-band progression rules and role mapping; coach assessment does not grant scholarship visibility.
- Resolve parent portal No/TBD and website integration boundary without enabling dormant player Users.

- Epic origin: **Both**. Individual rows distinguish questionnaire-only additions from overlapping scope.
- Source responses: [BA-QNR-001-Q01-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-04), [BA-QNR-001-Q01-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q01-05), [BA-QNR-001-Q02-12](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q02-12), [BA-QNR-001-Q03-06](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q03-06), [BA-QNR-001-Q05-10](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q05-10), [BA-QNR-001-Q06-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-03), [BA-QNR-001-Q06-05](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q06-05), [BA-QNR-001-Q07-01](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-01), [BA-QNR-001-Q07-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-02), [BA-QNR-001-Q07-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-03), [BA-QNR-001-Q07-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q07-04), [BA-QNR-001-Q08-02](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-02), [BA-QNR-001-Q08-03](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-03), [BA-QNR-001-Q08-04](../../discovery/BA-QNR-001-responses.md#ba-qnr-001-q08-04).
- [Question-level reconciliation](../../discovery/BA-QNR-001-reconciliation.md); [consolidation evidence](../../build-logs/2026-11-06-backlog-consolidated-epics.md).
- Open decisions are proposed refinements, not permission, pricing, delivery-state or commercial changes. Resolve them before affected work becomes Ready.
