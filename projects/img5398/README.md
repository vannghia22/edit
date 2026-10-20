# IMG_5398 — /editvideomau

[Tải bản MP4](../../IMG_5398_EDITVIDEOMAU_FINAL.mp4)

![Khung hình mở đầu của bản xuất](preview.jpg)

Nguồn MOV gốc 107.017.315 byte được tải nguyên vẹn từ [GitHub Release IMG_5398](https://github.com/vannghia22/edit/releases/tag/IMG_5398). Không ghi đè tệp gốc. SHA-256: `83118955a8bb0e281270e299d02954df5f638f505df3ecc173015e57bc3a929f`.

Nguồn HEVC 1920×1080 với metadata xoay 90°, 60 fps, 50,308 giây. Bản dựng áp dụng xoay đúng chiều và xuất dọc 1080×1920, 30 fps, 50,3 giây, H.264/AAC. Dung lượng bản xuất khác dung lượng nguồn do định dạng và các lớp dựng.

## Các yêu cầu đã áp dụng

- Hook từ câu hỏi mở đầu: 18 tuổi và 15 triệu. Không tự thêm năm sinh 2007 vì đó chỉ là ví dụ của người dùng.
- Chữ số dùng cho tuổi và số tiền: 18 tuổi, 15 triệu, 15–50 triệu. Phụ đề chia cụm ngắn, cân dòng, số và từ khóa nhấn vàng có viền tối.
- Khung tiêu đề trên được thiết kế lại, font Be Vietnam Pro ExtraBold, cỡ lớn tới 112px, góc nhấn vàng, nền trong suốt cục bộ và chuyển động ngắn.
- 21 tween zoom/return có chủ đích, phóng lớn tối đa 18%, đồng bộ whoosh/chime ở các điểm nhấn. Giữ khuôn mặt trong vùng nhìn rõ.
- Hình phủ kín khung; vignette chỉ mờ nhẹ ở góc, tối đa 16%. Không có hai mảng đen dày trên/dưới.
- Minh họa nét về giấy tờ, lựa chọn, địa điểm và tin nhắn; CTA inbox. Không thêm tài khoản, số điện thoại hoặc clip không liên quan.
- Giữ các điều kiện trong lời nói, cả nội dung có thể có thêm lựa chọn nếu thẩm định, và phạm vi hiện chỉ hỗ trợ tại Đà Nẵng. Không thêm lời bảo đảm duyệt hồ sơ.
- Nhạc nền 100 BPM và SFX tự tổng hợp, mix dưới giọng; tăng giọng theo mức đo, giữ đỉnh âm thanh dưới ngưỡng clipping.

## Phụ đề và từ cần che

Đối chiếu hai lượt ASR tiếng Việt (Whisper small và Whisper turbo), sửa các lỗi ngữ âm rõ theo ngữ cảnh, rút gọn từ đệm/đại từ. Các số và địa danh được đối chiếu giữa hai lượt. Không dùng câu kết tự suy ra ở đoạn im lặng cuối. Đây không phải tuyên bố đã rà nghe toàn bộ bằng tai.

Hai lượt nhận dạng đều ghi từ mở đầu là “góp”. Không phát hiện “vay” hoặc “nợ xấu” trong phần đã rà; không tự chèn bíp hoặc tạo danh sách cấm mới cho các từ khác. Mốc phụ đề ở `captions.json`, tiêu đề/zoom/minh họa ở `edit-plan.json`, mix ở `audio-audit.json`.

## Kiểm tra và dựng lại

HyperFrames check: runtime/motion không lỗi, layout không lỗi trong 9 mẫu, không có lỗi lint. 41 cảnh báo lint về tổ chức timeline/sub-composition. Bộ đo tương phản còn cảnh báo ở một số từ màu vàng trên áo sáng; đã rà ảnh thực tế, chữ có viền tối 5px và bóng rõ. Không tắt kiểm tra hoặc báo toàn bộ phép đo tương phản đều đạt. Chi tiết kiểm tra MP4 nằm trong `validation.json`.

Font kèm giấy phép OFL. Cần FFmpeg, Node >=22, Python có Pillow và NumPy. Trong thư mục này chạy `bash prepare.sh`, sau đó:

```bash
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium XDG_CACHE_HOME=/workspace/.cache npm_config_cache=/workspace/.npm-cache npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium XDG_CACHE_HOME=/workspace/.cache npm_config_cache=/workspace/.npm-cache npm run render
```

Media trung gian được tạo lại và được bỏ qua bởi `.gitignore`.
