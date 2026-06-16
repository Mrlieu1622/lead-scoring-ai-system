---
name: lead-scoring
description: Automatically scores real estate leads from Google Sheets or Excel files based on business criteria.
---

# Lead Scoring Skill

Skill này giúp tự động hóa việc lấy dữ liệu khách hàng từ Google Sheets (hoặc tệp Excel) và chấm điểm tiềm năng (Lead Scoring) dựa trên bộ tiêu chí kinh doanh bất động sản.

## Tiêu chí chấm điểm

1. **Cộng 50 điểm (VIP/Siêu tiềm năng):**
   - Ngân sách lớn: >= 20 tỷ hoặc chứa "tài chính mạnh", "không thành vấn đề".
   - Loại hình cao cấp: Biệt thự đơn lập, Penthouse, Shophouse mặt đường lớn, Quỹ đất công nghiệp, Sàn văn phòng diện tích lớn.
   - Vị trí đắc địa: Quận 1, Ven sông, Vinhomes Ocean Park, Phú Mỹ Hưng.
   - Phân loại khách: Chủ doanh nghiệp, Nhà đầu tư chuyên nghiệp, Mua sỉ, Mua số lượng lớn.
   - Tính cấp thiết & Minh bạch: Pháp lý chuẩn 100%, Sổ hồng riêng, Muốn gặp trực tiếp chủ đầu tư để đàm phán.

2. **Trừ 50 điểm (Không tiềm năng):**
   - Yêu cầu phi thực tế: Giá rẻ bất ngờ ở trung tâm (Quận 1 giá 1-2 tỷ, trung tâm có sân vườn hồ bơi giá vài trăm triệu).
   - Không có nhu cầu: Nhầm số, Không có nhu cầu, Dữ liệu cũ, Nhầm ngành.
   - Khách không thiện chí: Hỏi giá cho vui, Chưa có ý định mua, Thái độ không hợp tác.
   - Spam/Quảng cáo: Bảo hiểm, Vay vốn, Mời chào dịch vụ.
   - Thông tin liên lạc lỗi: Thuê bao, Gọi nhiều lần không bắt máy, Không phản hồi Zalo.

3. **Giữ nguyên (100 điểm - Tiềm năng):**
   - Mua chung cư, nhà phố tầm trung (3-10 tỷ).
   - Cần vay ngân hàng, đang cân nhắc chính sách.
   - Nhu cầu thực nhưng cần tư vấn thêm pháp lý hoặc vị trí.

## Hướng dẫn sử dụng

Sử dụng script Python `lead_scoring.py` nằm cùng thư mục để thực hiện chấm điểm.

### Cú pháp
```bash
python lead_scoring.py <source_path_or_google_sheets_url> [--output <path_to_output_file>]
```

### Tham số
- `<source_path_or_google_sheets_url>`: Đường dẫn tệp Excel đầu vào hoặc URL liên kết Google Sheets dạng công khai.
- `--output`: (Tùy chọn) Đường dẫn xuất tệp Excel kết quả. Mặc định là `lead_scored_report.xlsx`.

### Ví dụ
```bash
python "C:\Users\PC\.gemini\config\plugins\custom\skills\lead-scoring\lead_scoring.py" "https://docs.google.com/spreadsheets/d/1hRvHE6RXm1peVG07avfApPEHocOcPld9IA94hE3vUGE/edit?gid=0#gid=0" --output "d:\PDCA_Workspace_Template\05_san_pham\data_final.xlsx"
```
