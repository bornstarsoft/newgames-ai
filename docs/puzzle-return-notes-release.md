# Returning To A Puzzle

## Content Decision

Published an original practical guide at `/blog/return-to-a-puzzle-after-a-break/`. It covers remembering reasoning, distinct from the existing guide about persistence of browser-game state. The checklist separates certain work, unresolved questions and the next check; fictional notes are not valid puzzle boards or named-game solutions.

The guide explicitly says notes, bookmarks and screenshots are not restorable saves. It warns against reloading valued progress for a test and asks readers to verify the current puzzle/position before using old notes. No named-game feature, medical/psychological benefit, ranking, release, pricing or popularity claim. No copied material or external images. Existing abstract category artwork, table of contents and email feedback reused.

## Discovery And Scope

- Games & Guides: one link in the existing return path, with a clearer distinction between saving and remembering.
- New & Updated: the automatic latest list and one durable useful-guide entry.
- Web Games and the save checklist: brief contextual links; existing article dates unchanged.
- Homepage: existing six-article latest list rotates automatically, no new section or template change.

The owner authorized choosing content and return-visit improvements, validation and production deployment. Earlier design/artwork WIP stays excluded. No CSS, layouts, scripts, dependencies, tracking, accounts, Cloudflare setting or other repository changes.

## Acceptance

Validate an isolated staged-source build using `./tools/check_site.sh`, `hugo --gc --minify`, all existing checkers and the new guide checker. Confirm metadata, canonical, sitemap, both feed entries, the complete archive, contextual paths, native feedback, no new executable JavaScript and no unpublished/generated files in the commit.

Check the checklist/table of contents, category/guide/save return paths, mobile/desktop and 200% text in a browser; inspect live output after the GitHub push. Reader benefit, retention, email delivery and external RSS-reader polling are not measured by these acceptance tests.

## Pre-Release Results

- Both isolated Hugo builds and all thirteen static validators passed, including 65-page link/image/anchor checks, the complete twenty-article archive, six scoped feedback areas, visible-update fixtures and RSS fixtures.
- JavaScript-disabled browser checks passed at 320, 390, 768, 1280 and 1440px: closed table of contents, keyboard activation, five-item checklist, fragment reload/header clearance, 200% text, native mailto context, save-guide return loop and three contextual entry paths. Mobile and desktop screenshots were inspected.
- The first enlarged-text check found one long heading overflowing at 320px. Shortened it to "Check Saving First" and reran all checks successfully; no CSS adjustment was needed.
- Homepage remains the same six-card latest layout with all three official game links. No new section or interface feature. Existing source publication dates and game descriptions were not changed. No generated files are tracked/staged; diff whitespace checks passed.
