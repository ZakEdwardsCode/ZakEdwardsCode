"""Cut points from the audio itself, not from Whisper's word timings.

Whisper decides WHAT to keep. This module decides WHERE each cut lands: it maps when Zak is
actually speaking (WebRTC voice activity + loudness, 10 ms steps) and snaps every cut to the
real start/end of his voice, then trims silences inside a clip down to a short breath.
"""
import numpy as np
import scipy.io.wavfile as wf
import webrtcvad

HOP = 0.01  # 10 ms


class SpeechMap:
    def __init__(self, wav16k: str):
        sr, a = wf.read(wav16k)
        assert sr == 16000 and a.dtype == np.int16, "expects 16 kHz mono int16"
        n = len(a) // 160
        frames = a[: n * 160].reshape(n, 160)
        vad = webrtcvad.Vad(2)
        voiced = np.array([vad.is_speech(f.tobytes(), 16000) for f in frames])
        rms = np.sqrt(np.mean((frames.astype(np.float32) / 32768) ** 2, axis=1))
        db = 20 * np.log10(rms + 1e-7)
        # Smooth loudness over 30 ms so single clicks don't count.
        db = np.convolve(db, np.ones(3) / 3, mode="same")
        # Threshold from the speaker's own level: 15 dB under typical speech (90th percentile).
        # Room tone and pauses sit well below it; the VAD lets soft word endings through 4 dB lower.
        thr = np.percentile(db, 90) - 15
        self.noise = thr
        active = (db > thr) | (voiced & (db > thr - 4))
        active = self._close(active, int(0.12 / HOP))   # bridge tiny gaps between syllables
        active = self._open(active, int(0.06 / HOP))    # drop blips shorter than 60 ms
        self.active, self.db, self.n = active, db, n
        d = np.diff(active.astype(int))
        self.onsets = (np.where(d == 1)[0] + 1) * HOP
        self.offsets = (np.where(d == -1)[0] + 1) * HOP

    @staticmethod
    def _close(x, k):
        x = x.copy()
        i = 0
        while i < len(x):
            if not x[i]:
                j = i
                while j < len(x) and not x[j]:
                    j += 1
                if 0 < i and j < len(x) and j - i <= k:
                    x[i:j] = True
                i = j
            else:
                i += 1
        return x

    @staticmethod
    def _open(x, k):
        x = x.copy()
        i = 0
        while i < len(x):
            if x[i]:
                j = i
                while j < len(x) and x[j]:
                    j += 1
                if j - i < k:
                    x[i:j] = False
                i = j
            else:
                i += 1
        return x

    def is_active(self, t: float) -> bool:
        i = int(t / HOP)
        return 0 <= i < self.n and bool(self.active[i])

    def _dip(self, t: float, w: float = 0.12) -> float:
        """Quietest 10 ms within +-w of t: where to cut inside continuous speech."""
        a, b = max(0, int((t - w) / HOP)), min(self.n, int((t + w) / HOP) + 1)
        return (a + int(np.argmin(self.db[a:b]))) * HOP

    def _region(self, t: float):
        """(start, end) of the speech region containing t, or None if t is in silence."""
        i = int(t / HOP)
        if not (0 <= i < self.n and self.active[i]):
            return None
        j = i
        while j > 0 and self.active[j - 1]:
            j -= 1
        k = i
        while k < self.n and self.active[k]:
            k += 1
        return j * HOP, k * HOP

    def snap_in(self, t: float, lo: float = 0.0, pre: float = 0.06) -> float:
        """Where the voice really starts for a clip whose first word Whisper puts at t."""
        r = self._region(t)
        if r:  # t is mid-sound: go back to where this stretch of speech began
            start = r[0]
            if start - pre >= lo and t - start <= 1.2:
                return start - pre
            return max(lo, self._dip(max(t - 0.1, lo + 0.12)))  # a retake joins mid-speech
        nxt = [o for o in self.onsets if t <= o <= t + 0.6]  # t is in a pause: next time the voice starts
        if nxt:
            return max(lo, nxt[0] - pre)
        return max(lo, t - pre)

    def snap_out(self, t: float, hi: float = 1e9, post: float = 0.1) -> float:
        """Where the voice really stops for a clip whose last word Whisper ends at t."""
        r = self._region(t)
        if r:  # t is mid-sound: run on to where this stretch of speech ends
            end = r[1]
            if end + post <= hi and end - t <= 1.2:
                return end + post
            return min(hi, self._dip(min(t + 0.1, hi - 0.12)))
        prev = [o for o in self.offsets if t - 0.6 <= o <= t]  # t is in a pause: last time the voice stopped
        if prev:
            return min(hi, prev[-1] + post)
        return min(hi, t + post)

    def trim_silences(self, a: float, b: float, max_gap: float = 0.28, keep: float = 0.14):
        """Split [a, b] wherever the voice stops for longer than max_gap; leave `keep` of air."""
        out, cur = [], a
        i0, i1 = int(a / HOP), int(b / HOP)
        k = i0
        while k < i1:
            if not self.active[k]:
                j = k
                while j < i1 and not self.active[j]:
                    j += 1
                gap = (j - k) * HOP
                inner = k > i0 and j < i1
                if inner and gap > max_gap:
                    out.append((cur, k * HOP + keep / 2))
                    cur = j * HOP - keep / 2
                k = j
            else:
                k += 1
        out.append((cur, b))
        # Never start or end a clip on dead air: pull each edge in to the voice (+ lead-in / tail).
        tight = []
        for x, y in out:
            i, j = int(x / HOP), int(y / HOP)
            on = next((k for k in range(i, j) if self.active[k]), None)
            if on is None:
                continue
            off = next(k for k in range(j - 1, i - 1, -1) if self.active[k])
            x = max(x, on * HOP - 0.07)
            y = min(y, (off + 1) * HOP + 0.11)
            tight.append((x, y))
        return [(x, y) for x, y in tight if y - x > 0.08]

    def silent_fraction(self, t: float, w: float = 0.03) -> float:
        a, b = max(0, int((t - w) / HOP)), min(self.n, int((t + w) / HOP) + 1)
        return float(1 - self.active[a:b].mean()) if b > a else 1.0
