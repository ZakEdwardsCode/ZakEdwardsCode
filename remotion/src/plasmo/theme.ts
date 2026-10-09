import { continueRender, delayRender, staticFile } from "remotion";

// Libre Franklin is bundled in public/fonts so rendering never depends on the network.
export const fontFamily = "Libre Franklin";

if (typeof document !== "undefined") {
  const handle = delayRender("Loading Libre Franklin");
  const faces = [
    new FontFace(fontFamily, `url(${staticFile("fonts/LibreFranklin.woff2")}) format("woff2")`, {
      weight: "100 900",
      style: "normal",
    }),
    new FontFace(fontFamily, `url(${staticFile("fonts/LibreFranklin-Italic.woff2")}) format("woff2")`, {
      weight: "100 900",
      style: "italic",
    }),
  ];
  Promise.all(faces.map((f) => f.load()))
    .then((loaded) => {
      loaded.forEach((f) => document.fonts.add(f));
      continueRender(handle);
    })
    .catch((err) => {
      console.error(err);
      continueRender(handle);
    });
}

// Palette lifted from the orchestration diagram.
export const C = {
  navy: "#141B4D",
  navyMid: "#1B2366",
  sky: "#7DD3FC",
  skyDeep: "#38BDF8",
  coral: "#F87171",
  white: "#FFFFFF",
  ink: "#0B1033",
};

export const W = 1920;
export const H = 1080;

// Screen card: crop of the 1920x876 recording (x 160..1760, y 0..800), scaled 1.15x.
export const SCREEN = {
  srcW: 1920,
  srcH: 876,
  cropX: 160,
  cropY: 0,
  scale: 1.15,
  x: 40,
  y: 24,
  w: 1840,
  h: 890,
  radius: 22,
};

// Talking-head picture-in-picture box when in corner mode.
export const PIP = { w: 440, h: 330, margin: 44, radius: 28 };
