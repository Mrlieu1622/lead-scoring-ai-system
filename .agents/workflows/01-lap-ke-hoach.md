---
id: "WF-PDCA-PLAN-01"
name: "01-lap-ke-hoach"
description: "Thực hiện pha PLAN để lập kế hoạch công việc và xác định tiêu chí thành công."
version: v2.0
status: Production-Ready
semantic_triggers: ['/01-lap-ke-hoach', '/01-plan', 'lap ke hoach', 'lập kế hoạch']
owner: "STUDENT-AGENT"
skill_target: "01-planner"
hitl_timeout: "24h"
retry_policy: {max_attempts: 3, backoff: exponential_1s_2s_4s, fallback: "log_to_ACTION-LOG_and_report_human"}
---

# Workflow: 01 Lập Kế Hoạch

Sử dụng quy trình này để hướng dẫn học viên thiết kế bảng yêu cầu công việc (Task Brief) và tiêu chí nghiệm thu (Success Criteria) trước khi viết code hay thu thập dữ liệu.

## 1. Điều kiện tiên quyết (Prerequisites)
- Workspace đã được kiểm tra sức khỏe và quản trị bằng lệnh `/00-quan-tri`.
- Thư mục `00_ke_hoach/` đã sẵn sàng.

## 2. Đầu vào (Inputs)
- Yêu cầu thô từ người dùng hoặc giảng viên (raw prompt).

## 3. Các bước thực hiện tuần tự (Step-by-Step Execution)
1. **Thẩm định Chất lượng Đầu vào (Background COA Evaluation):**
   - Đọc yêu cầu thô của học viên.
   - Chạy ngầm đánh giá yêu cầu dựa trên bộ tiêu chí chất lượng đầu vào (What, Where, How much, Why, Which fields). Yêu cầu bắt buộc đạt tối thiểu 3/5 tiêu chí (phải có What và Where).
2. **Dẫn dắt Mentor (Mentoring Loop - 5W1H):**
   - Nếu yêu cầu KHÔNG ĐẠT tiêu chí đánh giá chạy ngầm: Tạm dừng việc tạo tài liệu. Đóng vai trò Mentor đưa ra các câu hỏi gợi mở theo khung 5W1H kết hợp với các đề xuất có sẵn (scaffolding) để hướng dẫn học viên bổ sung thông tin thiếu sót.
   - Nhận phản hồi của học viên và đánh giá lại cho đến khi yêu cầu vượt qua cổng kiểm soát chạy ngầm.
3. **Kích hoạt Kỹ năng Planner (Hydrate Task Brief):**
   - Sử dụng kỹ năng `01-planner` để sao chép biểu mẫu `.agents/skills/01-planner/templates/task_card_template.md` vào thư mục dự án dưới tên `00_ke_hoach/task_brief.md` và tự động điền các thông tin đã được chuẩn hóa ở hai bước trên.
   - Đồng thời khởi tạo tệp `00_ke_hoach/success_criteria.md` để cụ thể hóa các tiêu chuẩn kỹ thuật bằng số liệu định lượng cụ thể.
4. **Đánh giá & Phê duyệt (Review & Approve):** Yêu cầu học viên kiểm tra tính khả thi và duyệt thẻ công việc trước khi chuyển sang pha DO (chạy quy trình `/02-thu-thap`). Nếu rủi ro được đánh giá là Cao (High) hoặc Nghiêm trọng (Critical), Agent bắt buộc phải dừng lại chờ phê duyệt thủ công từ Giảng viên.

## 4. Maker-Checker Gate (Human Approval Point)
- **Halt Condition (Điều kiện dừng):** Sau khi khởi tạo `task_brief.md` và `success_criteria.md`, Agent bắt buộc phải dừng lại.
- **Báo cáo kiểm duyệt (Review Report):** Hiển thị tóm tắt mục tiêu công việc và các tiêu chí nghiệm thu định lượng (ví dụ: số lượng dòng tối thiểu, danh sách cột).
- **Lệnh xác nhận của Học viên:** Học viên phải kiểm duyệt thủ công và gõ `/02-thu-thap-du-lieu` để tiếp tục. Agent KHÔNG ĐƯỢC tự ý gọi pha tiếp theo.

## 5. Xử lý lỗi (Error Recovery)
- **Thiếu thư mục Brief (Missing Brief Folder):** Nếu thư mục `00_ke_hoach` chưa có, tự động chạy lại bước tạo thư mục từ `/00-quan-tri`.
