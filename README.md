# NewGames.ai

NewGames.ai is a lightweight Hugo website for discovering new games worth playing. The first MVP is a clean static site for GitHub and Cloudflare Pages deployment.

## Purpose

The site introduces evergreen discovery pages for new games, mobile games, web games, puzzle games, indie games, casual games, and starter blog guides. It is intentionally small, fast, and safe for launch.

## Local Development

```sh
hugo server
```

Visit the local URL printed by Hugo, usually `http://localhost:1313/`.

## Build

```sh
hugo --minify
```

Cloudflare Pages should publish the generated `public` directory.

## Deployment Target

- Production domain: `https://newgames.ai`
- Platform: Cloudflare Pages
- Repository: `newgames-ai`
- Production branch: `main`
- Build command: `hugo --minify`
- Output directory: `public`

## Content Policy

- Keep content evergreen, useful, and clear.
- Do not publish fake rankings, fake reviews, fake download counts, or unverifiable claims.
- Avoid third-party game facts unless they are checked before publishing.
- Do not describe NewGames.ai as an official ranking authority.

## Image Policy

- MVP images are simple SVG placeholders only.
- Do not imitate third-party games, characters, logos, brands, or store interfaces.
- Use abstract shapes, cards, puzzle blocks, browser motifs, gamepad motifs, and simple discovery visuals.

## Automation Policy

- No fully automatic public publishing in the MVP.
- Future AI and n8n workflows should create drafts or pull requests for human review.
- Automation must preserve editorial quality, source checks, and image safety.

## First Launch Checklist

- Confirm Cloudflare Pages build settings.
- Add the custom domain `newgames.ai`.
- Verify HTTPS and redirect behavior.
- Submit `https://newgames.ai/sitemap.xml` to Google Search Console.
- Review starter content before public announcement.
- Run `./tools/check_site.sh` before release.
