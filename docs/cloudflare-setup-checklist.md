# Cloudflare Setup Checklist

- Add `newgames.ai` to Cloudflare.
- Set nameservers at the registrar.
- Enable SSL/TLS Full.
- Set Always Use HTTPS to ON.
- Set Automatic HTTPS Rewrites to ON.
- Set TLS 1.3 to ON.
- Keep HSTS OFF initially.
- Connect the GitHub repo to Cloudflare Pages.
- Use project name `newgames-ai`.
- Use production branch `main`.
- Use build command `hugo --minify`.
- Use output directory `public`.
- Add custom domain `newgames.ai`.
- Redirect `www.newgames.ai` to `https://newgames.ai`.
- Enable Cloudflare Web Analytics.
- Register Google Search Console.
- Submit the sitemap at `https://newgames.ai/sitemap.xml`.
