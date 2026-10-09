import { continueRender, delayRender, staticFile } from "remotion";

// Plasmo's own identity, taken from plasmo.uk's stylesheet (dark theme + brand font).
export const BRAND = {
  bg: "#161a1d",
  bgAlt: "#1c2125",
  surface: "#20262a",
  surface2: "#282f34",
  text: "#d8e2ea",
  muted: "#7d8f9c",
  accent: "#22b0d2",
  accentLight: "#7fe0f4",
  accentDeep: "#1F869E",
  ink: "#0d1114",
  red: "#ff4d5e",
};
export const DISPLAY = "Bricolage Grotesque"; // --font-brand on plasmo.uk
export const UI = "Inter";

if (typeof document !== "undefined") {
  const handle = delayRender("Loading Plasmo brand fonts");
  Promise.all([
    new FontFace(DISPLAY, `url(${staticFile("fonts/BricolageGrotesque.woff2")}) format("woff2")`, { weight: "200 800" }).load(),
    new FontFace(UI, `url(${staticFile("fonts/Inter.woff2")}) format("woff2")`, { weight: "400 800" }).load(),
  ])
    .then((faces) => {
      faces.forEach((f) => document.fonts.add(f));
      continueRender(handle);
    })
    .catch((err) => {
      console.error(err);
      continueRender(handle);
    });
}
