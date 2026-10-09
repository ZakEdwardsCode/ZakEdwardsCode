import React, { useMemo } from "react";
import { AbsoluteFill, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { fontFamily } from "./theme";
import type { Platform, ShortEdit } from "./ShortVideo";

// The "creator cut": built to feel like a student talking to camera on the FYP, not an ad.
// Full-screen face for the story, split screen only while showing Plasmo, native-looking text,
// no branded cards, watermark, end slate, sound effects or music (add a trending sound in-app).
const W = 1080;
const H = 1920;
const TOP_H = 840; // split screen: screen recording on top, face (native res) below
const FULL_SCALE = 1.15; // talking-head shots: only a light zoom so Zak isn't huge in frame
const FULL_TOP = 300; // the zoomed-out frame sits here, plain dark background around it
const FULL_H = Math.round(1080 * FULL_SCALE);

type Clip = ShortEdit["clips"][number];

const HOOK: Record<string, string[]> = {
  ShortWeeksToMark: ["my teachers took WEEKS", "to mark my past papers"],
  ShortMarkedIn10s: ["i built an AI that marks", "past papers in 10 seconds"],
  ShortPaperIsOutdated: ["why i stopped doing", "past papers on paper"],
};

const OUTRO: Record<Platform, string> = {
  tiktok: "it's free btw → plasmo.uk",
  reels: "link in bio · plasmo.uk",
  shorts: "plasmo.uk · full video on my channel",
};

const isSplit = (c: Clip) => c.top.kind === "screen";

const FaceVideo: React.FC<{ clip: Clip; full: boolean; index: number }> = ({ clip, full, index }) => {
  const { fps } = useVideoConfig();
  const frames = Math.round((clip.out - clip.in) * fps);
  const volume = (f: number) => Math.max(0, Math.min(1, f / 2, (frames - f) / 2));
  if (full && clip.vert && FULL_SCALE > 1.5) { // only for full-bleed framing
    // Pre-cut 1080x1920 clip (scripts/make_vertical.py): played 1:1, no browser scaling.
    return (
      <div style={{ position: "absolute", left: 0, top: 0, width: W, height: H, overflow: "hidden", background: "#000" }}>
        <OffthreadVideo src={staticFile(clip.vert)} volume={volume} toneMapped={false} style={{ width: W, height: H }} />
      </div>
    );
  }
  const s = full ? FULL_SCALE : 1;
  const boxH = full ? FULL_H : H - TOP_H;
  const left = Math.max(W - 1920 * s, Math.min(0, W / 2 - clip.faceCx * s));
  const punch = 1;
  return (
    <div style={{ position: "absolute", left: 0, top: full ? FULL_TOP : TOP_H, width: W, height: boxH, overflow: "hidden", background: "#000" }}>
      <div style={{ position: "absolute", left, top: 0, width: 1920 * s, height: 1080 * s, transform: `scale(${punch})`, transformOrigin: `${clip.faceCx * s}px ${380 * s}px` }}>
        <OffthreadVideo
          src={staticFile("media/head.mp4")}
          startFrom={Math.round(clip.in * fps)}
          volume={volume}
          toneMapped={false}
          style={{ width: 1920 * s, height: 1080 * s }}
        />
      </div>
    </div>
  );
};

const ScreenPanel: React.FC<{ clip: Clip; screenOffset: number }> = ({ clip, screenOffset }) => {
  const { fps } = useVideoConfig();
  if (clip.top.kind !== "screen") return null;
  const cr = clip.top.crop;
  const s = W / cr.w;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: W, height: TOP_H, overflow: "hidden", background: "#000" }}>
      <OffthreadVideo
        src={staticFile("media/screen.mp4")}
        startFrom={Math.round((clip.in - screenOffset) * fps)}
        muted
        toneMapped={false}
        style={{ position: "absolute", left: -cr.x * s, top: -cr.y * s, width: 1920 * s, height: 876 * s }}
      />
    </div>
  );
};

/** Plain on-screen text in each app's own style. */
const Sticker: React.FC<{ lines: string[]; platform: Platform; top: number }> = ({ lines, platform, top }) => (
  <div style={{ position: "absolute", left: 60, right: 160, top, display: "flex", flexDirection: "column", alignItems: "center", gap: 8, zIndex: 30 }}>
    {lines.map((l, i) =>
      platform === "tiktok" ? (
        <span key={i} style={{ fontFamily, fontWeight: 700, fontSize: 52, lineHeight: 1.15, color: "#000", background: "#fff", borderRadius: 14, padding: "6px 18px", whiteSpace: "nowrap" }}>
          {l}
        </span>
      ) : (
        <span
          key={i}
          style={{
            fontFamily,
            fontWeight: platform === "reels" ? 700 : 800,
            fontSize: 54,
            lineHeight: 1.15,
            color: "#fff",
            whiteSpace: "nowrap",
            textShadow: platform === "reels" ? "0 2px 10px rgba(0,0,0,0.75)" : "none",
            WebkitTextStroke: platform === "shorts" ? "8px #000" : undefined,
            paintOrder: "stroke fill",
          }}
        >
          {l}
        </span>
      ),
    )}
  </div>
);

type Word = ShortEdit["words"][number];
const pagesOf = (words: Word[]) => {
  const pages: { words: Word[]; s: number; e: number }[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) pages.push({ words: cur, s: cur[0].s, e: cur[cur.length - 1].e });
    cur = [];
  };
  for (const w of words) {
    const chars = cur.reduce((n, x) => n + x.w.length + 1, 0);
    if (cur.length && (cur.length >= 4 || chars + w.w.length > 20 || w.s - cur[cur.length - 1].e > 0.4)) flush();
    cur.push(w);
    if (/[.!?,]$/.test(w.w)) flush();
  }
  flush();
  for (let i = 0; i < pages.length; i++) pages[i].e = pages[i + 1] ? Math.min(pages[i + 1].s, pages[i].e + 0.4) : pages[i].e + 0.3;
  return pages;
};

const Captions: React.FC<{ words: Word[]; top: number }> = ({ words, top }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pages = useMemo(() => pagesOf(words), [words]);
  const page = pages.find((p) => t >= p.s && t < p.e);
  if (!page) return null;
  return (
    <div style={{ position: "absolute", left: 60, right: 160, top, textAlign: "center", zIndex: 20 }}>
      <span
        style={{
          fontFamily,
          fontWeight: 800,
          fontSize: 66,
          lineHeight: 1.12,
          color: "#fff",
          WebkitTextStroke: "9px #000",
          paintOrder: "stroke fill",
        }}
      >
        {page.words.map((w) => w.w).join(" ").replace(/[,.]+$/, "")}
      </span>
    </div>
  );
};

export const CreatorShort: React.FC<{ edit: ShortEdit; platform: Platform }> = ({ edit, platform }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const cur = edit.clips.find((c) => t >= c.at && t < c.at + (c.out - c.in)) ?? edit.clips[edit.clips.length - 1];
  const split = isSplit(cur);
  // Text never sits on the face: below the chin in full-screen, on the screen panel in split.
  const textTop = split ? 180 : FULL_TOP + 820;
  const captionTop = split ? TOP_H - 130 : FULL_TOP + 1100;
  const outroFrom = Math.max(0, edit.talk - 2.6);
  return (
    <AbsoluteFill style={{ background: "#161a1d" }}>
      {edit.clips.map((c, i) => (
        <Sequence key={i} from={Math.round(c.at * fps)} durationInFrames={Math.max(1, Math.round((c.out - c.in) * fps))} premountFor={15}>
          {isSplit(c) ? <ScreenPanel clip={c} screenOffset={edit.screenOffset} /> : null}
          <FaceVideo clip={c} full={!isSplit(c)} index={i} />
        </Sequence>
      ))}
      {t < 2.6 ? null : <Captions words={edit.words} top={captionTop} />}
      {t < 2.6 ? <Sticker lines={HOOK[edit.id] ?? edit.hook} platform={platform} top={textTop} /> : null}
      {t >= outroFrom ? <Sticker lines={[OUTRO[platform]]} platform={platform} top={textTop} /> : null}
    </AbsoluteFill>
  );
};
