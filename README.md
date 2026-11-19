# ☯️ AI TỬ VI – CHUYÊN ĐỀ TẬT ÁCH

Website Streamlit tiếng Việt để kiểm nghiệm phương pháp luận Tử Vi truyền thống.

## V3 — Báo cáo chuyên sâu

- Bốn tâm điểm: Mệnh gốc, Tật gốc, Mệnh đại vận, Tật đại vận; xét đúng tọa thủ, xung chiếu, tam hợp, giáp và nhị hợp.
- Luận Tật vô chính diệu có xét sao xung/tam hợp; không coi là sao tọa thủ.
- 26 tổ hợp tra cứu nguồn A; 5 công thức đồng cung nguồn C (trang in 625–626). Kiểm tra đủ thành phần khác với xác nhận điều kiện thành cách.
- Tách tiền tố lưu tinh/phi hóa và giữ Lưu Hà nguyên cục.
- Nút **Tạo bài luận chuyên sâu (V3)** dùng AI viết sáu phần. Báo cáo căn cứ tự động không cần API Key.
- Nguồn A ưu tiên hơn B, bao gồm Long Trì–mũi, Phượng Các–tai, Nhật/Nguyệt–mắt và Thiên Đồng–tiêu hóa.
- Nếu vị trí Mệnh/Tật không hợp thứ tự 12 cung, hoặc còn cung trống, cần kiểm tra dữ liệu. Không tự khẳng định bệnh, tính cách, hành vi phạm tội hoặc biến cố thực tế.
- Kho nguồn C và các nhóm Ách chuyên biệt vẫn chưa đầy đủ; V3 chỉ là bản nâng cấp thử nghiệm. AI trực tuyến vẫn có giới hạn/quyền truy cập theo dịch vụ.

## Bản nâng cấp V2 – Luận nền tảng (18/11/2026)

- Có phần luận Tật gốc cho **14 chính tinh**, dựa trên bảng sao–tạng phủ của tài liệu “Cung Tật Ách: Bản chất, bệnh lý và các yếu tố liên quan”.
- Bổ sung luận phụ tinh có nguồn trong “Các cách chỉ bệnh tật trong Tử Vi”; nguồn này được ưu tiên khi phân tích bệnh lý.
- Phân biệt **Mệnh – biểu hiện bên ngoài** với **Tật – nội tâm**; với sao chưa có mô tả tâm tính trực tiếp trong tài liệu, ứng dụng sẽ báo chưa đủ căn cứ thay vì tự tạo diễn giải.
- Cung Tật đại vận được luận qua chính tinh và sao tại cung, rồi phối hợp các cách cục riêng.
- Nếu chưa khớp cách cục đặc biệt, **phần luận nền tảng vẫn hiển thị**. Với các cách bệnh, nội dung phản ánh phân loại trong cổ thư, không xác nhận bệnh thực tế.
- Kiểm thử bổ sung riêng lá số có **Thiên Tướng (Đ), Đại Hao (H), Tuần** ở Tật.
- Ứng dụng không tự xác định toàn bộ sự kiện hạn, cũng chưa có ấn bản đầy đủ các bộ Ách từ sách Bùi Quang Nhuận.

## Chức năng

- Hai lá số nghiên cứu mẫu và bảng nhập/chỉnh sửa sao tại 12 cung.
- Xét tọa thủ, tam hợp, xung chiếu, giáp cung, nhị hợp và Tật đại vận.
- Luận Tật gốc, Ách gốc, tính cách qua Mệnh–Tật, Tật–Ách đại vận.
- 21 quy tắc thử nghiệm kèm điều kiện sao và nguồn tham khảo.
- Báo cáo tải về TXT.
- **Tùy chọn:** AI nhận dạng ảnh và viết bài luận qua Google Gemini (có hạn mức miễn phí tùy tài khoản/khu vực) hoặc Hugging Face (có thể yêu cầu nạp tín dụng). Cần API Key tương ứng và kiểm tra dữ liệu sau nhận dạng.

## Triển khai website

Đọc [DEPLOY.md](DEPLOY.md). Dùng **Streamlit Community Cloud** với:

- Repository: `kynguyen1094/ai-tu-vi-tat-ach`
- Branch: `main`
- Main file path: `app.py`

Sau khi Streamlit triển khai thành công, nền tảng sẽ cung cấp URL website.

## Quyền riêng tư

Không đưa token vào GitHub. Token đặt tại Secrets của Streamlit. Khi dùng AI, ảnh được gửi đến nhà cung cấp bạn chọn; khi chỉ dùng lá số mẫu và bộ quy tắc thì không cần khóa. Google Gemini Free Tier có thể sử dụng dữ liệu để cải thiện dịch vụ theo chính sách của Google. Không đăng khóa công khai.

## Tình trạng

Đây là **bản thử nghiệm**, không phải bộ luận giải đầy đủ từ ba tài liệu nghiên cứu. Khả năng AI thị giác qua Hugging Face chưa được kiểm thử đầu cuối bằng token thực tế. Kết quả Tử Vi không phải chẩn đoán y khoa hay kết luận pháp lý.

## Kiểm thử

```bash
python test_engine_web.py
```

Mã nguồn công khai cho mục đích học tập và nghiên cứu.