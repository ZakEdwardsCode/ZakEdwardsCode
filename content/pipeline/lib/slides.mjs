// HTML/CSS templates for carousel slides, styled after the Plasmo app
// (dark teal hero screens, light grey pages with white cards, teal accents).
// Two formats: Instagram 4:5 and TikTok 9:16 (with TikTok's UI safe zones).
import { fontFaceCss } from './brand.mjs';

export const FORMATS = {
  ig: { w: 1080, h: 1350, top: 140, bottom: 150, left: 96, right: 96, counter: true },
  tiktok: { w: 1080, h: 1920, top: 300, bottom: 470, left: 80, right: 140, counter: false },
};
// kept for older callers
export const SLIDE_W = FORMATS.ig.w;
export const SLIDE_H = FORMATS.ig.h;

const esc = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// {word} -> highlighted span, \n -> line break
export const rich = (s = '') => esc(s).replace(/\{(.+?)\}/g, '<span class="hl">$1</span>').replace(/\n/g, '<br>');

function css(brand, F) {
  const c = brand.colors;
  const f = brand.fonts;
  return `
${fontFaceCss(brand)}
:root{--ink:${c.ink};--paper:${c.paper};--card:${c.card};--primary:${c.primary};--deep:${c.primaryDeep};--teal:${c.teal};--accent:${c.accent};
--dark:${c.dark};--dark2:${c.dark2};--dark3:${c.dark3};--chip:${c.chip};--orange:${c.orange};--green:${c.green};--muted:${c.muted};--line:${c.line};
--top:${F.top}px;--bottom:${F.bottom}px;--left:${F.left}px;--right:${F.right}px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:${F.w}px;height:${F.h}px;overflow:hidden}
body{font-family:'${f.body.family}',sans-serif;color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
.slide{position:relative;width:100%;height:100%;overflow:hidden}
.h-display{font-family:'${f.display.family}';font-weight:900;letter-spacing:-0.04em;line-height:0.95}
.h-heading{font-family:'${f.heading.family}';font-weight:800;letter-spacing:-0.03em;line-height:1.04}
.body{font-size:44px;line-height:1.34;font-weight:500;color:var(--muted)}
.hl{color:var(--teal)}
.dark .hl{background:linear-gradient(135deg,#B5ECF7 0%,${c.accent} 45%,${c.primary} 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.kicker{font-family:'${f.bodyBold.family}';font-weight:700;font-size:28px;letter-spacing:0.26em;text-transform:uppercase;color:var(--teal)}
.dark .kicker{color:var(--accent)}
.dark{background:radial-gradient(120% 70% at 80% 0%, var(--dark3) 0%, var(--dark) 45%, var(--dark2) 100%);color:#fff}
.dark .body{color:#C3D6DD}
/* content box inside the safe zone; [data-fit] shrinks headings until it fits */
.fit{position:absolute;left:var(--left);right:var(--right);top:var(--top);bottom:var(--bottom);display:flex;flex-direction:column;justify-content:flex-start}
.fit:not(.top)>:first-child{margin-top:auto}.fit:not(.top):not(.end)>:last-child{margin-bottom:auto}
/* chrome */
.counter{position:absolute;top:60px;right:var(--left);font-family:'${f.bodyBold.family}';font-weight:700;font-size:24px;letter-spacing:.14em;color:var(--muted)}
.dark .counter{color:#7FA3B0}
.wm{position:absolute;height:44px;color:var(--ink);opacity:.5;${F.counter ? 'bottom:56px;right:var(--left)' : 'top:190px;left:var(--left)'}}
.wm svg{height:100%;width:auto;display:block}
.dark .wm{color:#fff;opacity:.7}
.foot{position:absolute;left:var(--left);right:${F.counter ? '320px' : 'var(--right)'};${F.counter ? 'bottom:62px' : `bottom:${F.bottom - 60}px`};font-size:21px;line-height:1.3;color:var(--muted)}
.dark .foot{color:#86A7B3}
/* TikTok-native caption bubble (white box, dark text) */
.bubble{display:inline;background:#fff;color:#111;font-family:'${f.bodyBold.family}';font-weight:700;font-size:46px;line-height:1.55;padding:6px 18px;border-radius:14px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
`;
}

function chrome(brand, slide, ctx) {
  const F = ctx.F;
  const foot = slide._footnote ? `<div class="foot">${esc(slide._footnote)}</div>` : '';
  const counter = F.counter ? `<div class="counter">${ctx.i + 1} / ${ctx.n}</div>` : '';
  const wm = ctx.i === 0 || slide.layout === 'cta' ? '' : `<div class="wm">${brand.logoSvg}</div>`;
  return `${counter}${wm}${foot}`;
}

// Cover. heroUrl: transparent PNG of the 3D hero.
function hook(brand, s, ctx) {
  const F = ctx.F;
  const tt = ctx.format === 'tiktok';
  const heroH = tt ? 780 : 600;
  const heroBottom = tt ? F.bottom - 150 : 40;
  const textBottom = ctx.heroUrl ? heroBottom + heroH + 10 : F.bottom;
  return `
<div class="slide dark hook">
  <div class="glow"></div>
  ${ctx.chamUrl && !tt ? `<img class="cham" src="${ctx.chamUrl}">` : ''}
  <div class="fit end" data-fit style="bottom:${textBottom}px;gap:26px;top:${tt ? 250 : 190}px">
    ${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}
    <h1 class="h-display" data-shrink style="font-size:${s.size || (tt ? 132 : 124)}px">${rich(s.headline)}</h1>
    ${s.sub ? (tt ? `<p style="margin-top:8px"><span class="bubble">${rich(s.sub)}</span></p>` : `<p class="body" style="font-size:40px">${rich(s.sub)}</p>`) : ''}
  </div>
  ${ctx.heroUrl ? `<img class="hero" src="${ctx.heroUrl}" style="bottom:${heroBottom}px;height:${heroH}px">` : ''}
  ${chrome(brand, s, ctx)}
</div>
<style>
.hook .glow{position:absolute;width:1400px;height:1400px;left:-160px;bottom:-820px;border-radius:50%;background:radial-gradient(circle, ${brand.colors.primary}88 0%, ${brand.colors.primary}22 40%, transparent 68%)}
.hook .hero{position:absolute;left:0;right:0;width:${F.w}px;object-fit:contain}
.hook .cham{position:absolute;left:var(--left);top:${tt ? 170 : 70}px;height:${tt ? 120 : 104}px;filter:drop-shadow(0 10px 18px rgba(0,0,0,.45))}
</style>`;
}

function tip(brand, s, ctx) {
  const big = s.stat ? `<div class="stat h-display">${rich(s.stat)}</div>` : '';
  const chip = s.stat ? '' : `<span class="chip">${esc(s.chip ?? String(s.n ?? ctx.i))}</span>`;
  return `
<div class="slide tip">
  <div class="fit" data-fit>
    <div class="card">
      <div class="row">${chip}${s.kicker ? `<span class="kicker">${rich(s.kicker)}</span>` : ''}${s.tag ? `<span class="tag">${esc(s.tag)}</span>` : ''}</div>
      ${big}
      <h2 class="h-heading" data-shrink style="font-size:${s.size || (ctx.format === 'tiktok' ? 132 : 104)}px">${rich(s.headline)}</h2>
      ${s.body ? `<p class="body" style="font-size:${ctx.format === 'tiktok' ? 60 : 50}px">${rich(s.body)}</p>` : ''}
    </div>
  </div>
  ${chrome(brand, s, ctx)}
</div>
<style>
.tip .card{background:var(--card);border-radius:44px;padding:72px 64px;display:flex;flex-direction:column;gap:36px;box-shadow:0 30px 60px -36px rgba(14,26,32,.35);border:1px solid var(--line)}
.tip .row{display:flex;align-items:center;gap:22px;flex-wrap:wrap}
.tip .chip{font-family:'${brand.fonts.bodyBold.family}';font-weight:700;font-size:40px;color:var(--teal);background:var(--chip);border-radius:14px;padding:8px 18px}
.tip .tag{margin-left:auto;font-family:'${brand.fonts.bodyBold.family}';font-weight:700;font-size:28px;color:var(--muted)}
.tip .stat{font-size:${s.statSize || 168}px;color:var(--primary);line-height:1}
</style>`;
}

function plasmo(brand, s, ctx) {
  const tt = ctx.format === 'tiktok';
  return `
<div class="slide plasmo">
  <div class="fit top" data-fit style="gap:24px">
    <div class="kicker">${rich(s.kicker || 'Inside Plasmo')}</div>
    <h2 class="h-heading" data-shrink style="font-size:${s.size || (tt ? 84 : 76)}px">${rich(s.headline)}</h2>
    ${s.body ? `<p class="body" style="font-size:${tt ? 42 : 38}px">${rich(s.body)}</p>` : ''}
    <div class="shot"><img src="${ctx.screenshotUrl}" style="object-position:${s.focus || 'top'}"></div>
  </div>
  ${chrome(brand, s, ctx)}
</div>
<style>
.plasmo .shot{flex:1;min-height:${tt ? 760 : 420}px;margin-top:16px;border-radius:30px;overflow:hidden;background:#E5E5E5;box-shadow:0 40px 80px -40px rgba(14,26,32,.55),0 0 0 1px var(--line)}
.plasmo .shot img{width:100%;height:100%;object-fit:${s.fit || 'contain'};display:block}
</style>`;
}

function choice(brand, s, ctx) {
  const opt = (letter, text, cls) => `<div class="opt ${cls}"><div class="letter">${letter}</div><div class="otext h-heading">${rich(text)}</div></div>`;
  return `
<div class="slide choice">
  <div class="fit" data-fit style="gap:30px">
    ${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}
    ${s.headline ? `<h2 class="h-heading" data-shrink style="font-size:${s.size || 64}px">${rich(s.headline)}</h2>` : ''}
    ${opt('A', s.optionA, 'a')}
    <div class="or">or</div>
    ${opt('B', s.optionB, 'b')}
  </div>
  ${chrome(brand, s, ctx)}
</div>
<style>
.choice .opt{display:flex;align-items:center;gap:36px;padding:44px 44px;border-radius:32px;border:3px solid}
.choice .opt.a{background:#0F1A1F;color:#fff;border-color:var(--primary);box-shadow:0 0 0 6px ${brand.colors.primary}22}
.choice .opt.b{background:#1A120A;color:#fff;border-color:var(--orange);box-shadow:0 0 0 6px ${brand.colors.orange}22}
.choice .letter{flex:none;width:112px;height:112px;border-radius:28px;display:flex;align-items:center;justify-content:center;font:900 64px '${brand.fonts.display.family}';background:#ffffff14;border:2px solid #ffffff22}
.choice .opt.a .letter{color:var(--accent)}.choice .opt.b .letter{color:var(--orange)}
.choice .otext{font-size:${ctx.format === 'tiktok' ? 72 : 62}px}
.choice .or{text-align:center;font:700 30px '${brand.fonts.bodyBold.family}';letter-spacing:.24em;text-transform:uppercase;color:var(--muted)}
</style>`;
}

function cta(brand, s, ctx) {
  const tt = ctx.format === 'tiktok';
  return `
<div class="slide dark cta">
  <div class="fit" data-fit style="align-items:center;text-align:center;gap:30px">
    ${ctx.chamUrl ? `<img class="cham" src="${ctx.chamUrl}">` : ''}
    <div class="kicker">${rich(s.kicker || 'GCSE & A-Level exam prep')}</div>
    <div class="logo">${brand.logoSvg}</div>
    <h2 class="h-heading" data-shrink style="font-size:${s.size || (tt ? 76 : 68)}px;max-width:860px">${rich(s.headline || 'Save this for later')}</h2>
    <div class="btn">${rich(s.body || '100 free marks at plasmo.uk')} →</div>
    ${s.small ? `<p class="body" style="font-size:34px">${rich(s.small)}</p>` : ''}
  </div>
  ${chrome(brand, s, ctx)}
</div>
<style>
.cta .cham{height:${tt ? 230 : 190}px;filter:drop-shadow(0 18px 24px rgba(0,0,0,.5))}
.cta .logo{height:${tt ? 150 : 128}px;color:#fff}
.cta .logo svg{height:100%;width:auto}
.cta .btn{font:800 46px '${brand.fonts.heading.family}';background:var(--primary);color:#fff;padding:30px 54px;border-radius:24px;box-shadow:0 24px 40px -20px ${brand.colors.primary}}
.cta .btn .hl{background:none;color:#fff;-webkit-text-fill-color:#fff}
</style>`;
}

function mood(brand, s, ctx) {
  return tip(brand, { ...s, kicker: s.kicker || ctx.mood?.label }, ctx);
}

const LAYOUTS = { hook, tip, plasmo, cta, mood, choice };

const FIT_SCRIPT = `
<script>
window.__fit = () => {
  for (const box of document.querySelectorAll('[data-fit]')) {
    const heads = [...box.querySelectorAll('[data-shrink]')];
    let guard = 80;
    while (box.scrollHeight > box.clientHeight + 1 && guard--) {
      for (const h of heads) h.style.fontSize = (parseFloat(getComputedStyle(h).fontSize) * 0.96) + 'px';
      for (const b of box.querySelectorAll('.body')) b.style.fontSize = Math.max(28, parseFloat(getComputedStyle(b).fontSize) * 0.98) + 'px';
    }
    if (box.scrollHeight > box.clientHeight + 1) document.body.dataset.overflow = '1';
  }
};
</script>`;

export function slideHtml(brand, slide, ctx) {
  const layout = LAYOUTS[slide.layout];
  if (!layout) throw new Error(`Unknown layout "${slide.layout}"`);
  ctx.F = FORMATS[ctx.format || 'ig'];
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css(brand, ctx.F)}</style></head>
<body>${layout(brand, slide, ctx)}${FIT_SCRIPT}</body></html>`;
}

export function placeholderScreenshotHtml(brand, name) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fontFaceCss(brand)}
*{margin:0}html,body{width:390px;height:844px}
body{display:flex;align-items:center;justify-content:center;flex-direction:column;gap:14px;text-align:center;padding:30px;box-sizing:border-box;
background:repeating-linear-gradient(135deg,#efedf6 0 18px,#e6e2f2 18px 36px);font-family:'${brand.fonts.heading.family}';color:#6E6A86}
b{font-size:30px;color:#120E24}span{font-size:17px;font-family:'${brand.fonts.body.family}'}</style></head>
<body><b>Screenshot pending</b><span>${esc(name)}</span><span>Run <code>npm run screenshots</code> to capture the real app.</span></body></html>`;
}
