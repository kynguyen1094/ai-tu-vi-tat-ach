# ☯️ AI TỬ VI – CHUYÊN ĐỀ TẬT ÁCH

Website Streamlit tiếng Việt để kiểm nghiệm phương pháp luận Tử Vi truyền thống.

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