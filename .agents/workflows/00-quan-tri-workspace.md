---
id: "WF-PDCA-ADMIN-00"
name: "00-quan-tri-workspace"
description: "Quản trị và bảo trì Workspace: Kiểm tra sức khỏe, tự phục hồi tệp tin lỗi, và hỗ trợ dọn dẹp lưu trữ (99_luu_tru)."
version: "v2.0"
status: "Production-Ready"
semantic_triggers: ['/00-quan-tri-workspace', '/00-quan-tri', 'quan tri workspace', 'dọn dẹp workspace', 'clean workspace']
owner: "STUDENT-AGENT"
skill_target: ""
hitl_timeout: "24h"
retry_policy: {max_attempts: 3, backoff: exponential_1s_2s_4s, fallback: "log_to_ACTION-LOG_and_report_human"}
---

# Workflow: 00 Quản Trị Workspace

Sử dụng quy trình này định kỳ để kiểm tra sức khỏe hệ thống (Health Check), tự động sửa lỗi cấu trúc và dọn dẹp, lưu trữ tài liệu cũ sau mỗi chu kỳ PDCA.

## 1. Điều kiện tiên quyết (Prerequisites)
- Workspace đã được tải về IDE Google Antigravity.
- Có sẵn hai tệp cấu hình cốt lõi `AGENTS.md` và `GEMINI.md` ở thư mục gốc.

## 2. Đầu vào (Inputs)
- Yêu cầu hành động từ học viên: `check` (kiểm tra sức khỏe) hoặc `archive` (lưu trữ/dọn dẹp).
- Nếu không chỉ định, mặc định hệ thống sẽ thực hiện `check`.

## 3. Các bước thực hiện tuần tự (Step-by-Step Execution)

### Bước 1: Quét sức khỏe hệ thống (Health Check)
1. Kiểm tra sự tồn tại của 8 thư mục ranh giới: `00_ke_hoach`, `01_dau_vao`, `02_nhat_ky_va_nhap`, `03_cong_cu`, `04_ban_thao`, `05_san_pham`, `06_ban_giao`, `99_luu_tru`.
2. Kiểm tra các tệp tin theo dõi tối thiểu: `02_nhat_ky_va_nhap/pdca_log.md` và `02_nhat_ky_va_nhap/issue_log.md`.

### Bước 2: Tự sửa lỗi và Phục hồi (Self-Healing / Bootstrap)
1. Nếu thiếu bất kỳ thư mục con nào, tự động khởi tạo lại thư mục đó kèm tệp ẩn `.gitkeep`.
2. Nếu thiếu tệp nhật ký `pdca_log.md`, tự động khởi tạo lại tệp này với trạng thái trống và ghi nhận hoạt động `Self-healing: Re-initialized track logs`.
3. Nếu thiếu tệp `issue_log.md` hoặc `source_registry.md`, tự động tạo lại các tệp mẫu rỗng.

### Bước 3: Dọn dẹp và Lưu trữ (Cleanup & Archive - Chỉ chạy khi có yêu cầu "archive")
1. Quét các tệp tin kết quả cũ trong thư mục `04_ban_thao/` và `06_ban_giao/`.
2. Di chuyển (Move) toàn bộ các tệp tin kết quả cũ này vào thư mục `99_luu_tru/` dưới dạng thư mục con được đặt tên theo mốc thời gian (ví dụ: `99_luu_tru/run_YYYYMMDD/`).
3. Ghi nhận nhật ký dọn dẹp sạch sẽ vào `pdca_log.md`.

## 4. Cổng nghiệm thu (Exit Gates)
- Môi trường làm việc đạt trạng thái chuẩn hóa (đầy đủ thư mục và tệp nhật ký).
- Xuất báo cáo trạng thái: *"Hệ thống hoạt động Bình thường. Không phát hiện lỗi cấu trúc."* hoặc *"Đã hoàn thành dọn dẹp và di chuyển tài liệu cũ vào thư mục 99_luu_tru."*

## 5. Xử lý lỗi (Error Recovery)
- **Lỗi quyền ghi tệp (Write Permission Fail):** Nếu Agent không thể tự tạo hoặc di chuyển tệp do phân quyền thư mục trên Windows, Agent phải in ra câu lệnh PowerShell tương ứng (ví dụ: `Move-Item`) để học viên phê duyệt chạy trực tiếp.
