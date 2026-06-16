# Tài liệu Tham chiếu: Phương pháp luận SMART & WBS trong Lập kế hoạch Dữ liệu

Tệp tài liệu tham chiếu này định nghĩa và hướng dẫn áp dụng hai bộ khung quản trị dự án tiêu chuẩn quốc tế: mục tiêu **SMART** và cấu trúc phân rã công việc **WBS (Work Breakdown Structure)** trong pha PLAN của chu trình dữ liệu PDCA.

---

## 1. Bộ khung mục tiêu SMART trong Dự án Dữ liệu

Để một dự án dữ liệu hoặc một tác vụ phân tích được lập kế hoạch hiệu quả, mục tiêu đề ra không được chung chung mà phải tuân thủ nghiêm ngặt 5 tiêu chí SMART:

1. **S - Specific (Cụ thể):**
   - Định nghĩa rõ ràng đối tượng cần thu thập và phân tích.
   - *Ví dụ kém:* "Tìm kiếm các quán cafe ở Hà Nội."
   - *Ví dụ tốt:* "Thu thập dữ liệu các quán cafe phục vụ làm việc từ xa (co-working) tại Quận 1, TP.HCM."

2. **M - Measurable (Đo lường được):**
   - Xác định rõ số lượng dòng (dữ liệu mẫu) và số lượng trường thông tin (cột) tối thiểu cần đạt được.
   - *Ví dụ:* "Đạt tối thiểu 15 quán cafe độc lập với ít nhất 5 trường thông tin chi tiết: tên, giá trung bình, địa chỉ, đánh giá, và URL nguồn."

3. **A - Achievable (Khả thi):**
   - Đảm bảo nguồn dữ liệu có thể tiếp cận được (ví dụ: Google Maps, Foody, ShopeeFood) bằng các công cụ tìm kiếm và cào dữ liệu cơ bản, không vi phạm các rào cản bảo mật nghiêm trọng.
   - Thời gian thực hiện dự kiến trong vòng 2-3 giờ tự học của học viên.

4. **R - Relevant (Liên quan/Thực tế):**
   - Mục tiêu phân tích phải giải quyết được bài toán kinh doanh hoặc thực tiễn của học viên.
   - *Ví dụ:* Việc tìm quán cafe Quận 1 giúp học viên chọn được không gian làm việc tối ưu nhất về chi phí và chất lượng dịch vụ.

5. **T - Time-bound (Giới hạn thời gian):**
   - Xác định rõ thời hạn hoàn thành của từng bước và toàn bộ pha PLAN.

---

## 2. Cấu trúc phân rã công việc WBS (Work Breakdown Structure)

Áp dụng tiêu chuẩn quản trị dự án PMBOK, công việc thu thập và phân tích dữ liệu phải được phân rã thành các gói công việc (Work Packages) cụ thể theo sơ đồ hình cây:

```text
[Dự án Phân tích Dữ liệu PDCA]
  ├── 1.0 Pha PLAN: Lập kế hoạch & Thiết lập mục tiêu
  │     ├── 1.1 Khảo sát nhu cầu học viên & xác định bài toán
  │     ├── 1.2 Thiết lập SMART Goals & định nghĩa cột dữ liệu
  │     └── 1.3 Tạo tệp Task Brief & Tiêu chí Nghiệm thu (Success Criteria)
  ├── 2.0 Pha DO: Thực thi & Thu thập dữ liệu
  │     ├── 2.1 Tìm kiếm nguồn dữ liệu & đánh giá độ tin cậy
  │     ├── 2.2 Thu thập dữ liệu thô và xuất ra tệp data_raw.xlsx
  │     └── 2.3 Đăng ký nguồn vào sổ source_registry.md
  ├── 3.0 Pha CHECK: Kiểm tra chất lượng dữ liệu
  │     ├── 3.1 Kiểm tra các chiều chất lượng DAMA (khuyết thiếu, định dạng, trùng lặp)
  │     └── 3.2 Ghi nhận lỗi vào tệp check_notes.md / issue_log.md
  └── 4.0 Pha ACT: Làm sạch & Báo cáo cải tiến
        ├── 4.1 Viết script Python làm sạch và chuyển đổi (Tidy Data)
        ├── 4.2 Xuất tệp data_clean.xlsx và chạy kiểm định lại
        └── 4.3 Viết báo cáo phân tích theo nguyên lý Kim tự tháp Minto (OEIA)
```

---

## 3. Hướng dẫn Tích hợp vào Quy trình Vận hành

Khi viết tệp `00_ke_hoach/task_brief.md` và `00_ke_hoach/success_criteria.md`, Agent Planner phải:
- **Kiểm tra tiêu chí SMART:** Có con số dòng cụ thể không? Có danh sách cột dữ liệu không? Có đường dẫn đầu ra không?
- **Phân chia công việc theo WBS:** Giao nhiệm vụ rõ ràng cho từng Agent tiếp theo (Collector, Cleaner, Writer, Reviewer).
- **Thiết lập Cổng kiểm soát (Gate):** Đảm bảo học viên phê duyệt Task Brief trước khi Agent tiếp theo thực hiện pha DO.
