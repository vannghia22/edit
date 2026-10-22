#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -f source.mp4 ]; then
  echo 'Place the original uploaded b (2).mp4 here as source.mp4.' >&2
  exit 1
fi
python3 build.py
ffmpeg -nostdin -y -hide_banner -loglevel error -i source.mp4 -vn -ar 48000 -ac 2 -c:a pcm_s16le source-stereo.wav
python3 audio_mix.py
