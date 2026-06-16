---
name: 02-data-collector
description: Thu thập dữ liệu từ file Excel gốc (raw data), kiểm tra tính toàn vẹn (schema validation) và chuyển đổi thành định dạng chuẩn bị làm sạch. Đóng vai trò là cổng Data Ingestion.
version: v1.0.0
status: Active
---

# Kỹ năng Data Collector (Chuyên gia Kỹ sư Dữ liệu - Data Engineer)

## 1. Mục tiêu
Đóng vai trò là chốt chặn đầu tiên (Ingestion Layer) trong quy trình Business Intelligence, kỹ năng này chịu trách nhiệm nạp dữ liệu thô (raw data) từ file Excel, quét cấu trúc (Schema Validation) để phát hiện các lỗi định dạng nghiêm trọng trước khi chuyển sang pha làm sạch.

## 2. Kích hoạt (Triggers)
- Tự động kích hoạt thông qua workflow `/02-thu-thap-du-lieu`.
- Khi người dùng cung cấp file dữ liệu thô (vd: `.xlsx`, `.csv`) và yêu cầu "kiểm tra cấu trúc", "load data", hoặc "thu thập dữ liệu".

## 3. Vai trò chuyên gia (Expert Identity)
**Kỹ sư Dữ liệu (Data Engineer)**: Tập trung vào tính toàn vẹn, tính khả dụng và khả năng truy xuất dữ liệu. Luôn làm việc bằng mã nguồn (hands-on with Code) thay vì chỉ phân tích lý thuyết.

## 4. Khung phương pháp luận (Methodology Framework)
- **ETL (Extract - Transform - Load):** Kỹ năng này phụ trách phần **Extract** (Trích xuất).
- **Data Contract / Schema Validation:** Mọi nguồn dữ liệu đầu vào đều phải được quét qua một hệ thống rào chắn (Quality Gate) để kiểm tra:
  - Tên các trường (Columns) có khớp với định nghĩa không.
  - Loại dữ liệu (Data types) có bị lệch (VD: Chữ lẫn vào số, Ngày tháng sai định dạng) không.

## 5. Hướng dẫn chi tiết
1. **Quét và Nạp (Extract):**
   - Xác định file đầu vào tại `01_dau_vao/raw_data.xlsx`.
   - Chạy script Python `scripts/collect_data.py` để nạp dữ liệu.
2. **Kiểm tra tính toàn vẹn (Validate):**
   - Script tự động tính toán tổng số dòng, cột.
   - Nhận diện kiểu dữ liệu của từng cột.
   - Kiểm tra sơ bộ số lượng giá trị rỗng (Null/NaN).
3. **Ghi nhật ký (Logging):**
   - Cập nhật kết quả kiểm tra vào `02_nhat_ky_va_nhap/schema_validation.md`.
   - Nếu phát hiện lỗi quá lớn (ví dụ không mở được file), trả về lỗi (Raise Error) ngay lập tức, từ chối đưa qua bước làm sạch.

## 6. Các ràng buộc nghiêm ngặt
- **Tuyệt đối không sửa dữ liệu:** Kỹ năng này CHỈ NẠP VÀ KIỂM TRA (Read-only). Cấm mọi hành vi biến đổi dữ liệu (Transform/Clean) tại bước này.
- **Thực thi bằng Code:** Bắt buộc phải chạy `collect_data.py`. Không được dùng trí tưởng tượng (Hallucination) để đoán cấu trúc dữ liệu.

## 7. Xử lý lỗi
- **File not found:** Nếu không thấy `raw_data.xlsx`, báo lỗi ngay: "CẢNH BÁO: Không tìm thấy nguồn dữ liệu đầu vào."
- **Unsupported Format:** Nếu định dạng không phải `.xlsx` hoặc `.csv`, chặn tiến trình.

## 8. Tài nguyên & Tham chiếu
- **Tài liệu phương pháp luận:** 
- **Script Thực thi:** `scripts/collect_data.py`
- **Đường dẫn thư mục liên quan:**
  - Đầu vào: `01_dau_vao/raw_data.xlsx`
  - Output log: `02_nhat_ky_va_nhap/schema_validation.md`

## 9. Quy trình nghiệm thu
- [ ] Chạy thành công `scripts/collect_data.py`.
- [ ] File log `schema_validation.md` được sinh ra với đầy đủ thông tin về tổng số dòng, số cột và kiểu dữ liệu.
