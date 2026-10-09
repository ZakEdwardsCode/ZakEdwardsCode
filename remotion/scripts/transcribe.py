import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("small.en", device="cpu", compute_type="int8", cpu_threads=2)
import numpy as np, scipy.io.wavfile as wf
sr, a = wf.read(sys.argv[1]); a = a.astype(np.float32) / 32768.0
segs, info = m.transcribe(a, word_timestamps=True, vad_filter=False, beam_size=5,
                          condition_on_previous_text=False)
out = []
for s in segs:
    out.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word, "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 3)} for w in s.words]})
    print(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}", flush=True)
json.dump(out, open(sys.argv[2], "w"))
