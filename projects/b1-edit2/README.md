# B1 — /edit2

[Download the edited MP4](../../B1_EDIT2_FINAL.mp4)

![Opening frame](preview.jpg)

Edited from the user's uploaded `b (1).mp4` with HyperFrames 0.8.181 and the saved `/edit2` preset. Source: 720×1280, 30 fps, 41.5 seconds. Delivery: 720×1280, 30 fps, 40.4 seconds; only the trailing reach toward the camera after the spoken CTA is trimmed. No generated voice or unrelated stock footage.

- Opening question retained as hook: 18 tuổi / góp 15 triệu.
- 25 Vietnamese caption groups, 10 animated headers, numeric amounts and ages.
- White outlined typography, aqua accents and deep aqua caption emphasis for contrast against the pale shirt; relevant outline illustrations for ID, age, location, contact and amount range.
- 17 deliberate zoom/return tweens, scale up to 1.16; full-frame footage and subtle corner vignette.
- Restrained photographic contrast/saturation/sharpness correction.
- HyperFrames master optimized for download using H.264 CRF 22, slow preset, 2.1 Mbps maximum video rate, unchanged AAC audio, and faststart. Native resolution is preserved.
- Original synthesized 92 BPM music and short whoosh/pop effects mixed under speech; final audio limited to approximately -1.5 dBTP.
- The geographic restriction to Đà Nẵng remains in speech, captions and headings; the original contact CTA is retained without inventing phone numbers or account details.

## Captions and censorship

Independent local Vietnamese Zipformer and multilingual Whisper turbo results were compared. Obvious phonetic errors were corrected to “căn cước công dân” and “Đà Nẵng”; repeated filler is shortened in some captions. Both recognize “góp”, and neither finds the user-specified `vay` / `nợ xấu`; no unrelated word is beeped. There is no claim of direct auditory review in this session. ASR timestamps guide phrase alignment; no forced alignment or human listening verification is claimed.

`captions.json` and `edit-plan.json` hold text, timing and zoom settings. `audio-audit.json` records the generated audio and measured mastering. `validation.json` records delivery checks and their limits.

## Rebuild

Use Node >=22, FFmpeg, Python with Pillow and NumPy. Put the original uploaded video in this directory as `source.mp4`; the raw upload and intermediate media are intentionally not published with the project. Run:

```bash
bash prepare.sh
npm run check
npm run render
```

HyperFrames is pinned to 0.8.181 in package.json. Font files are included under the OFL license in OFL.txt. The user authorized applying `/edit2` and public delivery of the edited video; this project does not post to social accounts.
