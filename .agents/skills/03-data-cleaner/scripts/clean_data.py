import sys
import os
import pandas as pd

# UTF-8 Encoding Handler
sys.stdout.reconfigure(encoding='utf-8')

def main():
    if len(sys.argv) < 3:
        print("Usage: python clean_data.py <input_raw_path> <output_clean_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    print(f"[INFO] Bắt đầu làm sạch dữ liệu từ: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"[ERROR] Không tìm thấy file: {input_path}")
        sys.exit(1)
        
    try:
        # Hỗ trợ cả csv và excel
        if input_path.endswith('.csv'):
            df = pd.read_csv(input_path)
        else:
            df = pd.read_excel(input_path)
            
        initial_rows = len(df)
        
        # 1. Drop duplicates
        df = df.drop_duplicates()
        dedup_rows = len(df)
        print(f"[INFO] Đã xóa {initial_rows - dedup_rows} dòng trùng lặp.")
        
        # 2. Xử lý Nulls cơ bản
        # - Cột số: Điền 0 (hoặc mean tùy logic nâng cao, ở đây dùng 0 cho an toàn)
        # - Cột chuỗi: Điền 'Unknown'
        numeric_cols = df.select_dtypes(include=['number']).columns
        string_cols = df.select_dtypes(include=['object', 'string']).columns
        
        df[numeric_cols] = df[numeric_cols].fillna(0)
        df[string_cols] = df[string_cols].fillna('Unknown')
        
        print("[INFO] Đã xử lý các giá trị Null.")
        
        # 3. Ép kiểu dữ liệu (nếu cần thiết, dựa vào data types)
        # 4. Xuất file data_clean.xlsx
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_excel(output_path, index=False)
        
        print(f"[SUCCESS] Dữ liệu sạch đã được lưu tại: {output_path}")

    except Exception as e:
        print(f"[ERROR] Lỗi trong quá trình làm sạch: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
