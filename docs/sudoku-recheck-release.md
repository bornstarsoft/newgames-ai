# Sudoku Rechecking Help

## Scope

Expanded the existing first-move guide with a worked example of conflicting written checks and a cautious four-step rechecking routine. A native "No candidates?" shortcut returns directly to that section. The original three exercises, their answers and existing fragment links remain unchanged.

The example is original and deliberately inconsistent: the row excludes every digit except 5, and the column excludes 5. It is not a valid puzzle, a game screenshot, a game solution or evidence of a defect in any named game. It identifies a conflict, not the particular incorrect entry. The advice does not assume an undo, notes, hint or recovery feature. Existing rule citation: https://www.nikoli.co.jp/en/puzzles/sudoku/ (checked 2026-10-23).

## Return Visits And Publication

The article keeps its title, description, original publication timestamp and URL. A real lastmod timestamp and updateNote describe the substantive addition, so the existing New & Updated page and combined RSS can surface it. No new post or homepage section is added. No tracking or measured retention claim.

## Validation

Use the isolated staged-source build, `./tools/check_site.sh`, `hugo --gc --minify`, `python3 tools/check_sudoku_recheck.py`, and all existing guide/feed checks. Confirm the new shortcut, preserved exercise disclosures, table reading, 200% text, and fragment reload/back navigation with JavaScript disabled on mobile and desktop. The new validator checks the rendered digits, empty candidate set, a nonempty counter-check, editorial boundaries and one correctly identified update event.

Only this article, the shortcut expectation, the new validator and this note belong to the commit. Earlier local design/artwork WIP is excluded. No other repository, Cloudflare setting, stylesheet, template, script, dependency or external service is changed. Production acceptance is recorded in the local project handoff after deployment.

## Pre-Release Results

- Isolated Hugo builds and all eleven static validators passed, including RSS fixtures, rendered mathematics, original exercises, 64-page links/images/anchors and the new update event.
- JavaScript-disabled browser checks passed at 320, 390, 768, 1280 and 1440px. Native links work by click and Enter, including fragment reload/back. The new heading clears the sticky header, the table is readable, original answers stay closed until opened, and 200% text does not overflow. Mobile/desktop screenshots were inspected.
- Homepage HTML is byte-identical. All 19 article identities and original publication dates in the legacy blog feed are unchanged. Generated changes are the article, automatic archive reading time, update directory, sitemap and affected RSS metadata/content. No generated files are tracked or staged; whitespace checks passed.
- Retention impact, real email delivery and external RSS-reader polling remain unmeasured/unverified. The work does not claim those outcomes.
