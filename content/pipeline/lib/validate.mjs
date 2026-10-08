// Content rules for a post JSON. Returns { errors, warnings }.
const LAYOUTS = ['hook', 'tip', 'plasmo', 'cta', 'mood', 'choice'];
const TEXT_FIELDS = ['kicker', 'headline', 'sub', 'body', 'stat', 'small', 'optionA', 'optionB'];

// Never imply Plasmo guarantees grades or offers; no fabricated testimonials.
const BANNED = [
  [/guarantee/i, 'no guarantees'],
  [/\b(will|100%)\s+(get|pass|boost|improve)\b/i, 'no promised outcomes'],
  [/\bpromise\b/i, 'no promises'],
  [/\b(secure|land|get) (an? )?(offer|place) (with|using) plasmo\b/i, 'Plasmo cannot secure offers'],
  [/\bplasmo (users|students) (got|achieved|scored)\b/i, 'no unverified user-outcome claims'],
  [/"[^"]{12,}"\s*[-–—]\s*[A-Z][a-z]+/, 'looks like a quote/testimonial; needs a real source'],
];

// Text that looks factual (stats, dates, years) must cite a source.
const FACTY = /(\d+(\.\d+)?\s*%|\b(19|20)\d\d\b|\b\d{1,3}(,\d{3})+\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b\s*\d|\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b|\b\d+\s*(in|out of)\s*\d+\b|\b\d+\s*[–-]\s*\d+\s*hours?\b)/i;

export const slideText = (s) => TEXT_FIELDS.map((k) => s[k]).filter(Boolean).join(' ').replace(/[{}\n]/g, ' ');
export const wordCount = (t) => t.split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length;

export function validatePost(post, { brand } = {}) {
  const errors = [], warnings = [];
  const where = (i) => `slide ${i + 1}`;
  if (!post.id || !/^[a-z0-9-]+$/.test(post.id)) errors.push('id must be kebab-case');
  if (!Array.isArray(post.slides)) return { errors: [...errors, 'slides[] missing'], warnings };
  const n = post.slides.length;
  if (n < 6 || n > 8) errors.push(`needs 6–8 slides, has ${n}`);
  if (post.slides[0]?.layout !== 'hook') errors.push('slide 1 must be layout "hook"');
  if (post.slides[n - 1]?.layout !== 'cta') errors.push('last slide must be layout "cta"');
  if (!post.slides.some((s) => s.layout === 'plasmo')) warnings.push('no "plasmo" slide showing the app');

  const sourceIds = new Set();
  for (const [k, src] of (post.sources || []).entries()) {
    if (!src.id || !src.url || !src.publisher || !src.accessed) errors.push(`sources[${k}] needs id, url, publisher, accessed`);
    if (src.url && !/^https?:\/\//.test(src.url)) errors.push(`sources[${k}].url must be http(s)`);
    sourceIds.add(src.id);
  }

  post.slides.forEach((s, i) => {
    if (!LAYOUTS.includes(s.layout)) errors.push(`${where(i)}: unknown layout "${s.layout}"`);
    const text = slideText(s);
    const wc = wordCount(text);
    if (wc > 32) errors.push(`${where(i)}: ${wc} words (max ~25)`);
    else if (wc > 25) warnings.push(`${where(i)}: ${wc} words (aim for ≤25)`);
    for (const [re, why] of BANNED) if (re.test(text)) errors.push(`${where(i)}: "${text.match(re)[0]}" — ${why}`);
    for (const id of s.sources || []) if (!sourceIds.has(id)) errors.push(`${where(i)}: unknown source "${id}"`);
    if (s.layout !== 'cta' && FACTY.test(text) && !(s.sources || []).length && !s.noSourceNeeded) {
      errors.push(`${where(i)}: looks factual ("${text.match(FACTY)[0]}") but cites no source (add sources[] or noSourceNeeded:true with a reason)`);
    }
    if (s.layout === 'plasmo' && !s.screenshot) errors.push(`${where(i)}: plasmo slide needs a screenshot`);
    if (s.layout === 'choice' && !(s.optionA && s.optionB)) errors.push(`${where(i)}: choice slide needs optionA and optionB`);
    if (s.layout === 'mood' && brand && !brand.chamMoods[s.mood]) errors.push(`${where(i)}: unknown mood "${s.mood}" (see brand.json chamMoods)`);
    if (s.hero && s.layout !== 'hook') warnings.push(`${where(i)}: 3D heroes are designed for the hook slide`);
  });
  return { errors, warnings };
}
