// HTML/CSS templates for 1080x1350 carousel slides.
import { fontFaceCss } from './brand.mjs';

export const SLIDE_W = 1080;
export const SLIDE_H = 1350;

const esc = (s = '') => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
// {word} -> highlighted span, \n -> line break
export const rich = (s = '') => esc(s).replace(/\{(.+?)\}/g, '<span class="hl">$1</span>').replace(/\n/g, '<br>');

function css(brand) {
  const c = brand.colors;
  return `
${fontFaceCss(brand)}
:root{--ink:${c.ink};--paper:${c.paper};--primary:${c.primary};--deep:${c.primaryDeep};--accent:${c.accent};--pink:${c.pink};--muted:${c.muted};--line:${c.line};--m:96px}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:${SLIDE_W}px;height:${SLIDE_H}px;overflow:hidden}
body{font-family:'${brand.fonts.body.family}',sans-serif;color:var(--ink);background:var(--paper);-webkit-font-smoothing:antialiased}
.slide{position:relative;width:100%;height:100%;overflow:hidden;padding:var(--m)}
.h-display{font-family:'${brand.fonts.display.family}';font-weight:900;letter-spacing:-0.035em;line-height:0.95}
.h-heading{font-family:'${brand.fonts.heading.family}';font-weight:800;letter-spacing:-0.025em;line-height:1.02}
.body{font-size:46px;line-height:1.32;font-weight:500;color:var(--muted)}
.body b{font-weight:700;color:var(--ink)}
.hl{color:var(--primary)}
.dark .hl{color:var(--accent)}
.kicker{display:inline-block;font-family:'${brand.fonts.heading.family}';font-weight:800;font-size:28px;letter-spacing:0.12em;text-transform:uppercase;padding:14px 24px;border-radius:999px;background:var(--primary);color:#fff}
.dark .kicker{background:var(--accent);color:var(--ink)}
/* chrome */
.counter{position:absolute;top:56px;right:var(--m);font-family:'${brand.fonts.heading.family}';font-weight:800;font-size:26px;letter-spacing:0.06em;opacity:.45}
.wm{position:absolute;bottom:52px;right:var(--m);height:40px;opacity:.16;color:var(--ink)}
.wm svg{height:100%;width:auto;display:block}
.dark .wm{color:#fff;opacity:.22}
.foot{position:absolute;bottom:58px;left:var(--m);right:360px;font-size:22px;line-height:1.3;color:var(--muted);opacity:.85}
.dark .foot{color:#cfc9ea}
.dark{background:var(--ink);color:#fff}
.dark .body{color:#d8d3ee}
/* fit box: headline shrinks until content fits */
.fit{position:absolute;left:var(--m);right:var(--m);top:150px}
`;
}

function chrome(brand, slide, i, n, dark = false) {
  const foot = slide._footnote ? `<div class="foot">${esc(slide._footnote)}</div>` : '';
  return `<div class="counter">${i + 1}/${n}</div><div class="wm">${brand.logoSvg}</div>${foot}`;
}

// Hook / cover slide. heroUrl: transparent PNG of the 3D (or 2D) hero.
function hook(brand, s, ctx) {
  return `
<div class="slide dark hook">
  <div class="glow"></div>
  <div class="fit" data-fit style="bottom:${ctx.heroUrl ? 790 : 220}px">
    ${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}
    <h1 class="h-display" data-shrink style="font-size:${s.size || 132}px;margin-top:34px">${rich(s.headline)}</h1>
    ${s.sub ? `<p class="body" style="margin-top:30px;font-size:42px">${rich(s.sub)}</p>` : ''}
  </div>
  ${ctx.heroUrl ? `<img class="hero" src="${ctx.heroUrl}">` : ''}
  ${chrome(brand, s, ctx.i, ctx.n, true)}
</div>
<style>
.hook .glow{position:absolute;width:1300px;height:1300px;left:-110px;bottom:-760px;border-radius:50%;background:radial-gradient(circle, ${brand.colors.primary}cc 0%, ${brand.colors.primary}33 42%, transparent 70%)}
.hook .hero{position:absolute;left:0;right:0;bottom:50px;width:1080px;height:700px;object-fit:contain}
</style>`;
}

function tip(brand, s, ctx) {
  const big = s.stat
    ? `<div class="stat h-display">${rich(s.stat)}</div>`
    : `<div class="num h-display">${String(s.n ?? ctx.i).padStart(2, '0')}</div>`;
  return `
<div class="slide tip">
  <div class="fit" data-fit style="bottom:170px;display:flex;flex-direction:column;justify-content:center;padding-bottom:60px">
    ${s.kicker ? `<div class="kicker">${rich(s.kicker)}</div>` : ''}
    ${big}
    <h2 class="h-heading" data-shrink style="font-size:${s.size || 104}px;margin-top:26px">${rich(s.headline)}</h2>
    ${s.body ? `<p class="body" style="margin-top:38px;font-size:50px">${rich(s.body)}</p>` : ''}
  </div>
  <div class="bar"></div>
  ${chrome(brand, s, ctx.i, ctx.n)}
</div>
<style>
.tip .kicker{align-self:flex-start}
.tip .num{font-size:220px;color:transparent;-webkit-text-stroke:5px var(--primary);margin-top:18px;line-height:1}
.tip .stat{font-size:${s.statSize || 170}px;color:var(--primary);margin-top:22px;line-height:1}
.tip .bar{position:absolute;left:0;top:0;bottom:0;width:18px;background:linear-gradient(var(--primary),var(--pink))}
</style>`;
}

function plasmo(brand, s, ctx) {
  return `
<div class="slide plasmo">
  <div class="copy">
    <div class="kicker">${rich(s.kicker || 'Where Plasmo fits')}</div>
    <h2 class="h-heading" data-shrink style="font-size:${s.size || 74}px;margin-top:30px">${rich(s.headline)}</h2>
    ${s.body ? `<p class="body" style="margin-top:28px;font-size:38px">${rich(s.body)}</p>` : ''}
  </div>
  <div class="phone"><img src="${ctx.screenshotUrl}"><div class="island"></div></div>
  ${chrome(brand, s, ctx.i, ctx.n)}
</div>
<style>
.plasmo{background:linear-gradient(160deg,var(--paper) 0%,#ece6ff 100%)}
.plasmo .copy{position:absolute;left:var(--m);top:150px;width:470px;bottom:170px;overflow:hidden}
.plasmo .phone{position:absolute;right:76px;top:120px;width:420px;height:910px;border-radius:64px;background:#1c1830;padding:14px;box-shadow:0 50px 90px -30px rgba(40,20,110,.45),0 18px 30px -12px rgba(18,14,36,.35)}
.plasmo .phone img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:52px;display:block;background:#fff}
.plasmo .island{position:absolute;top:30px;left:50%;transform:translateX(-50%);width:110px;height:32px;border-radius:20px;background:#000}
</style>`;
}

function cta(brand, s, ctx) {
  return `
<div class="slide dark cta">
  <div class="fit" data-fit style="bottom:200px;display:flex;flex-direction:column;justify-content:center">
    <svg class="bm" viewBox="0 0 24 24"><path d="M6 3h12a1 1 0 0 1 1 1v17l-7-4.5L5 21V4a1 1 0 0 1 1-1z" fill="currentColor"/></svg>
    <h2 class="h-display" data-shrink style="font-size:${s.size || 128}px;margin-top:40px">${rich(s.headline || 'Save this')}</h2>
    <p class="h-heading" style="font-size:60px;margin-top:36px;color:#fff">${rich(s.body || '+ *100 free marks* at plasmo.uk')}</p>
    ${s.small ? `<p class="body" style="margin-top:28px;font-size:36px">${rich(s.small)}</p>` : ''}
  </div>
  <div class="logo">${brand.logoSvg}</div>
  ${chrome(brand, s, ctx.i, ctx.n, true)}
</div>
<style>
.cta{background:radial-gradient(120% 90% at 85% 0%, var(--primary) 0%, var(--deep) 45%, var(--ink) 100%)}
.cta .bm{width:120px;height:120px;color:var(--accent)}
.cta .logo{position:absolute;left:var(--m);bottom:150px;height:64px;color:#fff}
.cta .logo svg{height:100%;width:auto}
.cta .wm{display:none}
</style>`;
}

function mood(brand, s, ctx) {
  const m = ctx.mood;
  return `
<div class="slide mood">
  <div class="tint"></div>
  <div class="fit" data-fit style="bottom:600px">
    <div class="kicker" style="background:${m.body};color:var(--ink)">${rich(s.kicker || m.label)}</div>
    <h2 class="h-heading" data-shrink style="font-size:${s.size || 84}px;margin-top:28px">${rich(s.headline)}</h2>
    ${s.body ? `<p class="body" style="margin-top:26px;font-size:42px">${rich(s.body)}</p>` : ''}
  </div>
  <div class="cham">${ctx.chamMarkup}</div>
  ${chrome(brand, s, ctx.i, ctx.n)}
</div>
<style>
.mood .tint{position:absolute;inset:0;background:radial-gradient(90% 60% at 70% 85%, ${m.body}55 0%, ${m.belly}22 45%, transparent 75%)}
.mood .cham{position:absolute;right:60px;bottom:120px;width:640px;height:520px;filter:drop-shadow(0 40px 34px rgba(18,14,36,.28)) drop-shadow(0 10px 10px rgba(18,14,36,.18))}
.mood .cham svg,.mood .cham img{width:100%;height:100%;object-fit:contain}
</style>`;
}

// "This or that" poll slide: a question and two lettered options.
function choice(brand, s, ctx) {
  const opt = (letter, text, cls) => `<div class="opt ${cls}"><div class="letter h-display">${letter}</div><div class="otext h-heading">${rich(text)}</div></div>`;
  return `
<div class="slide choice">
  <div class="fit" data-fit style="bottom:170px;display:flex;flex-direction:column;justify-content:center;gap:34px;padding-bottom:40px">
    ${s.kicker ? `<div class="kicker" style="align-self:flex-start">${rich(s.kicker)}</div>` : ''}
    ${s.headline ? `<h2 class="h-heading" data-shrink style="font-size:${s.size || 64}px">${rich(s.headline)}</h2>` : ''}
    ${opt('A', s.optionA, 'a')}
    <div class="or h-heading">or</div>
    ${opt('B', s.optionB, 'b')}
  </div>
  ${chrome(brand, s, ctx.i, ctx.n)}
</div>
<style>
.choice .opt{display:flex;align-items:center;gap:40px;padding:44px 48px;border-radius:44px;background:#fff;box-shadow:0 24px 50px -24px rgba(40,20,110,.35);border:4px solid var(--line)}
.choice .opt.b{background:var(--ink);color:#fff;border-color:var(--ink)}
.choice .letter{flex:none;width:130px;height:130px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:84px;background:var(--primary);color:#fff;padding-bottom:6px}
.choice .opt.b .letter{background:var(--accent);color:var(--ink)}
.choice .otext{font-size:64px}
.choice .or{text-align:center;font-size:36px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}
</style>`;
}

const LAYOUTS = { hook, tip, plasmo, cta, mood, choice };

// Shrinks every [data-shrink] heading until its [data-fit] box stops overflowing.
const FIT_SCRIPT = `
<script>
window.__fit = () => {
  for (const box of document.querySelectorAll('[data-fit], .plasmo .copy')) {
    const heads = [...box.querySelectorAll('[data-shrink]')];
    let guard = 80;
    while (box.scrollHeight > box.clientHeight + 1 && guard--) {
      for (const h of heads) h.style.fontSize = (parseFloat(getComputedStyle(h).fontSize) * 0.96) + 'px';
      for (const b of box.querySelectorAll('.body')) b.style.fontSize = Math.max(30, parseFloat(getComputedStyle(b).fontSize) * 0.98) + 'px';
    }
    if (box.scrollHeight > box.clientHeight + 1) document.body.dataset.overflow = '1';
  }
};
</script>`;

export function slideHtml(brand, slide, ctx) {
  const layout = LAYOUTS[slide.layout];
  if (!layout) throw new Error(`Unknown layout "${slide.layout}"`);
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css(brand)}</style></head>
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
