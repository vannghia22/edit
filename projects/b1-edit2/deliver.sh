#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ffmpeg -nostdin -y -hide_banner -loglevel error -threads 2 -i ../../B1_EDIT2_MASTER.mp4 -c:v libx264 -preset slow -crf 22 -maxrate 2100k -bufsize 4200k -threads 2 -pix_fmt yuv420p -c:a copy -movflags +faststart ../../B1_EDIT2_FINAL.mp4
