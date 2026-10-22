# Practice Guide Shortcuts

## Scope

On 2026-10-23, the owner authorized another useful return-visit improvement, validation and production deployment while keeping the homepage simple. This release adds two ordinary in-page links near the top of each existing practice guide. Returning readers can reach the exercises or review routine without scrolling through the large cover image and introduction.

- Sudoku: "Practice examples" reaches the existing exercise introduction; "Review the steps" reaches the row, column and box checks.
- Block placement: "Rules & practice" reaches the explicit teaching rules before the exercises; "Review the steps" reaches the fit/clear/space checklist. The first link deliberately does not skip the rules or imply the examples reproduce a named game.

Links appear before the title, after the existing breadcrumb, so they remain easy to reach on narrow screens. Both pages retain their full content, original dates, cover, closed answer disclosures and table of contents. There is no automatic scrolling, answer opening or saved progress. Existing section IDs and page URLs are preserved and can be bookmarked normally.

## Release Boundaries

Only these two pages opt in through frontmatter. The shared single template receives one partial call; existing unreleased artwork/layout WIP is selectively excluded. The current scoped guide stylesheet receives the link styles. Homepage, article bodies, feeds, navigation, tracking and game repositories are unchanged. No new article, image, JavaScript, account, storage or dependency is added.

The guide stylesheet's anchor offset retains its 160px minimum and scales with the root text size. This fixes heading occlusion observed at 200% text size while preserving the normal-size offset. It also benefits the existing guide index and opt-in article headings; it does not change the shared site header or main stylesheet.

At 200% text on narrow screens, existing article-heading and footer grid children also exceeded the available width. Scoped minimum-width and wrapping safeguards in the guide stylesheet resolve that overflow without changing the normal grid structure or loading additional styles on the homepage.

RSS remains a separate acceptance item: previous browser XML checks pass, but Python requests received Cloudflare 403 on both existing and new routes. No real RSS-reader connector is available in this session. Do not claim subscription delivery is verified, change Cloudflare security rules, or impersonate another client to bypass a block.

## Verification

Run standard Hugo checks, existing content/feed validators and `tools/check_practice_shortcuts.py` against an isolated staged-source build. Verify every fragment, opt-in scope, initial answer state, original publication dates and byte-identical unaffected homepage/feed output. Test click and keyboard activation, browser back/reload with fragments, heading clearance under the sticky header, narrow screens, enlarged text and the existing exercise interactions. Record deployment results and remaining RSS-reader acceptance work in the local project-status handoff. No measured retention improvement is claimed.
