import sys
import os
import pandas as pd

# UTF-8 Encoding Handler (Antigravity Mandate)
sys.stdout.reconfigure(encoding='utf-8')

def main():
    if len(sys.argv) < 3:
        print("Usage: python collect_data.py <input_file_path> <output_log_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_log_path = sys.argv[2]

    print(f"[INFO] Bắt đầu thu thập dữ liệu từ: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"[ERROR] Không tìm thấy file tại đường dẫn: {input_path}")
        sys.exit(1)
        
    try:
        # Hỗ trợ cả csv và excel
        if input_path.endswith('.csv'):
            df = pd.read_csv(input_path)
        else:
            df = pd.read_excel(input_path)
            
        print("[SUCCESS] Đã tải dữ liệu thành công.")
        
        # Trích xuất metadata
        num_rows, num_cols = df.shape
        missing_values = df.isnull().sum()
        data_types = df.dtypes
        
        # Viết log Markdown
        log_content = f"# Báo Cáo Kiểm Tra Cấu Trúc (Schema Validation)\n\n"
        log_content += f"- **Nguồn dữ liệu:** `{os.path.basename(input_path)}`\n"
        log_content += f"- **Tổng số dòng:** {num_rows}\n"
        log_content += f"- **Tổng số cột:** {num_cols}\n\n"
        
        log_content += "## Cấu trúc cột và Kiểu dữ liệu\n"
        log_content += "| Tên Cột | Kiểu Dữ Liệu | Số lượng Null |\n"
        log_content += "|---|---|---|\n"
        
        for col in df.columns:
            log_content += f"| {col} | {data_types[col]} | {missing_values[col]} |\n"
            
        os.makedirs(os.path.dirname(output_log_path), exist_ok=True)
        with open(output_log_path, 'w', encoding='utf-8') as f:
            f.write(log_content)
            
        print(f"[INFO] Báo cáo Schema Validation đã được lưu tại: {output_log_path}")

    except Exception as e:
        print(f"[ERROR] Lỗi trong quá trình nạp dữ liệu: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
