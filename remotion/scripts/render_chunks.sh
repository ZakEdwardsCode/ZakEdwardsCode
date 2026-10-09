#!/bin/bash
# Render the composition in frame-range chunks (resumable), then join them losslessly.
set -u
cd /home/user/ZakEdwardsCode/remotion
TOTAL=$(python3 -c "import json,math;e=json.load(open('src/plasmo/edit.json'));print(math.ceil(e['duration']*e['fps']))")
CHUNK=2800
OUT=/home/user/work/out/parts
i=0
for ((s=0; s<TOTAL; s+=CHUNK)); do
  e=$((s+CHUNK-1)); [ $e -ge $TOTAL ] && e=$((TOTAL-1))
  f=$(printf "$OUT/part_%02d.mp4" $i)
  if [ ! -s "$f" ]; then
    for try in 1 2; do
      npx remotion render src/index.ts PlasmoVideo "$f.tmp.mp4" --frames=$s-$e --codec=h264 --crf=16 \
        --audio-codec=aac --audio-bitrate=320k --concurrency=3 \
        --offthreadvideo-cache-size-in-bytes=1500000000 --log=error > "$OUT/part_$i.log" 2>&1 \
        && mv "$f.tmp.mp4" "$f" && break
      echo "chunk $i try $try failed"
    done
  fi
  [ -s "$f" ] && echo "chunk $i done ($s-$e of $TOTAL)" || { echo "chunk $i FAILED"; exit 1; }
  echo "file '$f'" >> $OUT/list.tmp
  i=$((i+1))
done
mv $OUT/list.tmp $OUT/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $OUT/list.txt -c copy -movflags +faststart /home/user/work/out/plasmo_v2_raw.mp4 && echo "JOINED" && ffmpeg -v error -y -i /home/user/work/out/plasmo_v2_raw.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 320k -ar 48000 -movflags +faststart /home/user/work/out/plasmo_v2.mp4 && echo "MASTERED"
