# Build log: Payments summary cards

- Date: 7 November 2026 (Africa/Lagos)
- Story / epic: US-005-02 / EPIC-005
- Requirements: SPORTS-FR-011, SPORTS-FR-012, SPORTS-FR-023
- Affected apps / branches / versions: Sports App, `story/epic-004-scholarships-and-monthly-billing`, current uncommitted development checkout
- Pull requests: None requested
- Status: Verified development refinement

## Intended outcome and starting context

User requested the Overview summary labels/cards on Payments too. Previously cards were rendered only by the Overview branch.

## Policy decisions and plan

Reuse the existing Overview API and native permission scope. Selected-year totals cover all visible enrollments, not only the current grid page/search results. Explain that distinction in the UI. Retain current enrollment count semantics.

## Work performed

`public/js/subscription_console.js` now loads Overview totals alongside the Payments grid in parallel and shares the four-card renderer across both tabs. Existing payment/reversal refresh paths reload the totals. Finance-denied users return before requesting totals. No changes to accounting, billing, permissions or APIs. Updated requirements, PRD, story, billing guide and log index.

## Commands and observations

- Scoped pre-commit checks: passed (Prettier, ESLint, conflict/whitespace checks).
- `test_subscriptions_browser.cjs`: passed at 1440px and 390px using synthetic APIs. Confirmed all four Payments cards, correct values, refreshed outstanding after payment and reversal, selected-year request, retained checkbox and denied-control behavior. Phone screenshot visually inspected; cards wrap without page overflow.

## Verification evidence

| Acceptance criterion | Check / artifact | Result |
|---|---|---|
| Same summary cards on Payments | Desktop/phone browser fixture | Passed |
| Totals refresh after financial actions and year changes | Synthetic payment, reversal and year request assertions | Passed |
| Read scope/payment behavior preserved | Existing scoped API reused; denied controls/checkbox assertions | Passed |

## Decisions, deviations and recovery

No data/schema changes, temporary accounts, cash movements or test records. Synthetic browser screenshots remain under `/tmp`. Existing checkout work preserved. No whole-story completion claim.

## Remaining work and release impact

Sports-only development assets published and cache cleared. HTTPS verification passed: billing assets returned HTTP 200 with exact JavaScript bytes; native configuration, overview and grid reads passed. No production deployment, commit, PR, merge, Boost or Community changes. Provider asset rollback can restore the prior JavaScript release without accounting changes.
