# Save and return guide shortcuts

Work ID: NEWGAMES-RETURN-SHORTCUTS

## Scope

The owner approved a useful return-visit improvement, a simple homepage, validation and deployment. The save and return-note guides already contain concise checklists, but repeat readers previously had to pass the title and cover before reaching the contents navigation. Reuse the existing native top-of-article shortcut pattern instead of adding another article or homepage section.

- Save guide: Save checklist; Progress missing?
- Return-note guide: Return checklist; Note example.
- Add an optional accessible navigation label. The three existing practice pages retain the Practice shortcuts default and their exact links.

These links scroll to existing sections. They do not save progress, collect notes, restore missing games or imply a game-specific feature. The missing-progress link leads to the existing caution against resetting or clearing data, not to a reload test.

Article bodies, headings, URLs, dates, description, existing cover images and indexing remain unchanged. No lastmod/updateNote is manufactured for a navigation-only change. Existing CSS, print hiding, keyboard focus and responsive wrapping are reused. No script, storage, dependency, tracking, external service, Cloudflare setting or other repository change. Earlier artwork/design WIP is excluded.

## Validation plan

Use an isolated staged export for `./tools/check_site.sh`, `hugo --gc --minify`, all tracked static validators and RSS fixtures. The generated output should differ only in the two opted-in article HTML files; all feeds, sitemap, homepage and existing practice pages must remain identical.

Test the four links at mobile/desktop widths, 200% text, keyboard activation, history back, fresh fragment entry, header clearance and print hiding with JavaScript disabled. Check the existing three practice navigations retain their labels and links. After the GitHub main push, verify both production pages and repeat browser acceptance.

No user study or retention/revenue improvement is claimed by this navigation change.

## Local results

2026-10-24: both Hugo commands, twenty static validators, RSS/update fixtures and whitespace checks passed in the isolated staged export. All 66 HTML pages passed link/fragment/image checks. A full generated-output comparison found only the two intended article HTML files changed; homepage, other articles, CSS, sitemap and all feeds are byte-identical.

Chromium passed at 320/390/768/1280/1440px with JavaScript disabled: exact labels/targets, first-viewport visibility, visible keyboard focus, Enter/click, browser back/reload, fresh fragment arrivals, sticky-header clearance and 200% text without overflow. Print-media checks hide the shortcuts and retain the source line; screen mode restores them. Existing three practice pages retain their original label and links. JavaScript-enabled navigation passed. Local mobile/desktop screenshots inspected.

Actual screen-reader narration, Safari/Firefox, physical printing and retention effects were not tested. Production verification remains a separate post-push step.
