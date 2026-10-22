# Purpose-Based Guide Discovery

## Scope

Owner approved choosing the next suitable content and return-visit improvement, keeping the homepage simple, validating and deploying on 2026-10-23. This release makes existing material easier to revisit rather than publishing another overlapping article. The existing project-specific GitHub to Cloudflare Pages exception remains applicable.

## Reader Changes

- Keep `/blog/` and its feed URL. Use the clearer title "Games & Guides" and three editorial paths: choose a game, learn a first move, and prepare to return. New concise descriptions explain the decision each path addresses without adding game-specific claims.
- Retain every published article in the date-ordered archive below the paths. The paths are editorial entry points, not rankings or popularity lists.
- Add an initially collapsed native table of contents and "Find another guide" link to the save checklist, Sudoku first-move guide and puzzle-style comparison. Preserve their bodies and publication dates; navigation changes do not justify fabricated freshness.
- Leave the homepage template, header/footer navigation, shared CSS and existing game URLs unchanged. Load the small guide stylesheet only on the index and opted-in articles.

## Implementation Boundaries

No JavaScript, search service, personalization, browser storage, analytics, accounts or dependencies. Native disclosures work with JavaScript disabled. Earlier artwork/data/layout WIP is not included; shared-template changes are selectively staged. The local WIP single template suppresses its older rail TOC only on opted-in articles to avoid duplicate IDs, but that unreleased redesign remains excluded.

## Verification

Use an isolated staged-source export. Run `./tools/check_site.sh`, `hugo --gc --minify`, `tools/check_updates.py`, `tools/check_sudoku_guide.py` and `tools/check_guide_finder.py`. The new checker compares the archive against Hugo's published-content inventory and validates TOC targets, disclosure state, original dates and stylesheet scope.

Browser-check purpose anchors, archive access, TOC open/close and target visibility below the sticky header, return navigation and existing game links at mobile and desktop widths with JavaScript disabled. Check sitemap/RSS and production deployment. Record results in the local project-status handoff.

No user study or measured retention/revenue improvement is claimed. Keep the paths small and editorially maintained; do not add categories solely to increase page count.
