import React from "react";
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
import type { Callout, Chapter, Clip, Edit } from "./types";
import { C, H, PIP, SCREEN, W, fontFamily } from "./theme";
import { headRect, lerp, pipAmount } from "./layout";
import { Captions } from "./Captions";

const IconByName: React.FC<{ name: string; size: number; color: string; stroke?: number }> = ({
  name,
  size,
  color,
  stroke = 2.2,
}) => {
  const I = (Icons as unknown as Record<string, React.FC<any>>)[name] ?? Icons.Sparkles;
  return <I size={size} color={color} strokeWidth={stroke} />;
};

/** objectPosition x% that keeps the face centred inside the corner window. */
const pipFaceX = (edit: Edit, headT: number) => {
  const i = Math.max(0, Math.min(edit.faceCx.length - 1, Math.round(headT * edit.faceHz)));
  const scaled = (PIP.h / H) * W; // width of the cover-scaled frame inside the PiP box
  const overflow = scaled - PIP.w;
  const pct = ((edit.faceCx[i] * (PIP.h / H) - PIP.w / 2) / overflow) * 100;
  return Math.max(0, Math.min(100, pct));
};

/** One edited clip: the talking head plus the screen recording in sync. */
const ClipView: React.FC<{ clip: Clip; edit: Edit }> = ({ clip, edit }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = clip.at + frame / fps;
  const p = pipAmount(edit.clips, t);
  const r = headRect(p);
  const len = (clip.out - clip.in) / clip.rate;
  const ff = clip.rate > 1;
  const screenIn = clip.in - edit.screenOffset;
  const showScreen = p > 0.001 && screenIn >= 0;

  // 2-frame audio ramps at every cut so jump cuts don't click.
  const fadeFrames = 2;
  const totalFrames = Math.round(len * fps);
  const volume = (f: number) =>
    Math.min(1, f / fadeFrames, (totalFrames - f) / fadeFrames) > 0
      ? Math.min(1, f / fadeFrames, (totalFrames - f) / fadeFrames)
      : 0;

  return (
    <AbsoluteFill>
      {showScreen ? (
        <div
          style={{
            position: "absolute",
            left: SCREEN.x,
            top: SCREEN.y,
            width: SCREEN.w,
            height: SCREEN.h,
            borderRadius: SCREEN.radius,
            overflow: "hidden",
            opacity: p,
            transform: `scale(${lerp(1.06, 1, p)})`,
            boxShadow: "0 30px 80px rgba(0,0,0,0.55), 0 0 0 1px rgba(125,211,252,0.25)",
            background: "#000",
          }}
        >
          <OffthreadVideo
            src={staticFile("media/screen.mp4")}
            startFrom={Math.round(screenIn * fps)}
            playbackRate={clip.rate}
            muted
            style={{
              position: "absolute",
              left: -SCREEN.cropX * SCREEN.scale,
              top: -SCREEN.cropY * SCREEN.scale,
              width: SCREEN.srcW * SCREEN.scale,
              height: SCREEN.srcH * SCREEN.scale,
            }}
          />
        </div>
      ) : null}
      <div
        style={{
          position: "absolute",
          left: r.x,
          top: r.y,
          width: r.w,
          height: r.h,
          borderRadius: r.r,
          overflow: "hidden",
          boxShadow:
            p > 0.01
              ? `0 0 0 ${3 * p}px rgba(255,255,255,0.95), 0 0 0 ${6 * p}px rgba(11,16,51,0.85), 0 24px 60px rgba(0,0,0,${0.6 * p})`
              : "none",
        }}
      >
        <OffthreadVideo
          src={staticFile("media/head.mp4")}
          startFrom={Math.round(clip.in * fps)}
          playbackRate={clip.rate}
          muted={ff}
          volume={ff ? 0 : volume}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: `${lerp(50, pipFaceX(edit, clip.in + (frame / fps) * clip.rate), p)}% 50%`,
          }}
        />
      </div>
      {ff ? <FastForwardBadge rate={clip.rate} /> : null}
    </AbsoluteFill>
  );
};

const FastForwardBadge: React.FC<{ rate: number }> = ({ rate }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const k = spring({ frame, fps, config: { damping: 12, stiffness: 180 } });
  const blink = 0.75 + 0.25 * Math.sin(frame / 3);
  return (
    <div
      style={{
        position: "absolute",
        left: 80,
        top: 70,
        display: "flex",
        alignItems: "center",
        gap: 16,
        padding: "16px 28px",
        borderRadius: 18,
        background: C.coral,
        color: C.ink,
        fontFamily,
        fontWeight: 900,
        fontSize: 44,
        textTransform: "uppercase",
        boxShadow: "0 20px 50px rgba(0,0,0,0.5)",
        transform: `scale(${k})`,
      }}
    >
      <span style={{ opacity: blink, display: "flex" }}>
        <Icons.FastForward size={44} color={C.ink} fill={C.ink} strokeWidth={2} />
      </span>
      Fast forward {rate}x
    </div>
  );
};

const CalloutCard: React.FC<{ c: Callout }> = ({ c }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dur = Math.round(c.d * fps);
  const inS = spring({ frame, fps, config: { damping: 13, stiffness: 160 } });
  const outS = interpolate(frame, [dur - 10, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const k = inS * outS;
  const iconK = spring({ frame: frame - 4, fps, config: { damping: 8, stiffness: 200 } });
  // Full screen: the face-safe spot chosen from face tracking. Corner mode: stacked above the corner head.
  const inCorner = c.layout === "pip" || c.x === undefined;
  const width = inCorner ? 620 : (c.w ?? 600);
  const x = inCorner ? W - PIP.margin - 620 : (c.x as number);
  const y = inCorner ? H - PIP.margin - PIP.h - 24 - 236 : (c.y ?? 140);
  const fromLeft = !inCorner && x < W / 2;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width,
        boxSizing: "border-box",
        padding: "30px 34px",
        borderRadius: 26,
        background: "rgba(20,27,77,0.92)",
        border: `2px solid rgba(125,211,252,0.55)`,
        boxShadow: "0 30px 70px rgba(0,0,0,0.5)",
        display: "flex",
        gap: 26,
        alignItems: "center",
        opacity: k,
        transform: `translateX(${interpolate(inS, [0, 1], [fromLeft ? -80 : 80, 0])}px) scale(${lerp(0.92, 1, k)})`,
      }}
    >
      <div
        style={{
          flex: "0 0 auto",
          width: 112,
          height: 112,
          borderRadius: 28,
          background: C.sky,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transform: `scale(${iconK}) rotate(${interpolate(iconK, [0, 1], [-25, 0])}deg)`,
        }}
      >
        <IconByName name={c.icon} size={66} color={C.navy} stroke={2.4} />
      </div>
      <div style={{ fontFamily, color: C.white }}>
        <div style={{ fontWeight: 900, fontSize: 46, lineHeight: 1.05, textTransform: "uppercase" }}>{c.title}</div>
        {c.sub ? (
          <div
            style={{
              marginTop: 10,
              fontWeight: 700,
              fontSize: 22,
              letterSpacing: 3,
              textTransform: "uppercase",
              color: C.coral,
            }}
          >
            {c.sub}
          </div>
        ) : null}
      </div>
    </div>
  );
};

const ChapterTitle: React.FC<{ c: Chapter; big?: boolean }> = ({ c, big }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dur = Math.round(c.d * fps);
  const k1 = spring({ frame, fps, config: { damping: 14, stiffness: 140 } });
  const k2 = spring({ frame: frame - 6, fps, config: { damping: 14, stiffness: 140 } });
  const out = interpolate(frame, [dur - 12, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const full = c.layout === "full" && c.x !== undefined;
  const size = full ? (big ? 80 : 76) : 92;
  const alignRight = full && (c.x as number) > W / 2;
  // Anchor to the outer edge so a long title grows toward the middle, never off-screen.
  const box: React.CSSProperties = full
    ? alignRight
      ? { right: W - (c.x as number) - (c.w as number), top: c.y, textAlign: "right" }
      : { left: c.x, top: c.y, textAlign: "left" }
    : { left: 96, top: 80 };
  return (
    <div
      style={{
        position: "absolute",
        ...box,
        opacity: out,
        display: "flex",
        flexDirection: "column",
        alignItems: alignRight ? "flex-end" : "flex-start",
      }}
    >
      <div
        style={{
          fontFamily,
          fontWeight: 700,
          fontStyle: "italic",
          fontSize: big ? 38 : 34,
          color: C.sky,
          display: "inline-block",
          padding: "6px 16px",
          borderRadius: 10,
          background: "rgba(20,27,77,0.88)",
          opacity: k1,
          transform: `translateY(${interpolate(k1, [0, 1], [20, 0])}px)`,
          marginBottom: 12,
        }}
      >
        {c.kicker}
      </div>
      <div
        style={{
          display: "inline-block",
          background: C.sky,
          padding: big ? "10px 26px 4px" : "8px 22px 2px",
          clipPath: alignRight ? `inset(0 0 0 ${100 - k2 * 100}%)` : `inset(0 ${100 - k2 * 100}% 0 0)`,
          boxShadow: "0 20px 50px rgba(0,0,0,0.45)",
        }}
      >
        <div
          style={{
            fontFamily,
            fontWeight: 900,
            fontSize: size,
            lineHeight: 1,
            textTransform: "uppercase",
            color: C.navy,
            letterSpacing: -2,
            whiteSpace: "pre",
            textAlign: alignRight ? "right" : "left",
          }}
        >
          {c.title}
        </div>
      </div>
    </div>
  );
};

/** Background music: sits well under the voice, swells a little when nobody is talking. */
const musicVolume = (edit: Edit, t: number) => {
  const UNDER = 0.07;
  const OPEN = 0.17;
  const RAMP = 0.5;
  let dist = Infinity;
  for (const [a, b] of edit.speech) {
    if (t >= a && t <= b) return UNDER;
    dist = Math.min(dist, Math.abs(t - a), Math.abs(t - b));
  }
  const k = Math.min(1, dist / RAMP);
  return UNDER + (OPEN - UNDER) * k;
};

const ProgressBar: React.FC<{ duration: number }> = ({ duration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, height: 6, width: W, background: "rgba(255,255,255,0.08)" }}>
      <div style={{ height: "100%", width: `${(frame / fps / duration) * 100}%`, background: C.sky }} />
    </div>
  );
};

export const PlasmoVideo: React.FC<{ edit: Edit }> = ({ edit }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pipNow = pipAmount(edit.clips, t);
  const pipAt = (s: number) => pipAmount(edit.clips, s);

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 50% 45%, ${C.navyMid} 0%, ${C.navy} 60%, #0E1338 100%)`,
      }}
    >
      {edit.clips.map((c, i) => (
        <Sequence
          key={i}
          from={Math.round(c.at * fps)}
          durationInFrames={Math.max(1, Math.round(((c.out - c.in) / c.rate) * fps))}
          premountFor={15}
        >
          <ClipView clip={c} edit={edit} />
        </Sequence>
      ))}

      {/* Bottom shade so captions read on top of the talking head. */}
      <AbsoluteFill
        style={{
          background: "linear-gradient(180deg, rgba(0,0,0,0) 62%, rgba(8,10,30,0.55) 100%)",
          opacity: 1 - pipNow,
        }}
      />

      {edit.chapters.map((c, i) => (
        <Sequence key={`ch${i}`} from={Math.round(c.t * fps)} durationInFrames={Math.round(c.d * fps)}>
          <ChapterTitle c={c} big={i === 0} />
        </Sequence>
      ))}

      {edit.callouts.map((c, i) => (
        <Sequence key={`co${i}`} from={Math.round(c.t * fps)} durationInFrames={Math.round(c.d * fps)}>
          <CalloutCard c={c} />
        </Sequence>
      ))}

      <Captions words={edit.words} pip={pipAt} />
      <ProgressBar duration={edit.duration} />

      <Audio
        src={staticFile("music/lofi.wav")}
        volume={(f) => musicVolume(edit, f / fps)}
      />

      {edit.sfx.map((s, i) => (
        <Sequence key={`sfx${i}`} from={Math.max(0, Math.round(s.t * fps))} durationInFrames={Math.round(1.6 * fps)}>
          <Audio src={staticFile(`sfx/${s.name}.wav`)} volume={s.vol ?? 0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

