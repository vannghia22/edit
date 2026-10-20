# MM Đường — /editvideomau

Nguồn: `MM_TIKTOK_DNA_V1_FINAL.mp4` ở gốc repository, trùng SHA-256 với tệp người dùng tải lên tên `mmduong.mp4`.

Bản xuất: `MM_DUONG_EDITVIDEOMAU_FINAL.mp4`, khung dọc 1080×1920, 30 fps, 19,1 giây. Bản cũ được giữ nguyên.

[Mở bản MP4](../../MM_DUONG_EDITVIDEOMAU_FINAL.mp4)

![Khung hình mở đầu](preview.jpg)

## Nội dung dựng

- Hook chữ “Sinh viên / Cần 10 triệu?” lấy từ câu hỏi có trong nguồn.
- Thay các khung tiêu đề cũ bằng chữ trắng/vàng, gạch nhấn và chuyển động ngắn. Hai lớp matte tối chuyển mềm che chữ đã được ghi cứng trong nguồn, tránh chồng phụ đề; khuôn mặt nằm giữa vùng rõ.
- Chia 16 cụm phụ đề, đối chiếu thủ công với phụ đề gốc theo khung hình 0,2 giây. Kết quả Whisper tiny/small có lỗi, không được dùng làm transcript xuất bản. Không tuyên bố đã kiểm tra bằng nghe toàn bộ lời nói.
- Ba khoảng âm thanh đã có bíp được xác định theo phổ âm 1047 Hz; thay tín hiệu ở các khoảng đó bằng bíp 880 Hz có fade ngắn. Khoảng giây: 2,577–2,852; 8,482–8,842; 17,227–17,452. Chữ tương ứng dùng `v*y`, `n* x*u`.
- Minh họa nét cho căn cước, hồ sơ và tin nhắn; giữ điều kiện “hồ sơ đậu” khi nhấn việc giải ngân trong ngày. Không thêm lời bảo đảm phê duyệt.
- Reframe/zoom nhẹ, tăng tương phản/màu/độ nét vừa phải. Nhạc nền 100 BPM và whoosh/chime tự tổng hợp, không dùng bản ghi nhạc bên ngoài.
- CTA nhắn tin theo lời có trong nguồn; không thêm số điện thoại hoặc tài khoản.

## Dựng lại

Cần FFmpeg, Node.js >=22, Python có NumPy. Trong thư mục này chạy `bash prepare.sh`, sau đó chạy các lệnh trong `package.json`. Các media tạo lại được bỏ qua bởi `.gitignore`.

`build.py` tạo composition; `audio_mix.py` tạo nhạc/SFX và mix dựa trên nguồn; `captions.json`, `timing.json` lưu mốc dựng. Font Be Vietnam Pro được đóng kèm giấy phép OFL.

HyperFrames được ghim ở 0.8.181. Kiểm tra cuối composition: runtime/motion không lỗi, layout không lỗi trong 9 mẫu, 21/21 kiểm tra chữ đạt tương phản. 28 cảnh báo lint còn lại liên quan tổ chức timeline/sub-composition; không phải lỗi render hay tràn chữ. Kết quả kiểm tra bản MP4 hoàn tất được ghi trong `validation.json` sau khi xuất.

Trong máy đám mây này, dùng browser và cache có sẵn khi chạy CLI:

```bash
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium XDG_CACHE_HOME=/workspace/.cache npm_config_cache=/workspace/.npm-cache npm run check
HYPERFRAMES_BROWSER_PATH=/usr/bin/chromium XDG_CACHE_HOME=/workspace/.cache npm_config_cache=/workspace/.npm-cache npm run render
```
