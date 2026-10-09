"""Score talking-head frames for a thumbnail: sharp face, facing camera, eyes open, mouth closed."""
import json, subprocess, sys
import numpy as np, cv2
SRC = "/home/user/work/src/head.mov"
W, H, FPS = 1920, 1080, 2
det = cv2.FaceDetectorYN.create("/home/user/work/models/yunet.onnx", "", (W, H), 0.7, 0.3, 5)
vf = (f"fps={FPS},zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=bgr24")
p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
out, i = [], 0
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    _, faces = det.detect(img)
    if faces is not None and len(faces):
        f = max(faces, key=lambda f: f[2] * f[3])
        x, y, w, h = map(int, f[:4])
        (rex, rey), (lex, ley), (nx, ny), (rmx, rmy), (lmx, lmy) = f[4:14].reshape(5, 2)
        crop = cv2.cvtColor(img[max(0, y):y + h, max(0, x):x + w], cv2.COLOR_BGR2GRAY)
        sharp = cv2.Laplacian(crop, cv2.CV_64F).var() if crop.size else 0
        eye_mid = (rex + lex) / 2
        frontal = 1 - min(1, abs(nx - eye_mid) / (0.25 * w))       # nose centred between eyes
        level = 1 - min(1, abs(rey - ley) / (0.15 * w))              # head not tilted
        mouth_w = abs(lmx - rmx) / w
        out.append({"t": i / FPS, "sharp": float(sharp), "frontal": float(frontal), "level": float(level),
                    "score": float(f[14]), "box": [x, y, w, h], "mouth": float(mouth_w)})
    i += 1
json.dump(out, open("/home/user/work/thumb/scan/scores.json", "w"))
print("frames", i, "faces", len(out))
