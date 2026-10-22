#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 build.py
if [ -f music-original.wav ]; then
  ffmpeg -nostdin -y -hide_banner -loglevel error -i music-original.wav -t 28 -af 'volume=3,afade=t=in:st=0:d=0.6,afade=t=out:st=27:d=1,loudnorm=I=-22:TP=-2:LRA=9' -ar 48000 -ac 2 music.wav
fi
