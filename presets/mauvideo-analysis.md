# Phân tích mauvideo.mp4

## Phạm vi và bằng chứng

Tệp 24.164.614 byte, dài 106,9 giây, 576×1024 (9:16), 30 fps, H.264/AAC stereo 44,1 kHz. Đã giải mã toàn bộ hình/âm thanh bằng FFmpeg với `-xerror`, kết thúc mã 0. Đã khảo sát khung hình mỗi giây trên toàn chiều dài và thêm khung mỗi 0,25 giây trong đoạn 9–15 giây. Việc này xác minh diện mạo và các mốc bố cục, không tương đương việc nghe kiểm tra toàn bộ âm thanh hay đo chính xác từng điểm cắt bằng timeline gốc.

Âm thanh đã được trích để phân tích. HyperFrames không chép lời được do thiếu whisper-cpp. Đã cài faster-whisper vào môi trường riêng ngoài repository, nhưng nơi tải model Hugging Face trả HTTP 403. Chưa xác minh được nội dung âm thanh bằng nghe trực tiếp, tên nhạc, BPM, loại SFX, cân bằng nhạc/giọng hay độ khớp beat. Không suy đoán những mục này từ hình ảnh.

## Mở đầu và điểm thu hút

0–8 giây: người dẫn mặc vest, đeo kính, đứng/đi ngoài trời; cảnh cây xanh và trời xanh sáng. Logo Masterise Homes xuất hiện sớm, sau đó có phối cảnh dự án ở vùng trên. Chữ ngắn giới thiệu chủ đầu tư, Sola, bán đảo Ánh Dương và khu nhà ở compound. Cách mở dựa vào người dẫn, nhận diện thương hiệu và hình sản phẩm, không có title card dài đứng riêng trước nội dung.

Khoảng 9–13 giây: chuyển sang người dẫn ngồi, ảnh tổng mặt bằng ở trên, tia nhấn và dấu hỏi. Chữ “4 điều đặc biệt” tạo lời hứa có cấu trúc. Đây là hook thị giác rõ nhất; không có bằng chứng khẳng định tác giả đã đưa một đoạn cuối lên đầu.

## Nhịp dựng và chuyển cảnh

| Mốc gần đúng | Nội dung hình và cách dựng |
|---|---|
| 0–9 s | Người dẫn, logo, ảnh phối cảnh, chữ giới thiệu đổi theo cụm |
| 9–14 s | Người dẫn ngồi, mặt bằng, dấu hỏi/tia nhấn; ảnh trượt ra trên trước chớp sáng |
| 14–18 s | “Thứ nhất / tiến độ xây dựng”, người dẫn và thay cỡ cảnh |
| 18–26 s | Ảnh công trường/phối cảnh/logo trên nền lưới đen nâu; chữ nhấn 70%, uy tín |
| 26–37 s | “Thứ hai / yếu tố pháp lí”, ảnh dự án, minh họa giấy tờ đỏ, ảnh sự kiện bàn giao |
| 37–45 s | “Thứ ba / yếu tố thiết kế”; chồng mờ sang phối cảnh nhà, nhãn trệt, 4 lầu, sân thượng |
| 45–62 s | Người dẫn + ảnh đơn vị thiết kế, logo, mặt bằng, sân vườn; nhấn 53 mẫu nhà, 3 mặt thoáng |
| 62–78 s | “Thứ tư”; tổng mặt bằng có khoanh đỏ, nền lưới, mũi tên chỉ mặt nước và nhãn giải thích |
| 78–80 s | Cảnh đêm nhạc nước ngang, lấp vùng thừa bằng nền mờ |
| 80–86 s | Người dẫn, ảnh mặt bằng phía trên, chữ công viên bờ sông |
| 86–98 s | Cảnh trên cao ven sông giữ lâu hơn; chữ 10.000 mét vuông, 1 km, rất hiếm có |
| 98–103 s | Người dẫn, tên Lê Hiếu, nhận diện The Global City và biểu tượng trái tim |
| 103–106,9 s | Outro TikTok và thanh tìm kiếm tài khoản |

Các mốc là gần đúng từ mẫu khung hình, không phải EDL chính xác. Ảnh phụ thường tồn tại khoảng vài giây; nhiều ý khoảng 2–4 giây, có đoạn một giây và đoạn giữ nền dài hơn. Nhịp không chỉ phụ thuộc cắt cảnh: ảnh và chữ thay trong khi người dẫn tiếp tục ở cùng bố cục.

Có cắt trực tiếp, chồng mờ quanh 39 giây, chớp sáng vàng/cam quanh 13,5 giây và lớp sáng hồng/cam quanh 49–50 giây. Không xác định tên plugin hay preset chuyển cảnh.

## Zoom, crop, reframe và nhấn chi tiết

Khung dọc ưu tiên người dẫn ở giữa/nửa dưới, nhường vùng trên cho phối cảnh/bản đồ. Có xen khung toàn thân, trung cảnh và cận hơn; các khung liên tiếp cho thấy cỡ ảnh thay đổi. Không đủ dữ liệu để tách hoàn toàn zoom hậu kỳ khỏi chuyển động máy/người dẫn.

Ảnh phụ có trượt, đổi vị trí/kích thước; đoạn 9–15 giây thấy ảnh mặt bằng đi lên khỏi khung trước khi đổi phần. Các chi tiết nhà được nhấn bằng đường nối, vòng tròn, nhãn “trệt”, “4 lầu”, “sân thượng”. Bản đồ có nét đỏ khoanh khu và mũi tên chỉ bờ nước. Đây là cách nhấn thông tin bằng đồ họa cụ thể thay vì chỉ zoom khuôn mặt.

## Chữ, màu và bố cục

Chữ sans-serif đậm, phần lớn in hoa, trắng và vàng; viền/bóng tối giúp đọc trên cây xanh và áo vest. Tên font chính xác chưa xác định. Một số chữ vàng có bóng/lớp sắc độ tạo cảm giác nổi.

Cụm trắng thường xuất hiện trước, cụm vàng bổ sung từ khóa sau. Chữ chia một đến hai dòng là chính, đôi lúc ba dòng; bố trí giữa/ngang thân người hoặc ở phần trời khi nền là cảnh trên cao. Quan sát được chữ đang trượt có mờ chuyển động; không đủ căn cứ gọi là karaoke từng từ. Phụ đề đóng vai trò tóm/nhấn cụm nội dung trên hình; chưa đối chiếu với toàn bộ lời nói nên không khẳng định đây là bản chép lời đầy đủ.

Ví dụ điểm nhấn: “70% được cất nóc”, “cuối năm 2026”, “53 mẫu nhà”, “3 mặt thoáng”, “3 mặt nước”, “1 km”. Những số liệu này thuộc nội dung video mẫu, không tự đưa sang video khác và không được coi là đã kiểm chứng bên ngoài.

## Đồ họa, hình minh họa và màu sắc

Ảnh bo góc viền/glow vàng được dùng thường xuyên, cùng logo, dấu hỏi, tia nhấn, giấy tờ, bản đồ, đường khoanh và mũi tên đỏ. Các đoạn giải thích riêng chuyển sang nền đen/nâu có lưới và texture. Có lớp tối ở vùng dưới nhiều cảnh, giúp chữ nổi hơn. Cảnh đêm ngang có nền phóng lớn làm mờ để điền khung dọc.

Diện mạo sáng, tương phản rõ, xanh trời và xanh lá bão hòa; các chuyển cảnh có ánh sáng vàng/cam/hồng. Không thể suy ra LUT, mức sharpen, camera hay thông số grading chính xác từ bản xuất.

## Điều chuyển sang preset và điều thay đổi theo yêu cầu

Giữ cấu trúc hook–các ý chính–CTA khi nguồn phù hợp; giữ chữ trắng/vàng có viền, minh họa theo lời và nhãn chỉ chi tiết. Theo yêu cầu người dùng, giảm khung/glow dày so với mẫu và ưu tiên chữ có viền. Bíp từ nhạy cảm, đổi cách viết, nhạc nền và cách mix là yêu cầu thêm; không trình bày chúng như kỹ thuật đã xác minh có trong mẫu.

Preset đầy đủ: `presets/editvideomau.md`. Chưa dựng hoặc công khai video mới trong bước phân tích này; cần xác định tệp cần chỉnh. Việc tạo preset không đăng ký slash command toàn cục cho tài khoản.
