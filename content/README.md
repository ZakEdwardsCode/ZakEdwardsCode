# Plasmo carousel pipeline

Turns researched topics into Instagram (1080×1350) and TikTok (1080×1920) carousels, plus a cover MP4, for [plasmo.uk](https://plasmo.uk).

```
topics.json            ranked topic ideas, every fact tagged with a source
posts/*.json           one file per carousel  ← add posts here, no code changes
screenshots/*.png      real app screenshots (cropped from app captures, or captured by script)
brand/brand.json       colours, fonts, wordmark and Cham, sampled from the real app
assets/cham.glb        optional 3D Cham (used on covers automatically if present)
output/<post-id>/      ig/01-08.png (4:5), tiktok/01-08.png (9:16), cover.mp4,
                       caption-ig.txt, caption-tiktok.txt, manifest.json
pipeline/              the scripts
```

## Setup

```bash
cd content
npm install                      # playwright
npx playwright install chromium  # once
# ffmpeg must be on PATH for cover.mp4
```

Three.js (r170) and the Inter fonts are vendored, so nothing else is downloaded at render time.

## Run

```bash
npm run topics        # re-score + rank topics.json by hook strength, flag expired news
npm run news          # scan Ofqual / DfE / UCAS / Schools Week feeds -> research/news-candidates.json
PLASMO_TEST_EMAIL=… PLASMO_TEST_PASSWORD=… npm run screenshots   # add -- --headed to watch
npm run validate      # word counts, sources, no-guarantee rules
npm run build         # render every post (slides + MP4)
npm run build:fast    # slides only, no video
node pipeline/render.mjs six-weeks-until-mocks   # one post
```

If a screenshot is missing, the build uses a striped "Screenshot pending" placeholder and marks the post `"draft": true` in `manifest.json`. Don't post drafts.

## Writing a post

Copy any file in `posts/`. Rules (enforced by `npm run validate`):

- 6–8 slides: `hook` first, `cta` last, one `plasmo` slide with a real screenshot.
- Layouts: `hook`, `tip` (`n` for 01/02…, or `stat` for a big number), `plasmo`, `mood` (Cham), `cta`.
- About 25 words per slide at most. Wrap words in `{braces}` to highlight them.
- Any stat, %, date or year needs `"sources": ["id"]` pointing at the post's `sources[]` (url, publisher, accessed date, and the exact claim). The source shows as a small footnote.
- No guarantees, promised outcomes, invented quotes or student stories. The validator blocks "guarantee", "promise", "will get/pass…" and similar.
- Put a 3D hero on the hook slide with `"hero"`: `{ "type": "phone", "screenshot": "x.png" }`, `{ "type": "number", "text": "6" }` or `{ "type": "cham", "mood": "smug" }`. One hero per slide; everything else stays flat.
- News posts can set `"expires"`, and the validator then warns once the date has passed.

## TikTok versions

Every post renders twice. The TikTok version is 1080×1920 and keeps text out of TikTok's UI: nothing important in the top ~300px (the For You header) or the bottom ~470px and right ~140px (caption and buttons). Add a `"tiktok"` block to a post to change the TikTok copy without touching the Instagram one:

```json
"tiktok": {
  "slides": { "0": { "kicker": "be honest", "headline": "revision: {this or that?}", "sub": "comment your 5 letters BEFORE you swipe" } },
  "caption": "keyword-first caption, because people search TikTok like Google",
  "sound": "which sound to pick"
}
```

House style for TikTok: lowercase, conversational hooks ("pov:", "stop doing X"), a white caption-bubble subline, keyword-led captions with 3–5 hashtags, and a comment prompt. Business accounts can only use sounds from TikTok's Commercial Music Library.

## Screenshot safety

`pipeline/screenshots.mjs` blocks Stripe, checkout, billing and subscribe traffic. It refuses to click anything that looks like pay, buy, upgrade or delete. It stops after `maxAiMarks` (5) AI-marked answers and only logs in with the test account from env vars. The selectors in `pipeline/screenshots.config.json` are best guesses, because the site wasn't reachable when they were written. Run it with `--headed` once and fix any step that fails (failures save a capture to `screenshots/_debug/`).

## 3D

`pipeline/scene/` is a Three.js scene driven by Playwright (WebGL via SwiftShader works headless). It has a tilted phone mockup with the screenshot as the screen texture, an extruded brand-colour number, and either the 3D Cham (`assets/cham.glb`, recoloured to the mood's `body` colour, or only the material named in `brand.cham.glbMaterialName`) or a layered 2D Cham card with depth. The scene uses studio lighting (room environment, key light and brand-coloured rim light) and a soft contact shadow. The cover MP4 is the same scene swaying slowly for 7s at 30fps, encoded with H.264.
