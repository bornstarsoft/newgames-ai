# Learning Guide Print Layout

## Scope

NEWGAMES-GUIDE-PRINT improves browser printing and PDF saving for the six existing learning guides and `/puzzle-terms/`. A print-only line contains each page's absolute canonical URL, so a saved reference points back to the original. No new article, game feature, downloadable puzzle collection or daily-content promise is introduced.

Print styles remove site navigation, the decorative cover, guide navigation/feedback and related-article cards. Article title, description, publication/update information, body, questions, clue tables and visible answers remain. Closed answer disclosures are omitted; opened answers are included, without changing their on-screen state or adding script. The block boards retain their X/dot symbols and coordinates with dark ink on white backgrounds.

The existing guide stylesheet uses print-only rules scoped to pages containing the source line. Ordinary game introductions, category pages, homepage and archive printing are not opted in. Screen content, layout and answer behavior are unchanged. No new CSS file, image, dependency, JavaScript, analytics, storage, account or Cloudflare setting is added. Earlier redesign WIP is excluded.

## Acceptance

Build isolated staged sources, run the repository checker, Hugo, all static validators and whitespace checks. Verify exactly seven canonical source links, no new script and unchanged feeds/sitemap/homepage. Browser tests cover normal and print media, closed/open answers, screen restoration, all seven pages, mobile/desktop and 200% text. Generate actual A4/Letter PDFs with backgrounds disabled, inspect rendered pages and verify source links, complete text, table symbols and answer inclusion/omission.

Use the existing approved GitHub-to-Cloudflare deployment and verify the production output. Actual physical printers, other PDF viewers, screen-reader narration and business/retention impact remain outside this automated acceptance.

## Pre-release Results

The isolated site checker, `hugo --gc --minify`, eighteen static validators and RSS/update fixtures passed. Generated output differs only in seven guide HTML source lines and the guide stylesheet. Homepage, article bodies/dates, exercises, sitemap and all three feeds remain unchanged. No generated PDF or public build is committed.

Chromium with JavaScript disabled passed all seven pages at 320/390/768/1280/1440px and 200% text, print/screen switching, canonical source links, closed-answer omission, keyboard-opened answer inclusion and preservation of answer state after printing. Non-opted homepage/archive/game introductions retain their original print behavior. Mobile and desktop full-page screen captures are pixel-identical to the preceding release.

Fourteen actual PDFs were generated: seven A4 closed-answer copies and seven Letter opened-answer copies, with backgrounds disabled. All 52 pages passed question/answer and visible paragraph checks, clickable canonical-source checks, glyph-boundary and blank-page checks. Rendered proof sheets were inspected. Compact print table spacing and a print-only inline-block result comparison avoid the excessive gaps from the initial grid/whole-exercise pagination attempt. Individual tables stay intact; long articles still span multiple pages.

PDF extraction normalizes equivalent apostrophe glyphs from the browser font subset; no article text was changed. PDF tests use existing bundled libraries, with no installed dependency. Safari/Firefox print engines, physical printer output and reader/business impact are NOT_RUN; no universal print-layout or retention claim is made.
