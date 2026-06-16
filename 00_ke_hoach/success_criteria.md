# SUCCESS CRITERIA: TIÊU CHÍ NGHIỆM THU DASHBOARD (Tối ưu hóa KPIs & Biểu đồ phòng ban)

## 1. Tiêu chí đối với API Backend (`server.py`)
- [ ] **Lập trình so sánh Q-o-Q:** API trả về đối tượng `trends` trong `kpis` chứa phần trăm thay đổi của Tổng ngân sách, Tổng chi tiêu, và Chênh lệch chênh số lần vượt định mức so với Quý trước đó (ví dụ: đối chiếu Q2-2026 vs Q1-2026).
- [ ] **API dữ liệu phòng ban nâng cao:** Trả về cả danh sách `ngan_sach` và `chi_tieu` cho biểu đồ bộ phận, thay vì chỉ trả về một mảng chi tiêu thô.

## 2. Tiêu chí đối với Giao diện Frontend (`dashboard.html`)
- [ ] **Giao diện xu hướng liên quý (Q-o-Q trends):** Dưới mỗi thẻ KPI chính phải hiển thị dòng chữ so sánh với Quý trước (Ví dụ: `↑ 12% so với quý trước`).
  - Màu sắc tích cực (tiết kiệm tăng, chi tiêu giảm) dùng màu xanh bạc hà `#14B8A6`.
  - Màu sắc tiêu cực (vượt ngân sách tăng, chi tiêu tăng) dùng màu hồng san hô `#F43F5E`.
- [ ] **Biểu đồ phòng ban nâng cấp:** Biểu đồ hiển thị song song Ngân Sách vs Chi Tiêu của từng bộ phận (ke toan, marketing, v.v.), giúp thấy rõ phòng ban nào bị thâm hụt (chi tiêu vượt ngân sách).

## 3. Tiêu chí đối với Đóng gói bàn giao
- [ ] **Tệp nén hợp lệ:** Tạo tệp tin `TH_NganSach_Beta.zip` có mật khẩu bảo mật chứa tệp `dashboard.html`.
