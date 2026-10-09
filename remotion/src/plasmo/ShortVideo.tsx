import React, { useMemo } from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import * as Icons from "lucide-react";
import { C, fontFamily } from "./theme";

// Vertical 1080x1920 Short: top panel (graphic or synced screen crop), bottom panel (face, native res).
// Shorts UI covers roughly the bottom 380px and the right 160px, so text stays above and left of that.
export const SW = 1080;
export const SH = 1920;
const TOP_H = 840;
const FACE_H = SH - TOP_H; // 1080: the camera's full height, so the face is never upscaled

type Crop = { x: number; y: number; w: number; h: number };
type Top =
  | { kind: "screen"; crop: Crop }
  | { kind: "gfx"; icon: string; title: string; paper?: boolean; cross?: boolean; accent?: boolean };
type ShortClip = { in: number; out: number; at: number; top: Top; faceCx: number };
type Word = { w: string; s: number; e: number };
export type ShortEdit = {
  id: string;
  fps: number;
  duration: number;
  talk: number;
  screenOffset: number;
  hook: string[];
  cta: string;
  clips: ShortClip[];
  words: Word[];
  sfx: { t: number; name: string; vol?: number }[];
};

export type Platform = "tiktok" | "reels" | "shorts";

/** What each platform rewards, and where its own UI sits on top of the video. */
export const PLATFORM: Record<Platform, { ctaSeconds: number; hookTop: number; markTop: number }> = {
  // TikTok: For You tabs across the top ~160px; instant hook; comments drive reach.
  tiktok: { ctaSeconds: 2.4, hookTop: 170, markTop: 170 },
  // Reels: profile header at the top; the grid shows only the centre 4:5 (y 285-1635); saves/shares drive reach.
  reels: { ctaSeconds: 3, hookTop: 288, markTop: 300 },
  // Shorts: light top bar; end screen points to the long-form video.
  shorts: { ctaSeconds: 3, hookTop: 90, markTop: 40 },
};

const T = { red: "#FF2E3D", redDeep: "#7A0B1E", yellow: "#FFE14D", green: "#22E07A", blue: "#14C8FF" };

const Icon: React.FC<{ name: string; size: number; color: string; stroke?: number }> = ({ name, size, color, stroke = 2.4 }) => {
  const I = (Icons as unknown as Record<string, React.FC<any>>)[name] ?? Icons.Sparkles;
  return <I size={size} color={color} strokeWidth={stroke} />;
};

const Paper: React.FC<{ r: number; x: number; y: number }> = ({ r, x, y }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: 250,
      height: 330,
      background: "#FBFAF5",
      borderRadius: 6,
      transform: `rotate(${r}deg)`,
      boxShadow: "0 16px 36px rgba(0,0,0,0.45)",
      padding: 22,
      boxSizing: "border-box",
      display: "flex",
      flexDirection: "column",
      gap: 9,
      fontFamily: "Georgia, serif",
      color: "#222",
    }}
  >
    <div style={{ fontWeight: 700, fontSize: 24 }}>GCSE (9–1)</div>
    <div style={{ fontWeight: 700, fontSize: 26 }}>Mathematics</div>
    <div style={{ fontSize: 15 }}>Paper 1 · Higher Tier</div>
    {Array.from({ length: 6 }).map((_, i) => (
      <div key={i} style={{ height: 2, background: "#C9C6BC", width: i % 3 === 2 ? "65%" : "100%", marginTop: 6 }} />
    ))}
  </div>
);

const GfxPanel: React.FC<{ top: Extract<Top, { kind: "gfx" }>; local: number }> = ({ top, local }) => {
  const { fps } = useVideoConfig();
  const f = Math.round(local * fps);
  const pop = spring({ frame: f, fps, config: { damping: 10, stiffness: 200 } });
  const title = spring({ frame: f - 4, fps, config: { damping: 14, stiffness: 180 } });
  const cross = spring({ frame: f - 8, fps, config: { damping: 9, stiffness: 220 } });
  const bg = top.accent
    ? `radial-gradient(circle at 50% 40%, ${T.blue} 0%, ${C.navyMid} 75%)`
    : `radial-gradient(circle at 50% 40%, ${T.red} 0%, ${T.redDeep} 78%)`;
  const showPaper = !!top.paper;
  return (
    <AbsoluteFill style={{ background: bg, overflow: "hidden" }}>
      {showPaper ? (
        <div style={{ position: "absolute", left: 0, top: 0, width: SW, height: TOP_H, transform: `scale(${0.9 + 0.1 * pop})` }}>
          <Paper r={-12} x={300} y={110} />
          <Paper r={-2} x={410} y={95} />
          <Paper r={9} x={520} y={115} />
        </div>
      ) : (
        <div
          style={{
            position: "absolute",
            left: SW / 2 - 150,
            top: 130,
            width: 280,
            height: 280,
            borderRadius: 80,
            background: C.white,
            border: `10px solid ${C.ink}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 24px 60px rgba(0,0,0,0.45)",
            transform: `scale(${pop}) rotate(${interpolate(pop, [0, 1], [-20, 0])}deg)`,
          }}
        >
          <Icon name={top.icon} size={160} color={top.accent ? C.navy : T.red} stroke={2.6} />
        </div>
      )}
      {top.cross ? (
        <div style={{ position: "absolute", left: SW / 2 - 300, top: 0, width: 600, height: 520, transform: `scale(${cross})` }}>
          {[45, -45].map((r) => (
            <div
              key={r}
              style={{
                position: "absolute",
                left: 0,
                top: 220,
                width: 600,
                height: 80,
                borderRadius: 40,
                background: T.red,
                border: `9px solid ${C.white}`,
                transform: `rotate(${r}deg)`,
                boxShadow: "0 14px 34px rgba(0,0,0,0.5)",
              }}
            />
          ))}
        </div>
      ) : null}
      <div
        style={{
          position: "absolute",
          left: 60,
          right: 60,
          top: 450,
          textAlign: "center",
          fontFamily,
          fontWeight: 900,
          fontSize: 80,
          lineHeight: 0.95,
          textTransform: "uppercase",
          letterSpacing: -2,
          color: top.accent ? T.yellow : C.white,
          WebkitTextStroke: `14px ${C.ink}`,
          paintOrder: "stroke fill",
          opacity: title,
          transform: `translateY(${interpolate(title, [0, 1], [40, 0])}px)`,
        }}
      >
        {top.title}
      </div>
    </AbsoluteFill>
  );
};

const ClipView: React.FC<{ clip: ShortClip; edit: ShortEdit; topStart: number; index: number }> = ({ clip, edit, topStart, index }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const len = clip.out - clip.in;
  const totalFrames = Math.round(len * fps);
  const local = clip.at + frame / fps - topStart;
  const volume = (f: number) => Math.max(0, Math.min(1, f / 2, (totalFrames - f) / 2));
  const faceLeft = Math.max(0, Math.min(1920 - SW, clip.faceCx - SW / 2));
  const punch = index % 2 === 1 ? 1.06 : 1; // alternate punch-ins hide the jump cuts
  return (
    <AbsoluteFill>
      {/* top panel */}
      <div style={{ position: "absolute", left: 0, top: 0, width: SW, height: TOP_H, overflow: "hidden" }}>
        {clip.top.kind === "screen" ? (
          (() => {
            const cr = clip.top.crop;
            const s = SW / cr.w;
            const zoom = 1 + 0.035 * Math.min(1, local / 6);
            return (
              <div style={{ position: "absolute", inset: 0, background: "#000", transform: `scale(${zoom})`, transformOrigin: "50% 60%" }}>
                <OffthreadVideo
                  src={staticFile("media/screen.mp4")}
                  startFrom={Math.round((clip.in - edit.screenOffset) * fps)}
                  muted
                  toneMapped={false}
                  style={{ position: "absolute", left: -cr.x * s, top: -cr.y * s, width: 1920 * s, height: 876 * s }}
                />
              </div>
            );
          })()
        ) : (
          <GfxPanel top={clip.top} local={local} />
        )}
      </div>
      {/* face panel */}
      <div style={{ position: "absolute", left: 0, top: TOP_H, width: SW, height: FACE_H, overflow: "hidden", background: "#000" }}>
        <div
          style={{
            position: "absolute",
            left: -faceLeft,
            top: 0,
            width: 1920,
            height: 1080,
            transform: `scale(${punch})`,
            transformOrigin: `${clip.faceCx}px 380px`,
          }}
        >
          <OffthreadVideo
            src={staticFile("media/head.mp4")}
            startFrom={Math.round(clip.in * fps)}
            volume={volume}
            toneMapped={false}
            style={{ width: 1920, height: 1080 }}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};

type Page = { words: Word[]; s: number; e: number };
const pagesOf = (words: Word[]): Page[] => {
  const pages: Page[] = [];
  let cur: Word[] = [];
  const flush = () => {
    if (cur.length) pages.push({ words: cur, s: cur[0].s, e: cur[cur.length - 1].e });
    cur = [];
  };
  for (const w of words) {
    const chars = cur.reduce((n, x) => n + x.w.length + 1, 0);
    if (cur.length && (cur.length >= 3 || chars + w.w.length > 14 || w.s - cur[cur.length - 1].e > 0.4)) flush();
    cur.push(w);
    if (/[.!?,]$/.test(w.w)) flush();
  }
  flush();
  for (let i = 0; i < pages.length; i++) pages[i].e = pages[i + 1] ? Math.min(pages[i + 1].s, pages[i].e + 0.5) : pages[i].e + 0.4;
  return pages;
};

const Captions: React.FC<{ words: Word[] }> = ({ words }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pages = useMemo(() => pagesOf(words), [words]);
  const page = pages.find((p) => t >= p.s && t < p.e);
  if (!page) return null;
  const k = spring({ frame: Math.round((t - page.s) * fps), fps, config: { damping: 12, stiffness: 220 } });
  return (
    <div
      style={{
        position: "absolute",
        left: 40,
        right: 40,
        top: TOP_H - 150,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "0 0.32em",
        fontFamily,
        fontWeight: 900,
        fontSize: 104,
        lineHeight: 1,
        textTransform: "uppercase",
        letterSpacing: -1,
        transform: `scale(${interpolate(k, [0, 1], [0.85, 1])})`,
        opacity: k,
        zIndex: 20,
      }}
    >
      {page.words.map((w, i) => {
        const active = t >= w.s && t < w.e + 0.06;
        const a = active ? spring({ frame: Math.round((t - w.s) * fps), fps, config: { damping: 10, stiffness: 260 } }) : 0;
        return (
          <span
            key={i}
            style={{
              display: "inline-block",
              color: active ? T.yellow : C.white,
              WebkitTextStroke: `16px ${C.ink}`,
              paintOrder: "stroke fill",
              textShadow: "0 8px 24px rgba(0,0,0,0.6)",
              padding: `0 ${0.1 * a}em`,
              transform: `scale(${1 + 0.1 * a}) rotate(${active ? -2 : 0}deg)`,
            }}
          >
            {w.w.replace(/[^\w'%£$.-]+$/g, "").replace(/\.$/, "")}
          </span>
        );
      })}
    </div>
  );
};

const TikTokHook: React.FC<{ lines: string[]; top: number }> = ({ lines, top }) => {
  // TikTok's own text-tool look: white rounded stickers, black text, on screen from frame 0.
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const out = interpolate(frame, [2.4 * fps, 2.8 * fps], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 40, right: 180, top, zIndex: 30, display: "flex", flexDirection: "column", alignItems: "center", gap: 10, opacity: out }}>
      {lines.map((l, i) => (
        <div
          key={i}
          style={{
            fontFamily,
            fontWeight: 800,
            fontSize: 66,
            lineHeight: 1.1,
            color: "#000",
            background: "#fff",
            borderRadius: 18,
            padding: "8px 22px",
            whiteSpace: "nowrap",
            boxShadow: "0 6px 18px rgba(0,0,0,0.25)",
          }}
        >
          {l.charAt(0) + l.slice(1).toLowerCase()}
        </div>
      ))}
    </div>
  );
};

const ReelsHook: React.FC<{ lines: string[]; top: number }> = ({ lines, top }) => {
  // Reels: polished and calm, inside the 4:5 grid crop.
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = spring({ frame, fps, config: { damping: 20, stiffness: 120 } });
  const out = interpolate(frame, [2.6 * fps, 3 * fps], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 60, right: 60, top, zIndex: 30, textAlign: "center", opacity: a * out, transform: `translateY(${interpolate(a, [0, 1], [30, 0])}px)` }}>
      <div style={{ display: "inline-block", background: "rgba(11,16,51,0.82)", borderRadius: 28, padding: "14px 30px", border: `3px solid ${T.yellow}` }}>
        <div style={{ fontFamily, fontWeight: 800, fontSize: 46, color: C.white, textTransform: "uppercase", letterSpacing: -1, lineHeight: 1.05 }}>{lines[0]}</div>
        <div style={{ fontFamily, fontWeight: 900, fontSize: 54, color: T.yellow, textTransform: "uppercase", letterSpacing: -1, lineHeight: 1.05 }}>{lines[1]}</div>
      </div>
    </div>
  );
};

const Hook: React.FC<{ lines: string[]; top?: number }> = ({ lines, top = 70 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = spring({ frame, fps, config: { damping: 11, stiffness: 200 } });
  const b = spring({ frame: frame - 5, fps, config: { damping: 11, stiffness: 200 } });
  const out = interpolate(frame, [2.6 * fps, 3 * fps], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <div style={{ position: "absolute", left: 40, right: 40, top, zIndex: 30, textAlign: "center", opacity: out, fontFamily, fontWeight: 900, textTransform: "uppercase", letterSpacing: -2, lineHeight: 0.95 }}>
      <div style={{ fontSize: 70, whiteSpace: "nowrap", color: C.white, WebkitTextStroke: `14px ${C.ink}`, paintOrder: "stroke fill", transform: `scale(${interpolate(a, [0, 1], [1.6, 1])})`, opacity: a }}>
        {lines[0]}
      </div>
      <div
        style={{
          display: "inline-block",
          marginTop: 14,
          fontSize: 70,
          whiteSpace: "nowrap",
          color: C.ink,
          background: T.yellow,
          border: `7px solid ${C.ink}`,
          padding: "6px 22px 0",
          transform: `rotate(-2deg) scale(${interpolate(b, [0, 1], [1.6, 1])})`,
          opacity: b,
        }}
      >
        {lines[1]}
      </div>
    </div>
  );
};

const CTA_ACTION: Record<Platform, { icon: string; label: string }> = {
  tiktok: { icon: "MessageCircle", label: "Comment your subject" },
  reels: { icon: "Bookmark", label: "Save this for your mocks" },
  shorts: { icon: "SquarePlay", label: "Full video on my channel" },
};

const Cta: React.FC<{ text: string; platform: Platform }> = ({ text, platform }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = spring({ frame, fps, config: { damping: 14, stiffness: 150 } });
  const url = spring({ frame: frame - 6, fps, config: { damping: 9, stiffness: 200 } });
  const btn = spring({ frame: frame - 14, fps, config: { damping: 10, stiffness: 200 } });
  const pulse = 1 + 0.03 * Math.sin(frame / 4);
  return (
    <AbsoluteFill
      style={{
        zIndex: 40,
        background: `radial-gradient(circle at 50% 38%, ${T.blue} 0%, ${C.navy} 70%)`,
        transform: `translateY(${interpolate(k, [0, 1], [SH, 0])}px)`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 46,
        paddingBottom: 300,
        fontFamily,
        textAlign: "center",
      }}
    >
      <div style={{ width: 220, height: 220, borderRadius: 60, background: T.green, border: `10px solid ${C.white}`, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: "0 24px 60px rgba(0,0,0,0.45)" }}>
        <Icons.Check size={140} color={C.ink} strokeWidth={4} />
      </div>
      <div style={{ fontWeight: 900, fontSize: 70, color: C.white, textTransform: "uppercase", lineHeight: 1, maxWidth: 900, WebkitTextStroke: `12px ${C.ink}`, paintOrder: "stroke fill" }}>{text}</div>
      <div
        style={{
          fontWeight: 900,
          fontSize: 150,
          letterSpacing: -4,
          color: T.yellow,
          WebkitTextStroke: `18px ${C.ink}`,
          paintOrder: "stroke fill",
          transform: `scale(${url * pulse})`,
        }}
      >
        plasmo.uk
      </div>
      <div
        style={{
          fontWeight: 900,
          fontSize: 50,
          color: C.ink,
          background: C.white,
          borderRadius: 999,
          padding: "20px 44px",
          border: `7px solid ${C.ink}`,
          textTransform: "uppercase",
          transform: `scale(${btn})`,
          boxShadow: "0 18px 40px rgba(0,0,0,0.4)",
        }}
      >
        <span style={{ display: "inline-flex", alignItems: "center", gap: 18 }}>
          <Icon name={CTA_ACTION[platform].icon} size={56} color={C.ink} stroke={2.8} />
          {CTA_ACTION[platform].label}
        </span>
      </div>
      <div style={{ fontWeight: 800, fontSize: 40, color: C.white, opacity: btn, textTransform: "uppercase", letterSpacing: 2 }}>
        {platform === "reels" ? "Link in bio · free for GCSE & A-level" : "Free for GCSE & A-level"}
      </div>
    </AbsoluteFill>
  );
};

const Watermark: React.FC<{ top: number }> = ({ top }) => (
  <div
    style={{
      position: "absolute",
      left: 36,
      top,
      zIndex: 25,
      fontFamily,
      fontWeight: 900,
      fontSize: 40,
      color: C.ink,
      background: T.yellow,
      border: `5px solid ${C.ink}`,
      borderRadius: 14,
      padding: "6px 18px 2px",
    }}
  >
    plasmo.uk
  </div>
);

export const ShortVideo: React.FC<{ edit: ShortEdit; platform: Platform }> = ({ edit, platform }) => {
  const P = PLATFORM[platform];
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();
  const t = frame / fps;
  // Where each clip's top-panel graphic started, so a card split across cuts animates once.
  const topStarts = useMemo(() => {
    const out: number[] = [];
    edit.clips.forEach((c, i) => {
      const prev = edit.clips[i - 1];
      out.push(prev && JSON.stringify(prev.top) === JSON.stringify(c.top) ? out[i - 1] : c.at);
    });
    return out;
  }, [edit]);
  return (
    <AbsoluteFill style={{ background: C.navy }}>
      {edit.clips.map((c, i) => (
        <Sequence key={i} from={Math.round(c.at * fps)} durationInFrames={Math.max(1, Math.round((c.out - c.in) * fps))} premountFor={15}>
          <ClipView clip={c} edit={edit} topStart={topStarts[i]} index={i} />
        </Sequence>
      ))}
      {/* glowing seam between panels */}
      <div style={{ position: "absolute", left: 0, top: TOP_H - 4, width: SW, height: 8, background: T.yellow, boxShadow: `0 0 24px ${T.yellow}`, zIndex: 10 }} />
      <Captions words={edit.words} />
      {t > 3 ? <Watermark top={P.markTop} /> : null}
      <Sequence durationInFrames={Math.round(3 * fps)}>
        {platform === "tiktok" ? (
          <TikTokHook lines={edit.hook} top={P.hookTop} />
        ) : platform === "reels" ? (
          <ReelsHook lines={edit.hook} top={P.hookTop} />
        ) : (
          <Hook lines={edit.hook} top={P.hookTop} />
        )}
      </Sequence>
      <Sequence from={Math.round(edit.talk * fps)}>
        <Cta text={edit.cta} platform={platform} />
      </Sequence>
      {/* start where the drums come in (bar 9 of the track) so a short gets the groove straight away */}
      <Audio
        src={staticFile("music/lofi.wav")}
        startFrom={Math.round(8 * (240 / 84) * fps)}
        volume={(f) => (f / fps >= edit.talk ? 0.2 : 0.06)}
      />
      {edit.sfx.map((s, i) => (
        <Sequence key={i} from={Math.max(0, Math.round(s.t * fps))} durationInFrames={Math.round(1.6 * fps)}>
          <Audio src={staticFile(`sfx/${s.name}.wav`)} volume={s.vol ?? 0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
