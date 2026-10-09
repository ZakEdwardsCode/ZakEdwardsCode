import React, { useMemo } from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import * as Icons from "lucide-react";
import type { Word } from "./types";
import { C, fontFamily } from "./theme";
import { lerp } from "./layout";
import { iconForWord } from "./keywords";

type Page = { words: Word[]; s: number; e: number };

const buildPages = (words: Word[]): Page[] => {
  const pages: Page[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) pages.push({ words: cur, s: cur[0].s, e: cur[cur.length - 1].e });
    cur = [];
  };
  for (const w of words) {
    const last = cur[cur.length - 1];
    const chars = cur.reduce((n, x) => n + x.w.length + 1, 0);
    if (last && (w.s - last.e > 0.45 || cur.length >= 4 || chars + w.w.length > 22)) flush();
    cur.push(w);
    if (/[.!?,]$/.test(w.w)) flush();
  }
  flush();
  // Each page stays up until the next one starts (capped), so captions don't flicker.
  for (let i = 0; i < pages.length; i++) {
    const next = pages[i + 1];
    pages[i].e = next ? Math.min(next.s, pages[i].e + 0.6) : pages[i].e + 0.6;
  }
  return pages;
};

const clean = (w: string) => w.replace(/^[^\w£$%]+|[^\w%]+$/g, "");

export const Captions: React.FC<{ words: Word[]; pip: (t: number) => number }> = ({ words, pip }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pages = useMemo(() => buildPages(words), [words]);
  const page = pages.find((p) => t >= p.s && t < p.e);
  if (!page) return null;

  const p = pip(t);
  const size = lerp(76, 58, p);
  const centerX = lerp(960, 760, p);
  const bottom = lerp(110, 62, p);
  const pageIn = spring({ frame: Math.round((t - page.s) * fps), fps, config: { damping: 14, stiffness: 180 } });

  const active = page.words.find((w) => t >= w.s && t < w.e + 0.08) ?? null;
  const activeIcon = active ? iconForWord(clean(active.w)) : null;
  const Icon = activeIcon ? (Icons as unknown as Record<string, React.FC<any>>)[activeIcon] : null;
  const iconPop = active
    ? spring({ frame: Math.round((t - active.s) * fps), fps, config: { damping: 9, stiffness: 220 } })
    : 0;

  return (
    <div
      style={{
        position: "absolute",
        left: centerX - 800,
        width: 1600,
        bottom,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        transform: `translateY(${interpolate(pageIn, [0, 1], [24, 0])}px) scale(${interpolate(pageIn, [0, 1], [0.9, 1])})`,
        opacity: pageIn,
      }}
    >
      {Icon ? (
        <div
          style={{
            marginBottom: 14,
            width: 92,
            height: 92,
            borderRadius: 24,
            background: C.navy,
            border: `3px solid ${C.sky}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 12px 30px rgba(0,0,0,0.45)",
            transform: `scale(${iconPop}) rotate(${interpolate(iconPop, [0, 1], [-18, 0])}deg)`,
          }}
        >
          <Icon size={54} color={C.sky} strokeWidth={2.4} />
        </div>
      ) : null}
      <div
        style={{
          fontFamily,
          fontWeight: 900,
          fontSize: size,
          lineHeight: 1.1,
          textTransform: "uppercase",
          letterSpacing: -0.5,
          textAlign: "center",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "0 0.4em",
        }}
      >
        {page.words.map((w, i) => {
          const isActive = w === active;
          const spoken = t >= w.s;
          const k = isActive
            ? spring({ frame: Math.round((t - w.s) * fps), fps, config: { damping: 10, stiffness: 260 } })
            : 0;
          const hasIcon = iconForWord(clean(w.w)) !== null;
          return (
            <span
              key={i}
              style={{
                color: isActive ? (hasIcon ? C.coral : C.sky) : C.white,
                opacity: spoken ? 1 : 0.55,
                WebkitTextStroke: `${Math.round(size * 0.14)}px ${C.ink}`,
                paintOrder: "stroke fill",
                textShadow: "0 6px 18px rgba(0,0,0,0.55)",
                display: "inline-block",
                transform: `scale(${1 + 0.12 * k}) translateY(${-6 * k}px)`,
              }}
            >
              {clean(w.w)}
            </span>
          );
        })}
      </div>
    </div>
  );
};
