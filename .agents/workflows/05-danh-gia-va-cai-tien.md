---
id: "WF-PDCA-REVIEW-05"
name: "05-danh-gia-va-cai-tien"
description: "Đánh giá chất lượng toàn bộ sản phẩm trong workspace (pha CHECK) và lập kế hoạch cải tiến (pha ACT 2)."
version: v2.0
status: Production-Ready
semantic_triggers: ['/05-danh-gia-va-cai-tien', '/05-danh-gia', 'danh gia va cai tien', 'đánh giá và cải tiến']
owner: "STUDENT-AGENT"
skill_target: "05-reviewer"
hitl_timeout: "24h"
retry_policy: {max_attempts: 3, backoff: exponential_1s_2s_4s, fallback: "log_to_ACTION-LOG_and_report_human"}
---

# Workflow: 05 Đánh Giá Và Cải Tiến

Sử dụng quy trình này để thực hiện kiểm tra pha CHECK cuối cùng và lên kế hoạch ACT 2 để nâng cao chất lượng toàn workspace.

## 1. Điều kiện tiên quyết (Prerequisites)
- Các báo cáo cuối cùng (`final_report.docx` hoặc `.md`, `submission_summary.md`) đã được tạo.
- Nhật ký hoạt động `02_nhat_ky_va_nhap/pdca_log.md` đã cập nhật đầy đủ thông tin.

## 2. Đầu vào (Inputs)
- Toàn bộ các file hiện có trong workspace.
- Tệp tiêu chí nghiệm thu `00_ke_hoach/success_criteria.md`.

## 3. Các bước thực hiện tuần tự (Step-by-Step Execution)
1. **Kiểm tra tệp tin (Audit Files):** Quét toàn bộ thư mục workspace để đảm bảo không thiếu bất kỳ thư mục hay tệp yêu cầu nào.
2. **Chấm điểm sản phẩm bàn giao (Grade Deliverables):**
   - Chạy các tiêu chí kiểm tra QA chất lượng dựa trên `00_ke_hoach/success_criteria.md` và bảng điểm Rubric 7 tiêu chí.
   - Sao chép biểu mẫu `.agents/skills/05-reviewer/templates/check_report_template.md` vào thư mục dự án dưới tên `02_nhat_ky_va_nhap/qa_review.md`.
3. **Ghi nhận kết quả đánh giá (Log Findings):**
   - Tự động điền (hydrate) thông tin điểm số từ 1 đến 5 cho 7 tiêu chí chất lượng và các lỗi phát hiện (Findings) vào tệp `02_nhat_ky_va_nhap/qa_review.md`.
   - Ghi nhận các thiếu sót kỹ thuật chi tiết vào tệp `02_nhat_ky_va_nhap/issue_log.md`.
4. **Thực hiện pha cải tiến & chuẩn hóa (ACT Phase):**
   - **Nhánh A1: Điểm trung bình Q-Score < 4.0 hoặc Điểm tổng dưới 85 (Cải tiến - Remediation):**
     1. Sao chép biểu mẫu `.agents/skills/05-reviewer/templates/act_patch_spec_template.md` sang tệp `02_nhat_ky_va_nhap/act_patch_spec.md`.
     2. Lập kế hoạch sửa lỗi chi tiết, phân tích nguyên nhân gốc rễ và xác định kiểm thử hồi quy để học viên sửa chữa.
     3. Yêu cầu tạo phiên bản cải tiến v2 (ví dụ: `final_report_v2.docx`) chứ không được ghi đè trực tiếp lên file cũ để đối chiếu kết quả (chu kỳ ACT 2).
   - **Nhánh A2: Q-Score >= 4.0 và Điểm tổng >= 85 (Chuẩn hóa & Bàn giao - Standardization):**
     1. Sao chép và đóng gói các sản phẩm chính thức đạt chuẩn (`data_clean.xlsx`, `final_report.docx`) sang thư mục bàn giao `06_ban_giao/`.
     2. Hướng dẫn học viên điền biểu mẫu "Nhật ký Rút kinh nghiệm" (Learning Capture) theo mẫu trong luật `05_phuong_phap_su_pham.md`.
     3. Khởi chạy quy trình dọn dẹp `/00-quan-tri` với tham số `archive` để đóng gói tệp trung gian vào `99_luu_tru/`, chuẩn bị cho chu trình PDCA tiếp theo.
5. **Cập nhật nhật ký hoạt động (Log Execution):** Ghi nhận hoàn thành pha CHECK/ACT vào tệp `02_nhat_ky_va_nhap/pdca_log.md`.

## 4. Maker-Checker Gate (Human Approval Point)
- **Halt Condition (Điều kiện dừng):** Sau khi lập bảng điểm đánh giá chất lượng `qa_review.md` và đóng gói sản phẩm tại `06_ban_giao/`, Agent bắt buộc phải dừng lại.
- **Báo cáo kiểm duyệt (Review Report):** Báo cáo điểm số trung bình (Q-Score), các điểm cải thiện còn tồn đọng (Grow), danh sách các tệp tin trong thư mục `06_ban_giao/` và xác nhận lưu trữ trung gian.
- **Lệnh xác nhận của Học viên:** Học viên xem xét báo cáo chấm điểm cuối cùng, xác nhận sản phẩm đạt yêu cầu và gõ `/00-quan-tri archive` để đóng gói, hoặc yêu cầu Agent thực hiện sửa lỗi dựa trên `act_patch_spec.md`.

## 5. Xử lý lỗi (Error Recovery)
- **Thiếu tiêu chí nghiệm thu (Missing Success Criteria):** Nếu thiếu tệp tiêu chí nghiệm thu do học viên không lập ban đầu, Agent tự động dùng hệ tiêu chí mặc định để chấm điểm, đồng thời ghi lại cảnh báo nhắc nhở học viên bổ sung tệp này trong các bài tập tiếp theo.
