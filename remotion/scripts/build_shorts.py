"""Build three vertical Shorts (1080x1920) from the long-form footage.

Times are on the talking-head (camera) timeline in seconds. Each span says what fills the
top panel: an animated graphic ("gfx") or a crop of the synced screen recording ("screen").
"""
import json
import re
import numpy as np
import scipy.io.wavfile as wf

FPS = 30
SCREEN_OFFSET = 12.2
OUT = "/home/user/ZakEdwardsCode/remotion/src/plasmo/shorts.json"

words = json.load(open("/home/user/work/proxy/words.json"))
for i, w in enumerate(words):
    w["i"], w["w"] = i, w["w"].strip()

sr, audio = wf.read("/home/user/work/proxy/head16k.wav")
audio = audio.astype(np.float32) / 32768
hop = sr // 100
rms = np.sqrt(np.convolve(audio**2, np.ones(hop) / hop, mode="same")[::hop])
db = 20 * np.log10(rms + 1e-7)
floor = np.percentile(db, 30) + 0.45 * (np.percentile(db, 97) - np.percentile(db, 30))
for w in words:
    w["se"], w["ee"] = w["s"], w["e"]
    if w["e"] - w["s"] > 0.6:
        fa, fb = int(w["s"] * 100), int(w["e"] * 100)
        idx = np.where(db[fa:fb] > floor)[0]
        if len(idx):
            w["se"] = max(w["s"], (fa + idx[0]) / 100 - 0.06)
            w["ee"] = min(w["e"], (fa + idx[-1]) / 100 + 0.1)

# Forced-alignment times (align.py): exact word positions for cuts and captions.
# Which words are kept is still decided on Whisper's times above, so the edit choices don't shift.
_aligned = json.load(open("/home/user/work/proxy/words_aligned.json"))
for w, al in zip(words, _aligned):
    w["se"], w["ee"] = al["s"], al["e"]

faces = json.load(open("/home/user/work/proxy/faces.json"))


def face_cx(h):
    i = int(round(h * 4))
    for d in range(12):
        for j in (i - d, i + d):
            if 0 <= j < len(faces) and "x" in faces[j]:
                return faces[j]["x"] + faces[j]["w"] / 2
    return 900


FIX = {"plasma": "Plasmo", "plasmo": "Plasmo", "pp": "PP"}

# Screen crops (in screen-recording pixels, 1920x876) sized to the 1080x840 top panel.
CARD = {"x": 500, "y": 170, "w": 908, "h": 706}       # question, answer and feedback card
DASH = {"x": 380, "y": 0, "w": 1126, "h": 876}         # weak-topics dashboard

SHORTS = [
    {
        "id": "ShortWeeksToMark",
        "hook": ["YOUR TEACHER TAKES", "WEEKS TO MARK THIS"],
        "spans": [
            (42.6, 45.5, {"kind": "gfx", "icon": "Printer", "title": "Print the stack", "paper": True}),
            (57.0, 59.1, {"kind": "gfx", "icon": "CalendarClock", "title": "Hand it in next week"}),
            (60.35, 65.4, {"kind": "gfx", "icon": "BrainCircuit", "title": "Already forgotten"}),
            (67.85, 70.3, {"kind": "gfx", "icon": "Frown", "title": "How did it even go?"}),
            (77.2, 80.75, {"kind": "gfx", "icon": "Hourglass", "title": "Weeks to mark", "cross": True}),
            (80.75, 84.0, {"kind": "gfx", "icon": "Frown", "title": "Guilt on both sides"}),
            (135.25, 137.55, {"kind": "gfx", "icon": "Sparkles", "title": "So I built Plasmo", "accent": True}),
            (623.2, 624.6, {"kind": "screen", "crop": CARD}),
            (632.8, 633.8, {"kind": "screen", "crop": CARD}),
        ],
        "drops": [],
        "cta": "Get your past papers marked in seconds",
    },
    {
        "id": "ShortMarkedIn10s",
        "hook": ["AI MARKED MY EXAM", "ANSWER IN 10 SECONDS"],
        "spans": [
            (622.25, 624.6, {"kind": "screen", "crop": CARD}),
            (625.1, 627.75, {"kind": "screen", "crop": CARD}),
            (630.2, 632.3, {"kind": "screen", "crop": CARD}),
            (632.8, 633.8, {"kind": "screen", "crop": CARD}),
            (638.65, 646.9, {"kind": "screen", "crop": CARD}),
            (654.55, 660.1, {"kind": "screen", "crop": CARD}),
        ],
        "drops": [],
        "cta": "Try it free on real GCSE & A-level papers",
    },
    {
        "id": "ShortPaperIsOutdated",
        "hook": ["PAST PAPERS ON", "PAPER ARE OUTDATED"],
        "spans": [
            (949.3, 952.7, {"kind": "gfx", "icon": "TriangleAlert", "title": "Outdated", "paper": True, "cross": True}),
            (953.35, 954.43, {"kind": "gfx", "icon": "Frown", "title": "I hated it"}),
            (955.25, 958.2, {"kind": "gfx", "icon": "FileX", "title": "So much paper", "paper": True}),
            (958.95, 960.0, {"kind": "gfx", "icon": "Timer", "title": "Takes so long"}),
            (960.05, 962.3, {"kind": "gfx", "icon": "Ban", "title": "No active feedback"}),
            (964.45, 965.95, {"kind": "gfx", "icon": "ChartColumn", "title": "No stats"}),
            (877.8, 886.7, {"kind": "screen", "crop": DASH}),
        ],
        "drops": [],
        "cta": "Find your weak topics before the mocks",
    },
]

import sys
sys.path.insert(0, "/home/user/work/scripts")
from audiocut import SpeechMap

SM = SpeechMap("/home/user/work/proxy/head16k.wav")


def build(spec):
    clips, out_words, t = [], [], 0.0
    for a, b, top in spec["spans"]:
        ws = [w for w in words if a <= (w["s"] + w["e"]) / 2 <= b
              and not any(x <= (w["s"] + w["e"]) / 2 <= y for x, y in spec["drops"])
              and not re.fullmatch(r"(um|uh|erm)[,.]?", w["w"].lower())]
        if not ws:
            continue
        i0, i1 = ws[0]["i"], ws[-1]["i"]
        p = words[i0 - 1] if i0 > 0 else None
        n = words[i1 + 1] if i1 + 1 < len(words) else None
        lo = min(ws[0]["se"] - 0.05, max((p["se"] + p["ee"]) / 2, p["ee"] - 0.25)) if p else 0.0
        hi = max(ws[-1]["ee"] + 0.05, min((n["se"] + n["ee"]) / 2, n["se"] + 0.25)) if n else 1e9
        # Cut where the voice actually starts and stops, and squeeze out pauses inside the span.
        cin0, cout0 = SM.snap_in(ws[0]["se"], lo), SM.snap_out(ws[-1]["ee"], hi)
        for x, y in SM.trim_silences(cin0, cout0):
            cin, cout = round(x * FPS) / FPS, round(y * FPS) / FPS
            g = [w for w in ws if x - 0.05 <= (w["se"] + w["ee"]) / 2 <= y + 0.05]
            clips.append({"in": cin, "out": cout, "at": round(t, 4), "top": top,
                          "faceCx": round(face_cx((cin + cout) / 2))})
            for w in g:
                s = t + max(w["se"], cin) - cin
                e = t + min(w["ee"], cout) - cin
                core = w["w"].strip(".,?!")
                rep = FIX.get(core.lower())
                out_words.append({"w": w["w"].replace(core, rep) if rep else w["w"],
                                  "s": round(s, 3), "e": round(e, 3)})
            t += cout - cin
    talk = t
    cta_len = 3.0
    duration = round(talk + cta_len, 3)
    # sound design
    sfx = [{"t": 0.0, "name": "impact", "vol": 0.4}]
    for k, c in enumerate(clips):
        if k > 0 and c["top"] != clips[k - 1]["top"]:
            sfx.append({"t": c["at"], "name": "whoosh" if c["top"]["kind"] != clips[k - 1]["top"]["kind"] else "pop",
                        "vol": 0.3})
    for w in out_words:
        if w["w"].lower().startswith("boom"):
            sfx.append({"t": w["s"], "name": "chime", "vol": 0.45})
    sfx.append({"t": talk, "name": "riser", "vol": 0.25})
    sfx.append({"t": talk + 0.35, "name": "ding", "vol": 0.4})
    return {"id": spec["id"], "fps": FPS, "duration": duration, "talk": round(talk, 3),
            "screenOffset": SCREEN_OFFSET, "hook": spec["hook"], "cta": spec["cta"],
            "clips": clips, "words": out_words, "sfx": sfx}


shorts = [build(s) for s in SHORTS]
json.dump(shorts, open(OUT, "w"), indent=1)
for s in shorts:
    print(f"{s['id']}: {s['duration']:.1f}s ({len(s['clips'])} clips)  |  " + " ".join(w["w"] for w in s["words"]))
