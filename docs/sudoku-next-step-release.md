# Sudoku Next-Step Guide

Work: NEWGAMES-SUDOKU-NEXT-STEP
Date: 2026-10-23

## Reader Value

`/blog/sudoku-one-place-for-a-number/` follows the first-move guide with a different deduction: a digit has only one possible location in a group even though its cell has several candidates. Two original row snapshots contrast a justified placement with an unresolved choice. They are fixed learning examples, not a complete game, a daily puzzle feed or a named game's board.

The old Sudoku guide links forward and the new guide links back to its prerequisite. The Games & Guides learning path and puzzle category provide discovery links; the existing six-card homepage latest list and updates feed include the new publication automatically. No homepage section, layout, CSS, script, storage, tracking or dependency is added. Existing article dates stay unchanged; adding a follow-up link is not advertised as a substantive correction.

## Evidence And Validation

Rules and terminology reviewed against [Nikoli](https://www.nikoli.co.jp/en/puzzles/sudoku/) and [Sudoku.com's hidden-single explanation](https://sudoku.com/sudoku-rules/hidden-singles/) on 2026-10-23. No source grids, screenshots or example text copied. The sparse backing grids in `data/sudoku_places.json` are subsets of a constructed valid reference grid. They exist to verify the displayed candidate tables, not to claim a unique full puzzle.

`tools/check_sudoku_places.py` recomputes every candidate from row/column/box clues, checks that all row blanks are represented, enumerates row assignments, validates answer destinations and rendered cells, and rejects four corrupted fixtures. Existing shortcut/feedback validators include the new opt-in guide. Publication identity, sitemap, both feeds and internal links are checked against the isolated release.

Browser acceptance covers small/large viewports, initially closed explanations, mouse/keyboard disclosure controls, shortcuts, prerequisite/follow-up navigation, enlarged text, no horizontal overflow, native feedback email links and the unchanged six-card homepage structure. Build and production checks must exclude the pre-existing artwork/design WIP.

## Limits

No claim is made about named-game controls, scoring, saves, difficulty, popularity, measurable retention or revenue. Reader study, real email delivery and third-party RSS-reader polling are not established by these checks. The owner's current instruction authorizes choosing, validating and publishing this scoped guide; older unrelated redesign work remains outside this release.
