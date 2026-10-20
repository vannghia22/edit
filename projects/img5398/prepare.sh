#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if [ ! -f source.MOV ]; then
  curl -L --fail --max-time 300 -o source.MOV 'https://github.com/vannghia22/edit/releases/download/IMG_5398/IMG_5398.MOV'
fi
python3 - <<'PY'
import hashlib
from pathlib import Path
assert hashlib.sha256(Path('source.MOV').read_bytes()).hexdigest()=='83118955a8bb0e281270e299d02954df5f638f505df3ecc173015e57bc3a929f', 'Source differs from the reviewed original.'
PY
ffmpeg -nostdin -y -v error -i source.MOV -vn -ac 2 -ar 48000 source-stereo.wav
ffmpeg -nostdin -y -v error -threads 2 -i source.MOV -vf 'fps=30,eq=contrast=1.035:saturation=1.035:brightness=0.005,unsharp=5:5:0.25:5:5:0' -c:v libx264 -preset fast -crf 17 -threads 2 -g 30 -keyint_min 30 -movflags +faststart -an graded.mp4
python3 build.py
python3 audio_mix.py
