import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Check, X } from "lucide-react";
import { C, fontFamily } from "./theme";

// Instagram Reel cover, 1080x1920, Plasmo-branded (no people). The profile grid shows only the
// centre 4:5 (y 285-1635), so tag, headline, visual and URL all sit inside that band.
const T = { yellow: "#FFE14D", red: "#FF2E3D", green: "#22E07A", ink: "#0B1033" };
const SAFE_TOP = 300;

export type CoverProps = { n: number; lines: [string, string]; visual: "papers" | "card" | "dash"; caption: string };

const Paper: React.FC<{ x: number; y: number; r: number; scale?: number; children?: React.ReactNode }> = ({ x, y, r, scale = 1, children }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: 300,
      height: 400,
      background: "#FBFAF5",
      borderRadius: 6,
      transform: `rotate(${r}deg) scale(${scale})`,
      transformOrigin: "0 0",
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

const Shot: React.FC<{ src: string; x: number; y: number; w: number; r: number }> = ({ src, x, y, w, r }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: w,
      borderRadius: 22,
      overflow: "hidden",
      border: `8px solid ${C.white}`,
      boxShadow: "0 26px 60px rgba(0,0,0,0.55)",
      transform: `rotate(${r}deg)`,
      zIndex: 5,
    }}
  >
    <Img src={staticFile(src)} style={{ width: "100%", display: "block" }} />
  </div>
);

export const ReelCover: React.FC<CoverProps> = ({ lines, visual, caption }) => (
  <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 46%, ${C.navyMid} 0%, ${C.navy} 58%, #0A0F33 100%)`, overflow: "hidden" }}>
    {/* faint exam-paper ruling: the series' texture */}
    <AbsoluteFill
      style={{
        backgroundImage: "repeating-linear-gradient(0deg, rgba(125,211,252,0.07) 0 2px, transparent 2px 64px)",
        maskImage: "linear-gradient(180deg, transparent 0%, #000 20%, #000 75%, transparent 100%)",
      }}
    />

    {/* brand tag: the Plasmo mascot */}
    <div style={{ position: "absolute", left: 60, top: SAFE_TOP, display: "flex", alignItems: "center", gap: 18, fontFamily, fontWeight: 900, fontSize: 40, letterSpacing: 2, color: C.sky }}>
      <Img src={staticFile("cover_mascot.png")} style={{ width: 72, height: 66, borderRadius: 16, objectFit: "cover" }} />
      PLASMO
    </div>

    {/* headline */}
    <div style={{ position: "absolute", left: 56, right: 56, top: SAFE_TOP + 100, fontFamily, fontWeight: 900, textTransform: "uppercase", letterSpacing: -3, lineHeight: 0.92 }}>
      <div style={{ fontSize: 132, color: C.white, WebkitTextStroke: `14px ${T.ink}`, paintOrder: "stroke fill" }}>{lines[0]}</div>
      <div style={{ display: "inline-block", marginTop: 10, fontSize: 132, color: T.ink, background: T.yellow, border: `8px solid ${T.ink}`, padding: "6px 22px 0", transform: "rotate(-2deg)", whiteSpace: "nowrap" }}>
        {lines[1]}
      </div>
    </div>

    {/* the visual: the old way crossed out, the real marking, or paper vs the dashboard */}
    {visual === "papers" ? (
      <>
        <Paper x={250} y={800} r={-12} scale={1.25} />
        <Paper x={330} y={770} r={-2} scale={1.25} />
        <Paper x={410} y={790} r={9} scale={1.25} />
        <div style={{ position: "absolute", left: 240, top: 760, width: 620, height: 620, zIndex: 6 }}>
          <X size={620} color={T.red} strokeWidth={4} style={{ filter: "drop-shadow(0 12px 24px rgba(0,0,0,0.55))" }} />
        </div>
      </>
    ) : null}
    {visual === "card" ? (
      <>
        <Shot src="thumb_plasmo.png" x={70} y={830} w={940} r={-3} />
        <div
          style={{
            position: "absolute",
            right: 50,
            top: 740,
            width: 250,
            height: 250,
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
          <Check size={86} color={T.ink} strokeWidth={4.5} />
          <div style={{ fontFamily, fontWeight: 900, fontSize: 72, color: T.ink, lineHeight: 0.9 }}>4/4</div>
        </div>
      </>
    ) : null}
    {visual === "dash" ? (
      <>
        <Paper x={60} y={790} r={-10} scale={1.05}>
          <div
            style={{
              position: "absolute",
              left: 18,
              top: 150,
              transform: "rotate(-18deg)",
              border: `8px solid ${T.red}`,
              color: T.red,
              fontFamily,
              fontWeight: 900,
              fontSize: 58,
              letterSpacing: 2,
              padding: "4px 14px",
              borderRadius: 8,
              background: "rgba(251,250,245,0.88)",
            }}
          >
            OUTDATED
          </div>
        </Paper>
        <Shot src="cover_dash.png" x={300} y={1090} w={720} r={3} />
      </>
    ) : null}

    {/* caption + URL, still inside the grid crop */}
    <div style={{ position: "absolute", left: 0, right: 0, top: 1470, display: "flex", flexDirection: "column", alignItems: "center", gap: 14, zIndex: 9 }}>
      <div style={{ fontFamily, fontWeight: 900, fontSize: 46, textTransform: "uppercase", color: T.ink, background: C.white, borderRadius: 999, padding: "12px 34px", border: `6px solid ${T.ink}` }}>{caption}</div>
      <div style={{ fontFamily, fontWeight: 800, fontSize: 40, color: C.sky, letterSpacing: 1 }}>plasmo.uk</div>
    </div>
  </AbsoluteFill>
);

export const COVERS: CoverProps[] = [
  { n: 1, lines: ["Weeks", "to mark?"], visual: "papers", caption: "There's a faster way" },
  { n: 2, lines: ["Marked in", "10 seconds"], visual: "card", caption: "Real AI feedback" },
  { n: 3, lines: ["Paper is", "outdated"], visual: "dash", caption: "Know your weak topics" },
];
