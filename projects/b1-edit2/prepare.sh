#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -f source.mp4 ]; then
  echo 'Place the original uploaded b (1).mp4 here as source.mp4, then run again.' >&2
  exit 1
fi
ffmpeg -nostdin -y -v error -threads 2 -i source.mp4 -t 40.4 -vf 'eq=contrast=1.025:saturation=1.02:brightness=0.003,unsharp=5:5:0.20:5:5:0' -c:v libx264 -preset fast -crf 18 -threads 2 -g 30 -keyint_min 30 -movflags +faststart -an graded.mp4
ffmpeg -nostdin -y -v error -i source.mp4 -vn -ar 48000 -ac 2 -c:a pcm_s16le source-stereo.wav
python3 build.py
python3 audio_mix.py
