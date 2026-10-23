# Step-by-step Sudoku Candidate Checks

## Scope

The first-move Sudoku guide now shows a four-row candidate table inside each of its three existing answers: start with 1-9, check the row, check the column, then check the box. The tables are generated at build time from the original example data, with no duplicate answer data or client-side calculation. A short note explains unchanged lists and why several remaining candidates do not justify a guess.

Original clue groups, questions, answers, exercise fragments and publication date are preserved. No game-specific feature, full-puzzle solution or new technique is claimed. The conflicting-notes example and rechecking routine remain intact. The existing lastmod/updateNote now records this substantive addition while acknowledging the earlier improvement.

The initially closed answers keep the page compact. Existing table styling is reused; no homepage change, CSS, JavaScript, storage, image, dependency, analytics or account is added. Earlier design WIP is excluded.

## Acceptance

Build only isolated staged sources. Run the repository checker, Hugo and all existing validators. Independently recompute all twelve candidate sets from the clue groups and check ordered labels, table scopes, closed answer placement and preserved rechecking content. Verify keyboard/pointer disclosures, mobile/desktop and enlarged-text layouts, direct fragments, the finder journey, update notices and production deployment. These tests do not measure retention, comprehension or revenue.

## Pre-release Results

The isolated site checker, `hugo --gc --minify` and sixteen static validators passed. All twelve displayed candidate sets agree with independent set subtraction, including an unchanged step and the unresolved two-candidate example. Existing clue-group consistency, conflicting-notes math, block result boards and feed fixtures still pass.

Browser checks passed at 320, 390, 768, 1280 and 1440 pixels with JavaScript disabled, plus an enabled-mode reveal smoke. Exact cells/labels, closed answers, description associations, keyboard focus/Space, pointer close, reload, direct fragments, finder/back and 200% text without overflow were checked. Mobile/desktop screenshots were inspected. Actual screen-reader narration was not tested.

Generated changes are limited to the first-move guide, its automatic archive reading/update metadata, the update directory and affected sitemap/RSS metadata. Homepage, other articles, all stylesheets and source example data are unchanged. All twenty legacy RSS item identities, titles, order and publication dates are preserved. The current update event supersedes the earlier one in the existing latest-update-per-article feed model; the earlier rechecking content remains in the article.
