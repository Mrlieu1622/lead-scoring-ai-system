---
name: 02-Data-Safety-Rules
type: L1-Rule
priority: 2
trigger: always_on
---

> [!IMPORTANT]
> Override Priority: TIER 2


# Nguyên tắc 02: An toàn dữ liệu, Bảo mật & Xác thực nguồn gốc

## 1. Mục tiêu
Đảm bảo không có bất kỳ thông tin cá nhân nhạy cảm hoặc dữ liệu có bản quyền nào bị xử lý trong workspace, đồng thời mọi điểm dữ liệu đều có nguồn gốc công khai, xác thực.

## 2. Bảo vệ thông tin cá nhân (PII Guard)
Agent phải chủ động quét tất cả dữ liệu đầu vào và đầu ra để loại bỏ:
- **Họ tên & Danh tính:** Thay thế bằng các nhãn chung (ví dụ: "Khách hàng A", "Cửa hàng X").
- **Thông tin liên lạc:** Số điện thoại, địa chỉ email, liên kết mạng xã hội cá nhân.
- **Mã định danh:** Mã số học viên, số căn cước công dân, biển số xe.
- **Thông tin đăng nhập:** API keys, mật khẩu, đường dẫn kết nối cơ sở dữ liệu (thay thế bằng biến môi trường hoặc dữ liệu giả lập).

Nếu phát hiện thông tin cá nhân (PII), Agent phải DỪNG THỰC THI NGAY LẬP TỨC, cô lập tệp tin lỗi và cảnh báo cho học viên.

## 3. Giao thức xác thực nguồn gốc (Source Traceability)
- **Sổ đăng ký nguồn:** Mọi dữ liệu thu thập từ web bắt buộc phải đăng ký vào tệp `01_dau_vao/source_registry.md`.
- **Các trường thông tin yêu cầu:**
  - `data_id`: Mã định danh dòng dữ liệu.
  - `source_url`: Liên kết HTTP có thể kiểm chứng trực tiếp.
  - `access_timestamp`: Thời gian truy cập thu thập dữ liệu.
  - `source_status`:
    - `verified` (Xác thực): Trang web có uy tín cao, cơ sở dữ liệu chính phủ, viện nghiên cứu công bố.
    - `weak` (Yếu): Blog cá nhân, bình luận diễn đàn, bài đăng mạng xã hội chưa kiểm chứng.
    - `missing` (Thiếu): Không tìm thấy nguồn gốc xác thực (cần cắm cờ cảnh báo thủ công).

## 4. Ngăn chặn ảo tưởng (Hallucination Prevention)
- Nghiêm cấm Agent tự ý "bịa đặt" hoặc "sáng tạo" ra các thông tin thực tế (như địa chỉ cửa hàng hoặc giá bán đồ uống) khi quá trình tìm kiếm thất bại.
- Nếu không tìm thấy dữ liệu thực tế, bắt buộc phải ghi nhận là `N/A` hoặc `unknown` và ghi vào nhật ký lỗi `02_nhat_ky_va_nhap/issue_log.md`.
