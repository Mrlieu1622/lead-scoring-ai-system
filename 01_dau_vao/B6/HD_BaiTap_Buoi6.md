# HƯỚNG DẪN BÀI TẬP THỰC HÀNH BUỔI 6: XÂY DỰNG REAL-TIME BUDGET DASHBOARD - BETA SOLUTIONS

Chào mừng bạn đến với bài tập thực hành Buổi 6. Trong bài tập này, bạn sẽ đóng vai trò là một **Kỹ sư Dữ liệu kiêm UI/UX Developer** để chuyển đổi hệ thống Dashboard giám sát từ phiên bản Demo (Công ty Alpha) sang phiên bản thực tế cho **Công ty Cổ phần Beta Solutions**.

Phương pháp tiếp cận của chúng ta sẽ tuân thủ nghiêm ngặt chu trình **PDCA (Plan - Do - Check - Act)** nhằm xây dựng tư duy hệ thống và thói quen làm việc chuẩn mực.

---

## 🗺️ TỔNG QUAN HỆ THỐNG & DỮ LIỆU ĐẦU VÀO

Hệ thống của chúng ta hoạt động theo mô hình Client-Server đơn giản nhưng mạnh mẽ:
1. **Backend (`server.py`):** Viết bằng Python, sử dụng thư viện `pandas` để đọc tệp Excel dữ liệu thô, thực hiện các phép tính toán thống kê (KPIs, Groupby, Top 5) và trả về định dạng JSON qua API `/api/data`.
2. **Frontend (`dashboard.html`):** Sử dụng HTML, CSS (Glassmorphism & Dark Mode) và Javascript để gọi API từ Backend mỗi 2 giây, cập nhật số liệu bằng hiệu ứng đếm số mượt mà (Smooth Counter) và vẽ biểu đồ động bằng thư viện `ApexCharts`.

### 📊 Cấu trúc Tệp Dữ liệu Thực hành (`TH_ngan_sach_phong_ban.xlsx`)
Tệp dữ liệu thực hành của bạn bao gồm 300 dòng giao dịch ngân sách với các cột sau:
* `Ma_Giao_Dich`: Mã định danh giao dịch.
* `Quy`: Quý thực hiện (ví dụ: `Q1-2026`, `Q2-2026`,...).
* `Phong_Ban`: Bộ phận phụ trách (`Cong Nghe`, `Marketing`, `Kinh Doanh`, `Nhan Su`, `Ke Toan`, `Van Phong`).
* `Hang_Muc_Chi`: Danh mục chi tiêu (ví dụ: Quảng cáo, Thiết bị, Lương,...).
* `Ngan_Sach_Duyet`: Số tiền ngân sách được phê duyệt (VNĐ).
* `Chi_Tieu_Thuc_Te`: Số tiền thực tế đã chi tiêu (VNĐ).
* `Chenh_Lech`: Giá trị chênh lệch (`Ngan_Sach_Duyet - Chi_Tieu_Thuc_Te`).
* `Trang_Thai`: Trạng thái chi tiêu (trong tệp Excel được ghi là `'Vuot Ngan Sach'` hoặc `'Tiet Kiem'` - không có dấu tiếng Việt).

---

## 🔄 QUY TRÌNH THỰC HIỆN THEO 4 BƯỚC PDCA

### 📌 PHA 1: PLAN (LẬP KẾ HOẠCH & XÁC ĐỊNH MỤC TIÊU)

Trước khi viết bất kỳ dòng mã nào, bạn cần lập kế hoạch và xác định rõ ràng các tiêu chí thành công.

> [!IMPORTANT]
> **Yêu cầu bắt buộc:**
> Hãy tạo hoặc cập nhật tệp `00_ke_hoach/task_brief.md` và `00_ke_hoach/success_criteria.md` của bạn để mô tả:
> 1. Mục tiêu chuyển đổi sang thương hiệu Beta Solutions.
> 2. Các chỉ số KPI cần hiển thị trên Dashboard.
> 3. Các ràng buộc về màu sắc và bố cục theo Brand Guideline của Beta.

#### ❓ Câu hỏi gợi mở Socratic (Hãy tự trả lời trước khi làm):
* *Làm thế nào để đo lường hiệu quả sử dụng ngân sách của một phòng ban? Chỉ số nào quan trọng nhất (Tổng ngân sách, Thực chi, hay Tỷ lệ vượt)?*
* *Bảng màu của Beta Solutions yêu cầu những màu nào? Màu sắc nào đại diện cho sự tích cực (tiết kiệm) và tiêu cực (vượt hạn mức)?*

---

### 🚀 PHA 2: DO (TRIỂN KHAI BACKEND & FRONTEND)

#### 🛠️ Nhiệm vụ 1: Cấu hình và Tính toán logic tại Backend (`server.py`)

Mở tệp [server.py](file:///d:/PDCA_Workspace_Template/01_dau_vao/B6/server.py) và tiến hành điều chỉnh. Bạn cần thực hiện các công việc sau:

1. **Thay đổi tệp dữ liệu nguồn:**
   Chuyển đổi biến `EXCEL_FILE` từ tệp Demo sang tệp thực hành:
   ```python
   EXCEL_FILE = "TH_ngan_sach_phong_ban.xlsx"
   ```

2. **Cập nhật logic tính toán KPIs:**
   Thay vì tính toán doanh thu và chi phí như của Alpha, đối với Beta Solutions bạn cần tính toán:
   * **Tổng ngân sách được duyệt** (Sum của `Ngan_Sach_Duyet`).
   * **Tổng chi tiêu thực tế** (Sum của `Chi_Tieu_Thuc_Te`).
   * **Hiệu số chênh lệch tích lũy** (Tổng ngân sách - Tổng chi tiêu).
   * **Số lượng giao dịch bị vượt ngân sách** (Đếm số dòng có `Trang_Thai` là `"Vuot Ngan Sach"` hoặc `Chenh_Lech < 0`).

   *Gợi ý khung mã Python cần điền:*
   ```python
   # TODO: Thực hiện tính toán KPIs cho Beta Solutions
   tong_ngan_sach = float(df_slice["Ngan_Sach_Duyet"].sum())
   tong_chi_tieu = float(df_slice["Chi_Tieu_Thuc_Te"].sum())
   hieu_so = tong_ngan_sach - tong_chi_tieu  # Giá trị dương = Tiết kiệm, Âm = Vượt
   so_don_vuot = int((df_slice["Chi_Tieu_Thuc_Te"] > df_slice["Ngan_Sach_Duyet"]).sum())
   ```

3. **Cập nhật dữ liệu biểu đồ:**
   * **Biểu đồ Cột & Đường (Theo Quý):** Nhóm theo cột `Quy` và tính tổng `Ngan_Sach_Duyet` và `Chi_Tieu_Thuc_Te`.
   * **Biểu đồ Tròn (Theo Phòng Ban):** Nhóm theo cột `Phong_Ban` và tính tổng `Chi_Tieu_Thuc_Te` để xem phòng ban nào tiêu tiền nhiều nhất.
   * **Bảng Top 5 hạng mục chi tiêu:** Nhóm theo `Hang_Muc_Chi`, sắp xếp giảm dần theo `Chi_Tieu_Thuc_Te` để hiển thị 5 hạng mục tiêu tốn nhất.

#### 🎨 Nhiệm vụ 2: Thiết kế giao diện và Áp dụng Brand Guideline tại Frontend (`dashboard.html`)

Mở tệp [dashboard.html](file:///d:/PDCA_Workspace_Template/01_dau_vao/B6/dashboard.html). Dựa vào tài liệu thiết kế thương hiệu của Beta Solutions (`TH_brand_guideline_beta.txt`), hãy thực hiện các cải tiến UI/UX sau:

1. **Cập nhật hệ thống biến CSS Color Tokens:**
   Thay đổi các màu sắc của Alpha thành bảng màu hoàng gia của Beta:
   ```css
   :root {
       --primary-purple: #7C3AED;   /* Tím Hoàng Gia - Ngân sách duyệt */
       --primary-teal: #06B6D4;     /* Xanh Ngọc - Chi tiêu thực tế */
       --secondary-pink: #F43F5E;    /* Hồng San Hô - Vượt ngân sách */
       --secondary-mint: #14B8A6;    /* Xanh Bạc Hà - Tiết kiệm/Hiệu quả */
       
       --glass-bg: rgba(30, 30, 46, 0.65); /* Nền tối sang trọng của Beta */
       --glass-border: rgba(255, 255, 255, 0.05);
       --text-primary: #f8fafc;
       --text-secondary: #a1a1aa;
   }
   ```

2. **Chỉnh sửa cấu trúc 4 thẻ KPI:**
   * **Thẻ 1:** Tổng Ngân Sách Được Duyệt (Sử dụng màu `--primary-purple`).
   * **Thẻ 2:** Tổng Chi Tiêu Thực Tế (Sử dụng màu `--primary-teal`).
   * **Thẻ 3:** Chênh Lệch Ngân Sách (Nếu dương hiển thị màu Mint đại diện cho tiết kiệm, nếu âm hiển thị màu Pink đại diện cho thâm hụt).
   * **Thẻ 4:** Số Giao Dịch Vượt Định Mức (Sử dụng màu `--secondary-pink` làm cảnh báo).

3. **Cập nhật cấu hình màu sắc trong ApexCharts:**
   Trong phần mã Javascript khởi tạo biểu đồ, hãy thay đổi mảng màu tương ứng:
   * **Biểu đồ Cột:** Cần dùng màu Tím Hoàng gia (`#7C3AED`) cho cột Ngân sách duyệt và màu Xanh Ngọc (`#06B6D4`) cho cột Chi tiêu thực tế.
   * **Biểu đồ Tròn (Phòng Ban):** Sử dụng dải màu kết hợp giữa Tím, Xanh ngọc, Xanh bạc hà để hiển thị tỉ lệ phân bổ chi tiêu.

#### ❓ Câu hỏi gợi mở Socratic:
* *Tại sao việc đồng nhất màu sắc giữa thẻ KPI và cột biểu đồ tương ứng lại quan trọng đối với trải nghiệm người dùng (Cognitive Load)?*
* *Làm thế nào để hàm `fetchDashboardData()` cập nhật đúng các trường dữ liệu JSON mới mà Python trả về? Bạn đã kiểm tra sự khớp tên biến giữa Frontend và Backend chưa?*

---

### 🔍 PHA 3: CHECK (KIỂM TRA & ĐÁNH GIÁ CHẤT LƯỢNG)

Sau khi code xong, hãy chạy server bằng lệnh:
```powershell
python server.py
```
Trình duyệt sẽ tự động mở trang `http://localhost:9090`. Hãy tiến hành kiểm tra theo danh sách sau:

- [ ] **Độ chính xác dữ liệu:** Số liệu trên 4 thẻ KPI có khớp đúng với dữ liệu trong Excel không? (Mẹo: Mở Excel lên và dùng hàm `SUM` để đối chiếu chéo).
- [ ] **Hiệu ứng động:** Con số trên KPI có chạy tăng dần mượt mà khi dữ liệu cập nhật không?
- [ ] **Quy chuẩn thương hiệu:** Màu nền có phải là xám tối sang trọng `#1E1E2E` không? Các cột biểu đồ có đúng màu Tím `#7C3AED` và Xanh Ngọc `#06B6D4` không?
- [ ] **Kiểm tra vượt hạn mức:** Các giao dịch hoặc danh mục vượt ngân sách có được làm nổi bật bằng màu Hồng San Hô `#F43F5E` không?

#### 📝 Ghi nhận lỗi vào nhật ký
Hãy tạo tệp `02_nhat_ky_va_nhap/check_notes.md` và ghi nhận lại ít nhất 3 điểm chưa hoàn hảo hoặc lỗi giao diện phát hiện được trong lần chạy đầu tiên.

---

### 🔄 PHA 4: ACT (CẢI TIẾN & CHUẨN HÓA)

Dựa trên các lỗi phát hiện ở pha CHECK, hãy thực hiện tối ưu hóa:
* **Tối ưu hóa UI:** Căn chỉnh độ rộng cột bảng hiển thị để không bị tràn chữ trên giao diện di động.
* **Tối ưu hóa logic:** Định dạng số tiền có dấu phân cách hàng nghìn (ví dụ: `1,250,000,000 VNĐ` thay vì `1250000000 VNĐ`).
* **Đóng gói bàn giao:** Khi mọi thứ hoạt động hoàn hảo và đạt điểm đánh giá chất lượng cao, hãy sao chép các tệp tin hoàn thiện vào thư mục `06_ban_giao/` và ghi nhận bài học kinh nghiệm vào tệp `02_nhat_ky_va_nhap/pdca_log.md`.

---

## 🏆 TIÊU CHÍ ĐÁNH GIÁ BÀI TẬP (RUBRIC CHẤM ĐIỂM)

| Tiêu chuẩn | Trọng số | Yêu cầu đạt (Pass) |
|---|---|---|
| **Độ chính xác Logic** | 40% | Tính toán đúng các chỉ số ngân sách, chi tiêu và chênh lệch. Không bị lệch số liệu khi mô phỏng real-time tăng dần dòng dữ liệu. |
| **Quy chuẩn Thương hiệu** | 30% | Áp dụng đúng 100% bảng màu của Beta Solutions. Không còn sót lại bất kỳ màu xanh Navy hay Gold nào của Alpha. |
| **Trải nghiệm UI/UX** | 20% | Hiệu ứng chuyển động mượt mà, định dạng tiền tệ rõ ràng, không bị vỡ bố cục trên các màn hình có độ phân giải khác nhau. |
| **Kỷ luật PDCA** | 10% | Có đầy đủ các tệp kế hoạch (`task_brief.md`), nhật ký thực hiện (`pdca_log.md`) và ghi chú lỗi (`check_notes.md`). |

Chúc bạn thực hiện bài tập xuất sắc! Nếu gặp bất kỳ khó khăn nào trong quá trình viết code, hãy gọi Trợ lý AI và hỏi theo phương pháp Socratic để được gợi ý hướng giải quyết.
