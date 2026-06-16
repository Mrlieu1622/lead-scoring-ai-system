import os
import sys
import urllib.request
import pandas as pd

# Force UTF-8 stdout for Windows terminals to avoid UnicodeEncodeErrors
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1hRvHE6RXm1peVG07avfApPEHocOcPld9IA94hE3vUGE/export?format=csv"
RAW_DATA_PATH = os.path.join("01_dau_vao", "data_raw.xlsx")

def generate_mock_data():
    """Generates realistic real estate customer leads matching the rules in tieu_chi_cham_diem."""
    print("Generating high-quality mock BĐS leads data...")
    mock_leads = [
        {
            "Mã KH": "KH001",
            "Họ tên": "Nguyễn Văn A",
            "Số điện thoại": "0912345678",
            "Nhu cầu": "Cần tìm mua Biệt thự đơn lập tại Vinhomes Ocean Park, tài chính khoảng 35 tỷ, yêu cầu pháp lý chuẩn 100% có sổ hồng riêng. Muốn gặp trực tiếp chủ đầu tư để đàm phán."
        },
        {
            "Mã KH": "KH002",
            "Họ tên": "Trần Thị B",
            "Số điện thoại": "0987654321",
            "Nhu cầu": "Tìm kiếm căn Penthouse ven sông khu Phú Mỹ Hưng, Quận 1. Tài chính mạnh không thành vấn đề. Tôi là nhà đầu tư chuyên nghiệp muốn mua sỉ."
        },
        {
            "Mã KH": "KH003",
            "Họ tên": "Phạm Minh C",
            "Số điện thoại": "0901234567",
            "Nhu cầu": "Là chủ doanh nghiệp cần tìm mua Quỹ đất công nghiệp hoặc sàn văn phòng diện tích lớn khu vực TP.HCM. Pháp lý sổ hồng riêng rõ ràng."
        },
        {
            "Mã KH": "KH004",
            "Họ tên": "Lê Văn D",
            "Số điện thoại": "0934567890",
            "Nhu cầu": "Cần mua nhà mặt phố Quận 1 giá 1-2 tỷ có sân vườn hồ bơi."
        },
        {
            "Mã KH": "KH005",
            "Họ tên": "Hoàng Thị E",
            "Số điện thoại": "0945678901",
            "Nhu cầu": "Nhầm số rồi em ơi, chị không có nhu cầu mua bán bất động sản gì đâu nhé, dữ liệu cũ rồi."
        },
        {
            "Mã KH": "KH006",
            "Họ tên": "Nguyễn Văn F",
            "Số điện thoại": "0956789012",
            "Nhu cầu": "Mời chào gói bảo hiểm nhân thọ và hỗ trợ vay vốn ngân hàng lãi suất thấp 5%."
        },
        {
            "Mã KH": "KH007",
            "Họ tên": "Trần Văn G",
            "Số điện thoại": "0967890123",
            "Nhu cầu": "Khách này gọi nhiều lần không bắt máy, thuê bao không liên lạc được, không phản hồi Zalo."
        },
        {
            "Mã KH": "KH008",
            "Họ tên": "Phạm Thị H",
            "Số điện thoại": "0978901234",
            "Nhu cầu": "Cần tìm mua căn hộ chung cư 2 phòng ngủ khoảng 3.5 tỷ tại Quận 7. Cần vay ngân hàng hỗ trợ 70%."
        },
        {
            "Mã KH": "KH009",
            "Họ tên": "Vũ Văn I",
            "Số điện thoại": "0989012345",
            "Nhu cầu": "Tìm nhà phố phân khúc 5-7 tỷ ở Bình Thạnh, đang cân nhắc chính sách thanh toán của chủ đầu tư."
        },
        {
            "Mã KH": "KH010",
            "Họ tên": "Đặng Thị J",
            "Số điện thoại": "0990123456",
            "Nhu cầu": "Nhu cầu thực tìm mua đất nền vùng ven tầm 2 tỷ, cần tư vấn thêm về pháp lý và quy hoạch vị trí."
        }
    ]
    
    df = pd.DataFrame(mock_leads)
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    df.to_excel(RAW_DATA_PATH, index=False)
    print(f"Mock leads written successfully to {RAW_DATA_PATH}")

def main():
    print("Executing fetch_leads...")
    try:
        req = urllib.request.Request(
            SPREADSHEET_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        print(f"Attempting to download Google Sheet from: {SPREADSHEET_URL}")
        with urllib.request.urlopen(req) as response:
            content = response.read()
            temp_csv = "temp_leads.csv"
            with open(temp_csv, "wb") as f:
                f.write(content)
            
            df = pd.read_csv(temp_csv)
            os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
            df.to_excel(RAW_DATA_PATH, index=False)
            os.remove(temp_csv)
            print(f"Dữ liệu tải về từ Google Sheets và lưu thành công vào {RAW_DATA_PATH}!")
    except Exception as e:
        print(f"Không thể tải từ Google Sheets (Lỗi: {e}).")
        print("Kích hoạt cơ chế dự phòng: Sử dụng dữ liệu giả lập chuẩn.")
        if not os.path.exists(RAW_DATA_PATH):
            generate_mock_data()
        else:
            print(f"Tệp dữ liệu gốc {RAW_DATA_PATH} đã tồn tại, tiếp tục sử dụng.")

if __name__ == "__main__":
    main()
