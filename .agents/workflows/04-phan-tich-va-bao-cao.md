---
id: "WF-PDCA-ANALYZE-04"
name: "04-phan-tich-va-bao-cao"
description: "Thực hiện phân tích dữ liệu sạch, tạo dashboard Excel và viết báo cáo Word theo chuẩn OEIA."
version: v2.0
status: Production-Ready
semantic_triggers: ['/04-phan-tich-va-bao-cao', '/04-phan-tich', 'phan tich va bao cao', 'phân tích và báo cáo']
owner: "STUDENT-AGENT"
skill_target: "04-data-analyst, 05-insight-writer"
hitl_timeout: "24h"
retry_policy: {max_attempts: 3, backoff: exponential_1s_2s_4s, fallback: "log_to_ACTION-LOG_and_report_human"}
---

# Workflow: 04 Phân Tích Và Báo Cáo

Sử dụng quy trình này để thực hiện tính toán thống kê, xuất file dashboard và soạn thảo các insight kinh doanh.

## 1. Điều kiện tiên quyết (Prerequisites)
- Tệp `04_ban_thao/data_clean.xlsx` đã được phê duyệt.
- Tệp `00_ke_hoach/success_criteria.md` định hướng các nội dung cần phân tích.

## 2. Đầu vào (Inputs)
- Dữ liệu sạch: `04_ban_thao/data_clean.xlsx`.

## 3. Các bước thực hiện tuần tự (Step-by-Step Execution)
1. **Phân tích và Khởi tạo Bảng Điều Khiển (Data Analyst):**
   - Kích hoạt kỹ năng `04-data-analyst`.
   - Chạy script `.agents/skills/04-data-analyst/scripts/generate_dashboard.py` để tính toán số liệu và sinh biểu đồ.
   - Ghi kết quả vào `05_san_pham/dashboard.xlsx` và `05_san_pham/charts/`.
2. **Soạn thảo nhận định (Insight Writer):**
   - Kích hoạt kỹ năng `05-insight-writer`.
   - Viết ít nhất 3 Insights kinh doanh theo đúng công thức OEIA (Observation - Quan sát, Evidence - Bằng chứng, Interpretation - Diễn giải, Action - Hành động).
   - Đưa ra tối thiểu 2 kiến nghị hành động cụ thể cho doanh nghiệp.
4. **Xuất tài liệu báo cáo cuối cùng (Export Final Documents):**
   - Chạy script `.agents/skills/05-insight-writer/scripts/generate_report.py` để sinh file báo cáo `05_san_pham/final_report.docx` (hoặc `.md` dự phòng) có đầy đủ phần tóm tắt dự án, nhận định Insight và các biểu đồ tự động chèn vào.
   - Tạo bản tóm tắt nộp bài ngắn gọn trong `06_ban_giao/submission_summary.md`.
5. **Cập nhật nhật ký hoạt động (Update State Log):** Ghi nhận hoàn thành pha DO 2 vào tệp `02_nhat_ky_va_nhap/pdca_log.md`.

## 4. Maker-Checker Gate (Human Approval Point)
- **Halt Condition (Điều kiện dừng):** Sau khi xuất dashboard Excel, biểu đồ png, và tệp báo cáo `final_report.md` (hoặc `.docx`), Agent bắt buộc phải dừng lại.
- **Báo cáo kiểm duyệt (Review Report):** Hiển thị bảng KPI tóm tắt (Tổng doanh thu, Lợi nhuận, Tỷ lệ trả hàng, Thời gian giao hàng trung bình) cùng danh sách các biểu đồ đã được chèn vào báo cáo.
- **Lệnh xác nhận của Học viên:** Học viên kiểm duyệt chất lượng trực quan của báo cáo và gõ `/05-danh-gia-va-cai-tien` để bắt đầu pha kiểm định chất lượng (CHECK). Agent KHÔNG ĐƯỢC tự ý gọi pha tiếp theo.

## 5. Xử lý lỗi (Error Recovery)
- **Lỗi thiếu thư viện (Library Missing):** Nếu thiếu thư viện `docx` hoặc `openpyxl` để tạo file Word/Excel trực tiếp, Agent phải tự động chuyển sang viết báo cáo bằng định dạng Markdown (`05_san_pham/final_report.md`) với các bảng biểu dạng chữ vẽ ASCII, kèm theo hướng dẫn chi tiết để học viên tự chuyển đổi sang định dạng Word/Excel sau đó.
