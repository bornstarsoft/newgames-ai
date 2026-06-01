# AI Content Policy

This policy defines safe early use of AI-assisted content for NewGames.ai. It applies to topic ideas, outlines, draft articles, category copy, image prompts, and future n8n-assisted workflows.

## Acceptable Content Types

- Evergreen game discovery guides.
- General mobile, web, puzzle, indie, and casual game explainers.
- Safe curated category pages.
- NewGames.ai internal editorial guides.
- BornstarSoft, Puzzlepia, and related network cross-link content.
- Draft outlines and topic ideas for human review.

## Unacceptable Content Types

- Direct claims about newly released games without source verification.
- Pricing claims without a current source.
- Platform availability claims without a current source.
- Official ranking claims.
- Top 10 lists that pretend to be objective or comprehensive.
- Fake review scores.
- Fake download counts.
- Generated screenshots.
- Images that look like real game screenshots.
- Images resembling third-party games, characters, logos, store UI, or brand assets.
- Copied store descriptions.
- Copied press release text without rewriting and attribution.
- Copied text from news articles without rewriting and attribution.

## Source Verification Rules

- Verify specific game facts against current official sources before publishing.
- Use official game websites, platform store pages, developer posts, publisher pages, or direct announcements when available.
- Treat pricing, release dates, platform availability, monetization, and live-service features as time-sensitive.
- If a fact cannot be verified, remove it or rewrite the sentence as general guidance.
- Do not cite generated AI text as a source.

## Title Rules

- Titles should be clear, useful, and honest.
- Avoid official-sounding ranking language unless the article explains that it is an editorial guide.
- Avoid clickbait, exaggerated certainty, or claims that NewGames.ai has measured the whole market.
- Use "best" carefully as player-fit language, not as an objective ranking.

## SEO Description Rules

- Descriptions should summarize the page in one natural sentence.
- Avoid fake urgency, exaggerated claims, or current facts that have not been verified.
- Include relevant discovery language naturally, such as new games, mobile games, web games, puzzle games, indie games, casual games, or browser games.
- Keep descriptions useful for both readers and search snippets.

## Image Prompt Rules

- Use abstract, non-infringing visual prompts.
- Prefer discovery cards, puzzle blocks, browser windows, soft gamepad motifs, sparks, grids, and simple shapes.
- Do not request real game screenshots.
- Do not imitate third-party games, characters, logos, stores, platform UI, or brand styles.
- Do not include trademarked names in image prompts unless the image is not attempting to depict that trademark.

## External Link Rules

- Prefer official or primary sources for named games and factual claims.
- Avoid linking to unsafe, misleading, or unrelated pages.
- Use external links to support verification, not to imply official partnerships.
- Review links before publishing and during major updates.

## Human Review Checklist

- The draft fits NewGames.ai's positioning: "Discover New Games Worth Playing."
- The draft avoids fake rankings, fake reviews, fake scores, and fake download counts.
- Any named game facts are verified.
- The title and description are accurate and not exaggerated.
- The article does not copy store descriptions, press releases, or news articles.
- The cover image follows the image policy.
- External links are appropriate and reviewed.
- The page builds successfully with `./tools/check_site.sh`.

## When To Keep A Post As Draft

Use `draft: true` when:

- The topic was AI-generated and has not been reviewed.
- The article mentions named games with unverified facts.
- The title or SEO description needs editorial review.
- The cover image or coverAlt is missing or uncertain.
- External links have not been checked.
- The post may need legal, brand, or partnership review.

## When To Reject A Generated Post

Reject a generated post when:

- It invents game facts, scores, rankings, prices, release dates, or platform availability.
- It relies on copied third-party descriptions, press releases, or news articles.
- It imitates third-party trademarks, characters, brands, or store UI.
- It cannot be edited into a useful, trustworthy article without rewriting most of it.
- It conflicts with NewGames.ai's static MVP limits or publishing standards.
