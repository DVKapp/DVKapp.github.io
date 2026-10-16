# DVK — dvk.vn

Public static website for DVK and its apps/games. This repository contains website code and public policies only. The Flutter game source is kept in its separate private repository.

- `/`: DVK introduction and project directory.
- `/puzzle-spark/`: Puzzle Spark; `/puzzle-spark/privacy/` and `/puzzle-spark/terms/` are app-specific policies.
- `/privacy/`: website privacy information.
- `/support/`: email support and troubleshooting.
- `/vi/`: Vietnamese versions of the pages above.
- `/app-ads.txt`: Google DIRECT seller record for publisher `pub-3636940103463538`.

Build with Python 3 (standard library only):

```sh
python3 build.py
python3 -m http.server 8877 --bind 127.0.0.1 --directory dist
```

The generator writes `dist/` for local preview and copies the same output to the tracked `docs/` directory. GitHub Pages publishes `main` → `/docs`. The custom domain is in `docs/CNAME`; HTTPS should be enforced after GitHub issues its certificate. Cloudflare manages DNS. No secrets or private app files belong here.

Current app policies describe the preview build. Update the app and these policies together before enabling production advertising/consent. Domain hosting and app-ads.txt publication do not themselves grant AdMob readiness or store approval.

## Validation — 16 October 2026

- 14 bilingual content pages, six legacy URL redirects and a 404 page generated.
- Local links and assets checked; every referenced local path exists.
- All 14 pages checked at 375×812 and 1280×900: no horizontal overflow, one H1, correct `lang`.
- Uses local assets and system fonts; no analytics script, web advertising SDK or contact form.

## Brand hierarchy

DVK uses navy, white and blue. Each game has an isolated palette: Puzzle Spark uses forest green, cream and gold. `/games/` lists projects; game policies live under the game slug. The old `/game1/` routes use HTML redirects to their new URLs. New games should use their own names and scoped palette.

## SEO

Unique bilingual titles/descriptions, canonical/hreflang, social metadata and JSON-LD (Organization, WebSite, WebPage, VideoGame and BreadcrumbList). No invented ratings, offers or download links. VideoGame markup is descriptive; no SoftwareApplication rich-result eligibility is claimed. Sitemap lists canonical pages only. Google Play EN/VI copy is in `marketing/google-play-listing.md` and has not been submitted. Search Console verification and sitemap submission remain pending.
