import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Check, X } from "lucide-react";
import { C, fontFamily } from "./theme";

// Instagram Reel cover, 1080x1920. The profile grid shows only the centre 4:5 (y 285-1635),
// so the tag, headline, face and prop all sit inside that band. One template for the series.
const T = { yellow: "#FFE14D", red: "#FF2E3D", green: "#22E07A", ink: "#0B1033" };
const SAFE_TOP = 300;

export type CoverProps = { n: number; lines: [string, string]; photo: string; prop: "cross" | "tick" | "stamp" };

const Paper: React.FC<{ x: number; y: number; r: number; children?: React.ReactNode }> = ({ x, y, r, children }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: 300,
      height: 400,
      background: "#FBFAF5",
      borderRadius: 6,
      transform: `rotate(${r}deg)`,
      boxShadow: "0 18px 40px rgba(0,0,0,0.5)",
      padding: 24,
      boxSizing: "border-box",
      fontFamily: "Georgia, serif",
      color: "#222",
      display: "flex",
      flexDirection: "column",
      gap: 10,
    }}
  >
    <div style={{ fontWeight: 700, fontSize: 28 }}>GCSE (9–1)</div>
    <div style={{ fontWeight: 700, fontSize: 32 }}>Mathematics</div>
    <div style={{ fontSize: 18 }}>Paper 1 · Higher Tier</div>
    {Array.from({ length: 7 }).map((_, i) => (
      <div key={i} style={{ height: 2, background: "#C9C6BC", width: i % 3 === 2 ? "65%" : "100%", marginTop: 6 }} />
    ))}
    {children}
  </div>
);

export const ReelCover: React.FC<CoverProps> = ({ n, lines, photo, prop }) => (
  <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 42%, ${C.navyMid} 0%, ${C.navy} 58%, #0A0F33 100%)`, overflow: "hidden" }}>
    {/* faint exam-paper ruling: the series' texture */}
    <AbsoluteFill
      style={{
        backgroundImage: "repeating-linear-gradient(0deg, rgba(125,211,252,0.07) 0 2px, transparent 2px 64px)",
        maskImage: "linear-gradient(180deg, transparent 0%, #000 20%, #000 70%, transparent 100%)",
      }}
    />

    {/* series tag */}
    <div
      style={{
        position: "absolute",
        left: 60,
        top: SAFE_TOP,
        display: "flex",
        alignItems: "center",
        gap: 14,
        fontFamily,
        fontWeight: 900,
        fontSize: 40,
        letterSpacing: 2,
        color: C.sky,
      }}
    >
      PLASMO
      <span style={{ color: T.ink, background: C.sky, borderRadius: 10, padding: "2px 14px" }}>{String(n).padStart(2, "0")}</span>
    </div>

    {/* headline */}
    <div style={{ position: "absolute", left: 56, right: 56, top: SAFE_TOP + 80, fontFamily, fontWeight: 900, textTransform: "uppercase", letterSpacing: -3, lineHeight: 0.92 }}>
      <div style={{ fontSize: 132, color: C.white, WebkitTextStroke: `14px ${T.ink}`, paintOrder: "stroke fill" }}>{lines[0]}</div>
      <div
        style={{
          display: "inline-block",
          marginTop: 10,
          fontSize: 132,
          color: T.ink,
          background: T.yellow,
          border: `8px solid ${T.ink}`,
          padding: "6px 22px 0",
          transform: "rotate(-2deg)",
          whiteSpace: "nowrap",
        }}
      >
        {lines[1]}
      </div>
    </div>

    {/* story prop: the problem crossed out, the answer ticked, or paper stamped outdated */}
    {prop === "cross" ? (
      <>
        <div style={{ position: "absolute", left: 40, top: 690, width: 420, height: 420, transform: "scale(0.78)", transformOrigin: "0 0", zIndex: 6 }}>
          <Paper x={0} y={20} r={-12} />
          <Paper x={50} y={0} r={4} />
          <div style={{ position: "absolute", left: 10, top: 30, width: 380, height: 380 }}>
            <X size={380} color={T.red} strokeWidth={4.2} style={{ filter: "drop-shadow(0 10px 20px rgba(0,0,0,0.5))" }} />
          </div>
        </div>
      </>
    ) : null}
    {prop === "stamp" ? (
      <div style={{ position: "absolute", left: 50, top: 690, width: 320, height: 420, transform: "scale(0.82)", transformOrigin: "0 0", zIndex: 6 }}>
      <Paper x={0} y={0} r={-8}>
        <div
          style={{
            position: "absolute",
            left: 20,
            top: 150,
            transform: "rotate(-18deg)",
            border: `8px solid ${T.red}`,
            color: T.red,
            fontFamily,
            fontWeight: 900,
            fontSize: 56,
            letterSpacing: 2,
            padding: "4px 14px",
            borderRadius: 8,
            background: "rgba(251,250,245,0.85)",
          }}
        >
          OUTDATED
        </div>
      </Paper>
      </div>
    ) : null}

    {/* Zak */}
    <Img
      src={staticFile(photo)}
      style={{
        position: "absolute",
        left: "50%",
        bottom: -110,
        height: 1000,
        transform: "translateX(-42%)",
        zIndex: 5,
        filter:
          "brightness(1.03) contrast(1.06) saturate(1.08) drop-shadow(5px 0 0 #fff) drop-shadow(-5px 0 0 #fff) drop-shadow(0 -5px 0 #fff) drop-shadow(0 24px 40px rgba(0,0,0,0.5))",
      }}
    />

    {prop === "tick" ? (
      <div
        style={{
          position: "absolute",
          right: 70,
          top: 700,
          width: 280,
          height: 280,
          borderRadius: "50%",
          background: T.green,
          border: `12px solid ${C.white}`,
          boxShadow: "0 20px 44px rgba(0,0,0,0.5)",
          zIndex: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          transform: "rotate(8deg)",
        }}
      >
        <Check size={96} color={T.ink} strokeWidth={4.5} />
        <div style={{ fontFamily, fontWeight: 900, fontSize: 80, color: T.ink, lineHeight: 0.9 }}>4/4</div>
      </div>
    ) : null}
  </AbsoluteFill>
);

export const COVERS: CoverProps[] = [
  { n: 1, lines: ["Weeks", "to mark?"], photo: "cover_zak_1.png", prop: "cross" },
  { n: 2, lines: ["Marked in", "10 seconds"], photo: "cover_zak_2.png", prop: "tick" },
  { n: 3, lines: ["Paper is", "outdated"], photo: "cover_zak_3.png", prop: "stamp" },
];
