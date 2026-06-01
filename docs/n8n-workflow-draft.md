# n8n Workflow Draft

This is a planning document only. It does not include secrets, real API keys, credentials, webhook URLs, or automation code.

## Proposed Workflow

1. Cron trigger starts a scheduled workflow.
2. Topic source list provides approved evergreen topic areas.
3. AI topic classifier checks whether the topic fits NewGames.ai's content policy.
4. AI draft generator creates a first draft for review.
5. Policy checker flags risky claims, unsupported facts, ranking language, copied descriptions, and image-policy issues.
6. Markdown frontmatter generator creates Hugo-compatible metadata.
7. Optional image prompt generator creates a safe abstract prompt.
8. GitHub draft file creation writes the post with `draft: true`.
9. Human review edits, verifies, rejects, or approves the draft.
10. Manual merge/publish moves approved content to the production branch.
11. Cloudflare Pages deploys after the approved merge.

## Topic Source List

Early topic inputs should stay evergreen:

- New game discovery habits.
- Mobile game selection tips.
- Web game and browser game explainers.
- Puzzle game criteria for casual players.
- Indie game discovery guides.
- BornstarSoft, Puzzlepia, and NewGames.ai internal cross-link topics.

## Policy Checker Rules

The policy checker should flag:

- Unverified game facts.
- Pricing, release date, or platform claims without sources.
- Fake rankings, scores, reviews, or download counts.
- Third-party screenshots, logos, copied store descriptions, copied press release text, or copied news article text.
- Trademark imitation or brand confusion.
- Drafts that are not marked `draft: true`.

## Example Frontmatter

```yaml
title: ""
description: ""
date: ""
draft: true
categories: []
tags: []
cover: "/images/og/default-og.svg"
coverAlt: ""
robots: "index,follow"
```

## Review Gate

No generated draft should be published automatically. A human editor must review the Markdown, verify any factual claims, confirm image safety, run `./tools/check_site.sh`, and manually approve the merge or publish action.
