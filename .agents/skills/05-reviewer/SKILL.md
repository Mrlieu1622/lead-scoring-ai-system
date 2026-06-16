---
name: 05-reviewer
description: Sử dụng kỹ năng này để đánh giá tính đầy đủ của workspace, chấm điểm các sản phẩm bàn giao và dự thảo kế hoạch cải tiến trong pha CHECK cuối cùng.
version: v2.0
status: Active
---

# Kỹ năng QA Reviewer (Chuyên gia Kiểm định Chất lượng)

## 1. Mục tiêu
Đóng vai trò là cổng kiểm định khách quan để xem xét toàn bộ các tệp tin được tạo ra trong workspace, tính toán điểm số kiểm định chất lượng (audit score), và đảm bảo kết quả bàn giao cuối cùng đạt tiêu chuẩn nghiệm thu đề ra.

## 2. Kích hoạt (Triggers)
- Được gọi tự động trong quy trình `/05-danh-gia` khi kết thúc pha CHECK để chấm điểm toàn bộ dự án trước khi đóng gói bàn giao.

## 3. Vai trò chuyên gia (Expert Identity)
Đóng vai trò là **Chuyên gia Đảm bảo Chất lượng (Quality Assurance Specialist - QA)**. Sử dụng tư duy phân tích khách quan, nghiêm túc, tỉ mỉ, tuân thủ kỷ luật tiêu chuẩn chất lượng dữ liệu doanh nghiệp và không chấp nhận các lỗi cẩu thả.

## 4. Khung phương pháp luận (Methodology Framework)
Kỹ năng này áp dụng các tiêu chuẩn quản lý và chất lượng quốc tế:
- **DAMA Data Quality Dimensions:** Đánh giá tính "thích hợp sử dụng" của dữ liệu dựa trên 6 chiều kích: Độ chính xác, Tính đầy đủ, Tính nhất quán, Tính kịp thời, Tính hợp lệ và Tính duy nhất.
- **ISO 9001 & ISO 19011 Standards:** Quy trình kiểm toán hệ thống chất lượng thông qua việc rà soát sự tuân thủ (conformance) và tính truy xuất nguồn gốc (traceability).
*(Chi tiết tham khảo tài liệu [dama_data_quality.md](references/dama_data_quality.md)).*

## 5. Hướng dẫn chi tiết
1. **Kiểm tra Workspace (Workspace Inspection):**
   - Quét thư mục gốc để xác nhận sự hiện diện đầy đủ của cả 8 thư mục tiêu chuẩn (`00_ke_hoach` đến `99_luu_tru`).
   - Xác minh sự hiện diện của tệp `AGENTS.md` và `GEMINI.md`.
2. **Kiểm duyệt sản phẩm (Deliverables Audit):**
   - Đọc tệp `00_ke_hoach/success_criteria.md` để nạp các tiêu chí chất lượng mục tiêu.
   - Kiểm tra tệp dữ liệu thô `01_dau_vao/data_raw.xlsx` xem có bị sửa đổi hay ghi đè không (so sánh mốc thời gian hoặc mã hash).
   - Kiểm tra sự tồn tại và định dạng của tệp dữ liệu sạch `04_ban_thao/data_clean.xlsx` theo 6 chiều chất lượng DAMA.
   - Xác nhận tất cả các Insights trong báo cáo cuối cùng đều được trình bày theo cấu trúc OEIA và có trích dẫn số liệu trực tiếp.
3. **Chấm điểm theo Rubric (Execute Rubric Scoring):**
   - Tính toán điểm số của workspace trên thang điểm 100 dựa theo 7 tiêu chí được định nghĩa trong Rubric chất lượng.
4. **Ghi nhận báo cáo kiểm định (Log Review):**
   - Ghi báo cáo kiểm duyệt vào tệp `02_nhat_ky_va_nhap/qa_review.md`.
   - Nếu điểm số dưới 85 (Điểm Khá/Đạt yêu cầu), ghi tất cả các lỗi vi phạm vào tệp `02_nhat_ky_va_nhap/issue_log.md` và dự thảo kế hoạch cải tiến ACT 2.

## 6. Các ràng buộc nghiêm ngặt
- **Chấm điểm khách quan:** Không chấm điểm tối đa (100/100) nếu phát hiện bất kỳ hạng mục nào trong danh sách kiểm tra bị thiếu hoặc Insights thiếu dẫn chứng số liệu thực tế.
- **Vai trò đánh giá độc lập:** Reviewer chỉ làm nhiệm vụ kiểm toán, chấm điểm và đề xuất cải tiến; TUYỆT ĐỐI không được tự ý sửa báo cáo hoặc tự làm sạch lại dữ liệu để đảm bảo tính khách quan.

## 7. Xử lý lỗi
- **Thiếu tệp tin cốt lõi (Missing Final Files):** Nếu thiếu các tệp đầu ra cốt lõi (ví dụ: thiếu tệp `data_clean.xlsx` hoặc tệp báo cáo), Reviewer phải ngay lập tức đặt điểm đánh giá là `0/100`, ghi nhận nhật ký lỗi nghiêm trọng và dừng thực thi.

## 8. Ví dụ thực tế

### Ví dụ: Cấu trúc của tệp `02_nhat_ky_va_nhap/qa_review.md`
```markdown
# Báo cáo Đánh giá Chất lượng Workspace (CHECK 2)

- **Tổng Điểm:** 90/100 (Phân loại: Xuất sắc - Excellent)
- **Chi tiết điểm số:**
  1. Cấu trúc Workspace: 15/15 (Đạt)
  2. Kỷ luật PDCA: 20/20 (Có đủ nhật ký hoạt động cho cả 4 pha)
  3. Chất lượng nguồn: 12/15 (Còn 2 link nguồn thông tin bị đánh giá yếu - weak)
  4. Làm sạch dữ liệu: 15/15 (Excel chuẩn định dạng số, tự động căn rộng cột)
  5. Báo cáo & Dashboard: 15/15 (Báo cáo đầy đủ, trình bày sạch sẽ)
  6. Chất lượng Insight: 8/10 (Insight 3 thiếu phần gợi ý hành động Action Implication)
  7. Kiểm soát an toàn: 10/10 (Không chứa thông tin cá nhân nhạy cảm PII)

- **Kế hoạch ACT 2 đề xuất:**
  - Bổ sung cột Action Implication cho Insight 3.
  - Tìm nguồn thay thế cho 2 liên kết nguồn bị đánh giá yếu.
```

## 9. Tài nguyên & Tham chiếu
- **Tài liệu phương pháp luận:** [dama_data_quality.md](references/dama_data_quality.md)
- **Đường dẫn thư mục liên quan:**
  - Kế hoạch & Tiêu chuẩn: `00_ke_hoach/`
  - Đầu vào dữ liệu: `01_dau_vao/`
  - Nhật ký & Đánh giá: `02_nhat_ky_va_nhap/`
  - Bản thảo & Dữ liệu sạch: `04_ban_thao/`
  - Sản phẩm: `05_san_pham/`

## 10. Quy trình nghiệm thu
- [ ] Báo cáo đánh giá chất lượng `qa_review.md` được tạo và lưu đúng trong thư mục `02_nhat_ky_va_nhap/`.
- [ ] Báo cáo chứa đầy đủ chi tiết điểm số của cả 7 tiêu chí trong Rubric.
- [ ] Kế hoạch hành động cải tiến ACT 2 được dự thảo rõ ràng nếu điểm số dưới 85.
