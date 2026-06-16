---
name: 00-Workspace-Boundaries
type: L1-Rule
priority: 2
trigger: always_on
---

> [!IMPORTANT]
> Override Priority: TIER 2


# Nguyên tắc 00: Giới hạn Workspace & Quyền truy cập tệp tin

## 1. Mục tiêu
Ngăn chặn Agent tự ý sửa đổi các tệp tin hệ thống, truy cập các thư mục nằm ngoài phạm vi bài học hoặc thực hiện các thao tác phá hủy hệ thống tệp tin.

## 2. Ràng buộc về thư mục làm việc (Directory Constraints)
- **Đường dẫn gốc:** Mọi hoạt động của Agent bắt buộc phải nằm gọn trong thư mục workspace được chỉ định (`ThucHanh_AI4A_Buoi2`).
- **Cấm truy xuất ngoài:** Tuyệt đối KHÔNG sử dụng đường dẫn tương đối để đi lên thư mục cha (như `..`), đường dẫn tuyệt đối trỏ về gốc hệ thống (như `C:\`, `/`), hoặc các biến môi trường trỏ đến thư mục người dùng (như `%USERPROFILE%`, `~`).
- **Thư mục chỉ đọc (Read-Only):**
  - Thư mục `.agents/` và `.gemini/` là chỉ đọc. Agent tuyệt đối không được tự ý sửa đổi các tệp luật, quy trình hoặc kỹ năng trong quá trình thực hành dữ liệu của học viên.
  - Tệp dữ liệu thô `01_dau_vao/data_raw.xlsx` phải được giữ nguyên sau khi hoàn thành pha DO.

## 3. Ràng buộc thực thi lệnh (Command Execution Constraints)
- **Các lệnh bị cấm:**
  - Lệnh xóa tệp tin: `rm`, `del`, `Remove-Item`, `shred`.
  - Lệnh can thiệp hệ thống: `format`, `fdisk`, `reg`, `systemctl`.
  - Lệnh mạng: `curl`, `wget`, `ssh` (ngoại trừ các lệnh gọi API công khai đã được định nghĩa sẵn trong quy trình).
- **Giao thức thực thi:**
  - Trước khi viết hoặc chạy bất kỳ tập lệnh Python nào, Agent phải ghi lại log mô tả ngắn gọn:
    1. Đường dẫn tệp mục tiêu cần chạy.
    2. Mục đích hoạt động của tập lệnh.
    3. Các thư viện được import (chỉ cho phép thư viện chuẩn + `pandas`, `openpyxl`).

## 4. Ràng buộc kiểm soát phiên bản (Version Control Guardrails)
- **Không ghi đè trực tiếp:** Agent không được phép ghi đè trực tiếp lên tệp `data_raw.xlsx` when làm sạch dữ liệu.
- **Theo dõi lịch sử thay đổi:** Mọi thay đổi trong báo cáo hoặc bảng tính phải tạo ra một phiên bản mới (ví dụ: `final_report_v2.docx`) trừ khi học viên yêu cầu rõ ràng việc ghi đè.
- **Lưu trữ lịch sử:** Các phiên bản cũ cần lưu trữ phải được chuyển vào thư mục `99_luu_tru/old_versions/`.
