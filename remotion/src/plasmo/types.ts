export type Layout = "full" | "pip";

export type Clip = {
  /** Source in/out on the talking-head timeline, in seconds. */
  in: number;
  out: number;
  /** Where the clip starts in the edited timeline, in seconds. */
  at: number;
  layout: Layout;
  /** Playback speed; >1 is a muted fast-forward of a silent stretch. */
  rate: number;
};

export type Word = { w: string; s: number; e: number };

export type Sfx = { t: number; name: string; vol?: number };

/** Face-safe placement, set for overlays shown over the full-screen talking head. */
type Placement = { layout: Layout; x?: number; y?: number; w?: number };

export type Callout = Placement & {
  t: number;
  d: number;
  icon: string;
  title: string;
  sub?: string;
};

export type Chapter = Placement & { t: number; d: number; kicker: string; title: string };

export type Edit = {
  fps: number;
  duration: number;
  /** screenTime = headTime - screenOffset */
  screenOffset: number;
  clips: Clip[];
  words: Word[];
  sfx: Sfx[];
  callouts: Callout[];
  chapters: Chapter[];
  /** Smoothed face-centre x (1920-wide frame), sampled faceHz times per head-second. */
  faceHz: number;
  faceCx: number[];
  /** Output-time intervals where Zak is speaking; music ducks under them. */
  speech: [number, number][];
  /** Narrative score for this video (scripts/score.py), relative to public/. */
  music?: string;
};
