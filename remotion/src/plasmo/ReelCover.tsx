import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Check, X } from "lucide-react";
import { BRAND as B, DISPLAY, UI } from "./brand";

// Instagram Reel cover, 1080x1920, in Plasmo's own look: charcoal + cyan, Bricolage Grotesque.
// The profile grid shows only the centre 4:5 (y 285-1635), so everything that matters sits there.
const SAFE_TOP = 300;

export type CoverProps = { lines: [string, string]; visual: "papers" | "card" | "dash"; caption: string };

const glowText: React.CSSProperties = {
  backgroundImage: `linear-gradient(100deg, ${B.accentLight} 0%, ${B.accent} 55%, ${B.accentDeep} 100%)`,
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  color: "transparent",
  filter: `drop-shadow(0 0 28px rgba(34,176,210,0.55))`,
};

const Paper: React.FC<{ x: number; y: number; r: number; scale?: number; children?: React.ReactNode }> = ({ x, y, r, scale = 1, children }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: 300,
      height: 400,
      background: "#FBFAF5",
      borderRadius: 8,
      transform: `rotate(${r}deg) scale(${scale})`,
      transformOrigin: "0 0",
      boxShadow: "0 24px 50px rgba(0,0,0,0.6)",
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
      borderRadius: 26,
      overflow: "hidden",
      border: `3px solid ${B.accent}`,
      boxShadow: `0 0 0 10px rgba(34,176,210,0.12), 0 0 80px rgba(34,176,210,0.45), 0 30px 70px rgba(0,0,0,0.6)`,
      transform: `rotate(${r}deg)`,
      zIndex: 5,
    }}
  >
    <Img src={staticFile(src)} style={{ width: "100%", display: "block" }} />
  </div>
);

export const ReelCover: React.FC<CoverProps> = ({ lines, visual, caption }) => (
  <AbsoluteFill style={{ background: B.bg, overflow: "hidden" }}>
    {/* the real landing page, blurred: same world as plasmo.uk */}
    <Img src={staticFile("cover_bg.jpg")} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", opacity: 0.5, transform: "scale(1.15)" }} />
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at 15% 22%, rgba(34,176,210,0.42) 0%, transparent 42%),
          radial-gradient(circle at 90% 70%, rgba(34,176,210,0.30) 0%, transparent 45%),
          linear-gradient(180deg, rgba(22,26,29,0.35) 0%, rgba(22,26,29,0.15) 45%, rgba(22,26,29,0.85) 100%)`,
      }}
    />

    {/* wordmark + mascot, like the site header */}
    <div style={{ position: "absolute", left: 64, top: SAFE_TOP, display: "flex", alignItems: "center", gap: 18 }}>
      <Img src={staticFile("cover_mascot.png")} style={{ width: 84, height: 77, borderRadius: 18, objectFit: "cover", boxShadow: `0 0 30px rgba(34,176,210,0.35)` }} />
      <div style={{ fontFamily: DISPLAY, fontWeight: 800, fontSize: 64, letterSpacing: -2, color: B.text }}>
        Plas<span style={glowText}>mo</span>
      </div>
    </div>

    {/* headline */}
    <div style={{ position: "absolute", left: 60, right: 50, top: SAFE_TOP + 120, fontFamily: DISPLAY, fontWeight: 800, letterSpacing: -3, lineHeight: 0.92 }}>
      <div style={{ fontSize: 168, color: B.text, textShadow: "0 8px 30px rgba(0,0,0,0.5)" }}>{lines[0]}</div>
      <div style={{ fontSize: 168, ...glowText, whiteSpace: "nowrap" }}>{lines[1]}</div>
    </div>

    {visual === "papers" ? (
      <>
        <Paper x={250} y={830} r={-12} scale={1.22} />
        <Paper x={330} y={800} r={-2} scale={1.22} />
        <Paper x={410} y={820} r={9} scale={1.22} />
        <div style={{ position: "absolute", left: 250, top: 790, width: 600, height: 600, zIndex: 6 }}>
          <X size={600} color={B.red} strokeWidth={4} style={{ filter: "drop-shadow(0 0 30px rgba(255,77,94,0.6)) drop-shadow(0 14px 24px rgba(0,0,0,0.5))" }} />
        </div>
      </>
    ) : null}
    {visual === "card" ? (
      <>
        <Shot src="thumb_plasmo.png" x={70} y={860} w={940} r={-3} />
        <div
          style={{
            position: "absolute",
            right: 46,
            top: 760,
            width: 250,
            height: 250,
            borderRadius: "50%",
            background: `linear-gradient(140deg, ${B.accentLight}, ${B.accent})`,
            boxShadow: `0 0 60px rgba(34,176,210,0.7), 0 20px 40px rgba(0,0,0,0.5)`,
            zIndex: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            transform: "rotate(8deg)",
          }}
        >
          <Check size={86} color={B.ink} strokeWidth={4.5} />
          <div style={{ fontFamily: DISPLAY, fontWeight: 800, fontSize: 76, color: B.ink, lineHeight: 0.9, letterSpacing: -2 }}>4/4</div>
        </div>
      </>
    ) : null}
    {visual === "dash" ? (
      <>
        <Paper x={60} y={820} r={-10} scale={1.05}>
          <div
            style={{
              position: "absolute",
              left: 18,
              top: 150,
              transform: "rotate(-18deg)",
              border: `8px solid ${B.red}`,
              color: B.red,
              fontFamily: DISPLAY,
              fontWeight: 800,
              fontSize: 60,
              letterSpacing: 1,
              padding: "2px 14px",
              borderRadius: 10,
              background: "rgba(251,250,245,0.88)",
            }}
          >
            OUTDATED
          </div>
        </Paper>
        <Shot src="cover_dash.png" x={290} y={1110} w={740} r={3} />
      </>
    ) : null}

    {/* caption + URL, still inside the grid crop */}
    <div style={{ position: "absolute", left: 0, right: 0, top: 1478, display: "flex", flexDirection: "column", alignItems: "center", gap: 16, zIndex: 9 }}>
      <div
        style={{
          fontFamily: UI,
          fontWeight: 800,
          fontSize: 44,
          color: B.ink,
          background: B.accent,
          borderRadius: 999,
          padding: "14px 38px",
          boxShadow: `0 0 40px rgba(34,176,210,0.55)`,
        }}
      >
        {caption}
      </div>
      <div style={{ fontFamily: UI, fontWeight: 700, fontSize: 38, color: B.text, letterSpacing: 0.5 }}>plasmo.uk</div>
    </div>
  </AbsoluteFill>
);

export const COVERS: (CoverProps & { n: number })[] = [
  { n: 1, lines: ["Weeks", "to mark?"], visual: "papers", caption: "There's a faster way" },
  { n: 2, lines: ["Marked in", "10 seconds"], visual: "card", caption: "Real AI feedback" },
  { n: 3, lines: ["Paper is", "outdated"], visual: "dash", caption: "Know your weak topics" },
];
