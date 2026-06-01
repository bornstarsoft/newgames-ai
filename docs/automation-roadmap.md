# Automation Roadmap

NewGames.ai may later use automation to help draft and prepare content, but the MVP does not publish automatically.

## Future Workflow

- n8n cron workflow starts a scheduled content task.
- AI article draft generation creates an editorial draft.
- AI image prompt generation prepares safe visual prompts.
- Optional AI image generation creates abstract or approved supporting assets.
- Markdown generation formats the draft for Hugo.
- GitHub draft commit or pull request stores the proposed content.
- Cloudflare Pages deployment builds after approved merges.
- Human review happens before publishing.
- Future optional Cloudflare R2 image storage may use `media.newgames.ai`.

## Safety Rule

No fully automatic public publishing should be enabled until quality checks, source checks, image policy, and editorial review are stable.
