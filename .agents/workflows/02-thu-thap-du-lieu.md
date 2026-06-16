---
id: "WF-PDCA-COLLECT-02"
name: "02-thu-thap-du-lieu"
description: "Thực hiện tìm kiếm thông tin và biên soạn tệp dữ liệu thô (raw data) trong pha DO."
version: v2.0
status: Production-Ready
semantic_triggers: ['/02-thu-thap-du-lieu', '/02-thu-thap', 'thu thap du lieu', 'thu thập dữ liệu']
owner: "STUDENT-AGENT"
skill_target: "02-data-collector"
hitl_timeout: "24h"
retry_policy: {max_attempts: 3, backoff: exponential_1s_2s_4s, fallback: "log_to_ACTION-LOG_and_report_human"}
---

# Workflow: 02 Thu Thập Dữ Liệu

Sử dụng quy trình này trong pha DO để tìm kiếm thông tin trên web, thu thập dữ liệu công khai và ghi vào tệp dữ liệu thô.

## 1. Điều kiện tiên quyết (Prerequisites)
- Kế hoạch trong `00_ke_hoach/task_brief.md` đã được học viên duyệt.
- `00_ke_hoach/success_criteria.md` xác định các tiêu chí số lượng dòng và cột cần có.

## 2. Đầu vào (Inputs)
- Định nghĩa chủ đề trong `00_ke_hoach/task_brief.md`.
- Danh sách các cột dữ liệu yêu cầu trong `00_ke_hoach/success_criteria.md`.

## 3. Các bước thực hiện tuần tự (Step-by-Step Execution)
1. **Nạp ngữ cảnh (Load Context):** Đọc yêu cầu và tiêu chí nghiệm thu từ thư mục `00_ke_hoach/`.
2. **Thực hiện nghiên cứu (Execute Research):**
   - Tìm kiếm thông tin trên web về các thực thể được yêu cầu (ví dụ: quán cafe, thương hiệu mỹ phẩm, ứng dụng phần mềm).
   - Xác minh nguồn dữ liệu công khai, không yêu cầu đăng nhập.
3. **Biên soạn dữ liệu thô có giới hạn (Compile Raw Bounded Data):**
   - Thu thập từ 15 đến 20 dòng dữ liệu duy nhất.
   - Giữ nguyên định dạng thô như trên web, KHÔNG chuẩn hóa đơn vị tiền tệ, chữ viết hoa, hay định dạng đánh giá rating (ví dụ: `50k`, `150.000d`, `4.5/5`).
4. **Ghi tập dữ liệu (Write Dataset):**
   - Tạo và ghi vào tệp dữ liệu thô `01_dau_vao/data_raw.xlsx`.
   - Cập nhật tệp đăng ký nguồn `01_dau_vao/source_registry.md` với các liên kết URLs và trạng thái nguồn (`verified`, `weak`, `missing`).
5. **Cập nhật nhật ký hoạt động (Update State Log):** Ghi nhận hoàn thành pha DO vào `02_nhat_ky_va_nhap/pdca_log.md` kèm theo số lượng dòng dữ liệu đã thu thập được.

## 4. Maker-Checker Gate (Human Approval Point)
- **Halt Condition (Điều kiện dừng):** Sau khi tải/ghi tệp dữ liệu thô `data_raw.xlsx` và `source_registry.md`, Agent bắt buộc phải dừng lại.
- **Báo cáo kiểm duyệt (Review Report):** Báo cáo số dòng đã thu thập, các nguồn dữ liệu đã xác thực, và cấu trúc cột của dữ liệu thô.
- **Lệnh xác nhận của Học viên:** Học viên kiểm tra trực quan tệp `data_raw.xlsx` và gõ `/03-lam-sach-du-lieu` để tiếp tục. Agent KHÔNG ĐƯỢC tự ý gọi pha tiếp theo.

## 5. Xử lý lỗi (Error Recovery)
- **Lỗi tìm kiếm (Search Outage):** Nếu công cụ tìm kiếm lỗi, thử các câu truy vấn khác hoặc mô phỏng dữ liệu thực tế của thị trường nếu đã biết, nhưng phải đánh dấu nguồn là `missing` trong registry. KHÔNG được tự chế ra URL giả không tồn tại.
