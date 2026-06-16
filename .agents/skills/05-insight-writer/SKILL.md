---
name: 05-insight-writer
description: Chuyển đổi các con số thô từ Dashboard thành các nhận định kinh doanh (Insights) theo chuẩn OEIA và tự động sinh báo cáo Word/Markdown.
version: v2.0.0
status: Active
---

# Kỹ năng Insight Writer (Chuyên gia Phân tích Ngôn ngữ & Viết Báo Cáo)

## 1. Mục tiêu
Thực hiện khâu cuối cùng của Enterprise BI Pipeline: **Narrative BI**. Kỹ năng này không làm việc trực tiếp với Data thô, mà chỉ đọc kết quả đã được tổng hợp (Dashboard/Pivot) từ Data Analyst để kể một câu chuyện dữ liệu có cấu trúc.

## 2. Kích hoạt (Triggers)
- Được gọi sau khi kỹ năng `04-data-analyst` hoàn tất việc sinh ra `dashboard.xlsx`.
- Khi người dùng yêu cầu "viết báo cáo", "rút ra insight", "tạo file word".

## 3. Vai trò chuyên gia (Expert Identity)
**Nhà phân tích Kinh doanh (Business Analyst)**: Sử dụng tư duy logic Minto Pyramid. Lập luận chặt chẽ, Answer First, và tuân thủ tuyệt đối công thức phân tích Insight.

## 4. Khung phương pháp luận (Methodology Framework)
- **Minto Pyramid Principle (McKinsey):** Báo cáo theo cấu trúc từ trên xuống (câu trả lời trước, lập luận sau).
- **OEIA Framework:** Cấu trúc từng nhận định phân tích rõ ràng:
  - **Observation (Quan sát):** Nêu xu hướng.
  - **Evidence (Bằng chứng):** Trích dẫn số liệu tuyệt đối từ Dashboard.
  - **Interpretation (Diễn giải):** Giải thích nguyên nhân business.
  - **Action (Hành động):** Đề xuất giải pháp.

## 5. Hướng dẫn chi tiết
1. **Nạp kết quả phân tích:**
   - Agent đọc file `05_san_pham/dashboard.xlsx` (Đặc biệt là các sheet Thống kê và Pivot).
2. **Suy luận & Soạn thảo (LLM Processing):**
   - Agent áp dụng OEIA để viết ra ít nhất 3 Insights.
3. **Đóng gói báo cáo:**
   - Chạy script Python `scripts/generate_report.py` để nhúng các biểu đồ ảnh (`charts/*.png`) và văn bản Insight vào file Word (`05_san_pham/final_report.docx`).
4. **Tóm tắt bàn giao:**
   - Sinh file `06_ban_giao/submission_summary.md`.

## 6. Các ràng buộc nghiêm ngặt
- **Tuyệt đối tuân thủ số liệu (No Hallucination):** Nếu Dashboard báo doanh thu là 100, thì Evidence phải ghi đúng 100. Cấm bịa thêm số.
- **Answer First:** Bắt buộc có Executive Summary ở đầu file.

## 7. Xử lý lỗi
- **Không tìm thấy Dashboard:** Báo lỗi "Chưa có kết quả từ Data Analyst."
- **Lỗi sinh thư viện docx:** Chuyển sang lưu trữ tạm bằng định dạng Markdown (`final_report.md`).

## 8. Tài nguyên & Tham chiếu
- **Script Thực thi:** `scripts/generate_report.py`
- **Đường dẫn thư mục liên quan:**
  - Đầu vào: `05_san_pham/dashboard.xlsx` & `05_san_pham/charts/`
  - Đầu ra: `05_san_pham/final_report.docx`

## 9. Quy trình nghiệm thu
- [ ] Báo cáo `final_report.docx` được tạo thành công.
- [ ] Các Insight trong báo cáo được viết chuẩn khung OEIA và Minto.
- [ ] Hình ảnh biểu đồ được chèn vào báo cáo.
