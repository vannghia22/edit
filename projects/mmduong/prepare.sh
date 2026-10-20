#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source_video="../../MM_TIKTOK_DNA_V1_FINAL.mp4"
ffmpeg -nostdin -y -v error -i "$source_video" -vn -ac 1 -ar 16000 source.wav
ffmpeg -nostdin -y -v error -i "$source_video" -vn -ac 2 -ar 48000 source-stereo.wav
ffmpeg -nostdin -y -v error -i "$source_video" -vf 'eq=contrast=1.035:saturation=1.045:brightness=0.005,unsharp=5:5:0.25:5:5:0' -c:v libx264 -preset fast -crf 18 -threads 4 -r 30 -g 30 -keyint_min 30 -movflags +faststart -an graded.mp4
python3 audio_mix.py
python3 build.py
