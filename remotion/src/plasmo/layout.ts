import { Easing, interpolate } from "remotion";
import type { Clip } from "./types";
import { H, PIP, W } from "./theme";

const TRANSITION = 0.55; // seconds

const ease = Easing.bezier(0.65, 0, 0.35, 1);

/** 0 = talking head full screen, 1 = screen recording with head in the corner. */
export const pipAmount = (clips: Clip[], t: number): number => {
  let idx = 0;
  for (let i = 0; i < clips.length; i++) if (clips[i].at <= t) idx = i;
  const cur = clips[idx].layout === "pip" ? 1 : 0;
  // Find the most recent boundary where the layout changed.
  let j = idx;
  while (j > 0 && clips[j - 1].layout === clips[idx].layout) j--;
  if (j === 0) return cur;
  const prev = cur === 1 ? 0 : 1;
  const p = interpolate(t - clips[j].at, [0, TRANSITION], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  return prev + (cur - prev) * p;
};

export const layoutChanges = (clips: Clip[]): number[] =>
  clips.filter((c, i) => i > 0 && c.layout !== clips[i - 1].layout).map((c) => c.at);

export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;

export const headRect = (p: number) => {
  const pipX = W - PIP.margin - PIP.w;
  const pipY = H - PIP.margin - PIP.h;
  return {
    x: lerp(0, pipX, p),
    y: lerp(0, pipY, p),
    w: lerp(W, PIP.w, p),
    h: lerp(H, PIP.h, p),
    r: lerp(0, PIP.radius, p),
  };
};
