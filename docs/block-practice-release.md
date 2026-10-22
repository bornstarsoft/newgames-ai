# Block Placement Practice

## Scope And Approval

On 2026-10-23, the owner authorized choosing suitable content and a return-visit improvement, validation and production deployment while keeping the homepage simple. This release publishes one original learning guide, rather than another general game-selection article. The existing project-specific GitHub to Cloudflare Pages deployment exception remains applicable.

## Reader Value

`/blog/block-puzzle-fit-clear-leave-space/` separates three decisions: checking every cell of a piece, identifying simultaneous line clears, and preserving room for the next shape. Three original 4-by-4 teaching boards have explicit local rules, coordinate labels and initially closed answer explanations. Symbols distinguish occupied and empty cells without relying on color. These are fixed exercises, not a daily game or a simulation of a named game's rules or controls.

Links are added to the existing learn path on `/blog/`, useful guides on `/updates/`, and puzzle category. The existing six-item latest-article list picks up the new article automatically. Homepage layout, shared CSS, navigation, game introductions and official play links remain unchanged. No new homepage section is added.

## Boundaries

The guide makes no new named-game facts, ranking, score, popularity, price, release-date or platform claims. The existing puzzle-category illustration is reused and described as abstract art. No screenshots, external assets, JavaScript, browser storage, accounts, analytics or dependencies are added. The board data is rendered at build time; there is no game engine or user-data collection. Older artwork and layout WIP remains outside this release.

## Verification

`tools/check_block_guide.py` independently calculates each placement, row/column clear and remaining occupied cells. It exhaustively checks the next square's possible positions and validates the exact rendered grids, answer text, table headers, closed disclosures, canonical/index metadata, sitemap/RSS and discovery links. Run it alongside the existing build, updates, Sudoku and guide-finder checks against an isolated staged-source export.

Browser checks cover small and large viewports with JavaScript disabled, board legibility, closed answers, mouse/keyboard disclosure controls, table-of-contents targets below the header, return links and existing game links. Production checks must follow the Cloudflare Pages success result. Record results in the local project-status handoff; no retention or revenue improvement is claimed without measurement.
