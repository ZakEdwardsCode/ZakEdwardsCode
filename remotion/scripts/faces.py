"""Track the face in the talking-head video (4 samples/sec) -> faces.json in 1920x1080 coords."""
import json, subprocess, sys
import numpy as np, cv2
SRC, OUT = sys.argv[1], sys.argv[2]
W, H, S = 640, 360, 3.0  # analyse at 640x360, scale back up by 3
det = cv2.FaceDetectorYN.create("/home/user/work/models/yunet.onnx", "", (W, H), 0.6, 0.3, 5)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", f"fps=4,scale={W}:{H}", "-f", "rawvideo",
                      "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
out, i = [], 0
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    _, faces = det.detect(img)
    rec = {"t": round(i / 4, 2)}
    if faces is not None and len(faces):
        f = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = (float(v) * S for v in f[:4])
        rec.update(x=round(x), y=round(y), w=round(w), h=round(h))
    out.append(rec)
    i += 1
json.dump(out, open(OUT, "w"))
found = sum(1 for r in out if "x" in r)
print(f"samples={len(out)} found={found} ({100*found/len(out):.1f}%)")
