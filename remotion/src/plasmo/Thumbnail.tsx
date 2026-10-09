import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { Check, Clock } from "lucide-react";
import { fontFamily } from "./theme";

// YouTube thumbnail, 1920x1080 (exported down to 1280x720).
// Story left to right: the old way (paper, crossed out) -> Zak -> the better way (Plasmo, 4/4 in seconds).
const T = {
  red: "#FF2E3D",
  redDeep: "#7A0B1E",
  blue: "#14C8FF",
  blueDeep: "#1B2366",
  yellow: "#FFE14D",
  green: "#22E07A",
  ink: "#0B1033",
  white: "#FFFFFF",
};

const stroke = (px: number, color = T.ink): React.CSSProperties => ({
  WebkitTextStroke: `${px}px ${color}`,
  paintOrder: "stroke fill",
});

const ExamPaper: React.FC<{ rotate: number; x: number; y: number; z: number }> = ({ rotate, x, y, z }) => (
  <div
    style={{
      position: "absolute",
      left: x,
      top: y,
      width: 400,
      height: 540,
      background: "#FBFAF5",
      borderRadius: 6,
      transform: `rotate(${rotate}deg)`,
      boxShadow: "0 18px 40px rgba(0,0,0,0.45)",
      padding: "28px 30px",
      boxSizing: "border-box",
      zIndex: z,
      fontFamily: "Georgia, 'Times New Roman', serif",
      color: "#222",
      display: "flex",
      flexDirection: "column",
      gap: 10,
    }}
  >
    <div style={{ display: "flex", gap: 6 }}>
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} style={{ width: 26, height: 26, border: "2px solid #333" }} />
      ))}
    </div>
    <div style={{ fontSize: 15, letterSpacing: 1 }}>Candidate number</div>
    <div style={{ fontWeight: 700, fontSize: 34, lineHeight: 1.05, marginTop: 10 }}>GCSE (9–1)</div>
    <div style={{ fontWeight: 700, fontSize: 38, lineHeight: 1.05 }}>Mathematics</div>
    <div style={{ fontSize: 22 }}>Paper 1 (Non-Calculator)</div>
    <div style={{ fontSize: 22, fontWeight: 700 }}>Higher Tier</div>
    <div style={{ fontSize: 18, marginTop: 6 }}>Time: 1 hour 30 minutes</div>
    <div style={{ marginTop: 14, display: "flex", flexDirection: "column", gap: 13 }}>
      {Array.from({ length: 7 }).map((_, i) => (
        <div key={i} style={{ height: 2, background: "#C9C6BC", width: i % 3 === 2 ? "70%" : "100%" }} />
      ))}
    </div>
    <div
      style={{
        marginTop: "auto",
        alignSelf: "flex-end",
        border: "2px solid #333",
        padding: "6px 12px",
        fontSize: 16,
      }}
    >
      Total Marks <b>/80</b>
    </div>
  </div>
);

const BigCross: React.FC = () => {
  const bar: React.CSSProperties = {
    position: "absolute",
    left: "50%",
    top: "50%",
    width: 660,
    height: 92,
    marginLeft: -330,
    marginTop: -46,
    background: T.red,
    borderRadius: 46,
    border: `10px solid ${T.white}`,
    boxShadow: "0 16px 40px rgba(0,0,0,0.55)",
  };
  return (
    <div style={{ position: "absolute", left: 40, top: 330, width: 560, height: 620, zIndex: 6 }}>
      <div style={{ ...bar, transform: "rotate(45deg)" }} />
      <div style={{ ...bar, transform: "rotate(-45deg)" }} />
    </div>
  );
};

const Pill: React.FC<{ bg: string; color: string; children: React.ReactNode; style?: React.CSSProperties }> = ({
  bg,
  color,
  children,
  style,
}) => (
  <div
    style={{
      position: "absolute",
      display: "flex",
      alignItems: "center",
      gap: 14,
      background: bg,
      color,
      fontFamily,
      fontWeight: 900,
      fontSize: 44,
      textTransform: "uppercase",
      letterSpacing: -0.5,
      padding: "14px 26px",
      borderRadius: 18,
      border: `6px solid ${T.ink}`,
      boxShadow: "0 14px 30px rgba(0,0,0,0.5)",
      zIndex: 8,
      ...style,
    }}
  >
    {children}
  </div>
);

export const Thumbnail: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: T.ink, overflow: "hidden" }}>
      {/* Split background: hot red (old way) | electric blue (better way) */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 18% 60%, ${T.red} 0%, ${T.redDeep} 70%)`,
          clipPath: "polygon(0 0, 54% 0, 44% 100%, 0 100%)",
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(circle at 82% 55%, ${T.blue} 0%, ${T.blueDeep} 72%)`,
          clipPath: "polygon(54% 0, 100% 0, 100% 100%, 44% 100%)",
        }}
      />
      {/* Glowing divider */}
      <AbsoluteFill
        style={{
          background: T.yellow,
          clipPath: "polygon(53.4% 0, 54.6% 0, 44.6% 100%, 43.4% 100%)",
          filter: "drop-shadow(0 0 18px rgba(255,225,77,0.9))",
        }}
      />

      {/* Old way: a stack of exam papers, crossed out */}
      <ExamPaper rotate={-14} x={70} y={420} z={2} />
      <ExamPaper rotate={-4} x={120} y={390} z={3} />
      <ExamPaper rotate={7} x={150} y={410} z={4} />
      <BigCross />
      <Pill bg={T.white} color={T.red} style={{ left: 52, top: 930, fontSize: 40 }}>
        <Clock size={40} color={T.red} strokeWidth={3} /> Weeks to get marked
      </Pill>

      {/* Zak */}
      <Img
        src={staticFile("thumb_zak.png")}
        style={{
          position: "absolute",
          left: 470,
          bottom: -40,
          height: 800,
          zIndex: 5,
          filter:
            "brightness(1.06) contrast(1.14) saturate(1.18) drop-shadow(6px 0 0 #fff) drop-shadow(-6px 0 0 #fff) drop-shadow(0 -6px 0 #fff) drop-shadow(0 0 30px rgba(255,225,77,0.45)) drop-shadow(0 20px 40px rgba(0,0,0,0.55))",
        }}
      />

      {/* Better way: real Plasmo marking, 4/4 in seconds */}
      <div
        style={{
          position: "absolute",
          left: 1330,
          top: 420,
          width: 560,
          zIndex: 6,
          transform: "rotate(3deg)",
          borderRadius: 20,
          overflow: "hidden",
          border: `8px solid ${T.white}`,
          boxShadow: "0 24px 60px rgba(0,0,0,0.55)",
        }}
      >
        <Img src={staticFile("thumb_plasmo.png")} style={{ width: "100%", display: "block" }} />
      </div>
      <div
        style={{
          position: "absolute",
          left: 1640,
          top: 330,
          width: 230,
          height: 230,
          borderRadius: "50%",
          background: T.green,
          border: `10px solid ${T.white}`,
          boxShadow: "0 18px 40px rgba(0,0,0,0.5)",
          zIndex: 9,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          transform: "rotate(8deg)",
        }}
      >
        <Check size={78} color={T.ink} strokeWidth={4.5} />
        <div style={{ fontFamily, fontWeight: 900, fontSize: 64, color: T.ink, lineHeight: 0.95 }}>4/4</div>
      </div>
      <Pill bg={T.yellow} color={T.ink} style={{ left: 1300, top: 880, fontSize: 42 }}>
        Marked in 10 seconds
      </Pill>

      {/* Headline hook */}
      <div
        style={{
          position: "absolute",
          left: 52,
          top: 34,
          zIndex: 10,
          fontFamily,
          fontWeight: 900,
          textTransform: "uppercase",
          lineHeight: 0.92,
          letterSpacing: -3,
        }}
      >
        <div style={{ fontSize: 150, color: T.white, ...stroke(16) }}>Stop printing</div>
        <div
          style={{
            display: "inline-block",
            marginTop: 8,
            fontSize: 150,
            color: T.ink,
            background: T.yellow,
            padding: "4px 26px 0",
            border: `8px solid ${T.ink}`,
            transform: "rotate(-2deg)",
          }}
        >
          Past papers
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          right: 46,
          top: 230,
          zIndex: 10,
          display: "flex",
          alignItems: "center",
          gap: 8,
          fontFamily,
          fontWeight: 900,
          fontSize: 58,
          textTransform: "uppercase",
          color: T.white,
          ...stroke(10),
        }}
      >
        Do this instead
        <svg width="70" height="70" viewBox="0 0 24 24" style={{ transform: "rotate(90deg)" }}>
          <path d="M5 12h12M12 5l7 7-7 7" fill="none" stroke={T.ink} strokeWidth="6" strokeLinecap="round" strokeLinejoin="round" />
          <path d="M5 12h12M12 5l7 7-7 7" fill="none" stroke={T.yellow} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </AbsoluteFill>
  );
};
