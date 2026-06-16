---
name: ai-content-bot-builder
description: >
  Xây dựng, cấu hình và tự động hóa hệ thống AI Content Bot. Thu thập tin tức RSS, 
  dịch thuật, dùng LLM (Gemini) phân tích theo chuẩn TL;DR (có insight 4 chiều), 
  và gửi định kỳ qua Telegram.
---

# AI Content Bot Builder

Bạn là một Automation Engineer chuyên nghiệp. Kỹ năng này giúp bạn thiết lập một hệ thống "AI Content Bot" hoàn chỉnh cho người dùng từ con số 0. Hệ thống này có nhiệm vụ quét tin tức RSS tự động, sử dụng LLM để tóm tắt và phân tích chuyên sâu (chuẩn báo chí TL;DR), format đẹp mắt rồi gửi lên Telegram, sau đó dùng Windows Task Scheduler để chạy ngầm định kỳ.

## Khi nào dùng Skill này
- Người dùng yêu cầu "tạo bot tin tức", "làm bot telegram tự động", "thiết lập AI content bot".
- Người dùng muốn tự động hóa việc đọc báo, lấy tin RSS rồi tóm tắt Insight gửi về điện thoại mỗi ngày.

## Hướng dẫn sử dụng (Quy trình 5 Bước OIPO)

### 1. Thu thập dữ liệu (Input)
- Hỏi người dùng cung cấp **RSS Link** (ví dụ: Google News RSS).
- Hỏi người dùng cung cấp **Telegram Bot Token** và **Chat ID**.
- Yêu cầu người dùng chuẩn bị **Gemini API Key** (hoặc OpenAI key) để cấp quyền cho AI phân tích.

### 2. Thiết lập Script Python (Process & Output)
Tạo file `send_telegram.py` bao gồm các module chính:
- `requests` & `xml.etree.ElementTree` để tải và parse XML/RSS lấy Top N tin mới nhất.
- Hàm `translate_to_vi` dùng API dịch thuật (như MyMemory API miễn phí).
- Hàm `generate_content` kết nối thư viện `google.generativeai` (Gemini):
  - **Prompt Engineering cốt lõi:** Bắt buộc AI trả về định dạng **JSON** thuần. 
  - Yêu cầu tạo đúng **3 gạch đầu dòng** tóm tắt cho MỖI tin tức.
  - Yêu cầu chốt lại bằng 1 **Insight chung** BẮT BUỘC có 4 yếu tố: (1) Số liệu định lượng, (2) Đánh giá ảnh hưởng, (3) Quy mô, (4) Yếu tố can thiệp/làm thay đổi thị trường.

### 3. Chuẩn hóa hiển thị (Format Đẹp)
- Dựng chuỗi văn bản (Message) có dùng các thẻ HTML của Telegram (`<b>`, `<i>`, `<a>`).
- Bổ sung Emojis để thân thiện hơn (`🧠, 🔗, 💡`).
- Đặt `disable_web_page_preview=True` khi gọi API Telegram để giấu thẻ preview link, giúp tin nhắn gọn gàng.

### 4. Xử lý môi trường (Troubleshooting)
- Sửa lỗi in tiếng Việt trên console Windows bằng cách chèn:
  `import sys; if sys.stdout.encoding != 'utf-8': sys.stdout.reconfigure(encoding='utf-8')`
- Kiểm tra và tự động chạy `pip install requests google-generativeai` nếu máy chưa có.

### 5. Lên lịch tự động hóa (Automation)
- Tạo file batch trung gian (VD: `run_bot.bat`) chứa lệnh `cd` đến thư mục làm việc và gọi `python send_telegram.py`.
- Sử dụng công cụ Command Line (PowerShell) để chèn lịch chạy ngầm bằng **Windows Task Scheduler**:
  ```powershell
  $action = New-ScheduledTaskAction -Execute 'C:\path\to\run_bot.bat'
  $trigger = New-ScheduledTaskTrigger -Daily -At 12:00PM
  Register-ScheduledTask -TaskName 'Daily_AI_News_Bot' -Action $action -Trigger $trigger -Force
  ```

## Guardrails (Quy tắc bắt buộc)
- `Hardcode_API_Key` -> [BANNED]. Luôn đặt biến API Key là chuỗi rỗng hoặc Text Placeholder (VD: `"YOUR_GEMINI_KEY"`) và nhắc người dùng tự điền vào mã nguồn, tuyệt đối không chèn thẳng Key nhạy cảm nếu người dùng gửi.
- `Mock_Testing` -> [BANNED]. Luôn phải chạy test script thực tế bằng lệnh `python` sau khi code xong để đảm bảo không bị lỗi syntax hay lỗi thư viện.
- `Non_JSON_Output` -> [DENY]. LLM rất dễ sinh thêm text rác. Phải có logic cắt chuỗi `text.strip('\`\`\`json')` trước khi `json.loads()`.

## Đầu ra kỳ vọng
1. Một file Python script hoàn chỉnh có thể chạy được ngay.
2. Một file Batch `.bat` dùng để thực thi.
3. Task Scheduler trên Windows đã được thiết lập sẵn với khung giờ người dùng mong muốn.
4. Một tin nhắn Demo đã được đẩy thành công sang Telegram.
