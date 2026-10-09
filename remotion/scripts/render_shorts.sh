#!/bin/bash
# Render every Short x platform, then a sub-30MB delivery copy of each (two-pass, ~8 Mbps).
cd /home/user/ZakEdwardsCode/remotion
OUT=/home/user/work/shorts/out
mkdir -p $OUT
for id in ShortWeeksToMark ShortMarkedIn10s ShortPaperIsOutdated; do
  for p in tiktok reels shorts; do
    name=$id-$p
    if [ ! -s $OUT/$name.master.mp4 ]; then
      npx remotion render src/index.ts $name $OUT/$name.master.mp4 --codec=h264 --crf=14 --audio-codec=aac \
        --audio-bitrate=320k --concurrency=3 --timeout=240000 --offthreadvideo-cache-size-in-bytes=1500000000 \
        --log=error > $OUT/$name.log 2>&1 || { echo "$name FAILED"; continue; }
    fi
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $OUT/$name.master.mp4)
    vb=$(python3 -c "print(int(min(9500, (28.5*8*1000/$dur) - 200)))")
    ffmpeg -v error -y -i $OUT/$name.master.mp4 -c:v libx264 -preset slow -b:v ${vb}k -pass 1 -passlogfile $OUT/$name.2p -an -f mp4 /dev/null && \
    ffmpeg -v error -y -i $OUT/$name.master.mp4 -c:v libx264 -preset slow -b:v ${vb}k -maxrate $((vb*2))k -bufsize $((vb*3))k \
      -pass 2 -passlogfile $OUT/$name.2p -c:a aac -b:a 192k -movflags +faststart $OUT/$name.mp4 && \
    echo "$name done $(du -m $OUT/$name.mp4 | cut -f1)MB ${vb}k ${dur}s"
  done
done
echo ALL_DONE
