# Discovery source register

| Source ID | Document | Ingested | Integrity / status |
|---|---|---|---|
| BA-QNR-001 | Moyours Sports Academy Pre-Meeting Questionnaire, completed responses | 2026-11-06 (Africa/Lagos) | Original preserved; discovery evidence, not signed scope |

- [Response transcript](BA-QNR-001-responses.md) — stable question anchors, exact response wording and explicit blanks.
- [Reconciliation register](BA-QNR-001-reconciliation.md) — each question mapped to requirements/stories, origin, impact and decisions.
- [Archived original DOCX](BA-QNR-001-original.docx) — preserved bytes; DOCX is not rendered by Development Tools. Use the Markdown transcript in console modals.
- SHA-256: `815ccaece2f5f9c750a02a588dab5c73b5b4e8e30c53f888f2846a56f4fc865f`.
- Existing copies in `doc-sports/` and `doc-sports/backlog/` have the same hash and were left untouched. The blank respondent/date fields do not establish author identity or completion date. Ingestion date is not document completion date.

## Provenance rules

Use **Original baseline only**, **Questionnaire only**, or **Both** separately from assessment (**Confirmed**, **Expanded**, **Changed**, **Conflicting**, **Needs clarification**, **New**, or **Context**). “Original baseline” includes subsequent accepted user direction; preserve detailed historic provenance in requirement baseline and build logs.

Question IDs retain printed numbering: `BA-QNR-001-Q02-03` means original question 2.3. New questionnaire versions receive a new source ID and link to their predecessor. Never overwrite source evidence or reuse retired requirement/story IDs. Preserve blanks, ambiguous answers and conflicts; questions/examples alone are not client commitments. Copy provenance to any split story. New requirements/stories remain Proposed until policy, acceptance, dependencies and commercial impact are reviewed.

All existing stories carry a provenance section; new discovery stories include source references in Traceability. Reconcile against current REQUIREMENTS and implemented evidence, not only the initial brief. No production behavior changes follow automatically from discovery.

## Access

These documents include internal client responses. Sports Development Tools already recursively lists Markdown under this folder behind management-only permissions, sanitized modal rendering and allowlisted paths (story status/MoSCoW alone has a separate audited edit service); no public website route is introduced. The original DOCX is intentionally excluded from that viewer.
