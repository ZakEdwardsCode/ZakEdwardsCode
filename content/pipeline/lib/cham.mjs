// Placeholder 2D Cham (a chameleon) drawn as SVG so it can be recoloured per mood.
// If brand/cham.svg or brand/cham.png exists, render.mjs uses that instead.

const faces = {
  happy: { pupil: [0, 0], lid: 0, mouth: 'M318 212 Q332 226 350 214' },
  focused: { pupil: [6, 0], lid: 0.32, mouth: 'M318 216 L350 214' },
  worried: { pupil: [-2, -4], lid: 0, mouth: 'M318 222 Q334 208 350 220', sweat: true, brow: 'M286 128 L318 118' },
  sleepy: { pupil: [0, 4], lid: 0.58, mouth: 'M320 216 Q334 222 348 216', zzz: true },
  tired: { pupil: [0, 6], lid: 0.48, mouth: 'M318 220 Q334 214 350 220', bags: true },
  smug: { pupil: [8, -2], lid: 0.42, mouth: 'M316 210 Q338 228 352 204' },
};

export function chamSvg({ body = '#6B3BFF', belly = '#C8FF3D', face = 'happy', ink = '#120E24' } = {}) {
  const f = faces[face] || faces.happy;
  const eye = { cx: 300, cy: 156, r: 34 };
  const lidH = eye.r * 2 * f.lid;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 380">
  <defs>
    <linearGradient id="cb" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${body}"/><stop offset="1" stop-color="${body}" stop-opacity="0.82"/>
    </linearGradient>
    <clipPath id="eyeclip"><circle cx="${eye.cx}" cy="${eye.cy}" r="${eye.r - 6}"/></clipPath>
  </defs>
  <!-- tail -->
  <path d="M140 250 C 70 262, 40 320, 86 344 C 120 360, 150 322, 122 304 C 104 292, 92 318, 108 324"
        fill="none" stroke="${body}" stroke-width="30" stroke-linecap="round"/>
  <!-- back legs -->
  <path d="M170 262 l -10 62" stroke="${body}" stroke-width="26" stroke-linecap="round"/>
  <path d="M262 264 l 12 60" stroke="${body}" stroke-width="26" stroke-linecap="round"/>
  <!-- body -->
  <path d="M120 236 C 118 168, 196 132, 268 140 C 340 148, 372 196, 360 236 C 348 276, 160 296, 120 236 Z" fill="url(#cb)"/>
  <!-- belly stripe -->
  <path d="M138 250 C 190 278, 300 280, 352 240 C 330 268, 200 292, 138 250 Z" fill="${belly}"/>
  <!-- back crest dots -->
  <circle cx="190" cy="168" r="9" fill="${belly}" opacity="0.9"/>
  <circle cx="226" cy="156" r="8" fill="${belly}" opacity="0.9"/>
  <circle cx="160" cy="190" r="7" fill="${belly}" opacity="0.9"/>
  <!-- head casque -->
  <path d="M248 150 C 252 96, 330 92, 360 140 C 380 170, 384 214, 360 230 L 300 236 Z" fill="${body}"/>
  <!-- eye turret -->
  <circle cx="${eye.cx}" cy="${eye.cy}" r="${eye.r}" fill="${body}" stroke="${ink}" stroke-opacity="0.12" stroke-width="3"/>
  <circle cx="${eye.cx}" cy="${eye.cy}" r="${eye.r - 6}" fill="#fff"/>
  <circle cx="${eye.cx + 6 + f.pupil[0]}" cy="${eye.cy + f.pupil[1]}" r="13" fill="${ink}"/>
  <circle cx="${eye.cx + 10 + f.pupil[0]}" cy="${eye.cy - 5 + f.pupil[1]}" r="4" fill="#fff"/>
  ${lidH > 0 ? `<rect clip-path="url(#eyeclip)" x="${eye.cx - eye.r}" y="${eye.cy - eye.r}" width="${eye.r * 2}" height="${lidH}" fill="${body}"/>
  <line x1="${eye.cx - eye.r + 8}" y1="${eye.cy - eye.r + lidH}" x2="${eye.cx + eye.r - 8}" y2="${eye.cy - eye.r + lidH}" stroke="${ink}" stroke-width="4" stroke-linecap="round" opacity="0.7"/>` : ''}
  ${f.bags ? `<path d="M278 186 Q300 198 322 186" fill="none" stroke="${ink}" stroke-width="3" opacity="0.35"/>` : ''}
  ${f.brow ? `<path d="${f.brow}" stroke="${ink}" stroke-width="6" stroke-linecap="round"/>` : ''}
  <!-- mouth -->
  <path d="${f.mouth}" fill="none" stroke="${ink}" stroke-width="5" stroke-linecap="round"/>
  <!-- front leg -->
  <path d="M318 236 l 8 70" stroke="${body}" stroke-width="24" stroke-linecap="round"/>
  ${f.sweat ? `<path d="M372 120 q 10 18 0 26 q -10 -8 0 -26z" fill="#7FD4FF"/>` : ''}
  ${f.zzz ? `<text x="352" y="96" font-family="Plasmo Heading, sans-serif" font-weight="800" font-size="34" fill="${ink}" opacity="0.6">z</text><text x="378" y="70" font-family="Plasmo Heading, sans-serif" font-weight="800" font-size="26" fill="${ink}" opacity="0.45">z</text>` : ''}
</svg>`;
}
