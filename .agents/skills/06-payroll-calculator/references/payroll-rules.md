# Quy tắc Tính lương (Payroll Rules)

Tài liệu này định nghĩa các quy tắc tài chính bắt buộc để tính toán Lương thực lĩnh (Net Salary) từ dữ liệu ERP.

## 1. Công thức cơ bản (Basic Formula)
Công thức chuẩn hóa được áp dụng cho mọi nhân viên trong hệ thống:
`Net_Salary = Base_Salary + Bonus - Penalty`

## 2. Quy tắc Zero-Floor
Để đảm bảo tính hợp lệ của số liệu tài chính, không bao giờ cho phép lương thực lĩnh mang giá trị âm. 
- Nếu một nhân sự có khoản phạt (`Penalty`) lớn hơn tổng thu nhập (`Base_Salary + Bonus`), mức lương thực lĩnh phải được gán giá trị bằng `0`.
- **Mã giả (Pseudo-code):**
  ```python
  net_salary = base_salary + bonus - penalty
  if net_salary < 0:
      net_salary = 0
  ```

## 3. Định dạng Dữ liệu (Data Formatting)
- Cột `Net_Salary` phải được lưu trữ ở định dạng số nguyên (Integer), không có phần thập phân.
- Các cột `Base_Salary`, `Bonus`, `Penalty` cũng phải được làm sạch và chuyển về số nguyên trước khi tính toán để tránh lỗi do dấu phẩy động.

## 4. Xử lý Dữ liệu trống (Missing Values)
- Nếu bất kỳ cột `Base_Salary`, `Bonus`, hoặc `Penalty` bị trống (Null/NaN), phải điền mặc định bằng `0` trước khi tính toán.
