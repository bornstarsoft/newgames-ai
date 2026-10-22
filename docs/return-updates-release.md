# New And Updated Discovery

## Scope

Owner approved a minimal return-visit improvement and deployment on 2026-10-23. Add `/updates/` with six latest published guides and up to six explicitly documented article updates. The homepage changes one existing link only; the footer exposes the destination across the site. No new homepage section, JavaScript, tracking, login or email capture.

The existing GitHub deployment exception remains applicable. Earlier artwork/layout WIP and the save-progress draft are not part of this release.

## Editorial Contract

- A new article uses its original publication date. The page never labels that as a game release date.
- A meaningful update requires both an explicit `updateNote` and a `lastmod` later than the original date. Cosmetic edits do not justify new dates or update notes.
- Drafts and future publications are excluded even in a draft-inclusive preview. Future modification dates are excluded from the updated list.
- DaySudoku's note describes the already published October 14 correction; it does not claim a fresh game update on October 23.
- RSS links to the existing blog feed for new guides. Do not imply it delivers every article correction, or promise a publishing cadence.
- Empty lists have explicit empty states. Existing article URLs and original publication dates remain unchanged.

## Verification

Run `./tools/check_site.sh`, `hugo --gc --minify`, and `python3 tools/check_updates.py` against an isolated copy of the staged release. Browser-check the release at mobile and desktop widths. Verify the deployed `/updates/`, home/footer links, RSS and sitemap after the Cloudflare Pages check succeeds.

This creates a predictable place to check for changes; it does not establish a measured retention improvement. Traffic and return metrics remain unknown.

Local release validation passed on 2026-10-23: the standard Hugo check and minified build; 57 generated HTML pages checked for links, images and anchors; sitemap/RSS and draft exclusion; browser checks at 320, 390, 768, 1280 and 1440px, including screenshot inspection. A draft-inclusive, future-inclusive fixture build confirmed that draft/future publications and future update notes stay out of the updates lists. The production deployment result is recorded in the local project-status handoff.
