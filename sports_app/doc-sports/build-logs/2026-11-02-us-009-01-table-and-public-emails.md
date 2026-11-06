# Build log: Club tables and sourced public email contacts

- Date: 2 November 2026 (Africa/Lagos)
- Story / epic: US-009-01 / EPIC-009
- Requirements: SPORTS-FR-032, SPORTS-FR-033
- Status: Verified development adjustment / In Review
- Branch: story/us-009-01-club-partner-relations

## Request and work performed

Replace club cards with a table and find email addresses where applicable. Organizations now show name/team category, country, sport, priority, relationship, public email, published purpose and native View/edit. Opportunities and Correspondence also use tables. Existing pagination/country/priority filters remain, with alphabetical ordering, email-address search and With email only filter. Wide tables scroll inside their container on phones; data uses text nodes, approved web links and native modals.

Added Sports Organization fields for email purpose/source URL/source review date, official contact page and restrictions. Native URL scheme validation covers these URLs. Separate opt-in club_contacts.json enrichment fills reviewed gaps without overwriting staff email/provenance or ratings. Saved organisation seed identities match the directory, avoiding name-only cross-team matches. No automatic enrichment on migrations or outbound email.

## Sources and quality decisions

Prepared14 published role/club email addresses and5 contact-page/form-only records. Nigerian coverage includes a Plateau United address published by its youth league, explicitly qualified as league-published rather than independently club-confirmed. Other sources are official club sites or official Premier League directory pages. Each populated email retains its exact source URL, purpose and review date. Legacy Premier League URLs with unrelated-looking slugs were fetched and their actual club headings/address text checked before use. No personal staff addresses, guessed addresses, mailbox probes or delivery tests.

Enyimba's official feedback form explicitly excludes trial/player enquiries. Villarreal's privacy-rights mailbox, Arsenal shop-only addresses and Bayer04's superseded service address were not treated as general recruitment contacts; official contact routes were retained instead. Missing emails display Not published / not yet sourced. Published supporter-service/general office addresses are not labelled recruitment addresses. Full evidence is retained per record in sports_app/data/club_contacts.json.

## Actual verification

- Sports isolated suite:90tests passed; new checks cover enrichment preservation/idempotency, prevention of mixed staff attribution, URL validation and contact dataset matching/source metadata.
- Development schema reload added contact provenance fields. First enrichment updated19 existing organisations; repeat updated0/skipped19.14 records now have email addresses. Organisation/Customer/User/SalesInvoice/PaymentEntry counts unchanged.
- Chromium real provider with actual site catalogue: table headings,30-row paging,14-row email-only filter,1440/390/320px contained scrolling, correct mailto/source links, Enyimba restriction, tab-specific tables and cleanup passed. Improved cell wrapping/padding after screenshot inspection. No settings/data were edited by browser fixtures and no messages sent.

- Final development refresh: published current content-addressed asset, cleared cache and restarted only development web. Actual native email-only query returned14 source-attributed records; email search returned Manchester United correctly; repeat enrichment updated0/skipped19; asset HTTPS200 includes final table/filter code; Guest HTTP access denied.

## Impact and limitations

This is an initial reviewed contact batch, not exhaustive email coverage of171 clubs. Existing staff contacts are preserved; enrichment skips rather than overwrites. Publication checks confirm source visibility, not current delivery, recruitment suitability or permission to share player data. New schema/data and source changes are development-only. No live Boost changes, QAaccounts, external correspondence, commits, merges or pushes. Existing uncommitted work preserved. Temporary verification fixtures under /tmp contain catalogue fields only.
