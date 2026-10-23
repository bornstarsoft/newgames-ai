# Ringzzle move checks

Work ID: NEWGAMES-RINGZZLE-CHECKS

## Decision and scope

The owner approved choosing a useful improvement, preserving a simple homepage, validating and deploying. The existing Sudoku and block guides have specific decision examples; the Ringzzle introduction described color clears and Color Burst without explaining their conditions. Improve that existing article instead of publishing another overlapping page.

- Preserve the article URL, June 9 publication date, original section anchors, official play/help/leaderboard links and save-checklist boundary.
- Explain size-slot legality, matching-color lines and Color Burst, with a repeatable size/color/remaining-space check.
- Add three original text examples: an occupied size slot, mixed-size red line with a blue survivor, and a blue Burst with a red survivor. Assume no other simultaneous clear; these are not game screenshots or live game states.
- Add one entry under the existing Learn path. Keep the homepage and its six latest cards unchanged.
- Record the substantive update through existing lastmod/updateNote and RSS, not a new publication date.

## Source and editorial review

On October 24, 2026, read the public official rules at https://ringzzle.com/how-to-play/ . Verified a 3-by-3 board; one slot per size per cell; same-color row/column/diagonal clears independent of size; other colors remaining; a three-size same-color cell clearing that color across the board. Examples follow those documented rules and deliberately avoid score totals, optimal-move or future-piece guarantees.

Web fetch initially returned a cache miss and sandbox curl could not resolve the host. An approved network curl request retrieved the official page successfully. No game source, credential or other repository was accessed. This was documentation verification, not hands-on gameplay, a leaderboard test or a claim about saving a run.

The site remains a discovery/learning site. No executable JavaScript, assets, dependencies, game implementation, accounts, tracking, ads, ranking claims, Cloudflare changes or homepage redesign. Earlier artwork/design WIP is excluded. One shared CSS declaration allows long content-body h2 words to wrap: the existing Leaderboard heading overflowed its column at 320px/200% text. No font sizes or homepage styling changed. Repetitive introduction copy was shortened while preserving all original headings and links.

## Release checks

Build and run all tracked static validators in an isolated index export. Verify new wording, preserved anchors/date/URLs, a single update event, untouched article inventory and homepage. Test phone/desktop, enlarged text and keyboard entry from Learn, with JavaScript disabled. Recheck the deployed article and update feed after the existing GitHub-to-Cloudflare deployment.

No retention or revenue result is claimed without actual evidence.

## Local acceptance

2026-10-24: `./tools/check_site.sh`, `hugo --gc --minify`, twenty static validators, RSS/update fixtures and whitespace checks passed from the isolated staged export. All 66 HTML pages passed internal link, fragment and image checks. Homepage and the other nineteen articles are byte-identical to the previous build. All twenty legacy RSS titles, URLs, identifiers, publication dates and order remain unchanged; the revised article's summary and substantive update propagate through the existing category/sitemap/feed templates.

Chromium passed at 320, 390, 768, 1280 and 1440 pixels, 200% text, keyboard entry/return/back, official-link focus and JavaScript-disabled reading. JavaScript-enabled entry also passed. Local mobile/desktop screenshots inspected; homepage screenshots at 390/1280 match the preceding live release pixel-for-pixel. The initial enlarged-text test caught the pre-existing long Leaderboard heading; the one-line wrapping fix passed the full rerun. The RSS validator was corrected to parse the actual +09:00 date instead of assuming a UTC-formatted date string.

Official play and leaderboard URLs returned HTTP 200; rules were read from the official help page. Gameplay/score submission, Safari/Firefox, screen-reader narration and business effects were not tested. Production verification follows the push; no production success is implied by these local results.
