---
id: "WF-PDCA-CLEAN-03"
name: "03-lam-sach-du-lieu"
description: "Chạy tập lệnh Python để làm sạch và chuẩn hóa dữ liệu thô trong pha ACT."
version: v2.0
status: Production-Ready
semantic_triggers: ['/03-lam-sach-du-lieu', '/03-lam-sach', 'lam sach du lieu', 'làm sạch dữ liệu']
owner: "STUDENT-AGENT"
skill_target: "03-data-cleaner"
hitl_timeout: "24h"
retry_policy: {max_attempts: 3, backoff: exponential_1s_2s_4s, fallback: "log_to_ACTION-LOG_and_report_human"}
---

# Workflow: 03 Làm Sạch Dữ Liệu

Sử dụng quy trình này trong pha ACT để đọc dữ liệu thô, thực thi các lệnh làm sạch và xuất tệp dữ liệu chuẩn hóa.

## 1. Điều kiện tiên quyết (Prerequisites)
- Tệp `01_dau_vao/data_raw.xlsx` đã được tạo.
- Tệp `02_nhat_ky_va_nhap/check_notes.md` ghi nhận các lỗi cần làm sạch đã được liệt kê trong pha CHECK.

## 2. Đầu vào (Inputs)
- Dữ liệu thô: `01_dau_vao/data_raw.xlsx`.
- Quy tắc làm sạch: `02_nhat_ky_va_nhap/check_notes.md` (ví dụ: đổi rating sang số thập phân, bỏ chữ tiền tệ).

## 3. Các bước thực hiện tuần tự (Step-by-Step Execution)
1. **Phân tích lỗi (Analyze Gaps):** Đọc dữ liệu thô và các ghi chú lỗi cần xử lý.
2. **Kích hoạt Kỹ năng (Execute Cleaner):**
   - Kích hoạt kỹ năng `03-data-cleaner` chạy script Python tại `.agents/skills/03-data-cleaner/scripts/clean_data.py` để làm sạch DataFrame.
   - Tập lệnh phải đảm bảo:
     1. Loại bỏ các dòng trùng lặp.
     2. Ghi nhận giá trị `unknown` cho các ô bị khuyết thiếu thông tin, tuyệt đối không được tự ý điền thông tin sai lệch.
     3. Chuẩn hóa giá cả về dạng số nguyên thuần túy (ví dụ: `50000`, `120000`).
     4. Chuẩn hóa đánh giá rating về dạng số thực float (ví dụ: `4.5`).
3. **Thực thi mã nguồn (Run Code):** Chạy tập lệnh Python và bắt lỗi (nếu có).
4. **Xuất tệp dữ liệu sạch (Export Clean File):** Ghi file sạch vào đường dẫn `04_ban_thao/data_clean.xlsx`.
5. **Cập nhật nhật ký (Update State Log):** Cập nhật nhật ký làm sạch `02_nhat_ky_va_nhap/cleaning_log.md` (ghi nhận chênh lệch số dòng trước và sau khi làm sạch) và cập nhật `02_nhat_ky_va_nhap/pdca_log.md` về việc hoàn thành pha ACT.

## 4. Maker-Checker Gate (Human Approval Point)
- **Halt Condition (Điều kiện dừng):** Sau khi làm sạch dữ liệu và xuất tệp `data_clean.xlsx`, Agent bắt buộc phải dừng lại.
- **Báo cáo kiểm duyệt (Review Report):** So sánh chênh lệch số lượng dòng dữ liệu thô vs dữ liệu sạch, số lượng ô trống đã được điền `unknown` hoặc xử lý mặc định, và cấu trúc định dạng các cột sau khi chuẩn hóa.
- **Lệnh xác nhận của Học viên:** Học viên kiểm tra trực quan tệp `data_clean.xlsx` và gõ `/04-phan-tich-va-bao-cao` để tiếp tục. Agent KHÔNG ĐƯỢC tự ý gọi pha tiếp theo.

## 5. Xử lý lỗi (Error Recovery)
- **Lỗi chạy tập lệnh (Python Crash):** Nếu pandas hoặc openpyxl bị crash do định dạng dữ liệu thô bị lỗi không thể parse, Agent phải viết code dự phòng (fallback) sử dụng các thư viện cơ bản của Python như `csv` hoặc `string`, ghi nhận lỗi vào `02_nhat_ky_va_nhap/issue_log.md` và thông báo cho học viên.
