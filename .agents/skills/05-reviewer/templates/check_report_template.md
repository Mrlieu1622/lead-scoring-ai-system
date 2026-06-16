# 🔍 Báo Cáo Kiểm Duyệt Chất Lượng (Check Report)

- **Nhiệm vụ kiểm duyệt:** [Tên nhiệm vụ]
- **Sản phẩm bàn giao (Artifact):** [Đường dẫn hoặc tên tệp sản phẩm]
- **Người kiểm duyệt (Reviewer):** [Trợ lý Agent hoặc Học viên]
- **Ngày kiểm duyệt:** [YYYY-MM-DD]
- **Trạng thái quyết định (Status):** Đạt (Pass) / Đạt có điều kiện (Conditional Pass) / Cần sửa đổi (Needs Revision) / Không đạt (Fail)

---

## 1. Bảng điểm đánh giá chất lượng (Scorecard)

| Tiêu chí đánh giá | Điểm số (1-5) | Minh chứng thực tế (Evidence) | Ghi chú & Đánh giá |
|---|---:|---|---|
| **Phù hợp mục tiêu (Goal fit)** | | | [Đầu ra có giải quyết được bài toán gốc không?] |
| **Tính đầy đủ (Completeness)** | | | [Có bị sót mục nào hoặc còn placeholder rỗng không?] |
| **Tính nhất quán nguồn (Source consistency)** | | | [Các số liệu/khẳng định có dẫn chiếu từ nguồn thật không?] |
| **Logic & Cấu trúc (Logic)** | | | [Mô hình dữ liệu và các lập luận có mạch lạc không?] |
| **An toàn bảo mật (Safety)** | | | [Có bị lộ thông tin cá nhân PII hay API key không?] |
| **Định dạng & Thẩm mỹ (Formatting)** | | | [Trình bày Markdown/biểu đồ có đúng quy chuẩn không?] |
| **Khả năng bảo trì (Maintainability)** | | | [Tài liệu có dễ tái sử dụng hoặc nâng cấp không?] |

- **Điểm chất lượng trung bình (Q-Score):** [Tổng điểm / 7]

## 2. Các vấn đề và lỗi phát hiện (Findings)

| Mã lỗi | Vấn đề phát hiện | Mức độ nghiêm trọng | Minh chứng / Vị trí lỗi | Yêu cầu sửa đổi (Fix) |
|---|---|---|---|---|
| **F-01** | [Ví dụ: Còn thông tin số điện thoại học viên] | Cao (High) | Dòng 45 tệp nháp | Che dấu hoặc xóa bỏ ngay |
| **F-02** | [Ví dụ: Thiếu ghi chú nguồn gốc giá của Highlands] | Trung bình (Medium) | Dòng 12 tệp báo cáo | Thêm liên kết tham chiếu |

*Mức độ nghiêm trọng: Cao (High - bắt buộc sửa để Pass) / Trung bình (Medium) / Thấp (Low).*

## 3. Các điểm bắt buộc phải sửa đổi (Required Fixes)
1. [Lỗi bắt buộc 1]
2. [Lỗi bắt buộc 2]

## 4. Các điểm khuyến nghị cải thiện (Recommended Improvements)
1. [Khuyến nghị 1: Nên trực quan hóa biểu đồ này dạng hình cột thay vì hình tròn]
2. [Khuyến nghị 2]

## 5. Giới hạn hoặc rủi ro đã biết (Known Limitations)
- [Ví dụ: Dữ liệu khảo sát chỉ đại diện cho 3 cơ sở tại Hà Nội, chưa bao quát miền Nam]
- 

## 6. Quyết định nghiệm thu cuối cùng (Decision)
**Lựa chọn một trong các quyết định sau:**
- **Bàn giao ngay (Ship):** Đạt chất lượng Pass, sẵn sàng xuất bản/bàn giao.
- **Dùng thử nghiệm (Pilot only):** Đạt có điều kiện, cần sửa các lỗi nhỏ nhưng được dùng thử.
- **Làm lại (Revise):** Cần sửa lại các lỗi nghiêm trọng và chạy lại pha PLAN-DO.
- **Dừng thực hiện (Stop):** Phát hiện lỗi nghiêm trọng ảnh hưởng đến hệ thống hoặc vi phạm bảo mật.
