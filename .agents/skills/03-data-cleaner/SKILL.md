---
name: 03-data-cleaner
description: Tự động hóa quá trình làm sạch dữ liệu (Data Cleaning & Transformation). Loại bỏ duplicates, xử lý Nulls, ép kiểu dữ liệu và xuất dữ liệu sạch chuẩn bị cho phân tích.
version: v1.0.0
status: Active
---

# Kỹ năng Data Cleaner (Chuyên gia Kỹ sư Dữ liệu - Data Engineer)

## 1. Mục tiêu
Thực hiện quá trình Transform trong luồng ETL. Chuyển đổi dữ liệu thô (đã qua bước validate của Data Collector) thành tập dữ liệu sạch, có cấu trúc chặt chẽ để phục vụ tính toán Dashboard.

## 2. Kích hoạt (Triggers)
- Được gọi tự động trong quy trình `/03-lam-sach-du-lieu`.
- Khi người dùng cung cấp file dữ liệu thô và yêu cầu "làm sạch", "xử lý null", "xóa trùng lặp".

## 3. Vai trò chuyên gia (Expert Identity)
**Kỹ sư Dữ liệu (Data Engineer)**: Tập trung vào chất lượng dữ liệu (Data Quality). Áp dụng các kỹ thuật xử lý tự động hóa thay vì thao tác bằng tay trên Excel.

## 4. Khung phương pháp luận (Methodology Framework)
Quy trình làm sạch 4 bước tiêu chuẩn doanh nghiệp:
1. **Deduplication:** Xóa bỏ các bản ghi trùng lặp hoàn toàn.
2. **Imputation / Drop Nulls:** Xử lý các giá trị bị thiếu.
3. **Type Casting:** Đảm bảo các cột số là kiểu Numeric, cột ngày là kiểu Datetime.
4. **Outlier Filtering:** (Tùy chọn) Lọc bỏ các giá trị dị biệt theo IQR nếu được yêu cầu.

## 5. Hướng dẫn chi tiết
1. **Nạp dữ liệu:**
   - Xác định file đầu vào tại `01_dau_vao/raw_data.xlsx`.
2. **Khởi chạy tiến trình làm sạch:**
   - Chạy script Python `scripts/clean_data.py`.
   - Script sẽ tự động xóa duplicates và điền/bỏ qua các giá trị null dựa trên loại dữ liệu (ví dụ: Số thì điền 0 hoặc trung bình, Text thì điền 'Unknown').
3. **Xuất kết quả:**
   - File kết quả bắt buộc lưu tại `04_ban_thao/data_clean.xlsx`.
4. **Ghi nhật ký:**
   - Ghi lại các bước đã làm (số dòng bị xóa, số null đã xử lý) vào `02_nhat_ky_va_nhap/pdca_log.md`.

## 6. Các ràng buộc nghiêm ngặt
- **Không phá vỡ cấu trúc cột:** Phải giữ nguyên cấu trúc cột gốc (trừ khi có lệnh drop cột).
- **Phải có file đầu ra:** Kỹ năng này bắt buộc phải sinh ra `data_clean.xlsx`.

## 7. Xử lý lỗi
- **Thiếu file:** Nếu không tìm thấy `raw_data.xlsx`, dừng lại và thông báo lỗi.
- **Empty DataFrame:** Nếu sau khi drop null mà dữ liệu trống trơn, cảnh báo: "Lỗi: File dữ liệu rỗng sau khi làm sạch."

## 8. Tài nguyên & Tham chiếu
- **Script Thực thi:** `scripts/clean_data.py`
- **Đường dẫn thư mục liên quan:**
  - Đầu vào: `01_dau_vao/raw_data.xlsx`
  - Đầu ra: `04_ban_thao/data_clean.xlsx`

## 9. Quy trình nghiệm thu
- [ ] Chạy thành công `scripts/clean_data.py`.
- [ ] Tệp `data_clean.xlsx` được sinh ra thành công và mở được trên Excel.
