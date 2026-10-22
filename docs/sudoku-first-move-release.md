# Sudoku First-Move Guide

## Scope And Approval

On 2026-10-23 the owner delegated suitable additional content and a return-visit improvement, with validation and production deployment. Publish one original beginner guide and three small answer-reveal exercises. Preserve previous artwork/layout WIP and the homepage structure. Retain the project-specific GitHub to Cloudflare Pages deployment exception.

## Editorial Basis

This fills a different reader need from the existing discovery, format-comparison and save-progress guides: finding a justified first move. The examples teach elimination and when not to guess. They are fixed educational examples, not a game engine, a complete puzzle, a daily challenge or a specific game's answers.

Classic rules were checked against Nikoli's primary rules page on 2026-10-23: https://www.nikoli.co.jp/en/puzzles/sudoku/ . No source examples, images or solution grids were copied. The DaySudoku rules page could not be retrieved through the web tool, so no new claims about its controls or features are made. The article links to the existing NewGames.ai introduction.

The three original clue sets are stored in `data/sudoku_practice.json`. Native HTML `details`/`summary` reveals answers without JavaScript. Explanations start closed, can be opened by keyboard, and do not store attempts. No scores, accounts, daily freshness claims, screenshots, ads, analytics or dependencies were added.

## Discovery

- Published route: `/blog/how-to-find-your-first-sudoku-move/`.
- Add one link to the puzzle category and one stable task-oriented link to `/updates/#handy-guides`.
- The unchanged homepage latest-post list includes the new article automatically.
- Reuse the existing puzzle-category illustration; article-only CSS styles tables and answer disclosures.

## Validation

Run the site checker and `hugo --gc --minify` on an isolated staged-source export, then `python3 tools/check_updates.py` and `python3 tools/check_sudoku_guide.py`.

The Sudoku validator computes candidate sets, verifies overlap consistency using an independently constructed valid reference, compares generated table values and answer text to the source data, and checks metadata, sitemap/RSS and discovery links. Browser checks cover native answer opening/closing by mouse/keyboard with JavaScript disabled, mobile/desktop layout, anchors and existing game links. Final QA and deployment results belong in the local project-status handoff.

No gameplay, user study, retention or revenue improvement is claimed. Future content should follow real reader questions rather than promise a daily exercise cadence.
