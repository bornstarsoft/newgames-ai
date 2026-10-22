# Game Introduction Learning Paths

## Scope

Added short, contextual reading paths to three existing introductions:

- DaySudoku: first-move Sudoku practice, then the one-place-for-a-number lesson.
- Blockzzle: Fit, Clear, Leave Space practice with three original teaching boards.
- Ringzzle: the general browser save checklist before ending a session.

The introductions retain their official play links. Learning examples are explicitly not game levels, solutions or demonstrations of game controls. The save checklist does not claim that Ringzzle saves a board or score; the new paragraph warns against testing with valued progress.

## Boundaries

No new article, homepage section, visual asset, template, script, storage, analytics, account or external service. Publication metadata and existing game claims are unchanged. No fabricated freshness or feature claim, and no other repository is modified. Earlier local redesign WIP is excluded from the staged release.

The 200% text check exposed an existing article-title/footer grid overflow on small screens (320px viewport, 423px page width both before and after the content edit). The existing guide-page `min-width: 0` and `overflow-wrap: anywhere` safeguards now also apply from the common stylesheet, allowing other articles to wrap rather than overflow. Only that rule is staged from the otherwise dirty common CSS file.

## Acceptance

Build the staged-source export with `./tools/check_site.sh` and `hugo --gc --minify`. Run `python3 tools/check_play_learn_paths.py` alongside existing validators. Check the new links with JavaScript disabled on mobile and desktop, including the two learning-guide return links and native answer disclosures. Compare generated output with the preceding release to establish the actual affected pages.

After the GitHub push, verify the new sections and destination pages on the production domain. Keep measured reader benefit separate from implementation acceptance: these links reduce the navigation steps to existing help, but retention or business impact has not been measured.

## Pre-Release Results

- Isolated staged build and all ten static validators passed, including RSS fixtures and the 64-page internal link/image/anchor check.
- JavaScript-disabled browser checks passed at 320, 390, 768, 1280 and 1440px: four guide destinations, two return links, keyboard activation, native answer disclosures, official play links and 200% text without horizontal overflow. Mobile and desktop screenshots were inspected.
- Generated changes are limited to the three introductions, the common CSS safeguard and the archive's automatically calculated DaySudoku reading time (2 to 3 minutes). Homepage HTML, sitemap, both feeds and all other generated files are identical to the preceding release.
- Frontmatter, original official links and published article count are unchanged. No generated files are tracked or staged. Diff whitespace checks passed. Deployment verification is recorded in the local project handoff after the push.
