#!/usr/bin/env node
// Renders every post in /content/posts (or the ids given) to
//   /content/output/<post-id>/{01.png..08.png, cover.mp4, caption.txt, manifest.json}
//
//   node pipeline/render.mjs                      all posts
//   node pipeline/render.mjs how-to-get-astar     one post
//   flags: --no-video  --force (render despite validation errors)
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { chromium } from 'playwright';
import { DIRS, p } from './lib/paths.mjs';
import { startServer } from './lib/server.mjs';
import { loadBrand, moodOf, fontFaceCss } from './lib/brand.mjs';
import { slideHtml, placeholderScreenshotHtml, rich, SLIDE_W, SLIDE_H } from './lib/slides.mjs';
import { validatePost } from './lib/validate.mjs';
import { chamSvg } from './lib/cham.mjs';

const args = process.argv.slice(2);
const flags = new Set(args.filter((a) => a.startsWith('--')));
const only = args.filter((a) => !a.startsWith('--'));
const VIDEO = { w: 1080, h: 1920, fps: 30 };
const GL_ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'];

const rel = (abs) => '/' + path.relative(p(), abs).split(path.sep).join('/');
const cacheDir = p('output', '_cache');

function loadPosts() {
  return fs.readdirSync(DIRS.posts)
    .filter((f) => f.endsWith('.json'))
    .map((f) => ({ file: f, ...JSON.parse(fs.readFileSync(path.join(DIRS.posts, f), 'utf8')) }))
    .filter((post) => !only.length || only.includes(post.id) || only.includes(post.file.replace(/\.json$/, '')))
    .sort((a, b) => (a.order ?? 99) - (b.order ?? 99));
}

// Real screenshot from /content/screenshots, else a clearly-labelled placeholder.
async function screenshotFor(ctx, name) {
  const real = path.join(DIRS.screenshots, name);
  if (fs.existsSync(real)) return rel(real);
  const out = path.join(cacheDir, `placeholder-${name.replace(/\.\w+$/, '')}.png`);
  if (!fs.existsSync(out)) {
    const page = await ctx.browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
    await page.goto(`${ctx.base}/pipeline/scene/scene.html`); // any same-origin page so /brand fonts resolve
    await page.setContent(placeholderScreenshotHtml(ctx.brand, name), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: out });
    await page.close();
  }
  ctx.draft.add(`screenshot missing: screenshots/${name} (placeholder used)`);
  return rel(out);
}

// 2D Cham as a transparent PNG (custom art in brand/ wins over the generated placeholder).
async function chamImage(ctx, moodKey) {
  for (const f of ['cham.png', 'cham.svg']) {
    const custom = path.join(DIRS.brand, f);
    if (fs.existsSync(custom)) return rel(custom);
  }
  const out = path.join(cacheDir, `cham-${moodKey}.png`);
  const mood = moodOf(ctx.brand, moodKey);
  const page = await ctx.browser.newPage({ viewport: { width: 840, height: 760 } });
  await page.goto(`${ctx.base}/pipeline/scene/scene.html`);
  await page.setContent(`<style>${fontFaceCss(ctx.brand)}html,body{margin:0;background:transparent}svg{width:840px;height:760px;display:block}</style>${chamSvg({ ...mood, ink: ctx.brand.colors.ink })}`);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: out, omitBackground: true });
  await page.close();
  return rel(out);
}

async function chamMarkup(ctx, moodKey) {
  for (const f of ['cham.png', 'cham.svg']) if (fs.existsSync(path.join(DIRS.brand, f))) return `<img src="${rel(path.join(DIRS.brand, f))}">`;
  return chamSvg({ ...moodOf(ctx.brand, moodKey), ink: ctx.brand.colors.ink });
}

async function sceneConfig(ctx, hero) {
  const c = ctx.brand.colors;
  const cfg = { colors: { primary: c.primary, primaryDeep: c.primaryDeep, rim: c.primary } };
  if (hero.type === 'phone') {
    Object.assign(cfg, { kind: 'phone', screenshotUrl: await screenshotFor(ctx, hero.screenshot) });
  } else if (hero.type === 'number') {
    Object.assign(cfg, { kind: 'number', text: hero.text, fontUrl: `/brand/${ctx.brand.fonts.number3d}` });
  } else if (hero.type === 'cham') {
    const mood = moodOf(ctx.brand, hero.mood || 'default');
    const glb = path.join(DIRS.assets, 'cham.glb');
    if (fs.existsSync(glb)) {
      Object.assign(cfg, { kind: 'cham3d', glbUrl: rel(glb), mood, glbMaterialName: ctx.brand.cham.glbMaterialName });
    } else {
      Object.assign(cfg, { kind: 'cham2d', imageUrl: await chamImage(ctx, hero.mood || 'default') });
    }
    cfg.colors.rim = mood.body;
  } else throw new Error(`Unknown hero type "${hero.type}"`);
  return cfg;
}

async function openScene(ctx, cfg, { width, height, scale = 1 }) {
  const page = await ctx.glBrowser.newPage({ viewport: { width, height }, deviceScaleFactor: scale });
  page.on('pageerror', (e) => console.error('  [scene]', e.message));
  await page.goto(`${ctx.base}/pipeline/scene/scene.html`);
  await page.waitForFunction(() => typeof window.setupScene === 'function');
  await page.evaluate((c) => window.setupScene(c), { ...cfg, width, height });
  return page;
}

async function renderHero(ctx, hero, outFile) {
  const cfg = await sceneConfig(ctx, hero);
  const page = await openScene(ctx, { ...cfg, fill: hero.fill ?? (hero.type === 'phone' ? 1.2 : 1.0) }, { width: 2160, height: 1400 });
  await page.screenshot({ path: outFile, omitBackground: true });
  await page.close();
}

async function renderVideo(ctx, post, hero, outFile) {
  const { brand } = ctx;
  const hook = post.slides[0];
  const seconds = post.video?.seconds ?? 7;
  const cfg = await sceneConfig(ctx, hero);
  const overlayCss = `${fontFaceCss(brand)}
    #overlay{font-family:'${brand.fonts.body.family}';color:#fff}
    .ov-top{position:absolute;left:96px;right:96px;top:230px}
    .ov-k{display:inline-block;font:800 34px '${brand.fonts.heading.family}';letter-spacing:.12em;text-transform:uppercase;padding:16px 28px;border-radius:999px;background:${brand.colors.accent};color:${brand.colors.ink}}
    .ov-h{font:900 ${post.video?.headlineSize || 124}px/0.95 '${brand.fonts.display.family}';letter-spacing:-.035em;margin-top:36px}
    .ov-h .hl{color:${brand.colors.accent}}
    .ov-logo{position:absolute;left:0;right:0;bottom:200px;display:flex;justify-content:center;height:62px;color:#fff;opacity:.9}
    .ov-logo svg{height:100%;width:auto}`;
  const overlayHtml = `<div class="ov-top">${hook.kicker ? `<div class="ov-k">${rich(hook.kicker)}</div>` : ''}<div class="ov-h">${rich(post.video?.headline || hook.headline)}</div></div><div class="ov-logo">${brand.logoSvg}</div>`;
  const background = `radial-gradient(90% 55% at 50% 72%, ${brand.colors.primary} 0%, ${brand.colors.primaryDeep} 40%, ${brand.colors.ink} 85%)`;
  const page = await openScene(ctx, { ...cfg, overlayHtml, overlayCss, background, fill: 0.55, shiftY: 0.14, sway: hero.type === 'phone' ? 0.42 : 0.5 }, { width: VIDEO.w, height: VIDEO.h });

  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(VIDEO.fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', outFile]);
  const done = new Promise((res, rej) => { ff.on('close', (code) => (code === 0 ? res() : rej(new Error(`ffmpeg exited ${code}`)))); ff.on('error', rej); });
  const frames = Math.round(seconds * VIDEO.fps);
  for (let f = 0; f < frames; f++) {
    await page.evaluate(([t, d]) => window.renderAt(t, d), [f / VIDEO.fps, seconds]);
    const jpg = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(jpg)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await done;
  await page.close();
}

function footnote(post, slide) {
  if (slide.footnote) return slide.footnote;
  const srcs = (slide.sources || []).map((id) => post.sources.find((s) => s.id === id)).filter(Boolean);
  if (!srcs.length) return '';
  return 'Source: ' + [...new Set(srcs.map((s) => s.short || s.publisher))].join('; ');
}

function caption(post) {
  const lines = [post.caption || post.title, '', (post.hashtags || []).map((h) => `#${h.replace(/^#/, '')}`).join(' ')];
  if (post.sources?.length) {
    lines.push('', 'Sources:');
    for (const s of post.sources) lines.push(`- ${s.publisher}: ${s.title} ${s.url}`);
  }
  return lines.join('\n') + '\n';
}

async function renderPost(ctx, post) {
  const t0 = Date.now();
  const { errors, warnings } = validatePost(post, { brand: ctx.brand });
  warnings.forEach((w) => console.warn(`  ! ${w}`));
  if (errors.length) {
    errors.forEach((e) => console.error(`  ✗ ${e}`));
    if (!flags.has('--force')) { console.error(`  skipped ${post.id} (fix errors or pass --force)`); return false; }
  }
  ctx.draft = new Set();
  const outDir = path.join(DIRS.output, post.id);
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(path.join(outDir, '_html'), { recursive: true });

  const n = post.slides.length;
  const hookHero = post.slides[0].hero;
  const files = [];
  for (const [i, s] of post.slides.entries()) {
    const slide = { ...s, _footnote: footnote(post, s) };
    const sctx = { i, n };
    if (s.hero) {
      const heroFile = path.join(outDir, `_hero-${i + 1}.png`);
      await renderHero(ctx, s.hero, heroFile);
      sctx.heroUrl = rel(heroFile);
    }
    if (s.screenshot) sctx.screenshotUrl = await screenshotFor(ctx, s.screenshot);
    if (s.layout === 'mood') { sctx.mood = moodOf(ctx.brand, s.mood); sctx.chamMarkup = await chamMarkup(ctx, s.mood); }

    const htmlFile = path.join(outDir, '_html', `slide-${String(i + 1).padStart(2, '0')}.html`);
    fs.writeFileSync(htmlFile, slideHtml(ctx.brand, slide, sctx));
    const page = ctx.slidePage;
    await page.goto(ctx.base + rel(htmlFile), { waitUntil: 'load' });
    await page.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((im) => im.decode().catch(() => {}))); window.__fit(); });
    if (await page.evaluate(() => document.body.dataset.overflow === '1')) warnings.push(`slide ${i + 1}: text still overflows after shrinking`);
    const png = path.join(outDir, `${String(i + 1).padStart(2, '0')}.png`);
    await page.screenshot({ path: png });
    files.push(path.basename(png));
  }

  let video = null;
  if (hookHero && !flags.has('--no-video')) {
    video = 'cover.mp4';
    await renderVideo(ctx, post, hookHero, path.join(outDir, video));
  }

  fs.writeFileSync(path.join(outDir, 'caption.txt'), caption(post));
  fs.writeFileSync(path.join(outDir, 'manifest.json'), JSON.stringify({
    id: post.id, title: post.title, renderedAt: new Date().toISOString(), slides: files, video,
    draft: ctx.draft.size > 0, draftReasons: [...ctx.draft], warnings, sources: post.sources,
  }, null, 2));
  console.log(`  ✓ ${post.id}: ${files.length} slides${video ? ' + cover.mp4' : ''} in ${((Date.now() - t0) / 1000).toFixed(1)}s${ctx.draft.size ? '  [DRAFT: ' + [...ctx.draft].join('; ') + ']' : ''}`);
  return true;
}

async function main() {
  fs.mkdirSync(cacheDir, { recursive: true });
  const brand = loadBrand();
  const posts = loadPosts();
  if (!posts.length) { console.error('No posts matched.'); process.exit(1); }
  const server = await startServer();
  const browser = await chromium.launch();
  const glBrowser = await chromium.launch({ args: GL_ARGS });
  const slidePage = await browser.newPage({ viewport: { width: SLIDE_W, height: SLIDE_H }, deviceScaleFactor: 1 });
  const ctx = { brand, base: server.base, browser, glBrowser, slidePage };
  let failed = 0;
  try {
    for (const post of posts) {
      console.log(`• ${post.id}`);
      try { if (!(await renderPost(ctx, post))) failed++; }
      catch (e) { failed++; console.error(`  ✗ ${e.stack || e}`); }
    }
  } finally {
    await browser.close(); await glBrowser.close(); await server.close();
  }
  process.exit(failed ? 1 : 0);
}

main();
