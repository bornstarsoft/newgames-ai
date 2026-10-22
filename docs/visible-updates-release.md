# Visible Article Updates

## Reader Benefit

Returning readers can see when an article received a substantive change and why, directly below its original publication metadata. The complete Games & Guides archive shows the corresponding update date without changing the publication-based order or adding another link per record.

Only the two existing articles with dated update notes qualify: the DaySudoku correction and the Sudoku rechecking addition. No content, publication date or lastmod value is changed by this release. The homepage remains unchanged.

## Rules And Scope

A shared partial renders the full note or compact date. It requires a published, unexpired blog article, a nonblank updateNote, and lastmod after actual publication but not in the future. Draft/future/expired preview pages cannot acquire a misleading update notice. Notes are escaped as text, not rendered as arbitrary markup. Original publication metadata remains visible.

The shared single template has older local redesign WIP. Stage only the one partial call from that file. No CSS, JavaScript, assets, dependency, analytics, storage, account, Cloudflare setting or other repository is changed.

## Validation

Build the isolated staged-source export using `./tools/check_site.sh` and `hugo --gc --minify`. Run all guide/feed validators, the revised complete-archive validator and `tools/check_visible_updates.py`. Its Hugo fixtures cover positive output, text escaping, blank notes, invalid/future dates, delayed publication, draft/future/expired previews and non-blog pages.

Check the two notices, archive labels, native navigation, 200% text and small/large viewports in a JavaScript-disabled browser. Compare output with the preceding release and verify the actual production pages after the GitHub push. Retention impact and third-party RSS-reader delivery remain unmeasured/unverified.

## Pre-Release Results

- Both Hugo builds and all twelve static validators passed, including the new exclusion/escaping fixtures and existing RSS fixtures. The fixture initially emitted an empty page when no notice applied; its test-only document shell was corrected, then every negative case passed.
- At 320, 390, 768, 1280 and 1440px, two dated article notices and two archive labels render correctly, with original publication dates retained. All nineteen archive links remain single native links; keyboard/back navigation and 200% text checks passed. Mobile/desktop screenshots were inspected.
- Generated differences are only the DaySudoku article, first-move Sudoku article and blog index HTML. Homepage, sitemap, feeds, CSS, article bodies, original source content and all other generated files remain unchanged. No generated files are tracked or staged.
