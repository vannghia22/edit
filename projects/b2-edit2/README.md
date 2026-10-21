# B2 — /edit2, restrained zoom

[Download the edited MP4](../../B2_EDIT2_FINAL.mp4)

![Opening frame](preview.jpg)

Edited with HyperFrames 0.8.181 from the user's uploaded `b (2).mp4` using `/edit2` plus the explicit per-video request to zoom much less than B1 and only on very important words. Source: 720×1280, 30 fps, 46.8 seconds. Delivery: 45.5 seconds, native 720×1280; only the trailing reach toward the camera after the spoken CTA is trimmed.

## This video's override

Only **2 punch-ins**, each followed by a return:

- 18.92–21.42 seconds: “15–50 triệu”, scale 1.10 then return.
- 30.72–33.43 seconds: the “Đà Nẵng / Quy Nhơn” restriction, scale 1.08 then return.

These are 4 zoom/return tweens total, compared with 17 in B1. The frame is stable for the rest of the video, including the hook and CTA. Source camera/subject movement remains. Typography, underlines and outline icons carry other emphases. The project edit-plan stores this exception; it does not overwrite the global `/edit2` preset.

## Applied edit

- Original opening question retained as hook: 18 tuổi / góp 15 triệu.
- 29 Vietnamese caption groups, numeric ages/amounts, 10 animated headers.
- White outlined text, restrained aqua/deep aqua emphasis, no large text boxes; full-frame footage and very light corner vignette.
- ID, age, people, amount, location and message outline illustrations linked to the content; no unrelated stock clips.
- Restrained contrast, saturation and sharpness adjustment; skin appearance preserved.
- Original synthesized 88 BPM music and fewer whoosh/pop sounds mixed under dialogue.
- Both **Đà Nẵng and Quy Nhơn** remain in the original speech, captions and headings. The existing contact CTA is retained without invented phone numbers or account details.

## Transcript and censorship

Vietnamese Zipformer and multilingual Whisper turbo outputs were compared; Whisper small checked selected condition/ending ranges. Obvious phonetic recognition errors were corrected, repeated filler shortened in captions. The unsupported “Hãy subscribe” from the isolated 0.8-second tail in an automatic transcription was discarded; no subscribe CTA was added. No direct auditory review or forced alignment is claimed.

The recognizers identify “góp”. The user-specified `vay` / `nợ xấu` terms were not found; no unrelated word is muted or beeped. `captions.json`, `edit-plan.json`, `audio-audit.json` and `validation.json` record timing, exceptions and verification limits.

## Rebuild

Requires Node >=22, FFmpeg, Python with Pillow and NumPy. Place the original uploaded video here as `source.mp4`, then run:

```bash
bash prepare.sh
npm run check
npm run render
```

The raw upload/intermediate media are not included in this public project. HyperFrames is pinned to 0.8.181. The font is supplied under the OFL license in OFL.txt. Delivery is H.264/AAC with faststart, 30 fps, target video bitrate 1.7 Mbps. The user authorized public delivery by invoking the saved `/edit2` workflow; this does not post to any social account.
