# Tài liệu Tham chiếu: Bộ tiêu chuẩn Đánh giá Chất lượng Dữ liệu DAMA & Quy trình Kiểm toán

Tệp tài liệu tham chiếu này định nghĩa và hướng dẫn áp dụng bộ khung **DAMA Data Quality Dimensions** (Các chiều chất lượng dữ liệu của Hiệp hội Quản trị Dữ liệu Quốc tế) và quy trình kiểm toán chất lượng theo tiêu chuẩn **ISO 9001 / ISO 19011** để đánh giá toàn diện sản phẩm đầu ra của chu trình PDCA.

---

## 1. 6 Chiều Chất lượng Dữ liệu Cốt lõi của DAMA

Agent Reviewer phải đánh giá tập dữ liệu sạch `data_clean.xlsx` dựa trên 6 chiều kích đo lường chuẩn hóa sau:

1. **Độ chính xác (Accuracy):**
   - Dữ liệu phản ánh đúng thực tế khách quan.
   - *Kiểm tra:* Tên địa điểm, địa chỉ phải tồn tại trên thực tế; giá cả và điểm đánh giá phải khớp với nguồn trích dẫn.

2. **Tính đầy đủ (Completeness):**
   - Không có trường thông tin bắt buộc nào bị bỏ trống hoặc khuyết thiếu mà không có lý do chính đáng.
   - *Kiểm tra:* Tỷ lệ khuyết dữ liệu (Null Rate) trên mỗi cột phải bằng 0% (hoặc được điền giá trị thay thế hợp lệ).

3. **Tính nhất quán (Consistency):**
   - Dữ liệu không mâu thuẫn giữa các bảng hoặc các phần khác nhau trong báo cáo.
   - *Kiểm tra:* Số lượng đối tượng phân tích trong báo cáo Word phải khớp chính xác với số dòng trong tệp Excel.

4. **Tính kịp thời (Timeliness):**
   - Dữ liệu phải cập nhật và phản ánh trạng thái mới nhất có thể tiếp cận được.
   - *Kiểm tra:* Ghi nhận mốc thời gian truy cập (access timestamp) trong tệp registry không được quá cũ so với thời gian chạy dự án.

5. **Tính hợp lệ (Validity):**
   - Dữ liệu phải tuân thủ đúng định dạng, kiểu dữ liệu và quy tắc nghiệp vụ đã định nghĩa.
   - *Kiểm tra:* Cột giá phải là số nguyên, cột rating phải là số thực từ 0.0 đến 5.0, cột URL phải đúng định dạng liên kết.

6. **Tính duy nhất (Uniqueness):**
   - Không có bản ghi hoặc dòng dữ liệu nào bị trùng lặp trong tập dữ liệu.
   - *Kiểm tra:* Thực hiện drop-duplicates trên cột khóa chính (ví dụ: tên quán cafe) để đảm bảo số lượng dòng là duy nhất.

---

## 2. Quy trình Kiểm toán Workspace theo chuẩn ISO 9001 / ISO 19011

Áp dụng phương pháp đánh giá hệ thống quản lý chất lượng, quy trình kiểm toán của Agent Reviewer gồm 3 bước:

1. **Kiểm tra Conformance (Sự tuân thủ Cấu trúc):**
   - Quét cấu trúc vật lý của workspace để đảm bảo đầy đủ 8 thư mục tiêu chuẩn.
   - Xác nhận sự tồn tại của các tệp nhật ký tiến trình (`pdca_log.md`, `issue_log.md`).

2. **Kiểm toán Data Provenance (Truy xuất nguồn gốc):**
   - Đối chiếu tệp dữ liệu sạch với tệp dữ liệu thô ban đầu để đảm bảo dữ liệu gốc không bị ghi đè (tính toàn vẹn dữ liệu).
   - Kiểm tra sổ đăng ký nguồn để xác nhận tất cả các liên kết URL đều hoạt động và hợp lệ.

3. **Đánh giá Rubric chất lượng:**
   - Thực hiện chấm điểm chi tiết trên thang 100 theo bộ tiêu chí đã định hình sẵn.
   - Phát hành báo cáo kiểm duyệt chất lượng `qa_review.md` kèm theo các điểm không tuân thủ (Non-conformity) và kế hoạch hành động cải tiến ACT 2.
