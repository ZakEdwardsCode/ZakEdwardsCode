import fs from 'node:fs';
import { p } from './paths.mjs';

export function loadBrand() {
  const brand = JSON.parse(fs.readFileSync(p('brand/brand.json'), 'utf8'));
  brand.logoSvg = fs.readFileSync(p('brand', brand.logo), 'utf8').replace(/<!--[\s\S]*?-->/g, '');
  return brand;
}

// @font-face rules. URLs are relative to the local server root (/content).
export function fontFaceCss(brand) {
  return Object.values(brand.fonts)
    .filter((f) => f && typeof f === 'object')
    .map((f) => `@font-face{font-family:'${f.family}';src:url('/brand/${f.file}');font-weight:${f.weight};font-display:block}`)
    .join('\n');
}

export function moodOf(brand, key) {
  return brand.chamMoods[key] || brand.chamMoods.default;
}
