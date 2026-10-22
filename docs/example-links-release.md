# Direct Links To Practice Examples

## Scope

The headings of eight original examples are native links to their existing section fragments: three first-move Sudoku checks, two next-step Sudoku snapshots and three block-placement exercises. Readers can follow a heading, retain that URL in a bookmark or share it, then return to the same example without replaying a session or finding it by scrolling.

No clipboard API, new storage, tracking, account, saved progress or daily rotation is added. Answers remain native closed disclosures on a fresh visit. Examples, title text, section IDs, ARIA labels, article URLs, dates and original content data are unchanged. The fragment identifies a location only, not an answer state or attempt history.

Only three shortcodes and two existing scoped stylesheets change. Links use the established blue, an underline and visible keyboard focus. Padding gives the heading link a larger target; scalable scroll margin keeps the section clear of the sticky header with enlarged text. Homepage and global styles remain untouched. Earlier local redesign WIP is excluded.

## Validation

Use the staged-source export for `./tools/check_site.sh`, `hugo --gc --minify`, all existing validators and `tools/check_example_links.py`. Confirm exact generated fragment URLs, unchanged labels/data, canonical pages and closed answers.

Browser acceptance covers click/Enter, direct URL entry in a new page, reload/back, normal/200% text, visible focus and no horizontal overflow at mobile/tablet/desktop widths. Inspect screenshots and compare generated scope before committing. Verify the actual production links, destinations and unchanged feeds after the GitHub push. No measured retention or revenue outcome is claimed.

## Pre-release Results

The isolated build and fourteen static validators passed. Browser checks passed at 320, 390, 768, 1280 and 1440 pixels with JavaScript disabled, including Tab focus, Enter/click, fragment reload/back, fresh-page arrival, closed answers and Space toggling. At 200% text size all eight example targets remain below the sticky header without horizontal overflow. Mobile and desktop screenshots were inspected.

Generated changes are limited to three practice-guide HTML files and their two scoped stylesheets. Homepage, sitemap and both RSS feeds are byte-identical to the preceding release. The initial focus assertion used programmatic focus after a mouse interaction; the test now uses Tab and Shift+Tab to verify actual keyboard focus visibility. No CSS workaround was needed.
