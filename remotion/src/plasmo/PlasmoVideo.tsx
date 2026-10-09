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
            objectPosition: `${lerp(50, 40, p)}% ${lerp(50, 30, p)}%`,
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

const CalloutCard: React.FC<{ c: Callout; pip: number }> = ({ c, pip }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const dur = Math.round(c.d * fps);
  const inS = spring({ frame, fps, config: { damping: 13, stiffness: 160 } });
  const outS = interpolate(frame, [dur - 10, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const k = inS * outS;
  const iconK = spring({ frame: frame - 4, fps, config: { damping: 8, stiffness: 200 } });
  // Right side when full screen (face sits left of centre); stacked above the corner head in corner mode.
  const x = pip > 0.5 ? W - PIP.margin - 620 : W - 120 - 620;
  const y = pip > 0.5 ? H - PIP.margin - PIP.h - 24 - 236 : 150;
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: 620,
        padding: "30px 34px",
        borderRadius: 26,
        background: "rgba(20,27,77,0.92)",
        border: `2px solid rgba(125,211,252,0.55)`,
        boxShadow: "0 30px 70px rgba(0,0,0,0.5)",
        display: "flex",
        gap: 26,
        alignItems: "center",
        opacity: k,
        transform: `translateX(${interpolate(inS, [0, 1], [80, 0])}px) scale(${lerp(0.92, 1, k)})`,
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
  const size = big ? 118 : 92;
  return (
    <div style={{ position: "absolute", left: 96, top: big ? 300 : 80, opacity: out }}>
      <div
        style={{
          fontFamily,
          fontWeight: 700,
          fontStyle: "italic",
          fontSize: big ? 44 : 36,
          color: C.sky,
          textShadow: "0 4px 16px rgba(0,0,0,0.6)",
          opacity: k1,
          transform: `translateY(${interpolate(k1, [0, 1], [20, 0])}px)`,
          marginBottom: 14,
        }}
      >
        {c.kicker}
      </div>
      <div
        style={{
          display: "inline-block",
          background: C.sky,
          padding: big ? "10px 26px 4px" : "8px 22px 2px",
          clipPath: `inset(0 ${100 - k2 * 100}% 0 0)`,
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
          }}
        >
          {c.title}
        </div>
      </div>
    </div>
  );
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
          <CalloutCard c={c} pip={pipAt(c.t)} />
        </Sequence>
      ))}

      <Captions words={edit.words} pip={pipAt} />
      <ProgressBar duration={edit.duration} />

      {edit.sfx.map((s, i) => (
        <Sequence key={`sfx${i}`} from={Math.max(0, Math.round(s.t * fps))} durationInFrames={Math.round(1.6 * fps)}>
          <Audio src={staticFile(`sfx/${s.name}.wav`)} volume={s.vol ?? 0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

