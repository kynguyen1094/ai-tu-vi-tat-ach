## Triển khai website

1. Mở https://share.streamlit.io/ và đăng nhập qua GitHub.
2. Chọn **Create app** > Repository **kynguyen1094/ai-tu-vi-tat-ach** > Branch **main** > Main file **app.py**.
3. Nhấn **Deploy**. Website hiện có địa chỉ: https://ai-tu-vi-tat-ach-byyeex3x6jjt5xqbwzmkjq.streamlit.app/

### Bật AI đọc ảnh (đề xuất Google Gemini)

1. Mở https://aistudio.google.com/app/apikey, đăng nhập Google, tạo **Gemini API Key**.
2. Tại website, ở thanh bên trái, chọn **Google Gemini (có hạn mức miễn phí)**.
3. Dán Gemini API Key vào ô tương ứng; chọn model `gemini-2.5-flash` (nếu gặp giới hạn có thể chọn `gemini-2.5-flash-lite`).
4. Tải ảnh JPG/PNG lá số, nhấn **AI đọc 12 cung** và **kiểm tra kỹ lại** 12 cung trước khi xác nhận.
5. Các lá số mẫu và quy tắc vẫn dùng được không cần khóa AI.

Có thể lưu khóa cho người quản trị tại **Streamlit App > Settings > Secrets** theo dạng `GEMINI_API_KEY = "..."`, nhưng với website công khai KHÔNG nên đặt khóa dùng chung nếu chưa có đăng nhập, giới hạn lượt và kiểm soát chi phí. Không đưa khóa vào GitHub.

### Hugging Face (tùy chọn)

Chọn nhà cung cấp **Hugging Face** và nhập token vào thanh bên. HTTP 402 có nghĩa dịch vụ yêu cầu mua tín dụng theo cơ chế thanh toán Hugging Face; không phải lỗi lá số. Có thể đổi sang Gemini để dùng hạn mức miễn phí (nếu tài khoản/khu vực có quyền).

### Giới hạn & quyền riêng tư

- Bộ luận hiện chỉ có 21 quy tắc nghiên cứu, chưa toàn bộ tài liệu gốc.
- Nhận dạng ảnh chưa kiểm thử đầu-cuối với API Key thực tế trên tài khoản chủ sở hữu; kết quả có thể đọc sai sao, vị trí cung và ký hiệu miếu vượng.
- Google Gemini Free Tier có giới hạn lượt và điều khoản sử dụng dữ liệu riêng; không tải lá số chứa thông tin nhạy cảm nếu bạn chưa đồng ý chuyển ảnh tới nhà cung cấp.
- Không dùng các cách bệnh lý làm chẩn đoán hay dự báo tai nạn/pháp lý chắc chắn.
