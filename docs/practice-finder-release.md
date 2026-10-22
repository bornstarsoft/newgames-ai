# Practice Example Finder

## Scope

Games & Guides now has a native, initially closed "Choose a practice example" disclosure within its existing Learn path. Eight links are grouped into checking a Sudoku cell, finding a place for a Sudoku number, and block placement. Each link opens the original guide at its existing example section. Readers can select a particular exercise without first scanning the entire article.

Labels come from the same data as the examples; explicit key lists preserve the teaching order. Missing guides or data keys fail the build. Draft, future and expired guide destinations are omitted. All existing full-guide links remain available above the disclosure. No new page, exercise, content date, game claim or homepage section is added.

Only the blog index template, one new partial and the existing guide stylesheet change. The native disclosure needs no JavaScript, storage, account or tracking. It does not remember an attempt, save progress or reveal an answer. Earlier redesign WIP is excluded from this release.

## Acceptance

Build the staged-source export, run the existing validators plus `tools/check_practice_finder.py`, and compare generated scope. Check all eight links, their matching heading labels, destination answers closed on arrival, keyboard navigation, browser back and mobile/desktop layouts with normal and enlarged text. Check the actual production site after the approved GitHub push. Homepage, article HTML, sitemap and both RSS feeds should remain byte-identical to the previous release.

No retention, traffic or revenue improvement is claimed without usage evidence.

## Pre-release Results

The isolated `./tools/check_site.sh`, `hugo --gc --minify` and fifteen static validators passed, including existing exercise arithmetic, archive, guide links, email feedback and RSS/update fixtures. Generated output differs only in `blog/index.html` and `css/guides.css`; all article HTML, homepage, sitemap and feeds are unchanged.

Browser checks passed with JavaScript disabled at 320, 390, 768, 1280 and 1440 pixels: initially closed state, visible keyboard focus, ordered Tab stops, Enter/Space toggles, all eight destinations, matching headings, closed answers, sticky-header clearance and browser back. Text enlarged to 200% fits without horizontal overflow. All twenty archive records remain available; homepage still has six latest cards and the three official game links. Mobile/desktop screenshots were inspected.
