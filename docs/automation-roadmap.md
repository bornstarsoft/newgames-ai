# Automation Roadmap

NewGames.ai is entering automation planning, but automation is not implemented yet. The site remains a static Hugo project published through GitHub and Cloudflare Pages.

## Guiding Rule

There is no fully automatic public publishing at this stage. Every AI-generated post must be reviewed before publishing.

## Phase A: Manual Content Publishing Only

Current operating mode:

- Humans choose topics.
- Humans write or edit Markdown files.
- Humans select safe SVG placeholder images already in the repo.
- Humans run `./tools/check_site.sh`.
- Humans commit, push, and allow Cloudflare Pages to deploy.

This phase keeps the launch site stable while editorial standards are defined.

## Phase B: Candidate Topics And AI-Assisted Topic Ideas Only

Future n8n scope:

- n8n may collect candidate topics from approved source lists.
- n8n may run a scheduled idea-generation workflow.
- AI may suggest evergreen topics for mobile games, web games, puzzle games, indie games, casual games, and game discovery.
- Output should be a review queue, not published content.
- No Markdown files should be published automatically.

Allowed output examples:

- Topic ideas.
- Suggested categories and tags.
- Short editorial briefs.
- Questions a human editor should answer.

## Phase C: Markdown Draft File Generation

Future n8n scope:

- n8n may generate Markdown draft files locally or in a GitHub draft branch.
- Draft files must use `draft: true`.
- Drafts may include safe frontmatter, editorial notes, and placeholder covers.
- Drafts must not be merged to the production branch without human review.

Acceptable storage options:

- Local review folder.
- GitHub draft branch.
- GitHub pull request marked clearly as draft.

## Phase D: Human Review Before Publishing

Required before any generated draft becomes public:

- Review title and description for accuracy and tone.
- Check that all third-party facts are verified from current sources.
- Remove or rewrite weak, generic, or exaggerated claims.
- Confirm that links point to appropriate official or trustworthy pages.
- Confirm that images follow the image policy.
- Run `./tools/check_site.sh`.
- Change `draft: true` to `draft: false` only after approval.

## Phase E: Limited Semi-Automatic Publishing

Only after quality is stable:

- Semi-automatic publishing may be considered for safe evergreen posts.
- Eligible topics should avoid current game facts, pricing, rankings, release dates, and platform availability claims.
- Human review remains required until there is a proven editorial QA process.
- Fully automatic public publishing should remain disabled unless a future explicit approval changes this policy.

## Safety Requirements

- No fully automatic public publishing at this stage.
- No unverified game facts.
- No fake rankings.
- No fake review scores.
- No fake download counts.
- No third-party screenshots.
- No third-party logos.
- No trademark imitation.
- No copied store descriptions.
- No copied press release text without rewriting and attribution.
- No copied news article text without rewriting and attribution.
- Every AI-generated post must be reviewed before publishing.

## Deferred Integrations

- No n8n production workflow yet.
- No OpenAI API connection yet.
- No API keys or credentials in the repo.
- No Cloudflare R2 or Cloudflare Images yet.
- No GA4, AdSense, external JavaScript, user accounts, comments, or database.
