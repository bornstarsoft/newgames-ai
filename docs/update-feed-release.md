# New And Updated Feed

## Scope

The owner authorized a suitable return-visit improvement, validation and production deployment on 2026-10-23. This release adds `/updates/index.xml` so readers can follow new articles and substantive corrections without email collection or another homepage section. The project-specific GitHub to Cloudflare Pages exception remains applicable.

`/updates/` offers the combined feed alongside the unchanged `/blog/index.xml` new-article feed. Its existing head partial automatically advertises the section's RSS output. No homepage, footer, shared styles, existing article text or publication dates are changed. Existing feeds retain their URLs and behavior.

## Editorial Contract

- The combined feed contains the latest 20 publication/correction events, newest first. It is a recent feed, not a permanent event archive.
- A publication event uses the article's publish date. A correction requires a nonblank `updateNote` and a `lastmod` after publication and not in the future. Routine styling edits are not corrections.
- Each article can contribute its publication and its latest correction. An update includes the existing editorial reason and original publication date. Historical notes are not manufactured or backfilled.
- Drafts, future publications and expired pages are excluded even from draft/future/expired-inclusive preview builds. A future correction does not suppress an otherwise published article's publication event.
- Event IDs use the article URL, event kind and event timestamp in UTC, never build time. Unchanged rebuilds do not create new identities. Update notes should summarize substantive changes and receive an accurate lastmod when another meaningful correction is made.
- There is no promise of daily posts, push delivery or exact refresh timing. RSS readers control polling and presentation. Only the current correction is retained; use the site/Git history for a full editorial history.

## Validation

Run the existing Hugo and HTML validators plus `tools/check_update_feed.py`. Regression fixtures exercise XML escaping, publication versus update dates, ordering, stable rebuilds, empty feeds, the 20-event limit and unpublished/expired/future-note exclusion. Fixtures live only in ignored output and never enter the release source.

Verify mobile/desktop feed discovery, existing article/game links, production HTTP/XML and the Cloudflare Pages deployment result. No analytics, login, email, JavaScript, dependencies or named-game claims are added. Actual subscriber delivery and retention/revenue impact are not measured.

References reviewed: [Hugo RSS templates](https://gohugo.io/templates/rss/) and [RSS 2.0 specification](https://www.rssboard.org/rss-specification). The implementation is tested with this repository's installed Hugo version rather than assuming the newest documentation's template lookup behavior.
