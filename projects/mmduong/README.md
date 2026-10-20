# MM Đường — /editvideomau, bản góc mờ nhẹ

[Bản MP4 mới](../../MM_DUONG_EDITVIDEOMAU_LIGHT.mp4) · 1080×1920 · 30 fps · 19,1 giây.

![Khung hình](preview.jpg)

Theo điều chỉnh của người dùng, hình phủ kín khung; bỏ hai mảng tối dày phía trên/dưới, chỉ giữ vignette trong suốt ở giữa và tối tối đa 18% ở các góc. Giữ tiêu đề/phụ đề đã gắn trong video nguồn để không chồng chữ hoặc phải làm nhòe nền. Các nhãn minh họa mới có viền/bóng chữ giúp đọc được trên hình sáng.

Giữ audio mix, ba đoạn bíp, nhạc tự tổng hợp 100 BPM, SFX, minh họa, zoom/reframe và CTA của bản trước. Bản trước `MM_DUONG_EDITVIDEOMAU_FINAL.mp4` được giữ nguyên.

Nguồn: `MM_TIKTOK_DNA_V1_FINAL.mp4` ở gốc repository, trùng SHA-256 với tệp tải lên `mmduong.mp4`. Nguồn đã có bíp và phụ đề che chữ. Ba đoạn bíp thay bằng 880 Hz: 2,577–2,852; 8,482–8,842; 17,227–17,452 giây. Không dùng kết quả ASR có lỗi để sửa nội dung.

## Dựng lại

Cần FFmpeg, Node.js >=22, Python có NumPy. Chạy `bash prepare.sh` trong thư mục này, sau đó:

```bash
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium XDG_CACHE_HOME=/workspace/.cache npm_config_cache=/workspace/.npm-cache npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium XDG_CACHE_HOME=/workspace/.cache npm_config_cache=/workspace/.npm-cache npm run render
```

HyperFrames ghim ở 0.8.181. `build.py` tạo composition; `audio_mix.py` tạo nhạc/SFX và mix. `captions.json`, `timing.json` lưu mốc nội dung nguồn và minh họa. Font Be Vietnam Pro kèm giấy phép OFL. Media tạo lại được bỏ qua bởi `.gitignore`.

Kiểm tra composition tại 1,0 / 8,6 / 14,7 / 17,9 giây: runtime, layout, motion không lỗi, 8/8 kiểm tra chữ đạt tương phản. Sáu cảnh báo lint là cảnh báo tổ chức timeline/sub-composition. Kiểm tra bản MP4 được ghi trong `validation.json`.
