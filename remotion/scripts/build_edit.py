"""Build the Remotion edit decision list from the Whisper transcript.

All times written below are on the talking-head (camera) timeline, in seconds.
"""
import json
import re
import numpy as np
import scipy.io.wavfile as wf

FPS = 30
SCREEN_OFFSET = 12.2  # screenTime = headTime - SCREEN_OFFSET
OUT = "/home/user/ZakEdwardsCode/remotion/src/plasmo/edit.json"

words = json.load(open("/home/user/work/proxy/words.json"))
for i, w in enumerate(words):
    w["i"] = i
    w["w"] = w["w"].strip()

# ---------- tighten word boundaries with the audio envelope ----------
sr, audio = wf.read("/home/user/work/proxy/head16k.wav")
audio = audio.astype(np.float32) / 32768
hop = sr // 100  # 10 ms
rms = np.sqrt(np.convolve(audio**2, np.ones(hop) / hop, mode="same")[::hop])
db = 20 * np.log10(rms + 1e-7)
speech_floor = np.percentile(db, 30) + 0.45 * (np.percentile(db, 97) - np.percentile(db, 30))


def voiced(a, b):
    fa, fb = int(a * 100), int(b * 100)
    idx = np.where(db[fa:fb] > speech_floor)[0]
    if len(idx) == 0:
        return None
    return (fa + idx[0]) / 100, (fa + idx[-1]) / 100


for w in words:
    w["se"], w["ee"] = w["s"], w["e"]
    if w["e"] - w["s"] > 0.6:
        v = voiced(w["s"], w["e"])
        if v:
            w["se"] = max(w["s"], v[0] - 0.06)
            w["ee"] = min(w["e"], v[1] + 0.1)

# ---------- the edit: spans (with layout switches), drops, fast-forwards ----------
# (start, end) of material to keep.
SPANS = [
    (26.2, 32.6), (35.4, 139.3), (140.0, 144.85), (204.6, 222.5), (229.0, 306.97), (364.4, 396.7),
    (427.8, 434.4), (437.9, 439.3), (488.4, 498.4), (503.0, 504.5),
    (600.1, 621.2), (622.2, 718.3), (719.1, 752.1), (753.1, 758.7), (770.3, 776.95),
    (871.6, 967.7), (972.0, 982.6), (994.5, 996.5), (998.4, 999.2),
]
# Fumbles, repeats and first takes to remove inside the spans (keep the last take).
DROPS = [
    (50.5, 53.62),    # "you do the" (repeat)
    (117.45, 117.89), # "it's" restart -> "utilizing it, it could be"
    (55.3, 56.9),     # "about you"
    (95.8, 98.87),    # "instead of," (first take)
    (299.8, 304.05),  # "and the reason why this is better." (abandoned)
    (371.6, 374.5),   # "or just have slightly different, I say slightly different,"
    (600.9, 601.19),  # "I've just," (first take)
    (601.85, 602.29), # "a, you know,"
    (603.2, 609.4),   # "um, as you can see,"
    (610.85, 611.62), # "very, uh," (first take)
    (612.45, 613.4),  # "but, um,"
    (617.5, 618.49),  # "maybe two or three,"
    (705.7, 708.6),   # "because you're basically doing,"
    (719.25, 722.13), # "if I, you know," -> "So if I wanted to"
    (722.9, 723.15),  # "I could," (first take)
    (738.3, 744.4),   # first "this will give you clues" + "not working"
    (765.7, 768.81),  # "over the last couple of them or"
    (791.25, 793.45), # "or like for completely free"
    (794.45, 795.55), # "you will get"
    (797.65, 798.07), # "you'll" (first take)
    (798.7, 799.45),  # "you know"
    (818.1, 824.2),   # "you could literally, you could get to the top, if you,"
    (831.75, 833.0),  # "you don't need to be a pro version," (first take)
    (973.15, 974.13), # "you know"
    (230.75, 233.6),  # "I am getting the foundation on it very very soon" (roadmap promo)
    (259.65, 262.75), # "I am going to add more papers to it in the future and" (roadmap promo)
    (977.9, 981.05),  # "PPP or triple P method"
]
# Silent stretches where the screen still shows something worth seeing -> fast-forward.
FASTFORWARD = [(312.8, 364.2, 12), (440.4, 488.3, 12), (504.6, 599.9, 20)]

# Layout schedule: (headTime, layout). "pip" = screen recording + head in the corner.
LAYOUT = [
    (0, "full"), (137.5, "pip"), (266.4, "full"), (304.0, "pip"), (600.0, "full"),
    (622.2, "pip"), (701.3, "full"), (719.0, "pip"), (780.3, "full"), (810.3, "pip"),
    (922.4, "full"),
]


def layout_at(t):
    cur = "full"
    for at, l in LAYOUT:
        if t >= at - 1e-6:
            cur = l
    return cur


def dropped(w):
    mid = (w["s"] + w["e"]) / 2
    return any(a <= mid <= b for a, b in DROPS)


kept = [w for w in words if any(a <= (w["s"] + w["e"]) / 2 <= b for a, b in SPANS) and not dropped(w)]


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w["w"].lower())


# Fillers: "um", "uh", and a comma-ended "you know," that's just a verbal tic.
FILLERS = {"um", "uh", "uhm", "erm", "er"}
fill = set()
for k, w in enumerate(kept):
    if norm(w) in FILLERS:
        fill.add(w["i"])
    if k > 0 and norm(kept[k - 1]) == "you" and w["w"].lower().startswith("know,") and kept[k - 1]["i"] == w["i"] - 1:
        fill.update({kept[k - 1]["i"], w["i"]})
kept = [w for w in kept if w["i"] not in fill]

# Stutters / restarts: when a 1-3 word phrase is said twice in a row, keep the last take.
KEEP_DOUBLES = {"very", "really", "dot", "paper", "no"}
changed = True
while changed:
    changed = False
    toks = [norm(w) for w in kept]
    for n in (3, 2, 1):
        for k in range(len(kept) - 2 * n + 1):
            a, b = toks[k:k + n], toks[k + n:k + 2 * n]
            contiguous = all(kept[k + j + 1]["i"] == kept[k + j]["i"] + 1 for j in range(2 * n - 1))
            if a == b and contiguous and not (n == 1 and a[0] in KEEP_DOUBLES):
                del kept[k:k + n]
                changed = True
                break
        if changed:
            break

GAP = 0.25
PAD_IN, PAD_OUT = 0.05, 0.09


def neighbour_bounds(w_first, w_last):
    """Never let padding reach into a word we are not keeping."""
    i0, i1 = w_first["i"], w_last["i"]
    lo = words[i0 - 1]["ee"] + 0.02 if i0 > 0 else 0
    hi = words[i1 + 1]["se"] - 0.02 if i1 + 1 < len(words) else 1e9
    return lo, hi


# Group kept words into clips: break on gaps, removed words, or layout changes.
groups = []
for w in kept:
    if groups:
        g = groups[-1]
        prev = g[-1]
        contiguous = w["i"] == prev["i"] + 1
        if contiguous and w["se"] - prev["ee"] <= GAP and layout_at(w["se"]) == layout_at(prev["se"]):
            g.append(w)
            continue
    groups.append([w])

clips = []
for gi, g in enumerate(groups):
    lo, hi = neighbour_bounds(g[0], g[-1])
    a = max(g[0]["se"] - PAD_IN, lo)
    b = min(g[-1]["ee"] + PAD_OUT, hi)
    # Seamless split where only the layout changed between two adjacent words.
    if gi > 0:
        p = groups[gi - 1][-1]
        if p["i"] + 1 == g[0]["i"] and g[0]["se"] - p["ee"] <= GAP:
            a = (p["ee"] + g[0]["se"]) / 2
    if gi + 1 < len(groups):
        n = groups[gi + 1][0]
        if g[-1]["i"] + 1 == n["i"] and n["se"] - g[-1]["ee"] <= GAP:
            b = (g[-1]["ee"] + n["se"]) / 2
    clips.append({"in": round(a, 3), "out": round(b, 3), "layout": layout_at(g[0]["se"]), "rate": 1, "words": g})

for a, b, r in FASTFORWARD:
    clips.append({"in": a, "out": b, "layout": "pip", "rate": r, "words": []})
clips.sort(key=lambda c: c["in"])

# Snap to frames and lay out on the output timeline.
t = 0.0
for c in clips:
    c["in"] = round(c["in"] * FPS) / FPS
    c["out"] = round(c["out"] * FPS) / FPS
    c["at"] = round(t, 4)
    t += (c["out"] - c["in"]) / c["rate"]
DURATION = round(t + 0.5, 3)


def to_out(h):
    """Map a head-time to the output timeline (nearest kept moment)."""
    best = None
    for c in clips:
        if c["in"] <= h <= c["out"]:
            return c["at"] + (h - c["in"]) / c["rate"]
        d = min(abs(h - c["in"]), abs(h - c["out"]))
        if best is None or d < best[0]:
            best = (d, c["at"] if h < c["in"] else c["at"] + (c["out"] - c["in"]) / c["rate"])
    return best[1]


FIX = {
    "zach": "Zak", "plasma": "Plasmo", "plasmo": "Plasmo", "pacific": "specific", "osea": "OCR",
    "ocrg": "OCR", "csc": "GCSE", "shic": "it", "guitarist": "Tyrese", "pp": "PP",
}


def fix(w):
    core = w.strip(".,?!")
    rep = FIX.get(core.lower())
    return w.replace(core, rep) if rep else w


out_words = []
for c in clips:
    for w in c["words"]:
        s = c["at"] + (max(w["se"], c["in"]) - c["in"])
        e = c["at"] + (min(w["ee"], c["out"]) - c["in"])
        if w["w"].startswith("-") and out_words:  # Whisper splits "A -level"
            out_words[-1]["w"] += w["w"]
            out_words[-1]["e"] = round(e, 3)
            continue
        out_words.append({"w": fix(w["w"]), "s": round(s, 3), "e": round(e, 3)})

# ---------- face tracking ----------
faces = json.load(open("/home/user/work/proxy/faces.json"))
FACE_HZ = 4


def face_at(h):
    """Face box (x0, y0, x1, y1) in 1920x1080 at head-time h, nearest detected sample."""
    i = int(round(h * FACE_HZ))
    for d in range(0, 12):
        for j in (i - d, i + d):
            if 0 <= j < len(faces) and "x" in faces[j]:
                f = faces[j]
                return (f["x"], f["y"], f["x"] + f["w"], f["y"] + f["h"])
    return (540, 50, 1200, 650)


def out_to_head(t):
    for c in clips:
        d = (c["out"] - c["in"]) / c["rate"]
        if c["at"] <= t < c["at"] + d:
            return c["in"] + (t - c["at"]) * c["rate"], c["layout"]
    return None, None


def face_union(t, d):
    """Union of face boxes on screen (full-screen layout only) during output [t, t+d]."""
    box = None
    k = t
    while k <= t + d:
        h, lay = out_to_head(k)
        if h is not None and lay == "full":
            b = face_at(h)
            box = b if box is None else (min(box[0], b[0]), min(box[1], b[1]), max(box[2], b[2]), max(box[3], b[3]))
        k += 0.25
    return box


MARGIN = 50


def place(t, d, width, height, top):
    """Pick a spot for a card in full-screen layout that never touches the face."""
    box = face_union(t, d)
    if box is None:
        return {"x": 1920 - 60 - width, "y": top, "w": width}
    fx0, fx1 = box[0] - MARGIN, box[2] + MARGIN
    right_x = 1920 - 60 - width
    if right_x >= fx1:
        return {"x": right_x, "y": top, "w": width}
    if 60 + width <= fx0:
        return {"x": 60, "y": top, "w": width}
    # Not enough room at full width: shrink the card into whichever side is wider.
    right_room, left_room = 1920 - 60 - fx1, fx0 - 60
    if right_room >= left_room:
        w = int(max(420, right_room))
        return {"x": 1920 - 60 - w, "y": top, "w": w}
    w = int(max(420, left_room))
    return {"x": 60, "y": top, "w": w}


# ---------- graphics ----------
CALLOUTS = [  # (headTime, seconds, icon, title, sub) - lead with the pain
    (44.1, 3.2, "Printer", "Print the stack", "trees, ink, hours"),
    (57.0, 3.0, "CalendarClock", "Hand it in next week", "the feedback clock starts"),
    (62.4, 3.6, "BrainCircuit", "Already forgotten", "what you wrote, how it felt"),
    (79.6, 3.2, "Hourglass", "Weeks to mark", "by then it's too late"),
    (81.3, 3.6, "Frown", "Guilt on both sides", "teachers marking after hours"),
    (110.4, 4.0, "Brain", "Feedback is how you learn", "and paper delays it"),
    (123.0, 3.6, "TrendingUp", "Fast feedback compounds", "slow feedback doesn't"),
    (270.0, 4.0, "Scale", "Exam-style papers", "no copyright issues"),
    (296.5, 3.0, "Target", "Topic-specific", "every question maps to a topic"),
    (633.2, 3.6, "Zap", "Feedback in seconds", "not weeks"),
    (661.2, 3.6, "ClipboardCheck", "See where marks come from", "the mark scheme, per answer"),
    (676.0, 3.6, "MessageCircleQuestion", "Disagree? Appeal it", "the AI rechecks"),
    (736.6, 3.2, "LifeBuoy", "Stuck? Get a clue", "not the answer"),
    (877.8, 3.6, "Target", "Know your weak topics", "before the mocks"),
    (926.2, 3.6, "MessageSquareText", "What do students need?", "tell me in the comments"),
    (952.0, 3.0, "TriangleAlert", "Paper is outdated", "here's why"),
    (955.4, 2.4, "FileX", "So much paper", ""),
    (959.2, 1.8, "Timer", "Takes so long", ""),
    (960.2, 2.6, "Ban", "No active feedback", ""),
    (964.5, 2.6, "ChartColumn", "No stats", "you can't see your gaps"),
]
CHAPTERS = [  # (headTime, seconds, kicker, title)
    (26.2, 3.6, "The new, smarter way", "PAST PAPERS\nARE OUTDATED"),
    (41.4, 2.6, "Here's what happens", "THE PROBLEM"),
    (137.5, 3.0, "So I built", "PLASMO"),
    (622.2, 3.0, "Instant feedback", "HIT MARK"),
    (994.5, 4.0, "Thanks for watching", "ZAK EDWARDS"),
]

callouts = []
for h, d, i, ti, su in CALLOUTS:
    t = round(to_out(h), 3)
    lay = out_to_head(t + 0.1)[1]
    c = {"t": t, "d": d, "icon": i, "title": ti, "sub": su, "layout": lay}
    if lay == "full":
        c.update(place(t, d, 600, 230, 140))
    callouts.append(c)

# Never stack two callouts: each one ends just before the next begins.
callouts.sort(key=lambda c: c["t"])
for a, b in zip(callouts, callouts[1:]):
    if a["t"] + a["d"] > b["t"] - 0.1:
        a["d"] = round(max(1.0, b["t"] - 0.1 - a["t"]), 3)

chapters = []
for h, d, k, ti in CHAPTERS:
    t = round(to_out(h), 3)
    lay = out_to_head(t + 0.6)[1]
    if lay == "pip":
        t += 0.6  # let the head finish shrinking into the corner first
    c = {"t": round(t, 3), "d": d, "kicker": k, "title": ti, "layout": lay}
    if lay == "full":
        c.update(place(t, d, 640, 300, 120))
    chapters.append(c)

# ---------- sound design ----------
sfx = []
for i, c in enumerate(clips):
    if i > 0 and c["layout"] != clips[i - 1]["layout"]:
        sfx.append({"t": c["at"] - 0.12, "name": "whoosh", "vol": 0.32})
    if c["rate"] > 1:
        sfx.append({"t": c["at"], "name": "riser", "vol": 0.22})
        sfx.append({"t": c["at"] + (c["out"] - c["in"]) / c["rate"] - 0.1, "name": "swoosh", "vol": 0.3})
for co in callouts:
    sfx.append({"t": co["t"], "name": "pop", "vol": 0.4})
for ch in chapters[1:]:
    sfx.append({"t": ch["t"], "name": "swoosh", "vol": 0.35})
sfx.append({"t": 0.0, "name": "impact", "vol": 0.45})
sfx.append({"t": to_out(633.2), "name": "chime", "vol": 0.4})
sfx.append({"t": to_out(952.1), "name": "impact", "vol": 0.35})
sfx.append({"t": to_out(994.6), "name": "ding", "vol": 0.35})

# Mouse-click sounds where the page changes on screen (only while the screen is visible at 1x).
scenes = [float(x) for x in open("/home/user/work/frames/scenes.txt").read().split()]
last = -9
for st in scenes:
    h = st + SCREEN_OFFSET
    c = next((c for c in clips if c["in"] <= h <= c["out"]), None)
    if c and c["layout"] == "pip" and c["rate"] == 1:
        o = c["at"] + (h - c["in"]) - 0.05
        if o - last > 1.5:
            sfx.append({"t": round(o, 3), "name": "click", "vol": 0.3})
            last = o
sfx.sort(key=lambda s: s["t"])
for s in sfx:
    s["t"] = round(max(0, s["t"]), 3)

# Smoothed face centre (x) for framing the corner window.
raw = np.array([f["x"] + f["w"] / 2 if "x" in f else np.nan for f in faces], float)
idx = np.arange(len(raw))
ok = ~np.isnan(raw)
raw = np.interp(idx, idx[ok], raw[ok])
kern = np.ones(9) / 9
face_cx = [int(v) for v in np.convolve(np.pad(raw, 4, mode="edge"), kern, mode="valid")]

# Merged speech intervals on the output timeline (music ducks under these).
speech = []
for w in out_words:
    if speech and w["s"] - speech[-1][1] < 0.8:
        speech[-1][1] = w["e"]
    else:
        speech.append([w["s"], w["e"]])
speech = [[round(a, 2), round(b, 2)] for a, b in speech]

edit = {
    "fps": FPS,
    "duration": DURATION,
    "screenOffset": SCREEN_OFFSET,
    "clips": [{k: c[k] for k in ("in", "out", "at", "layout", "rate")} for c in clips],
    "words": out_words,
    "sfx": sfx,
    "callouts": callouts,
    "chapters": chapters,
    "faceHz": FACE_HZ,
    "faceCx": face_cx,
    "speech": speech,
}
json.dump(edit, open(OUT, "w"), indent=1)
print(f"clips={len(clips)} words={len(out_words)} sfx={len(sfx)} duration={DURATION:.1f}s ({DURATION/60:.1f} min)")
print(" ".join(w["w"] for w in out_words))
