#!/usr/bin/env node
// Lints every post JSON: slide count, ≤25 words, sources for every stat/date, no guarantee language.
import fs from 'node:fs';
import path from 'node:path';
import { DIRS } from './lib/paths.mjs';
import { loadBrand } from './lib/brand.mjs';
import { validatePost } from './lib/validate.mjs';

const brand = loadBrand();
let bad = 0;
for (const f of fs.readdirSync(DIRS.posts).filter((x) => x.endsWith('.json')).sort()) {
  let post;
  try { post = JSON.parse(fs.readFileSync(path.join(DIRS.posts, f), 'utf8')); }
  catch (e) { console.error(`✗ ${f}: invalid JSON (${e.message})`); bad++; continue; }
  if (post.disabled) { console.log(`- ${f} (disabled)`); continue; }
  const tiktok = { ...post, slides: post.slides.map((s, i) => ({ ...s, ...(post.tiktok?.slides?.[i] || {}) })) };
  const a = validatePost(post, { brand }), b = validatePost(tiktok, { brand });
  const errors = [...new Set([...a.errors, ...b.errors.map((e) => 'tiktok ' + e)])];
  const warnings = [...new Set([...a.warnings, ...b.warnings.map((w) => 'tiktok ' + w)])].filter((w) => !w.startsWith('tiktok no "plasmo"'));
  console.log(`${errors.length ? '✗' : '✓'} ${f}`);
  warnings.forEach((w) => console.log(`   ! ${w}`));
  errors.forEach((e) => console.log(`   ✗ ${e}`));
  if (post.expires && new Date(post.expires) < new Date()) console.log(`   ! expired on ${post.expires} (news post)`);
  if (errors.length) bad++;
}
process.exit(bad ? 1 : 0);
