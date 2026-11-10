# Reusable puzzle note

Work ID: NEWGAMES-PUZZLE-NOTE

The owner authorized a useful content and return-visit improvement, validation and live deployment with the homepage kept simple. The existing return guide describes three questions but did not offer a blank template or a concrete example of spotting a stale note. This update gives readers both, using only the existing article and print layout.

The note stays on paper or in a reader's own notes. It does not save or recover a board. A visible board cue can catch a mismatch but does not prove a match. The changed-cell example advises rechecking instead of undoing moves to fit an old note. It describes no named game's behavior or new rules.

The existing URL, publication date, shortcuts and original headings remain. The new heading is linked from the checklist and existing contents menu. Existing update metadata and RSS report this substantive revision. No new page, JavaScript, CSS, tracking, storage, dependency, hosting settings or redesign. Earlier artwork/design WIP is excluded.

## Local validation

On 2026-11-10, `./tools/check_site.sh`, `hugo --gc --minify`, twenty static validators, RSS fixtures and whitespace checks passed in the isolated staged export. A generated-output comparison against the previous release found changes only to the intended article, its archive/update listings, and generated feed/sitemap metadata. Homepage, all other articles and styles were byte-identical.

Chromium passed at 320/390/768/1280/1440px with JavaScript disabled: checklist link by keyboard, contents menu, browser back, fresh fragment arrival, 200% text, and template visibility under print media. The loopback server stalled during reverse DNS, so local browser tests served the built files through Playwright response fixtures. A mobile screenshot was inspected. No physical printing, cross-browser or retention test was run. Live network acceptance follows deployment.
