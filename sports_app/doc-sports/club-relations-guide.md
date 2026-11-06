# Club and partner relations

Open **Sports → Clubs & Partners** in the shared Boost console as Administrator, System Manager or Sports Academy Administrator. No new roles are granted automatically.

Use Organizations to search by name and filter by country/priority. The table shows public email and purpose where sourced; With email only filters to populated addresses. Search accepts organisation names or email addresses. View/edit opens the native form. Add a record with any sport and an appropriate organisation type; no football-only field is mandatory. Create opportunities for trials, recruitment, friendlies, exchanges or other work. Correspondence logs record subject, method, direction, notes and follow-up date. Saving never sends email. Opportunity/player links remain private; they do not authorise player-profile sharing.

## Priority assessment

- Unrated: staff have not assessed relevance.
-1: low priority;2: limited relevance;3: useful prospect;4: strong fit;5: immediate strategic priority.

A scored record needs a written rationale. The server records the assessor/date and tracks changes. This is an internal relationship-priority assessment, not a sporting rank, quality certification or claim that a club is safe/verified for minors.

## Directory and provenance

The starter contains171 distinct team/club records: Nigeria113, Germany18, Spain20 and United Kingdom20. Nigeria includes men's, women's and academy/team entries from a historical NFF cup listing plus the NPFL directory. International batches come from official league listings. Each record has its source URL, snapshot date and qualification. Sources confirm a listing, not current league membership, recruitment contact, an academy relationship or permission to contact anyone. Verify before outreach. No personal contact details or guessed public emails were imported.

Sources (reviewed2November2026):

- [NFF Federation Cup representatives](https://thenff.com/president-federation-cup-states-submit-representative-teams-in-men-and-women-competitions/)
- [NPFL club directory](https://npfl.com.ng/clubs/)
- [Bundesliga club directory](https://www.bundesliga.com/en/bundesliga/clubs)
- [LaLiga club directory](https://www.laliga.com/en-GB/laliga-easports/clubs)
- [Premier League official club listing in its2026/27 kit guide](https://www.premierleague.com/en/news/4658330/premier-league-club-kits-for-202627-season)

## Import operations

The packaged data is sports_app/data/club_directory.json. Explicit administrator import: call sports_app.relations_api.import_club_directory with the selected company, or invoke it through the development Bench console. There is no automatic after-migrate reseed. Reimports skip records by company-scoped identity and immutable seed identity; they never reset ratings, contacts or staff notes. Imports serialize on the selected Company row. A renamed seeded record is recognised by seed identity. Resolve organisation aliases manually before adding more source batches.

The initial development import retained171 prospects. No opportunity or interaction examples were retained. To reverse a directory import, review source-provenance records and linked activity before controlled cleanup; do not bulk-delete staff relationship history. Do not share profiles, guardian information, medical or financial details through an unapproved channel. Public portal, approval/consent-controlled submissions and external email integration remain separate work.

## Published contact enrichment — 2 November 2026

Initial enrichment adds14 published email addresses and5 official form/contact routes. Each email has its purpose, source URL and source-review date. Supporter-service, imprint and general office addresses are not confirmed recruitment contacts. No SMTP/delivery tests or messages were sent. Club restrictions appear in the table, including Enyimba's no-trials feedback-form rule. Where no email was sourced, a contact page is shown if available; an empty email is not a guessed address.

Reviewed contact data lives in sports_app/data/club_contacts.json. Explicit management-only enrichment uses sports_app.relations_api.enrich_club_contacts for the chosen Company. It fills blank contact groups and preserves staff-entered addresses/provenance; repeat calls skip existing contacts. Directory import remains separate, so newly imported clubs require an explicit enrichment call. The list of email sources and their qualification is retained per dataset row and in each populated organisation.

## Column sorting and combined filters — 2 November 2026

Organizations have a clearly labelled Organization or email search, Country, Priority and Relationship filters, plus With email only. Filters combine; Clear filters resets them. Click Organization or Country (or another sortable column) to toggle ascending/descending ordering; arrows and accessible header state show the direction. Sorting runs on the server across the full Company-scoped result set before 30-row pagination, with a stable record-ID tie-break. Changing a filter or sort returns to page one. Switching tabs clears tab-specific filters and sorting. Opportunities and Correspondence support sorting of their own text/status/date columns; the linked organization label there is not sortable. This avoids sorting by opaque linked IDs.
