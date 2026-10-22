---
title: "Sudoku's Next Step: One Place for a Number"
slug: "sudoku-one-place-for-a-number"
description: "Learn the difference between one candidate in a cell and one possible place for a digit, with two original Sudoku checks and clear explanations."
date: 2026-10-23T02:10:00+09:00
draft: false
categories: ["Puzzle Games", "Web Games"]
tags: ["sudoku", "puzzle games", "beginner guides", "browser games"]
cover: "/images/categories/puzzle-games.svg"
coverAlt: "Abstract colored puzzle blocks, not a Sudoku game screenshot."
robots: "index,follow"
sudokuPractice: true
guideNavigation: true
guideShortcuts:
  - label: "Try the examples"
    anchor: "compare-two-row-snapshots"
  - label: "Review the check"
    anchor: "a-check-to-use-next-time"
---

You have checked a few empty cells, but each still has two or three possible digits. That does not always mean you need a more complicated technique. Try changing the question from "What can go in this cell?" to "Where can this number go in the row?"

This is a follow-up to our [first Sudoku move guide](/blog/how-to-find-your-first-sudoku-move/). That guide starts with the candidates for one cell. Here, you will follow one missing digit across a group of cells. Two original examples show when that gives you a certain placement and when it does not.

## One Candidate Or One Place?

Classic Sudoku requires the digits 1 through 9 in each row, column and 3-by-3 box, without repetition. See [Nikoli's standard rules](https://www.nikoli.co.jp/en/puzzles/sudoku/) for the underlying puzzle.

The two questions look similar but ask you to count different things:

- **One candidate in a cell:** only one digit survives the checks for that cell.
- **One place for a digit:** within a row, column or box, only one empty cell can take a particular missing digit. That cell may still have other candidates written in it.

The second pattern is called a **hidden single**. The digit must appear somewhere in the group, and every other place has been ruled out. [Sudoku.com's technique explanation](https://sudoku.com/sudoku-rules/hidden-singles/) describes this same distinction. The examples below are our own, not copied puzzles from that site.

## Compare Two Row Snapshots

Each table lists **every empty cell in one row**. The other six cells already contain 1, 3, 4, 6, 8 and 9, so the missing digits are 2, 5 and 7. Column numbers identify positions from left to right; they are not the values to enter.

The candidates have already been checked against the corresponding row, column and box. Your task is to read those complete candidate lists, not to reconstruct the unseen board. These are fixed teaching snapshots, not full playable puzzles, daily challenges, or examples from a named game's current board.

For the first table, follow only the digit **5**. Count how many of the listed cells allow it before opening the answer.

{{< sudoku-place id="one-place" >}}

Now compare a different snapshot. Most of the notes look familiar, but one cell has an extra possibility. Do not carry the previous answer across without checking it again.

{{< sudoku-place id="two-places" >}}

The important difference is not the total number of notes. It is whether all but one possible location for the chosen digit have been excluded. A cell with two notes is not automatically a better answer than a cell with three.

## Do Not Mistake Missing Notes For Evidence

On a real board, a digit appearing in only one note is not enough if you have filled in notes for only some cells. An unmarked square may still allow that digit. Recheck every empty cell in the group, including the ones you skipped earlier.

Likewise, old notes can be misleading after a placement elsewhere. Confirm that the remaining location still passes its row, column and box checks. If you have entered an incorrect number earlier, a tidy-looking set of notes can still lead you astray.

You do not need a particular notes button or automatic helper to use this reasoning. Follow the game's own instructions for its controls; this guide teaches a check, not a claim about features available in every Sudoku game.

## A Check To Use Next Time

1. Choose one row, column or box, and identify a digit it is missing.
2. Inspect every empty cell in that group. For each, check whether its row, column or box already excludes the digit.
3. Count the remaining locations. Exactly one supports a placement; two or more do not settle it with this check.
4. Before entering the digit, explain why it cannot go anywhere else in the group.
5. After placing it, recheck the affected groups and any notes you are relying on.

If there are no possible locations, stop and review the clues, entries and exclusions. Do not force a number into a cell to resolve the contradiction. If several places remain, move to another group rather than repeating the same scan and expecting a different result.

## Return To The Reason, Not Just The Answer

When revisiting the two examples, explain what changed between them. In the second table, which extra candidate prevents the earlier deduction? Closing the answers and checking that detail is more useful than remembering "column 5."

For a shorter refresher, return to the [three checks for one empty cell](/blog/how-to-find-your-first-sudoku-move/#start-with-the-three-checks). If you prefer spatial decisions, try our [block-placement examples](/blog/block-puzzle-fit-clear-leave-space/). Both are small exercises you can revisit without starting a full game.

Browse [puzzle games](/puzzle-games/) when you want to put the reasoning into practice, or keep [useful guides](/updates/#handy-guides) nearby for another visit. There is no score or saved attempt here: the aim is to leave with one more placement you can explain.
