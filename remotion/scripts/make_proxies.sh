#!/bin/bash
# Build edit proxies from the originals. The iPhone footage is HDR (HLG / BT.2020, 10-bit):
# tone-map it to SDR BT.709 (Hable) so colours keep their warmth and contrast.
set -e
W=${1:-/home/user/work}
ffmpeg -v error -y -i $W/src/screen.webm -vf fps=30 -c:v libx264 -preset medium -crf 10 -g 30 -pix_fmt yuv420p \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -movflags +faststart $W/proxy/screen_hq.mp4
ffmpeg -v error -y -i $W/src/head.mov -map 0:v:0 -map 0:a:0 \
  -vf "zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p" \
  -c:v libx264 -preset medium -crf 10 -g 30 -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 320k -movflags +faststart $W/proxy/head_hq.mp4
