# Dashboard mô phỏng & giám sát WSN tua-bin gió

## 1. Mục đích & Ý nghĩa
Ứng dụng này được xây dựng nhằm mô phỏng và giám sát mạng cảm biến không dây (WSN) cho hệ thống tua-bin gió, phục vụ nghiên cứu và thực hành về bảo trì dự đoán (predictive maintenance) trong công nghiệp. Thông qua dashboard này, người dùng có thể:
- Hiểu rõ hơn về cách dữ liệu cảm biến (độ rung, nhiệt độ, RPM, công suất...) phản ánh tình trạng vận hành của tua-bin gió.
- Thực hành các kịch bản gây nhiễu, phát hiện sớm nguy cơ hỏng hóc dựa trên xác suất, từ đó đưa ra cảnh báo kịp thời.
- Trực quan hóa trạng thái mạng WSN, kiểm soát và cấu hình từng tua-bin, giúp tối ưu hóa vận hành và bảo trì.
- Đóng góp cho việc phát triển các giải pháp số hóa, tự động hóa giám sát thiết bị công nghiệp, nâng cao hiệu quả và giảm chi phí bảo trì.

Ứng dụng phù hợp cho sinh viên, kỹ sư, nhà nghiên cứu hoặc bất kỳ ai quan tâm đến IoT, WSN, và bảo trì dự đoán trong lĩnh vực năng lượng tái tạo.

## 2. Giới thiệu
Đây là ứng dụng Streamlit mô phỏng và giám sát mạng cảm biến không dây (WSN) cho bảo trì dự đoán tua-bin gió. Giao diện hoàn toàn bằng tiếng Việt, dễ sử dụng, trực quan.

## 3. Yêu cầu hệ thống
- Python >= 3.8 (khuyến nghị Python 3.10+)
- Hệ điều hành: Windows, Linux, hoặc MacOS

## 4. Cài đặt thư viện cần thiết
**Bước 1:** Mở terminal/cmd tại thư mục dự án.

**Bước 2:** (Khuyến nghị) Tạo môi trường ảo:
```bash
python -m venv venv
# Kích hoạt (Windows)
venv\Scripts\activate
# Kích hoạt (Mac/Linux)
source venv/bin/activate
```

**Bước 3:** Cài đặt các package:
```bash
pip install streamlit numpy pandas networkx plotly
```

## 5. Chạy ứng dụng
```bash
streamlit run app.py
```
Sau đó mở trình duyệt và truy cập: [http://localhost:8501](http://localhost:8501)

## 6. Hướng dẫn sử dụng giao diện
### **A. Sidebar (bên trái)**
- **Số tua-bin:** Chọn số lượng tua-bin mô phỏng (1–20).
- **Bước lặp (giây):** Khoảng thời gian mỗi bước mô phỏng.
- **Độ nhiễu (σ):** Điều chỉnh mức nhiễu cho dữ liệu cảm biến.
- **Ngưỡng hỏng:** Ngưỡng xác suất để cảnh báo hỏng hóc.
- **Tốc độ gió (m/s):** Điều chỉnh tốc độ gió đầu vào.
- **Lưu tối đa điểm:** Số lượng điểm dữ liệu lưu lại cho mỗi tua-bin.
- **Cấu hình tua-bin:** Tùy chỉnh biên độ, pha, bật/tắt từng tua-bin.
- **Gây nhiễu:** Chọn tua-bin, cường độ và bấm "Kích hoạt" để mô phỏng sự cố.
- **Các nút điều khiển:**
  - **Bắt đầu:** Khởi động mô phỏng.
  - **Tạm dừng:** Tạm dừng mô phỏng.
  - **Dừng:** Xóa dữ liệu, dừng hoàn toàn.
  - **Đặt lại:** Đặt lại toàn bộ trạng thái về mặc định.

### **B. Các tab chính**
- **Bảng điều khiển:**
  - Hiển thị tổng quan: tổng công suất, số tua-bin hoạt động, % rủi ro, thời gian mô phỏng.
  - Biểu đồ gauge độ rung trung bình.
  - Biểu đồ công suất tổng theo thời gian.
  - Tải log dữ liệu CSV.
- **Mạng WSN:**
  - Sơ đồ mạng sao giữa Gateway và các tua-bin.
  - Màu sắc node thể hiện trạng thái (bình thường, rủi ro, tắt).
- **Chi tiết tua-bin:**
  - Chọn tua-bin để xem chi tiết.
  - 4 biểu đồ: Độ rung, Nhiệt độ, RPM, Công suất.
  - Hiển thị trạng thái hiện tại.
- **Bảng dữ liệu:**
  - Bảng dữ liệu mới nhất của tất cả tua-bin.
  - Có thể hiện/ẩn lịch sử cảnh báo.
  - Dòng rủi ro được tô màu đỏ nhạt.

## 7. Lưu ý & lỗi thường gặp
- **Lỗi import package:** Đảm bảo đã cài đúng môi trường Python, kích hoạt venv trước khi cài package.
- **Lỗi trắng trang khi bấm Dừng/Đặt lại:** Đã được vá, nếu còn lỗi hãy kiểm tra lại phiên bản app.py mới nhất.
- **Không nên tăng số tua-bin và số điểm lưu quá lớn trên máy yếu.**
- **Nếu giao diện không tự động cập nhật:** Hãy thử F5 hoặc khởi động lại app.

## 8. Đóng góp & liên hệ
Nếu gặp lỗi hoặc muốn nâng cấp thêm tính năng, hãy liên hệ tác giả hoặc tạo issue trên repository.

**Tác giả:** Liên Gia Bảo  
**Liên hệ Zalo:** 0813104318

---
**Chúc bạn sử dụng dashboard hiệu quả!** 