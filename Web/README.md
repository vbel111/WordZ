# Word Z website (Vercel)

Static site for the store listings. Everything that gets published is in `public/`.

| Page | URL | Use it for |
|---|---|---|
| `public/index.html` | `/` | Marketing URL (App Store), Website (Google Play) |
| `public/support.html` | `/support` | Support URL (App Store) |
| `public/privacy.html` | `/privacy` | Privacy Policy URL (both stores, in-game Settings) |
| `public/terms.html` | `/terms` | Terms of Use |

## Deploy
1. vercel.com → Add New → Project → import the GitHub repo.
2. **Root Directory: `Web`** (Framework preset: Other). `vercel.json` sets the output to `public/`, with no build step.
3. Deploy. Every push to `main` redeploys.

`cleanUrls` serves `/privacy` for `privacy.html` (the `.html` address redirects to it).
After the first deploy, put the real address in `GameConfig.PrivacyUrl` / `TermsUrl`.
