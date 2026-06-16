# Nhật ký Kiểm duyệt Chất lượng Dữ liệu (CHECK Notes)

Dự án: AI Lead Scoring & Automation - Ngành Bất Động Sản

## 1. Kiểm tra Cấu trúc Dữ liệu (Schema Validation)
Tệp `04_ban_thao/data_clean.xlsx` đã được kiểm tra:
- **Số dòng dữ liệu:** 10 dòng (hoàn thành 100% dữ liệu mẫu).
- **Các cột bắt buộc:**
  - `Mã KH`: Hợp lệ (dạng text chuỗi: KH001, KH002...).
  - `Họ tên`: Hợp lệ, không có giá trị Null.
  - `Số điện thoại`: Hợp lệ.
  - `Nhu cầu`: Đầy đủ thông tin mô tả chi tiết để phân tích.
  - `Điểm số`: Định dạng số nguyên (integer), nằm trong phạm vi 50 - 150.
  - `Phân loại`: Phân loại chính xác (VIP/Siêu tiềm năng, Tiềm năng, Không tiềm năng).
  - `Lý do chấm điểm`: Chứa thông tin giải thích chi tiết lý do cộng/trừ điểm.
  - `Trạng thái duyệt`: Giá trị mặc định `"Chờ duyệt"`.

## 2. Kiểm duyệt Quy tắc Nghiệp vụ (Scoring Validation)
- **VIP/Siêu tiềm năng (+50):** 3 leads (KH001, KH002, KH003) khớp chính xác các từ khóa cao cấp ("Biệt thự đơn lập", "Penthouse", "Vinhomes", "Quỹ đất công nghiệp", "tài chính mạnh", ngân sách >= 20 tỷ). Điểm số: 150.
- **Không tiềm năng / Rác (-50):** 4 leads (KH004, KH005, KH006, KH007) khớp dấu hiệu phi thực tế (nhà Q1 giá 1-2 tỷ) và các dấu hiệu không thiện chí/quảng cáo. Điểm số: 50.
- **Tiềm năng (Giữ nguyên):** 3 leads tầm trung (3-10 tỷ hoặc cần hỗ trợ ngân hàng). Điểm số: 100.

## 3. Kiểm định Web App
- Giao diện Premium Dark Mode hoạt động mượt mà.
- File upload SheetJS parse tốt dữ liệu Excel.
- Tính năng edit Human-in-the-loop tự động cập nhật phân loại theo điểm số.
- Nút xuất file Excel tải xuống đúng định dạng và đúng dữ liệu đã chỉnh sửa.
