"""Pre-cut every full-screen face clip of the creator Shorts straight from the original iPhone file:
HDR->SDR tone map, 9:16 crop around the face, Lanczos upscale to 1080x1920, adaptive sharpening.
Remotion then plays these 1:1 instead of scaling the landscape proxy in the browser."""
import json, os, subprocess
R = "/home/user/ZakEdwardsCode/remotion"
SRC = "/home/user/work/src/head.mov"
OUT = f"{R}/public/media/vert"
os.makedirs(OUT, exist_ok=True)
TM = "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p"
CW = round(1080 * 1080 / 1920 / 2) * 2  # 608: source width that fills 1080x1920 at full height
shorts = json.load(open(f"{R}/src/plasmo/shorts.json"))
jobs = 0
for s in shorts:
    for i, c in enumerate(s["clips"]):
        if c["top"]["kind"] == "screen":
            continue
        x = max(0, min(1920 - CW, int(c["faceCx"] - CW / 2)))
        x -= x % 2
        dst = f"{OUT}/{s['id']}_{i}.mp4"
        c["vert"] = f"media/vert/{s['id']}_{i}.mp4"
        if os.path.exists(dst):
            continue
        vf = f"{TM},crop={CW}:1080:{x}:0,scale=1080:1920:flags=lanczos,cas=0.45"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{c['in']:.3f}", "-i", SRC, "-t", f"{c['out'] - c['in']:.3f}",
                        "-map", "0:v:0", "-map", "0:a:0", "-vf", vf, "-r", "30", "-c:v", "libx264", "-preset", "slow", "-crf", "12",
                        "-g", "15", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                        "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", dst], check=True)
        jobs += 1
json.dump(shorts, open(f"{R}/src/plasmo/shorts.json", "w"), indent=1)
print("cut", jobs, "vertical clips")
