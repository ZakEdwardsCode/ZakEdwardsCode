#!/usr/bin/env node
// Topic research helpers.
//   node pipeline/research.mjs          re-score + rank topics.json by hook strength, flag expired news
//   node pipeline/research.mjs --scan   pull official UK education feeds into research/news-candidates.json
//
// The scan only *finds* candidate stories. A human (or Claude) still reads the source, writes the
// topic into topics.json with its facts + sources, and turns the best ones into posts/*.json.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { p, DIRS } from './lib/paths.mjs';

const FEEDS = [
  ['Ofqual (GOV.UK)', 'https://www.gov.uk/government/organisations/ofqual.atom'],
  ['Ofqual blog', 'https://ofqual.blog.gov.uk/feed/'],
  ['DfE (GOV.UK)', 'https://www.gov.uk/government/organisations/department-for-education.atom'],
  ['UCAS news', 'https://www.ucas.com/rss.xml'],
  ['Schools Week', 'https://schoolsweek.co.uk/feed/'],
  ['FE Week', 'https://feweek.co.uk/feed/'],
];
const KEYWORDS = /gcse|a[ -]level|exam|ofqual|grade boundar|results|ucas|oxbridge|oxford|cambridge|mock|revision|timetable|jcq|malpractice|curriculum|on-screen|formula/i;

export function hookScore(t, weights) {
  const s = t.scores || {};
  let total = 0;
  for (const [k, w] of Object.entries(weights)) total += (s[k] ?? 1) * w;
  return Math.round(total * 20);
}

function rank() {
  const file = p('topics.json');
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  const today = new Date().toISOString().slice(0, 10);
  for (const t of data.topics) {
    t.expired = Boolean(t.expires && t.expires < today);
    t.hookScore = hookScore(t, data.scoring.weights) - (t.expired ? 40 : 0);
    const ids = new Set(t.sources.map((s) => s.id));
    const missing = (t.facts || []).flatMap((f) => [...f.matchAll(/\[([\w-]+)\]/g)].map((m) => m[1])).filter((id) => !ids.has(id));
    if (missing.length) console.warn(`! ${t.id}: facts cite unknown sources ${missing.join(', ')}`);
    if (!(t.facts || []).every((f) => /\[[\w-]+\]/.test(f))) console.warn(`! ${t.id}: a fact has no [source] tag`);
  }
  data.topics.sort((a, b) => b.hookScore - a.hookScore);
  data.rankedOn = today;
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
  console.log('rank  score  status  topic');
  data.topics.forEach((t, i) => console.log(`${String(i + 1).padStart(4)}  ${String(t.hookScore).padStart(5)}  ${t.status.padEnd(6)}  ${t.title}${t.expired ? '  (expired)' : ''}${t.needsVerification ? '  [verify]' : ''}`));
}

// Minimal RSS/Atom parsing: enough for titles, links and dates.
export function parseFeed(xml) {
  const items = [];
  const blocks = xml.match(/<(item|entry)\b[\s\S]*?<\/\1>/g) || [];
  const tag = (b, n) => (b.match(new RegExp(`<${n}\\b[^>]*>([\\s\\S]*?)<\\/${n}>`)) || [])[1]?.replace(/<!\[CDATA\[|\]\]>/g, '').trim();
  for (const b of blocks) {
    const link = tag(b, 'link') || (b.match(/<link\b[^>]*href="([^"]+)"/) || [])[1];
    items.push({
      title: (tag(b, 'title') || '').replace(/&amp;/g, '&').replace(/&#8217;|&rsquo;/g, '’'),
      url: link,
      date: tag(b, 'pubDate') || tag(b, 'updated') || tag(b, 'published') || null,
      summary: (tag(b, 'description') || tag(b, 'summary') || '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/<[^>]+>/g, '').slice(0, 280),
    });
  }
  return items;
}

async function scan() {
  const since = Date.now() - 30 * 864e5;
  const out = [];
  for (const [name, url] of FEEDS) {
    try {
      const res = await fetch(url, { headers: { 'user-agent': 'plasmo-content-research/1.0' }, signal: AbortSignal.timeout(20000) });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const items = parseFeed(await res.text())
        .filter((it) => KEYWORDS.test(`${it.title} ${it.summary}`))
        .filter((it) => !it.date || Date.parse(it.date) >= since);
      out.push(...items.map((it) => ({ feed: name, ...it })));
      console.log(`✓ ${name}: ${items.length} relevant`);
    } catch (e) {
      console.warn(`✗ ${name}: ${e.message}`);
    }
  }
  out.sort((a, b) => Date.parse(b.date || 0) - Date.parse(a.date || 0));
  fs.mkdirSync(DIRS.research, { recursive: true });
  const file = path.join(DIRS.research, 'news-candidates.json');
  fs.writeFileSync(file, JSON.stringify({ scannedAt: new Date().toISOString(), items: out }, null, 2) + '\n');
  console.log(`${out.length} candidates -> ${path.relative(p(), file)}`);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  if (process.argv.includes('--scan')) await scan();
  else rank();
}
