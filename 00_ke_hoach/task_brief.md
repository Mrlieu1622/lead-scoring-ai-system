# TASK BRIEF: CHUYỂN ĐỔI BÁO CÁO NGÂN SÁCH - BETA SOLUTIONS (TỐI ƯU HÓA)

## 1. Thông tin chung
* **Dự án:** Hệ thống giám sát ngân sách thời gian thực (Real-time Budget Dashboard).
* **Đối tác:** Công ty Cổ phần Beta Solutions.
* **Mục tiêu:** Chuyển đổi Dashboard bán hàng Demo thành Dashboard quản lý chi tiêu ngân sách nâng cao của Beta Solutions.
* **Vai trò:** Trưởng phòng Tài chính kiêm Fullstack Developer.
* **Giai đoạn:** Tối ưu hóa nâng cấp KPIs liên Quý (Q-o-Q) và Biểu đồ phòng ban.

## 2. Dữ liệu đầu vào (Input)
* Tệp Excel dữ liệu: [TH_ngan_sach_phong_ban.xlsx](file:///d:/PDCA_Workspace_Template/01_dau_vao/B6/TH_ngan_sach_phong_ban.xlsx)
* Quy chuẩn thương hiệu Beta: Tím Hoàng Gia (`#7C3AED` - Ngân sách), Xanh Ngọc (`#06B6D4` - Chi tiêu), Hồng San Hô (`#F43F5E` - Vượt định mức), Xanh Bạc Hà (`#14B8A6` - Tiết kiệm).

## 3. Đầu ra mong muốn (Output)
* **API Backend:** `/api/data` hỗ trợ các tham số lọc `quy` và `phong_ban`. Cung cấp thêm so sánh liên quý (Q-o-Q) cho các KPIs và trả về dữ liệu so sánh Ngân Sách vs Chi Tiêu của từng bộ phận.
* **Giao diện Frontend:** `dashboard.html` hiển thị:
  * 3 thẻ KPI: Tổng ngân sách, Tổng chi tiêu, Giao dịch vượt định mức. Dưới mỗi thẻ có nhãn so sánh tăng/giảm so với quý trước (Q-o-Q).
  * 1 biểu đồ cột ghép (Ngân sách vs Chi tiêu theo Quý).
  * 1 biểu đồ tròn/donut hoặc biểu đồ cột mới thể hiện **Ngân sách vs Chi tiêu của từng phòng ban**.
  * Thanh bộ lọc tương tác: Chọn Quý và Bộ phận.
* **Đóng gói bàn giao:** Tệp tin nén `TH_NganSach_Beta.zip` có đặt mật khẩu chứa tệp `dashboard.html`.

## 4. Ràng buộc kỹ thuật (Constraints)
* Bắt buộc dùng đúng mã màu thương hiệu của Beta Solutions.
* Tần suất cập nhật Real-time: 2 giây/lần.
