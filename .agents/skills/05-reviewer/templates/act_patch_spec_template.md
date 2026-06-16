# 🛠️ Đặc Tả Bản Sửa Lỗi Cải Tiến (ACT Patch Spec)

- **Nhiệm vụ sửa lỗi:** [Tên nhiệm vụ gốc]
- **Sản phẩm lỗi (Artifact):** [Tên tệp tin cần vá lỗi]
- **Ngày lập bản vá:** [YYYY-MM-DD]
- **Trạng thái bản vá (Status):** Nháp (Draft) / Đang duyệt (Review) / Đã phê duyệt (Approved) / Đã triển khai (Implemented)

---

## 1. Nguyên nhân kích hoạt bản vá (Trigger)
[Tại sao cần bản vá này? Bản báo cáo kiểm duyệt Check Report phát hiện ra lỗi gì nghiêm trọng?]

## 2. Phân tích nguyên nhân gốc rễ (Root Cause)
[Vấn đề cốt lõi trong quy trình hoặc mã nguồn nào đã tạo ra lỗi sai này? Tại sao lỗi vượt qua được các pha trước?]

## 3. Phạm vi sửa đổi của bản vá (Patch Scope)
**Trong phạm vi vá (In Scope):**
- [ ] [Chỉ sửa lỗi ở dòng nào, tệp nào]
- [ ] 

**Ngoài phạm vi vá (Out of Scope):**
- [ ] [Không tự ý thay đổi cấu trúc hoặc logic nghiệp vụ khác]
- [ ] 

## 4. Các hạng mục sửa chữa chi tiết (Patch Items)

| Mã bản vá | Lỗi phát hiện | Giải pháp sửa lỗi cụ thể | Người sửa | Mức ưu tiên | Tiêu chí kiểm thử |
|---|---|---|---|---|---|
| **P-01** | [Ví dụ: Thiếu mã hóa UTF-8 khi lưu CSV] | Thêm tham số `encoding='utf-8'` vào dòng code số 42 | [Tên học viên] | Cao (High) | Mở CSV trên Excel không bị lỗi phông tiếng Việt |
| **P-02** | | | | | |

*Mức ưu tiên: Cao (High) / Trung bình (Medium) / Thấp (Low).*

## 5. Cập nhật Quy tắc/Quy trình/Kỹ năng để chuẩn hóa
Để tránh lỗi này lặp lại ở các nhiệm vụ khác trong tương lai, cần cập nhật hệ thống tri thức như thế nào:
- **Cập nhật Quy tắc (.agents/rules/):** [Ví dụ: Bổ sung quy tắc lưu file CSV bắt buộc dùng utf-8 vào luật 03_output_quality_rules.md]
- **Cập nhật Quy trình (.agents/workflows/):** [Ví dụ: Thêm bước kiểm tra font chữ ở workflow làm sạch dữ liệu]
- **Cập nhật Kỹ năng (.agents/skills/):** [Ví dụ: Thêm thư viện xử lý tiếng Việt vào kỹ năng data-cleaner]
- **Cập nhật Biểu mẫu mẫu (Templates):** [Ghi chú nếu có]

## 6. Lập kịch bản kiểm thử hồi quy (Regression Test)
Định nghĩa cách thức kiểm tra để đảm bảo lỗi đã được sửa triệt để và không tạo ra lỗi mới:
- **Câu lệnh/Thao tác kiểm thử:** [Nhập thao tác hoặc lệnh chạy thử]
- **Kết quả mong đợi:** [Trạng thái mong đợi của tệp tin]
- **Tiêu chí đánh giá Đạt (Pass criteria):** [Điều kiện để đóng bản vá]

## 7. Phê duyệt bản vá (Approval)
- **Người phê duyệt:** [Giảng viên hoặc Người vận hành lớp học]
- **Ngày phê duyệt:** [YYYY-MM-DD]
- **Ghi chú phê duyệt:** [Ý kiến bổ sung]
