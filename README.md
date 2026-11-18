# ☯️ AI TỬ VI – CHUYÊN ĐỀ TẬT ÁCH

Website Streamlit tiếng Việt để kiểm nghiệm phương pháp luận Tử Vi truyền thống.

## Chức năng

- Hai lá số nghiên cứu mẫu và bảng nhập/chỉnh sửa sao tại 12 cung.
- Xét tọa thủ, tam hợp, xung chiếu, giáp cung, nhị hợp và Tật đại vận.
- Luận Tật gốc, Ách gốc, tính cách qua Mệnh–Tật, Tật–Ách đại vận.
- 21 quy tắc thử nghiệm kèm điều kiện sao và nguồn tham khảo.
- Báo cáo tải về TXT.
- **Tùy chọn:** AI nhận dạng ảnh lá số và AI viết bài luận qua Hugging Face. Cần token riêng, nhà cung cấp hỗ trợ mô hình và kiểm tra dữ liệu sau nhận dạng.

## Triển khai website

Đọc [DEPLOY.md](DEPLOY.md). Dùng **Streamlit Community Cloud** với:

- Repository: `kynguyen1094/ai-tu-vi-tat-ach`
- Branch: `main`
- Main file path: `app.py`

Sau khi Streamlit triển khai thành công, nền tảng sẽ cung cấp URL website.

## Quyền riêng tư

Không đưa token vào GitHub. Token đặt tại Secrets của Streamlit. Khi dùng AI, ảnh sẽ được xử lý bởi dịch vụ bên ngoài; khi chỉ xem lá số mẫu và chạy quy tắc không cần token.

## Tình trạng

Đây là **bản thử nghiệm**, không phải bộ luận giải đầy đủ từ ba tài liệu nghiên cứu. Khả năng AI thị giác qua Hugging Face chưa được kiểm thử đầu cuối bằng token thực tế. Kết quả Tử Vi không phải chẩn đoán y khoa hay kết luận pháp lý.

## Kiểm thử

```bash
python test_engine_web.py
```

Mã nguồn công khai cho mục đích học tập và nghiên cứu.