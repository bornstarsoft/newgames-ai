# Missing-page recovery

Work ID: NEWGAMES-404-RECOVERY

## Scope

The existing 404 page now links to Games & guides, Puzzle practice, and New & updated. Home remains available, with a contact link for reporting a broken internal link. All links are root-relative so they work from nested missing addresses.

Only Hugo's 404 kind receives `noindex,follow`. Existing published pages keep their indexing policy. The response remains an error, not an automatic redirect or a replacement homepage. Existing styles are reused.

No homepage, article, URL, stylesheet, redirect rule, tracking, script, dependency, account, game feature, Cloudflare setting or other repository changes. Earlier artwork/design WIP is excluded from this release.

## Acceptance

- Run `./tools/check_site.sh`, `hugo --gc --minify`, all tracked static validators and RSS fixtures from the isolated staged export.
- Check desktop/mobile layouts, 200% text, keyboard recovery links and JavaScript-disabled navigation.
- Compare generated output with the preceding release: only `404.html` should change.
- After GitHub main deployment, verify actual HTTP 404 responses on nested unknown and draft-template paths, noindex metadata and all recovery destinations.

This addresses a concrete navigation dead end. No retention or revenue improvement is claimed without measurement. Live HTTP behavior must be checked separately from the static build.

## Local validation result

2026-10-23: both Hugo commands, nineteen static validators, feed/update fixtures and whitespace checks passed in the isolated staged export. All 66 HTML pages passed link/fragment/image checks. The previous release's generated output differs only at `404.html`; homepage, article pages, styles, sitemap and feeds are byte-identical.

Chromium passed at 320, 390, 768, 1280 and 1440 pixels, with 200% text and JavaScript disabled. All five main-content links worked by keyboard, including the Learn fragment and browser back. A JavaScript-enabled navigation smoke check also passed. Mobile/desktop screenshots were inspected. The local test harness serves the static error document with status 404; production status verification remains a separate deployment acceptance step. Safari, Firefox, screen-reader narration and retention effects were not tested.
