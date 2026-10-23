# Self-contained Practice Context

## Why

The practice finder and shared fragment URLs can bring a reader directly to an example, bypassing the article's introductory rules. The exercise must carry enough context to interpret its table without guessing what the numbers or board mean.

## Changes

All eight examples now have a short visible note before their table. First-move Sudoku examples identify their digits as sorted groups around one empty cell, not a board layout. Next-step Sudoku snapshots identify all empty cells of one row, position labels and complete candidate lists. Block examples state the fixed orientation, empty-cell placement, simultaneous full-line clearing, no falling cells and supplied piece order; their captions explain the coordinate directions and symbols. These are restatements of the existing articles, not new game rules or named-game feature claims.

Each table references its local note with `aria-describedby`. Notes are outside the initially closed answers. No new control, article, script, stylesheet, image, account or storage is added. Existing example IDs, questions, data, answers, dates and canonical URLs remain intact. The homepage stays unchanged; earlier redesign WIP is excluded.

## Validation

Use an isolated staged-source build. Run `./tools/check_site.sh`, `hugo --gc --minify`, existing validators and `tools/check_practice_context.py`. Test fresh fragment arrivals, visible context, table descriptions, answer controls, keyboard focus, enlarged text and mobile/desktop layouts. Inspect generated scope and verify actual production after the approved GitHub push. Retention and comprehension improvements require reader evidence and are not claimed as measured outcomes.

## Pre-release Results

Both builds and sixteen static validators passed. Browser checks passed at 320, 390, 768, 1280 and 1440 pixels with JavaScript disabled: eight fresh fragment arrivals, visible notes before tables, matching described-by targets, unchanged answers, keyboard focus/Space, fragment reload, 200% text and the finder-to-example return journey. A JavaScript-enabled answer-toggle smoke also passed. Mobile and desktop screenshots were inspected; actual screen-reader narration was not tested.

Generated changes are confined to the three practice guides and their automatic reading-time labels in the archive (5 to 6, 5 to 6 and 6 to 7 minutes). Homepage, sitemap, both RSS feeds and all stylesheets remain identical. The browser harness was corrected to separate temporary 200% root text sizing from reload scroll restoration and to open a fresh document for each direct-arrival test; no production workaround was required.
