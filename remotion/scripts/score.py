"""Score each video to its story: TENSION under the problem, LIFT once Plasmo appears.

Both moods share key (A minor / C major) and tempo (104 BPM), so a switch lands on a
downbeat exactly at the story beat. Reads edit.json / shorts.json, writes one WAV per video
into public/music/ and records its path in the JSON ("music").
"""
import json
import numpy as np
import scipy.io.wavfile as wf
import scipy.signal as ss

SR = 48000
BPM = 104
BEAT = 60 / BPM
BAR = 4 * BEAT
REMOTION = "/home/user/ZakEdwardsCode/remotion"
rng = np.random.default_rng(3)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(d):
    return np.arange(int(SR * d)) / SR


def place(buf, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= buf.shape[0] or i < 0:
        return
    sig = sig[: buf.shape[0] - i] * gain
    buf[i:i + len(sig), 0] += sig * np.sqrt(0.5 * (1 - pan))
    buf[i:i + len(sig), 1] += sig * np.sqrt(0.5 * (1 + pan))


# ---------- instruments ----------
def pluck(m, d=0.5):
    t = tt(d)
    f = hz(m)
    x = sum((1 / k) * np.sin(2 * np.pi * k * f * t) * np.exp(-t * (5 + 2.2 * k)) for k in range(1, 12))
    return (x * np.minimum(1, t / 0.003)).astype(np.float32)


def pad(notes, d, bright=1800):
    t = tt(d)
    x = np.zeros_like(t)
    for m in notes:
        for det in (-0.07, 0, 0.07):
            x += ss.sawtooth(2 * np.pi * hz(m + det) * t)
    x = ss.sosfilt(ss.butter(2, bright, fs=SR, output="sos"), x / (3 * len(notes)))
    env = np.minimum(1, t / 0.25) * np.minimum(1, (d - t) / 0.3)
    return (x * env).astype(np.float32)


def sub(m, d):
    t = tt(d)
    x = np.sin(2 * np.pi * hz(m) * t) + 0.18 * np.sin(4 * np.pi * hz(m) * t)
    return (x * np.minimum(1, t / 0.006) * np.minimum(1, (d - t) / 0.03)).astype(np.float32)


def kick():
    t = tt(0.4)
    f = 150 * np.exp(-t * 28) + 46
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7.5)).astype(np.float32)


def clap():
    t = tt(0.25)
    nz = ss.sosfilt(ss.butter(2, [1000, 4200], btype="band", fs=SR, output="sos"), rng.standard_normal(len(t)))
    env = np.zeros_like(t)
    for o in (0, 0.011, 0.022):
        env += (t >= o) * np.exp(-(t - o).clip(0) * 60)
    env += (t >= 0.03) * np.exp(-(t - 0.03).clip(0) * 14) * 0.6
    return (nz * env).astype(np.float32)


def hat(d=0.05, decay=80):
    t = tt(d)
    nz = ss.sosfilt(ss.butter(2, 8000, btype="high", fs=SR, output="sos"), rng.standard_normal(len(t)))
    return (nz * np.exp(-t * decay)).astype(np.float32)


def tick():
    t = tt(0.03)
    nz = ss.sosfilt(ss.butter(2, [3000, 9000], btype="band", fs=SR, output="sos"), rng.standard_normal(len(t)))
    return (nz * np.exp(-t * 300)).astype(np.float32)


K, CL, HC, HO, TK = kick(), clap(), hat(), hat(0.22, 16), tick()

TENSION = [(57, [57, 60, 64]), (53, [53, 57, 60]), (50, [50, 53, 57]), (52, [52, 56, 59])]   # Am F Dm E
LIFT = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [57, 60, 64]), (41, [57, 60, 65])]      # C G Am F


def render(mood, seconds, lite=False):
    """Render `seconds` of a mood starting on bar 1."""
    n = int(SR * (seconds + 2))
    buf = np.zeros((n, 2), np.float32)
    bars = int(np.ceil(seconds / BAR)) + 1
    pump = np.ones(n, np.float32)
    for b in range(bars):
        t0 = b * BAR
        if mood == "tension":
            root, ch = TENSION[b % 4]
            place(buf, pad(ch, BAR, bright=900), t0, 0.16)
            for k in range(8):  # pulsing low bass on 8ths, accent on the beat
                place(buf, sub(root - 24, BEAT / 2 * 0.9), t0 + k * BEAT / 2, 0.30 if k % 2 == 0 else 0.18)
            for k in range(16):  # ticking clock
                place(buf, TK, t0 + k * BEAT / 4, 0.10 if k % 4 == 0 else 0.045, pan=0.4 if k % 2 else -0.4)
        else:
            root, ch = LIFT[b % 4]
            place(buf, pad(ch, BAR, bright=2600), t0, 0.12)
            arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
            for k in range(16):
                place(buf, pluck(arp[k % 4] + (12 if k % 8 == 6 else 0), 0.35), t0 + k * BEAT / 4,
                      0.11 if k % 2 == 0 else 0.07, pan=-0.25 if k % 2 else 0.25)
            if not lite:
                for k in range(4):
                    place(buf, sub(root - 12, BEAT * 0.85), t0 + k * BEAT, 0.34)
                    place(buf, K, t0 + k * BEAT, 0.55 if k % 2 == 0 else 0.42)
                    i = int((t0 + k * BEAT) * SR)  # sidechain pump on every beat
                    L = int(BEAT * SR)
                    if i < n:
                        seg = np.linspace(0.35, 1.0, min(L, n - i)) ** 0.6
                        pump[i:i + len(seg)] = np.minimum(pump[i:i + len(seg)], seg)
                place(buf, CL, t0 + BEAT, 0.30)
                place(buf, CL, t0 + 3 * BEAT, 0.30)
                for k in range(4):
                    place(buf, HO if k % 2 else HC, t0 + k * BEAT + BEAT / 2, 0.09)
                    place(buf, HC, t0 + k * BEAT, 0.05)
    buf *= pump[:, None] if mood == "lift" and not lite else 1
    return buf[: int(SR * seconds)]


def assemble(sections, total):
    """sections: [(start, mood)] in output seconds. Each section starts on its own bar 1."""
    out = np.zeros((int(SR * total) + SR, 2), np.float32)
    for k, (start, mood) in enumerate(sections):
        end = sections[k + 1][0] if k + 1 < len(sections) else total + 0.5
        seg = render(mood.replace("-lite", ""), end - start + 0.08, lite=mood.endswith("-lite"))
        i = int(start * SR)
        fade = int(0.04 * SR)
        seg[:fade] *= np.linspace(0, 1, fade)[:, None]
        seg[-fade:] *= np.linspace(1, 0, fade)[:, None]
        out[i:i + len(seg)] += seg[: len(out) - i]
        # a one-bar riser into every switch to the lift
        if mood.startswith("lift") and start > BAR:
            t = tt(BAR / 2)
            nz = ss.sosfilt(ss.butter(2, [3000, 9000], btype="band", fs=SR, output="sos"), rng.standard_normal(len(t)))
            r = (nz * (t / (BAR / 2)) ** 3 * 0.03).astype(np.float32)
            j = int((start - BAR / 2) * SR)
            out[j:j + len(r), 0] += r
            out[j:j + len(r), 1] += r
    out = out[: int(SR * total)]
    n = len(out)
    out[: int(0.5 * SR)] *= np.linspace(0, 1, int(0.5 * SR))[:, None]
    out[n - int(1.5 * SR):] *= np.linspace(1, 0, int(1.5 * SR))[:, None]
    out = np.tanh(out * 1.6) / 1.6
    out /= np.max(np.abs(out)) + 1e-9
    return (out * 0.89 * 32767).astype(np.int16)


def write(name, sections, total):
    path = f"{REMOTION}/public/music/{name}.wav"
    wf.write(path, SR, assemble(sections, total))
    return f"music/{name}.wav"


# ---------- long form ----------
e = json.load(open(f"{REMOTION}/src/plasmo/edit.json"))
ch = {c["title"].replace("\n", " "): c["t"] for c in e["chapters"]}
co = {c["title"]: c["t"] for c in e["callouts"]}
long_sections = [(0.0, "tension"), (ch["PLASMO"] - 0.6, "lift"), (co["Paper is outdated"], "tension"),
                 (ch["ZAK EDWARDS"], "lift")]
e["music"] = write("score_long", long_sections, e["duration"])
json.dump(e, open(f"{REMOTION}/src/plasmo/edit.json", "w"), indent=1)
print("long-form:", [(round(t, 1), m) for t, m in long_sections])

# ---------- shorts ----------
S = json.load(open(f"{REMOTION}/src/plasmo/shorts.json"))
for s in S:
    total = s["talk"] + 3.2
    if s["id"] == "ShortWeeksToMark":
        drop = next(c["at"] for c in s["clips"] if c["top"].get("title") == "So I built Plasmo")
        secs = [(0.0, "tension"), (drop, "lift")]
    elif s["id"] == "ShortMarkedIn10s":
        boom = next(w["s"] for w in s["words"] if w["w"].lower().startswith("boom"))
        secs = [(0.0, "lift-lite"), (boom, "lift")]
    else:
        drop = next(c["at"] for c in s["clips"] if c["top"]["kind"] == "screen")
        secs = [(0.0, "tension"), (drop, "lift")]
    s["music"] = write(f"score_{s['id']}", secs, total)
    print(s["id"], [(round(t, 1), m) for t, m in secs])
json.dump(S, open(f"{REMOTION}/src/plasmo/shorts.json", "w"), indent=1)
