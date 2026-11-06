# Sourced club directory

club_directory.json is an opt-in starter dataset, not fixtures automatically reloaded on migrations. Source URLs/context and snapshot dates are recorded per entry. Public club/team names and country/region only; no images, guessed emails, personal contacts or priority scores. Names explicitly aliased between NFF and NPFL are canonicalised during preparation; men's and women's records remain distinct. See doc-sports/club-relations-guide.md for sources, limitations and import behavior.

club_contacts.json is a separate reviewed public-contact batch:14 published email addresses and5 contact-form/page routes. Publication and purpose are attributed; deliverability/recruitment suitability are not certified. No guessed or private individual staff emails. The explicit enrichment API skips existing staff contact/provenance fields.
