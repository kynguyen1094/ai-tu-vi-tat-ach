## Triển khai website

1. Mở https://share.streamlit.io/ và đăng nhập qua GitHub.
2. Chọn **Create app** > Repository **kynguyen1094/ai-tu-vi-tat-ach** > Branch **main** > Main file **app.py**.
3. Nhấn **Deploy**, chờ hệ thống tạo URL thực tế. Địa chỉ không được xác nhận cho tới khi triển khai thành công.
4. Để đọc ảnh: tạo token trên https://huggingface.co/settings/tokens, vào **App settings > Secrets** trên Streamlit và nhập `HF_TOKEN = "..."`. Không đưa token vào mã nguồn GitHub.
5. Chỉ dùng AI khi người dùng đồng ý chuyển ảnh lên bên thứ ba; kiểm tra thủ công vị trí 12 cung trước khi luận.

### Giới hạn

Bản web có 21 quy tắc nghiên cứu, chưa toàn bộ tài liệu; dùng lá số mẫu không cần AI. Khả năng chạy của mô hình Qwen3-VL qua Hugging Face phụ thuộc nhà cung cấp, quyền truy cập và hạn mức. Chưa kiểm thử suy luận trực tuyến với token thật. Không dùng các cách bệnh lý như chẩn đoán hoặc dự báo chắc chắn.
