"""Generate an original lo-fi background track (no licensing issues).

usage: lofi.py OUT.wav SECONDS
"""
import sys
import numpy as np
import scipy.io.wavfile as wf
import scipy.signal as ss

SR = 48000
OUT, LENGTH = sys.argv[1], float(sys.argv[2])
rng = np.random.default_rng(11)
BPM = 84
BEAT = 60 / BPM
BAR = 4 * BEAT
N = int(SR * (LENGTH + 4))
L = np.zeros(N, np.float32)
R = np.zeros(N, np.float32)


def hz(m):
    return 440 * 2 ** ((m - 69) / 12)


def add(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    L[i : i + len(sig)] += sig * np.sqrt(0.5 * (1 - pan))
    R[i : i + len(sig)] += sig * np.sqrt(0.5 * (1 + pan))


_cache = {}


def epiano(m, dur):
    key = (m, round(dur, 2))
    if key in _cache:
        return _cache[key]
    t = np.arange(int(SR * (dur + 1.2))) / SR
    f = hz(m)
    x = sum(a * np.sin(2 * np.pi * f * k * t + p) * np.exp(-t * d)
            for k, a, d, p in [(1, 1, 1.6, 0), (2, 0.35, 3.0, 0.3), (3, 0.12, 5, 0.1), (4, 0.06, 7, 0.5)])
    x += 0.15 * np.sin(2 * np.pi * f * 1.003 * t)  * np.exp(-t * 1.8)  # detune shimmer
    x *= 1 + 0.18 * np.sin(2 * np.pi * 4.2 * t)  # tremolo
    env = np.minimum(1, t / 0.012)
    rel = np.clip((dur + 1.2 - t) / 1.2, 0, 1)
    x = (x * env * rel).astype(np.float32)
    _cache[key] = x
    return x


def bass(m, dur):
    t = np.arange(int(SR * dur)) / SR
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t)
    env = np.minimum(1, t / 0.01) * np.exp(-t * 1.2) * np.clip((dur - t) / 0.08, 0, 1)
    return (x * env).astype(np.float32)


def kick():
    t = np.arange(int(SR * 0.45)) / SR
    f = 110 * np.exp(-t * 18) + 45
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)).astype(np.float32)


def snare():
    t = np.arange(int(SR * 0.3)) / SR
    nz = ss.sosfilt(ss.butter(2, [900, 5000], btype="band", fs=SR, output="sos"), rng.standard_normal(len(t)))
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 30)
    return ((0.7 * nz * np.exp(-t * 18) + 0.5 * tone)).astype(np.float32)


def hat(open_=False):
    t = np.arange(int(SR * (0.25 if open_ else 0.06))) / SR
    nz = ss.sosfilt(ss.butter(2, 7000, btype="high", fs=SR, output="sos"), rng.standard_normal(len(t)))
    return (nz * np.exp(-t * (14 if open_ else 70))).astype(np.float32)


def bell(m):
    t = np.arange(int(SR * 1.6)) / SR
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4)
    return (x * np.exp(-t * 2.2) * np.minimum(1, t / 0.005)).astype(np.float32)


K, S_ = kick(), snare()
# Fmaj7 - Em7 - Dm7 - Cmaj7 (+ a turnaround variant)
PROG = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
PROG_B = [[50, 53, 57, 60], [52, 55, 59, 62], [53, 57, 60, 64], [55, 59, 62, 65]]
ROOTS = {0: 41, 1: 40, 2: 38, 3: 36}
ROOTS_B = {0: 38, 1: 40, 2: 41, 3: 43}
SCALE = [60, 62, 64, 67, 69, 72, 74, 76]

bars = int(LENGTH / BAR) + 2
swing = 0.06 * BEAT
for b in range(bars):
    t0 = b * BAR
    section = (b // 8) % 6  # 0 intro, 1-2 groove, 3 melody, 4 breakdown, 5 groove+melody
    alt = section in (3, 5) and (b // 4) % 2 == 1
    chord = (PROG_B if alt else PROG)[b % 4]
    root = (ROOTS_B if alt else ROOTS)[b % 4]
    # chords: stab on 1, soft re-strike on the "and" of 3
    for i, m in enumerate(chord):
        add(epiano(m, BAR * 0.55), t0 + i * 0.012, pan=-0.25 + 0.17 * i, gain=0.11)
        add(epiano(m + 12 if i == 3 else m, BAR * 0.3), t0 + 2.5 * BEAT + swing + i * 0.01, pan=0.2 - 0.12 * i, gain=0.06)
    drums = section not in (0, 4)
    if section != 0:
        add(bass(root, BEAT * 1.4), t0, gain=0.32)
        add(bass(root, BEAT * 0.8), t0 + 1.5 * BEAT + swing, gain=0.24)
        add(bass(root + 7, BEAT * 0.9), t0 + 3 * BEAT, gain=0.22)
    if drums:
        add(K, t0, gain=0.55)
        add(K, t0 + 2.5 * BEAT + swing, gain=0.38)
        if b % 2 == 1:
            add(K, t0 + 3.5 * BEAT + swing, gain=0.25)
        add(S_, t0 + BEAT, gain=0.32)
        add(S_, t0 + 3 * BEAT, gain=0.32)
        for k in range(8):
            off = swing if k % 2 else 0
            add(hat(open_=(k == 7 and b % 4 == 3)), t0 + k * BEAT / 2 + off, pan=0.35,
                gain=0.10 if k % 2 == 0 else 0.065)
    if section in (3, 5):
        for k in range(8):
            if rng.random() < 0.38:
                add(bell(int(rng.choice(SCALE)) + 12), t0 + k * BEAT / 2 + (swing if k % 2 else 0),
                    pan=float(rng.uniform(-0.5, 0.5)), gain=0.05)

# vinyl crackle + hiss
crackle = np.zeros(N, np.float32)
pos = rng.integers(0, N, int(LENGTH * 9))
crackle[pos] = rng.uniform(-0.25, 0.25, len(pos))
crackle = ss.sosfilt(ss.butter(2, 2500, btype="high", fs=SR, output="sos"), crackle)
hiss = ss.sosfilt(ss.butter(2, [300, 4000], btype="band", fs=SR, output="sos"), rng.standard_normal(N)) * 0.004
L += crackle * 0.5 + hiss
R += crackle * 0.5 + hiss

# warm it up: low-pass, gentle saturation, fades
lp = ss.butter(2, 5500, fs=SR, output="sos")
L, R = ss.sosfilt(lp, L), ss.sosfilt(lp, R)
L, R = np.tanh(L * 1.4) / 1.4, np.tanh(R * 1.4) / 1.4
n = int(LENGTH * SR)
L, R = L[:n], R[:n]
fade_in, fade_out = int(2 * SR), int(4 * SR)
env = np.ones(n)
env[:fade_in] = np.linspace(0, 1, fade_in)
env[-fade_out:] = np.linspace(1, 0, fade_out)
st = np.stack([L * env, R * env], 1)
st /= np.max(np.abs(st)) + 1e-9
wf.write(OUT, SR, (st * 0.89 * 32767).astype(np.int16))
print(f"wrote {OUT}: {LENGTH:.1f}s, {bars} bars at {BPM} BPM")
