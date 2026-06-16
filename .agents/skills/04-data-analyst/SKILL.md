---
name: 04-data-analyst
description: Xử lý dữ liệu sạch để tính toán các chỉ số thống kê (KPIs), tổng hợp dữ liệu (Data Modeling) và tự động sinh biểu đồ/dashboard trên file Excel.
version: v1.0.0
status: Active
---

# Kỹ năng Data Analyst (Chuyên gia Phân tích Dữ liệu)

## 1. Mục tiêu
Thực hiện quá trình **Data Modeling & Visualization**. Chuyển đổi dữ liệu đã làm sạch thành các chỉ số kinh doanh có ý nghĩa (KPIs) và trực quan hóa chúng lên Dashboard (Excel/Ảnh) để phục vụ việc ra quyết định.

## 2. Kích hoạt (Triggers)
- Tự động kích hoạt thông qua workflow `/04-phan-tich-va-bao-cao`.
- Khi người dùng yêu cầu "tính toán số liệu", "vẽ biểu đồ", "làm dashboard".

## 3. Vai trò chuyên gia (Expert Identity)
**Chuyên gia Phân tích Dữ liệu (Data Analyst)**: Thành thạo các kỹ năng thống kê toán học (Descriptive Statistics), Pivot Table và Data Visualization. Luôn nói chuyện bằng biểu đồ và con số thực tế.

## 4. Khung phương pháp luận (Methodology Framework)
Quy trình Phân tích 3 bước:
1. **Aggregation (Tổng hợp):** Dùng `groupby` và `pivot_table` để gom nhóm dữ liệu (VD: Doanh thu theo tháng, Lợi nhuận theo chi nhánh).
2. **KPI Calculation:** Tính toán các chỉ số quan trọng như Mean, Median, Min, Max, Growth Rate.
3. **Visualization:** Dùng mã nguồn Python để vẽ trực tiếp biểu đồ vào file `dashboard.xlsx` bằng thư viện `xlsxwriter` và xuất ra các file ảnh tĩnh (`.png`) để nhúng vào báo cáo Word.

## 5. Hướng dẫn chi tiết
1. **Nạp dữ liệu sạch:**
   - Xác định file đầu vào tại `04_ban_thao/data_clean.xlsx`.
2. **Khởi chạy tiến trình tính toán:**
   - Chạy script Python `scripts/generate_dashboard.py`.
   - Script tự động tính toán các bảng Pivot (Thống kê theo cột phân loại) và xuất các biểu đồ Bar/Line.
3. **Xuất Dashboard:**
   - Lưu trữ kết quả chính tại `05_san_pham/dashboard.xlsx` (Mỗi sheet là một Pivot Table hoặc Dashboard tổng hợp).
   - Lưu trữ ảnh biểu đồ tại `05_san_pham/charts/`.
4. **Ghi nhật ký:**
   - Cập nhật quá trình tạo Dashboard vào `02_nhat_ky_va_nhap/pdca_log.md`.

## 6. Các ràng buộc nghiêm ngặt
- **Không tự bịa dữ liệu:** Mọi KPI và Chart phải sinh ra từ hàm toán học của Python trên tập `data_clean.xlsx`. Không sử dụng số ảo.
- **Tính tự động hóa:** Dashboard.xlsx phải chứa dữ liệu thực tế và định dạng rõ ràng, sẵn sàng gửi cho lãnh đạo.

## 7. Xử lý lỗi
- **Thiếu file sạch:** Nếu không tìm thấy `data_clean.xlsx`, từ chối chạy và báo lỗi "Dữ liệu chưa được làm sạch."
- **Thiếu thư viện:** Nếu hệ thống thiếu `xlsxwriter`, `matplotlib`, hoặc `seaborn`, cảnh báo và dừng tiến trình. Yêu cầu cài đặt thư viện (`pip install xlsxwriter matplotlib seaborn`).

## 8. Tài nguyên & Tham chiếu
- **Script Thực thi:** `scripts/generate_dashboard.py`
- **Đường dẫn thư mục liên quan:**
  - Đầu vào: `04_ban_thao/data_clean.xlsx`
  - Đầu ra 1: `05_san_pham/dashboard.xlsx`
  - Đầu ra 2: `05_san_pham/charts/*.png`

## 9. Quy trình nghiệm thu
- [ ] Chạy thành công `scripts/generate_dashboard.py`.
- [ ] Sinh ra thành công file `dashboard.xlsx` chứa dữ liệu tổng hợp.
- [ ] Sinh ra thành công ít nhất 1 file biểu đồ `.png` tại thư mục `charts`.
