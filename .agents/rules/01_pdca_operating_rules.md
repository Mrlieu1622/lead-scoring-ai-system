---
name: 01-PDCA-Operating-Rules
type: L1-Rule
priority: 2
trigger: always_on
---

> [!IMPORTANT]
> Override Priority: TIER 2


# Nguyên tắc 01: Quy tắc vận hành PDCA & Nhật ký vòng đời

## 1. Mục tiêu
Bắt buộc thực thi kỷ luật 4 bước PLAN -> DO -> CHECK -> ACT một cách tuần tự. Agent không được tự ý bỏ qua các pha hoặc chạy các prompt tùy tiện mà không cập nhật trạng thái làm việc.

## 2. Kỷ luật vận hành từng pha

### Pha PLAN (Lập kế hoạch)
- **Đầu vào:** Yêu cầu bằng ngôn ngữ tự nhiên từ học viên.
- **Ràng buộc:** KHÔNG được cào dữ liệu, viết code, hoặc tạo bảng biểu ở pha này.
- **Yêu cầu bắt buộc:** Phải sinh ra tệp `00_ke_hoach/task_brief.md` và `00_ke_hoach/success_criteria.md`.
- **Cổng nghiệm thu:** Cần có xác nhận đồng ý của học viên mới được đi tiếp.

### Pha DO (Thực hiện)
- **Đầu vào:** Kế hoạch đã được phê duyệt ở pha PLAN.
- **Ràng buộc:** Chia nhỏ công việc thành các bước nhỏ nhất và an sau nhất. Không gộp chung việc làm sạch dữ liệu và viết báo cáo trong cùng một lượt.
- **Yêu cầu bắt buộc:** Xuất dữ liệu thô ra tệp `01_dau_vao/data_raw.xlsx`.
- **Cổng nghiệm thu:** Tự động chuyển giao sang bước CHECK.

### Pha CHECK (Kiểm tra)
- **Đầu vào:** Kết quả thực hiện ở pha DO + Tiêu chí thành công ở pha PLAN.
- **Ràng buộc:** Tuyệt đối không chấp nhận các nhận xét chung chung vô thưởng vô phạt như "Mọi thứ đều ổn".
- **Yêu cầu bắt buộc:** Kiểm tra định dạng dữ liệu, giá trị bị khuyết, dòng trùng lặp và tính xác thực của nguồn. Ghi nhận kết quả vào tệp `02_nhat_ky_va_nhap/check_notes.md`.
- **Cổng nghiệm thu:** Phải tìm ra ít nhất 3 điểm cần cải thiện trước khi chuyển pha.

### Pha ACT (Cải tiến)
- **Đầu vào:** Nhật ký lỗi và ghi chú cải tiến ở pha CHECK.
- **Ràng buộc:** Không được phớt lờ lỗi hoặc nhảy cóc sang viết báo cáo tổng kết.
- **Yêu cầu bắt buộc:** Thực thi sửa code, làm sạch dữ liệu, hoặc tìm nguồn thay thế. Xuất kết quả sạch ra tệp `04_ban_thao/data_clean.xlsx`.
- **Cổng nghiệm thu:** Tự kiểm định lại định dạng dữ liệu sạch để đảm bảo không còn lỗi.

## 3. Yêu cầu ghi nhật ký (`pdca_log.md`)
Mỗi lần chuyển đổi giữa các pha, Agent phải cập nhật vào tệp `02_nhat_ky_va_nhap/pdca_log.md` các thông tin sau:
- **Dấu mốc thời gian:** Định dạng ISO 8601.
- **Pha đang hoạt động:** PLAN, DO, CHECK, hoặc ACT.
- **Hành động đã hoàn thành:** Các tệp tin nào đã được tạo hoặc sửa đổi.
- **Các chỉ số kiểm tra:** Số lượng dòng dữ liệu, tỷ lệ khuyết thiếu, hoặc điểm chất lượng.
- **Điều hướng tiếp theo:** Bước đi tiếp theo của quy trình.
