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

export type Callout = {
  t: number;
  d: number;
  icon: string;
  title: string;
  sub?: string;
};

export type Chapter = { t: number; d: number; kicker: string; title: string };

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
};
