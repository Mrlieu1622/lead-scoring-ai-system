---
name: 06-HAC-Effectiveness-Metrics
type: L1-Rule
priority: 2
trigger: always_on
---

> [!IMPORTANT]
> Override Priority: TIER 2


# Nguyên tắc 06: Chỉ số Đo lường Hiệu quả Cộng tác (HAC Metrics)

## 1. Mục tiêu
Định nghĩa hệ thống chỉ số để đo lường mức độ hiệu quả của mô hình Cộng tác Người - Máy (Human-Agent Co-working - HAC), giúp theo dõi sự tiến bộ về năng lực học tập của học viên và chất lượng đầu ra của hệ thống.

## 2. Các chỉ số đo lường cốt lõi (HAC Metrics)

| Chỉ số | Định nghĩa | Cách đo lường | Hướng mục tiêu |
|---|---|---|---|
| **Chỉ số Tải nhận thức (Cognitive Load Index)** | Mức độ khó khăn và nỗ lực trí óc học viên cảm thấy khi giải quyết nhiệm vụ. | Học viên đánh giá từ 1 (rất dễ) đến 5 (quá tải nhận thức) sau mỗi bài tập. | Giảm dần mà không làm giảm hiệu quả học tập. |
| **Tốc độ Chuẩn hóa (Standardization Velocity)** | Tốc độ đúc rút các công việc lặp đi lặp lại thành các biểu mẫu, quy trình hoặc kỹ năng mới. | Số lượng biểu mẫu/quy trình được đóng gói và phê duyệt trong mỗi giai đoạn học tập. | Tăng lên. |
| **Tỷ lệ Lỗi lọt lưới (Error Escape Rate)** | Các lỗi sai hoặc lỗ hổng được phát hiện sau khi tệp tin đã qua pha CHECK và bàn giao. | Số lỗi phát hiện sau bàn giao / Tổng số tiêu chí kiểm duyệt. | Giảm thiểu tối đa (hướng tới 0%). |
| **Tỷ lệ Can thiệp (Intervention Rate)** | Số lần học viên phải can thiệp để sửa chữa hoặc điều chỉnh hướng đi của Agent. | Số lần Người vận hành phải sửa đổi prompt hoặc nội dung của Agent trên mỗi nhiệm vụ. | Giảm dần theo thời gian. |
| **Số Chu kỳ Làm lại (Rework Cycle Count)** | Số vòng lặp PDCA (sửa đổi kế hoạch/làm lại) để sản phẩm đầu ra đạt mức phê duyệt (Pass). | Tổng số lần lặp lại pha PLAN-DO-CHECK cho đến khi bàn giao. | Giảm dần (hướng tới 1 vòng duy nhất). |
| **Điểm Minh bạch Nguồn gốc (Source Traceability Score)** | Mức độ dữ liệu đầu ra được dẫn nguồn xác thực và ghi chú giả định rõ ràng. | Đánh giá từ 1 đến 5 điểm dựa trên nhật ký nguồn dữ liệu. | Tăng lên (mục tiêu đạt 5/5). |
| **Mức độ Trưởng thành Kỹ năng (Skill Maturity Level)** | Trạng thái chuyển dịch của quy trình làm việc từ hành vi tự phát (ad-hoc) đến kỹ năng chuẩn hóa tái sử dụng. | Đánh giá theo thang đo năng lực tự chủ L0 - L4. | Tăng lên. |

## 3. Tần suất đánh giá
Hệ thống chỉ số này được áp dụng và đánh giá tại các mốc:
- Ngay sau khi kết thúc một nhiệm vụ lớn hoặc đồ án thực hành (để chấm điểm hiệu quả làm việc).
- Đánh giá tổng hợp hàng tuần trong suốt kỳ học.
- Đánh giá trước khi đóng gói một quy trình làm việc lặp lại thành kỹ năng tái sử dụng mới.

## 4. Mẫu đánh giá hiệu quả cộng tác (HAC Review Template)
Mỗi đợt đánh giá hiệu quả cộng tác sẽ được ghi nhận theo mẫu sau:
```markdown
# 📊 Báo cáo Đánh giá Hiệu quả Cộng tác Người - Máy (HAC Review)

- **Nhiệm vụ/Quy trình đánh giá:** [Tên nhiệm vụ]
- **Thời gian:** [Ngày thực hiện]
- **Người đánh giá (Học viên):** [Tên học viên]
- **Agent vận hành:** [Tên Agent]

### 1. Bảng điểm hiệu quả
| Chỉ số | Điểm số / Số liệu | Minh chứng thực tế | Đề xuất cải thiện |
|---|---:|---|---|
| Tải nhận thức (1-5) | | | |
| Số chu kỳ làm lại | | | |
| Điểm minh bạch nguồn | | | |
| Tỷ lệ lỗi lọt lưới | | | |

### 2. Ba nút thắt cổ chai lớn nhất (Bottlenecks)
1. [Nút thắt 1 - Ví dụ: Học viên mất nhiều thời gian duyệt lại kế hoạch]
2. [Nút thắt 2 - Ví dụ: Agent bị lỗi lặp lại trong pha làm sạch dữ liệu]
3. [Nút thắt 3]

### 3. Đề xuất chuẩn hóa quy trình (Standardization Candidates)
- [Đề xuất 1: Đóng gói mẫu làm sạch dữ liệu chuỗi đồ uống thành kỹ năng riêng]
- [Đề xuất 2]

### 4. Quyết định tiếp theo
- [ ] Tiếp tục chu kỳ học tập thử nghiệm (Pilot)
- [ ] Tinh chỉnh và vá lỗi quy trình (Patch workflow)
- [ ] Đóng gói và tạo mới kỹ năng (Create/update skill)
- [ ] Hoàn thành và đưa vào sử dụng thực tế (Scale)
```
