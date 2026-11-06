# Build log: BA questionnaire provenance and backlog reconciliation

- Date: 2026-11-06 (Africa/Lagos)
- Stories / epics: existing Sports backlog; new US-003-04, US-005-04, US-005-05, US-006-05, US-008-04
- Requirements: existing mapped SPORTS-FR/NFR IDs; proposed SPORTS-FR-038–042
- Affected app / branch: Sports App documentation / `story/us-007-01-fingerprint-preparation`; prior pending work preserved
- Pull requests: None; no commit, merge, push or release requested
- Status: Verified documentation reconciliation; policy and implementation approval remain pending

## Intended outcome and starting context

Import the BA's completed questionnaire and distinguish prior scope, questionnaire-only scope and overlapping evidence. Two existing DOCX copies were found in doc-sports and backlog; both have identical bytes. Existing requirement/story IDs, delivery states and historical evidence must remain intact.

## Policy decisions and plan

Assign source BA-QNR-001, preserve original bytes and hash, extract exact questions/responses with stable printed-question references, and reconcile each response. Do not infer policy from blank/TBD/N/A responses, embedded examples or ambiguous Yes answers. Record proposed impacts separately from live behavior and commercial commitments.

## Work performed

- Archived original DOCX under discovery, with source register, SHA-256 and byte-identical source-copy verification. Original copies remain untouched; respondent/completion metadata is blank, so only ingestion date is recorded.
- Extracted all 82 numbered questions/responses into a Markdown transcript with BA-QNR-001-Qxx-yy anchors and retained supporting-document checklist. Blank answer 3.7 explicitly marked unanswered.
- Added a complete question-level reconciliation register: requirements, linked stories, origin, assessment and required decisions. Listed original-only functional requirements separately; silence does not remove prior scope.
- Added provenance to all existing stories; existing states and acceptance criteria preserved. Added five Proposed stories with source references, dependencies, draft acceptance and verification criteria: performance assessments, native ERP procurement/player kit distribution, arrival/departure/absence review, email reminders/receipt delivery and gateway discovery/reconciliation.
- Registered proposed SPORTS-FR-038–042 in requirements/baseline; linked affected epics, PRD, document/backlog indexes and story template; documented ongoing source-reconciliation process.
- Explicitly retained fee, admission, numbering, role and disabled-user behavior pending decisions. Flagged conflicts involving fee composition, partial-payment registration, scholarship authority/privacy, parent portal, hardware/consent/retention, billing cadence, support and phased priorities.
- Discovery Markdown is already covered by the existing protected recursive Development Tools viewer and sanitized modal rendering. No new public route, API/category changes or DOCX rendering added.

## Commands and observations

- Parsed DOCX tables with Python ZIP/XML; 82 unique question IDs and exactly one reconciliation entry each.
- Verified source archive and both supplied copies are byte-identical; SHA-256 recorded in discovery/README.md.
- Verified discovery links/anchors, 33 story files with origin metadata and five new proposed stories.
- Existing documentation endpoint suite: 6 tests passed (management gate, traversal/symlink restrictions, discovery, sanitization, assets and size limits).
- Exercised Development Tools functions with document root/authorization patched: all three discovery Markdown documents listed and rendered; archived DOCX excluded. This is isolated verification, not an authenticated live browser test.
- `git diff --check` passed.

## Verification evidence

| Criterion | Evidence | Result |
|---|---|---|
| Preserve source and exact responses | [Source register](../discovery/README.md), [transcript](../discovery/BA-QNR-001-responses.md), byte/hash comparison | Passed |
| Classify overlaps and new scope | [82-row reconciliation](../discovery/BA-QNR-001-reconciliation.md), story provenance | Passed |
| Keep proposed changes distinct from implementation | Current states preserved; five additions Proposed; conflicts recorded | Passed |
| Discoverable protected documentation | Existing six endpoint tests and isolated real-document list/render check | Passed |

## Decisions, deviations and recovery

No source deletion, database/schema/role/configuration change, business-data import, email delivery, hardware validation or application code change. No temporary accounts/records created, so no cleanup needed. No migration/rebuild/restart required. Prior dirty work retained. No external fact checking was needed: the ZK-9500 name is reported as client-supplied evidence only, with compatibility explicitly unverified.

## Remaining work and release impact

Review the decision queue with BA/stakeholders and obtain the listed supporting documents. Resolve fees, authority, timing and acceptance before scheduling implementation or changing current rules. Questionnaire budget/go-live TBD does not alter the NGN7M/eight-week proposal. Proposed stories are unestimated and not a claim that the enlarged scope fits that budget or schedule. Existing completed stories are not reopened merely by attaching discovery provenance; changed behavior should receive a separately approved implementation slice and build log.
