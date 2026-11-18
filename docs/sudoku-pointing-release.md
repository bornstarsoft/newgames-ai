# Box-to-row Sudoku practice

Work ID: NEWGAMES-SUDOKU-POINTING

The existing next-step guide now has an optional box-to-row deduction after the original two exercises and post-placement explanation. Readers can revisit a small, initially closed answer and distinguish a candidate elimination from a confirmed entry. [HoDoKu documents the pointing technique](https://hodoku.sourceforge.net/en/tech_intersections.php). The example uses two extra clues on a copy of the second teaching board; it does not claim uniqueness.

Static regression verifies a consistent completion and independently recomputes every location for 7 in the box and outside it on the shared row. R3C1 and R3C3 are the local candidates; R3C9 is the only candidate outside the box on that row. The existing update listing links to the new section. Original dates of publication, URLs, two earlier exercises, shortcut destinations, homepage and styles are preserved. No script, tracking, game logic or hosting change. Earlier artwork and redesign work remains separate.

Local QA: clean Hugo builds and 20 static validators. Chromium at 320, 390, 768, 1280 and 1440px checked the update link, closed answer, keyboard control, 200% text and print behavior with JavaScript disabled.
