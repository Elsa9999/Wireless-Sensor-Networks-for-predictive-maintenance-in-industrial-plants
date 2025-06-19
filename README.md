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

## 9. Ý nghĩa trực quan của từng hoạt động & giao diện

### Tổng quan về dashboard
Ứng dụng này mô phỏng một hệ thống giám sát các tua-bin gió bằng mạng cảm biến không dây (WSN). Mỗi tua-bin được gắn nhiều cảm biến (độ rung, nhiệt độ, tốc độ quay, công suất...) để thu thập dữ liệu liên tục. Dữ liệu này giúp phát hiện sớm các dấu hiệu bất thường, từ đó dự đoán nguy cơ hỏng hóc và lên kế hoạch bảo trì hợp lý (bảo trì dự đoán).

### Ý nghĩa từng thành phần giao diện

- **Sidebar (bên trái):**
  - **Số tua-bin:** Số lượng tua-bin gió đang được mô phỏng/giám sát.
  - **Bước lặp (giây):** Khoảng thời gian giữa các lần cập nhật dữ liệu (giả lập thời gian thực).
  - **Độ nhiễu (σ):** Mức độ "nhiễu" (sai số, biến động) của dữ liệu cảm biến, giúp mô phỏng thực tế.
  - **Ngưỡng hỏng:** Nếu độ rung vượt ngưỡng này, hệ thống sẽ cảnh báo nguy cơ hỏng hóc.
  - **Tốc độ gió:** Ảnh hưởng đến tốc độ quay và công suất của tua-bin.
  - **Lưu tối đa điểm:** Số lượng dữ liệu lịch sử được lưu lại để vẽ biểu đồ.
  - **Cấu hình tua-bin:** Cho phép điều chỉnh từng tua-bin (biên độ rung, pha, bật/tắt), giúp mô phỏng các tình huống khác nhau.
  - **Gây nhiễu:** Mô phỏng sự cố hoặc bất thường trên một hoặc nhiều tua-bin để kiểm tra khả năng phát hiện cảnh báo.
  - **Các nút điều khiển:**
    - **Bắt đầu/Tạm dừng/Dừng/Đặt lại:** Điều khiển quá trình mô phỏng.

- **Tab "Bảng điều khiển":**
  - Hiển thị các chỉ số tổng quan: tổng công suất, số tua-bin hoạt động, % tua-bin rủi ro, thời gian mô phỏng.
  - Biểu đồ gauge: trực quan hóa độ rung trung bình toàn hệ thống (màu xanh/vàng/đỏ tương ứng mức độ an toàn/rủi ro).
  - Biểu đồ công suất tổng: cho thấy sự thay đổi công suất của toàn bộ hệ thống theo thời gian.
  - Nút tải log CSV: xuất toàn bộ dữ liệu để phân tích thêm.

- **Tab "Mạng WSN":**
  - Sơ đồ mạng sao: Gateway (trung tâm) kết nối tới các tua-bin.
  - Màu sắc node:
    - Xanh: tua-bin hoạt động bình thường.
    - Đỏ: tua-bin có nguy cơ hỏng hóc (vượt ngưỡng).
    - Xám: tua-bin bị tắt.
  - Giúp người dùng hình dung cấu trúc mạng cảm biến và trạng thái từng node.

- **Tab "Chi tiết tua-bin":**
  - Chọn tua-bin để xem chi tiết.
  - 4 biểu đồ nhỏ: Độ rung, Nhiệt độ, RPM, Công suất theo thời gian.
  - Hiển thị trạng thái hiện tại (ổn định/rủi ro/tắt) của tua-bin đó.
  - Giúp phát hiện sớm tua-bin nào có dấu hiệu bất thường.

- **Tab "Bảng dữ liệu":**
  - Bảng dữ liệu mới nhất của tất cả tua-bin.
  - Có thể hiện/ẩn lịch sử cảnh báo.
  - Dòng tua-bin rủi ro được tô màu đỏ nhạt để dễ nhận biết.

### Ý nghĩa thực tiễn
- **Trực quan hóa dữ liệu:** Người dùng không cần hiểu sâu về bảo trì dự đoán vẫn có thể thấy được khi nào tua-bin có nguy cơ hỏng, nhờ màu sắc, cảnh báo và biểu đồ.
- **Thực hành mô phỏng:** Có thể thử các kịch bản gây nhiễu, tắt/bật tua-bin, thay đổi tham số để quan sát ảnh hưởng.
- **Hỗ trợ quyết định:** Dashboard giúp minh họa cách hệ thống giám sát thông minh có thể hỗ trợ kỹ sư ra quyết định bảo trì đúng lúc, tiết kiệm chi phí và tăng hiệu quả vận hành.

---

**Chúc bạn sử dụng dashboard hiệu quả!** 