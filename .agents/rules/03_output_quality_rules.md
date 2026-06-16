---
name: 03-Output-Quality-Rules
type: L1-Rule
priority: 2
trigger: always_on
---

> [!IMPORTANT]
> Override Priority: TIER 2


# Nguyên tắc 03: Tiêu chuẩn chất lượng đầu ra & Quy cách tài liệu

## 1. Mục tiêu
Đảm bảo tất cả các bảng tính, báo cáo phân tích và dashboard do Agent tạo ra đều đạt tiêu chuẩn chuyên nghiệp, sẵn sàng cho việc kiểm duyệt của doanh nghiệp.

## 2. Tiêu chuẩn bảng tính Excel (`.xlsx`)
Mọi tệp Excel do Agent sinh ra phải tuân thủ nghiêm ngặt các quy tắc sau:
- **Định dạng nhất quán:** Giá bán phải được định dạng dạng số có dấu phân cách hàng nghìn (ví dụ: `150,000 VNĐ`). Không viết dạng text thô như `150k` hoặc `150000 vnđ`.
- **Chỉ số đánh giá (Ratings):** Phải lưu ở dạng số thuần túy (ví dụ: `4.5` thay vì `4.5/5 sao` hoặc `4.5/5`).
- **Không bị cắt chữ:** Độ rộng các cột phải được tự động điều chỉnh bằng thư viện `openpyxl` của Python để vừa với độ dài của chuỗi dài nhất.
- **Tiêu đề bảng dữ liệu:** Chữ in đậm, màu chữ trắng, nền tiêu đề màu tối (Xanh đậm Navy hoặc Xám đậm) và căn giữa.

## 3. Tiêu chuẩn viết Insight phân tích (Công thức OEIA)
Các nhận định (Insights) tuyệt đối không được chung chung (ví dụ: "Quán cafe Quận 1 rất đa dạng"). Mỗi Insight bắt buộc phải viết theo cấu trúc OEIA:
- **Quan sát (Observation - O):** Xu hướng chính hoặc sự bất thường được phát hiện từ dữ liệu.
- **Bằng chứng (Evidence - E):** Số liệu toán học trực tiếp chứng minh (ví dụ: "11 trên 15 quán, chiếm 73.3%", "Mức giá trung bình là 65,000 VNĐ").
- **Diễn giải (Interpretation - I):** Lý do thực tiễn kinh doanh hoặc lý thuyết thị trường đằng sau xu hướng đó.
- **Hành động gợi ý (Action Implication - A):** Đề xuất hành động thực tiễn cho chủ doanh nghiệp.

## 4. Tiêu chuẩn tài liệu báo cáo Word (`.docx`)
- **Phân cấp tiêu đề:** Tiêu đề lớn duy nhất H1, các tiêu đề mục H2, các chi tiết phụ H3.
- **Tóm tắt dự án:** Phải có phần tóm tắt ngắn gọn trong 3 câu ở đầu báo cáo.
- **Nhật ký giới hạn dữ liệu:** Mọi báo cáo phải có một mục riêng liệt kê các mặt hạn chế của dữ liệu, cỡ mẫu nhỏ, hoặc các nguồn tin có độ tin cậy thấp.
