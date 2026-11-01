# Guardrails, Development Tools and program Customer categories

- Date: 2026-11-01 (Africa/Lagos)
- Story / epic: US-002-04 / EPIC-002; adjustment to US-003-02 / EPIC-003
- Requirements: SPORTS-FR-026, SPORTS-FR-027, SPORTS-FR-028, SPORTS-NFR-002, SPORTS-NFR-003, SPORTS-NFR-009
- Affected apps / branch: Sports App, `story/us-003-02-player-numbering-and-enrollment`; Boost host unchanged
- Target: `moyours.ideltatech.com`, independent development bench
- Pull requests: None; changes remain uncommitted review work
- Status: Verified / In review

## Request and decisions

User requested repository agent guardrails, a build log after every story or adjustment, an exposed requirements/documentation hub like Boost Development Tools, background Customer creation without a remaining payer field, and program-named Customer Groups.

Each player keeps their own Customer, created in the registration transaction. The initial registration program determines Customer Group. Additional enrollments retain the original classification because ERPNext has one group per Customer; no existing accounting classification is silently changed.

## Implementation

- Repository-root AGENTS.md sets app ownership, designated dev bench, atomic player/Customer rules, role boundaries and mandatory dated/indexed build evidence for every adjustment.
- REQUIREMENTS.md records current user decisions, with stable IDs and links to the baseline, PRD and stories. Original client requirements.txt is preserved.
- Sports-owned Development Tools provider view lists requirements, PRD, epics, stories, ADRs, logs and guides, with search/category filters, sanitized Markdown and screenshot viewing. Read-only APIs enforce management roles and a resolved documentation-root allowlist, including rejection of traversal and external symlinks. Boost source is unchanged.
- Registration records an immutable initial program. Customer Group is created/reused using that program's friendly name inside the same transaction; parent-category collisions are rejected, and no general Customer Group write permission is granted.
- Derived enrollment Customer metadata is hidden from native forms/lists/print, with no payer selector. The internal link remains for compatibility and cannot be reassigned. The private profile exposes a read-only link to the already-created Customer.

## Verification

- 57 focused Python checks pass, including docs role enforcement, traversal/symlink denial, sanitized rendering, size/asset limits, program category company scope and incompatible-parent rejection.
- Real development-site checks passed: failed initial enrollment leaves no player/Customer/contact/program category; one program category is reused; Customer details, immutable links, same-name accounts and both concurrent request cases are correct.
- Sports-only, Finance-only and registrar-only profiles are denied documentation access. A configuration manager reaches Development Tools without Finance roles; requirements, category/search, adjustment logs, relative links and traversal rejection pass in the browser.
- Native enrollment browser check confirms the derived Customer field is hidden. Registration still uses friendly program/group names and has no payer selector.
- Both Boost JavaScript regression suites, new JavaScript syntax checks and Git whitespace checks pass.
- Development backup completed before targeted schema sync of Program, Group, Player and Enrollment. Cache clearing and development web reload applied metadata/endpoints. No live Boost code or global selling defaults changed.
- QA cleanup confirmed: temporary users/sessions, players, enrollments, auto-created Customers/contacts, program Customer Group and test masters removed; raw Academy Settings restored. Isolated documentation runs also deleted their single temporary account/session.

## Limitations and release impact

Management roles are System Manager and Sports Academy Administrator; registrar-only, basic Sports, Finance-only and Guest users cannot read project documents. Documentation is filesystem-backed and read-only; no live editable requirement DocType is introduced. Original planned public intake, complete profile histories and billing/attendance delivery remain open. No remote push, merge or production release is included.


## Findings and recovery

A browser failure exposed Frappe's normalization of hyphens in joined module paths: `get_app_path("sports_app", "doc-sports")` points to `doc_sports`. The endpoint now obtains the app root first and joins the literal documentation directory with pathlib. Added a regression against that normalization. The final management browser run passes. A registration search test was also waiting on a row already present before the asynchronous search completed; its selector now waits for the filtered result. Program/customer logic was unchanged by that test correction.

Markdown is always converted then sanitized. Tables retain readable column widths and horizontal scrolling on phones. Earlier full registration checks passed independently; only the documentation/browser checks were repeated after the isolated documentation fixes.

## Commands and artifacts

```sh
python -m unittest sports_app.tests.test_console sports_app.tests.test_academy_settings sports_app.tests.test_players sports_app.tests.test_development_docs erp_boost.tests.test_console_providers erp_boost.tests.test_console_optional_dimensions
node ../erp_boost/erp_boost/tests/js/test_console_providers.js
node ../erp_boost/erp_boost/tests/js/test_journal_entry_duplicate_reset.js
node --check sports_app/public/js/development_tools.js
git diff --check
```

Python checks use the development virtualenv with both application roots on PYTHONPATH. Temporary site/browser harnesses: `/tmp/sports_players_site_qa.py`, `/tmp/sports_docs_site_qa.py`, `/tmp/sports_development_browser_qa.js`; private credential files are deleted in finally cleanup. Browser uses the existing test-only HTTPS certificate bypass; existing socket/certificate environment errors do not affect the checked docs APIs.

Screenshots: [Development Tools desktop](assets/2026-11-01-development-tools-desktop.png), [phone](assets/2026-11-01-development-tools-mobile.png). The current requirements and this log are auto-discovered by Development Tools. Review is pending; no commit, push or merge is included.
