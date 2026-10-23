# Puzzle Terms Reference

## Scope

NEWGAMES-PUZZLE-TERMS adds `/puzzle-terms/`, a published, evergreen reference for nine terms used in the existing Sudoku, block and return-note guides. Each definition links to existing practice or explanatory context. The page is not a new game, news article, ranked recommendation or daily-content promise.

The six learning guides gain one `Puzzle terms` link beside their existing `Find another guide` link. The reference uses the same closed table of contents and existing abstract cover. It has no redundant self-link. Draft, future and expired reference pages are not linked by the partial.

A one-line safeguard in the existing guide stylesheet lets long content headings wrap at enlarged text sizes. The 320px/200% text check caught `Contradiction` overflowing before this fix. Normal-size typography and homepage styling are unchanged.

Classic Sudoku rules and hidden-single terminology were checked against Nikoli and Sudoku.com's primary explanations on 2026-10-23. Block definitions explicitly apply only to the local teaching rules. A return note is distinguished from saved game state. No named-game controls or features are inferred.

Homepage, blog inventory, existing publication dates and both blog/update RSS feeds are unchanged. Hugo's site-wide RSS also includes ordinary pages, so the new reference has its actual publication date rather than the undated default. No JavaScript, storage, account, image, dependency, analytics, Cloudflare setting or other repository change is included. Older artwork/design WIP is excluded.

## Acceptance

Use an isolated staged-source export. Run the repository checker, Hugo, existing validators and the new reference validator. Check canonical/robots/OG, sitemap, definition fragments, exact guide entry links and valid practice destinations. Confirm no homepage/blog-feed/update-feed changes and no tracked generated files. Check the new site-wide RSS entry uses the reference's real publication date.

Browser acceptance covers JavaScript-disabled mobile and desktop, keyboard navigation, the closed contents menu, direct heading fragments, guide-to-reference-to-example/back journeys and 200% text. Inspect mobile and desktop screenshots, then verify the same paths in production after the approved GitHub push.

Retention, reader comprehension, screen-reader narration and business impact are not measured by these checks.

## Pre-release Results

The isolated site checker, `hugo --gc --minify`, all seventeen static validators and RSS/update fixtures passed. All 66 HTML pages have valid internal links, fragments and image dimensions. The reference has nine term anchors and nine explanatory destinations; exactly six learning guides link to it. Existing exercises, dates, twenty blog records and both article feeds are preserved.

Chromium checks passed at 320, 390, 768, 1280 and 1440 pixels with JavaScript disabled: all six keyboard entry/back paths, closed contents menu and Space activation, all nine direct fragments, all nine practice/return journeys, and 200% text without horizontal overflow. JavaScript-enabled contents navigation also passed. Mobile and desktop screenshots were inspected.

Generated changes are limited to the reference page, six guide navigation areas, the one-line guide stylesheet safeguard, sitemap and site-wide RSS. Homepage, blog archive, update directory and both blog/update feeds are byte-identical to the previous release. No generated files are tracked or staged. Earlier redesign WIP remains local.
