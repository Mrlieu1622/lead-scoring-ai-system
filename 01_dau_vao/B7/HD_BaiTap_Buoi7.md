# Hướng dẫn Nâng cấp Hệ thống AI Lead Scoring - Buổi 7

Tài liệu này hướng dẫn chi tiết cách hoàn thành các yêu cầu nâng cấp hệ thống chấm điểm khách hàng tiềm năng (Lead Scoring) bao gồm: **Bảo mật kết nối Google Sheets ở chế độ riêng tư** và **Tối ưu giao diện Premium UI/UX**.

---

## Mục tiêu 1: Bảo mật dữ liệu (Private Google Sheets Integration)

Mặc định, việc tải dữ liệu bằng link công khai (`/export?format=xlsx`) yêu cầu trang tính phải ở chế độ công khai cho bất kỳ ai. Để đọc được tệp trang tính ở chế độ **Riêng tư (Private)** một cách an toàn, chúng ta cần sử dụng tài khoản dịch vụ **Google Service Account** và cấu hình bảo mật thông qua Streamlit Secrets.

### Bước 1.1: Tạo Google Service Account
1. Truy cập **[Google Cloud Console](https://console.cloud.google.com/)**.
2. Tạo một dự án mới (Project).
3. Bật (Enable) hai API sau:
   - **Google Sheets API**
   - **Google Drive API**
4. Vào mục **IAM & Admin** > **Service Accounts** > Chọn **Create Service Account**.
5. Nhập tên tài khoản dịch vụ và nhấn **Create**.
6. Tại danh sách Service Accounts, chọn tài khoản vừa tạo > vào tab **Keys** > **Add Key** > **Create new key** > Chọn định dạng **JSON**.
7. Một tệp JSON chứa thông tin xác thực bảo mật sẽ được tải xuống máy tính của bạn.

### Bước 1.2: Chia sẻ Google Sheet với Service Account
1. Mở tệp JSON vừa tải xuống, tìm trường `"client_email"` (địa chỉ email dạng: `tên-tài-khoản@dự-án.iam.gserviceaccount.com`).
2. Mở file Google Sheets riêng tư của bạn.
3. Bấm **Share** (Chia sẻ) > Thêm email của Service Account này vào với quyền **Viewer** (Người xem) hoặc **Editor** (Người chỉnh sửa).

### Bước 1.3: Cấu hình bảo mật trên Streamlit (Streamlit Secrets)
Khi đưa ứng dụng lên Streamlit Cloud, tuyệt đối **không được đẩy tệp JSON credential lên GitHub** vì lý do bảo mật. Chúng ta sẽ lưu thông tin tệp JSON vào Streamlit Secrets:

1. **Cấu hình cục bộ (Local testing):**
   Tạo tệp `.streamlit/secrets.toml` trong thư mục dự án của bạn và dán nội dung từ tệp JSON theo định dạng sau:
   ```toml
   [gcp_service_account]
   type = "service_account"
   project_id = "xxx"
   private_key_id = "xxx"
   private_key = "----BEGIN PRIVATE KEY----\\nxxx\\n-----END PRIVATE KEY-----\\n"
   client_email = "xxx"
   client_id = "xxx"
   auth_uri = "https://accounts.google.com/o/oauth2/auth"
   token_uri = "https://oauth2.googleapis.com/token"
   auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
   client_x509_cert_url = "https://www.googleapis.com/role/xxx"
   ```

2. **Cấu hình trên Streamlit Cloud:**
   Vào Dashboard Streamlit Cloud của ứng dụng > **Settings** > **Secrets** > Dán toàn bộ nội dung của tệp `secrets.toml` vào đây.

### Bước 1.4: Mã nguồn đọc Google Sheets riêng tư trong Python
Sử dụng thư viện `gspread` và `google-auth` để kết nối:
```python
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def load_private_sheet(sheet_url):
    # Định nghĩa các quyền truy cập cần thiết
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Lấy thông tin tài khoản dịch vụ từ Streamlit Secrets
    secret_info = st.secrets["gcp_service_account"]
    
    # Tạo đối tượng Credentials
    credentials = Credentials.from_service_account_info(secret_info, scopes=scopes)
    
    # Kết nối gspread
    client = gspread.authorize(credentials)
    
    # Mở bảng tính qua URL
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet(0) # Lấy sheet đầu tiên
    
    # Chuyển đổi dữ liệu sang Pandas DataFrame
    records = worksheet.get_all_records()
    return pd.DataFrame(records)
```

---

## Mục tiêu 2: Tối ưu giao diện Premium UI/UX (Techcombank Aesthetic)

Để giao diện không bị đơn sơ, ta áp dụng phong cách thiết kế ứng dụng ngân hàng số cao cấp **Techcombank Priority / Private Banking**:

### 2.1 Bảng màu thương hiệu (Techcombank Brand Palette)
- **Màu nhấn chủ đạo (Primary Red):** `#EB1F3A` (Màu đỏ Techcombank đặc trưng).
- **Màu nền (Background):** Slate/Obsidian Grey (`#0f172a` và `#1e293b`) tạo chiều sâu và cảm giác bảo mật tối đa.
- **Màu chữ chính:** Trắng (`#ffffff`) để tăng cường độ tương phản.
- **Màu chữ mô tả:** Xám mờ (`#94a3b8`) để giảm tải thông tin không quan trọng.

### 2.2 Tích hợp Dashboard KPI trực quan
Sử dụng các thẻ số liệu dạng Glassmorphism kèm đường kẻ định hạng ở đỉnh thẻ:
```python
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div class='metric-card' style='border-top: 4px solid #94a3b8;'><div class='metric-label'>👥 Tổng số hồ sơ</div><div class='metric-val'>10</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='metric-card' style='border-top: 4px solid #fbbf24;'><div class='metric-label' style='color:#fbbf24;'>👑 VIP / Priority</div><div class='metric-val'>3</div></div>", unsafe_allow_html=True)
```

### 2.3 Custom CSS trong Streamlit
Chèn mã CSS tùy chỉnh trực tiếp vào Streamlit để thiết kế lại nút bấm và thẻ số liệu:
```python
st.markdown("""
<style>
    /* Nút bấm đỏ đặc trưng Techcombank */
    .stButton>button {
        background: linear-gradient(135deg, #EB1F3A, #b91c1c) !important;
        color: white !important;
        border: 1px solid #EB1F3A !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        transition: all 0.25s ease !important;
    }
    .stButton>button:hover {
        background: #EB1F3A !important;
        box-shadow: 0 6px 22px rgba(235, 31, 58, 0.5) !important;
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)
```
