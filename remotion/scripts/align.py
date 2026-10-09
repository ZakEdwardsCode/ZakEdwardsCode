"""Re-time Whisper's words against the audio with forced alignment (torchaudio MMS_FA).

Whisper's word timestamps can drift by half a second; forced alignment pins each word to
where it is actually spoken (~20 ms). Output keeps words.json's shape: [{w, s, e, p}].
"""
import json
import re
import sys
import numpy as np
import scipy.io.wavfile as wf
import torch
from torchaudio.pipelines import MMS_FA

WAV, SEGS, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
sr, audio = wf.read(WAV)
audio = torch.from_numpy(audio.astype(np.float32) / 32768).unsqueeze(0)
model = MMS_FA.get_model(with_star=False).eval()
tokenizer, aligner = MMS_FA.get_tokenizer(), MMS_FA.get_aligner()
DIGITS = "zero one two three four five six seven eight nine".split()


def norm(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"\d", lambda m: " " + DIGITS[int(m.group())] + " ", w)
    return re.sub(r"[^a-z]", "", w)


segs = json.load(open(SEGS))
out, moved = [], []
for seg in segs:
    ws = seg["words"]
    a = max(0.0, seg["start"] - 0.4)
    b = min(audio.shape[1] / sr, seg["end"] + 0.4)
    chunk = audio[:, int(a * sr):int(b * sr)]
    toks = [norm(w["w"]) for w in ws]
    idx = [i for i, t in enumerate(toks) if t]
    times = {}
    if idx and chunk.shape[1] > sr * 0.2:
        with torch.inference_mode():
            emission, _ = model(chunk)
        try:
            spans = aligner(emission[0], tokenizer([" ".join(toks[i].split()) for i in idx]))
            ratio = chunk.shape[1] / emission.shape[1] / sr
            for i, sp in zip(idx, spans):
                times[i] = (a + sp[0].start * ratio, a + sp[-1].end * ratio)
        except Exception as e:  # alignment can fail on very short/odd segments: keep Whisper's times
            print("keep whisper times for segment at", round(seg["start"], 1), e)
    for i, w in enumerate(ws):
        s, e = times.get(i, (w["s"], w["e"]))
        moved.append(abs(s - w["s"]))
        out.append({"w": w["w"], "s": round(s, 3), "e": round(e, 3), "p": w["p"]})

json.dump(out, open(OUT, "w"))
m = np.array(moved)
print(f"words {len(out)}; moved >0.15s: {(m > 0.15).mean():.0%}, >0.4s: {(m > 0.4).mean():.0%}, max {m.max():.2f}s")
