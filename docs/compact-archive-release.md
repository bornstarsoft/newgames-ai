# Compact Guide Archive

Work: NEWGAMES-COMPACT-ARCHIVE
Date: 2026-10-23

## Scope

The complete archive at `/blog/#all-guides` changes from large repeated image cards to a compact reading list: one column on smaller screens and two on wide desktops, in left-to-right row order. All published articles retain their full titles, descriptions, dates and URLs in newest-first order. Each entry has a small decorative category thumbnail with reserved dimensions, one title link, and Hugo's estimated reading time. The count is generated from the same collection as the list.

No search script, filtering state, pagination, account, storage, analytics, new article or new asset is introduced. The existing choose/learn/return paths and archive fragment are preserved. Homepage HTML, article content, publication dates, sitemap and feeds must remain unchanged. Shared post cards are not edited, so the homepage and related-article areas keep their existing layout. Styles are restricted to the archive classes in the existing guide stylesheet.

## Acceptance

- Run the standard site check, production build and existing regression validators on the isolated staged source, excluding earlier artwork/design WIP.
- Verify archive row identity, uniqueness, order, full title/description, publication dates, image dimensions, reading-time labels and one keyboard stop per article.
- Compare the new archive with the previous production build at the same viewport and font settings; measure layout height, not user retention or performance metrics.
- Browser checks: 320/390/768/1280/1440px, no JavaScript, anchor/header clearance, keyboard activation/back navigation, image loading, text wrapping, 200% text and existing guide journeys.
- Verify the deployment on the actual domain, including all article destinations, the homepage, canonical metadata, sitemap and RSS.

## Limits

Local comparison against the previous isolated release retained the same 19 records. List heights were 8,714 to 6,198px at 320px width, 8,864 to 4,757px at 390px, 3,442 to 3,469px at 768px, and 2,389 to 1,977px at 1280/1440px. The tablet case is effectively unchanged, not a reduction. All measurements use the same browser and normal text size; they are not Core Web Vitals or reader-behavior measurements.

Estimated reading time describes the article, not the time needed to finish a game. The article count is not a popularity metric. A shorter rendered list is a layout observation only; it does not establish improved retention, engagement or revenue. No real email delivery or third-party RSS-reader polling is claimed.
