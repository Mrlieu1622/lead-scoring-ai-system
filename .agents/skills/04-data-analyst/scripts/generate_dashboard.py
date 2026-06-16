import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# UTF-8 Encoding Handler
sys.stdout.reconfigure(encoding='utf-8')

def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_dashboard.py <input_clean_path> <output_dashboard_path> <output_charts_dir>")
        sys.exit(1)

    input_path = sys.argv[1]
    dashboard_path = sys.argv[2]
    charts_dir = sys.argv[3]

    print(f"[INFO] Bắt đầu phân tích dữ liệu chuyên sâu từ: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"[ERROR] Không tìm thấy file dữ liệu sạch: {input_path}")
        sys.exit(1)
        
    try:
        if input_path.endswith('.csv'):
            df = pd.read_csv(input_path)
        else:
            df = pd.read_excel(input_path)
            
        os.makedirs(os.path.dirname(dashboard_path), exist_ok=True)
        os.makedirs(charts_dir, exist_ok=True)

        # 1. Thống kê mô tả cơ bản (Descriptive Statistics)
        numeric_df = df.select_dtypes(include=['number'])
        stats_df = numeric_df.describe().reset_index()

        # 2. Phân tích Mô Tả: Doanh thu & Lợi nhuận theo Ngành hàng, Vùng và Kênh
        # Tính Margin % = Profit / Revenue
        # Để tránh chia cho 0
        df['MARGIN_PCT'] = (df['PROFIT'] / df['REVENUE'].replace(0, 1)) * 100
        
        prod_summary = df.groupby('PRODUCT_CATEGORY').agg(
            TOTAL_QUANTITY=('QUANTITY', 'sum'),
            TOTAL_REVENUE=('REVENUE', 'sum'),
            TOTAL_PROFIT=('PROFIT', 'sum'),
            AVG_MARGIN_PCT=('MARGIN_PCT', 'mean')
        ).reset_index().sort_values(by='TOTAL_REVENUE', ascending=False)
        
        region_summary = df.groupby('REGION').agg(
            TOTAL_REVENUE=('REVENUE', 'sum'),
            TOTAL_PROFIT=('PROFIT', 'sum'),
            AVG_MARGIN_PCT=('MARGIN_PCT', 'mean')
        ).reset_index().sort_values(by='TOTAL_REVENUE', ascending=False)

        channel_summary = df.groupby('CHANNEL').agg(
            TOTAL_REVENUE=('REVENUE', 'sum'),
            TOTAL_PROFIT=('PROFIT', 'sum'),
            AVG_MARGIN_PCT=('MARGIN_PCT', 'mean')
        ).reset_index().sort_values(by='TOTAL_REVENUE', ascending=False)

        # Vẽ biểu đồ Doanh thu theo Ngành hàng (Bar Chart)
        plt.figure(figsize=(10, 6))
        plt.bar(prod_summary['PRODUCT_CATEGORY'], prod_summary['TOTAL_REVENUE'], color='#1f77b4')
        plt.title('Tổng Doanh Thu Theo Danh Mục Sản Phẩm (Descriptive)')
        plt.xlabel('Danh Mục Sản Phẩm')
        plt.ylabel('Doanh Thu ($)')
        plt.xticks(rotation=15)
        plt.tight_layout()
        chart_rev_path = os.path.join(charts_dir, 'revenue_by_product_category.png')
        plt.savefig(chart_rev_path)
        plt.close()

        # 3. Phân tích Chẩn Đoán (Diagnostic 1): Tại sao Tỷ lệ Trả Hàng (Return Rate) lại cao?
        # Tính tỷ lệ trả hàng (trung bình của RETURN_FLAG * 100) theo Ngành hàng và Vùng miền
        return_by_prod = df.groupby('PRODUCT_CATEGORY')['RETURN_FLAG'].mean().reset_index()
        return_by_prod['RETURN_RATE_PCT'] = return_by_prod['RETURN_FLAG'] * 100
        return_by_prod = return_by_prod.sort_values(by='RETURN_RATE_PCT', ascending=False)

        return_by_region = df.groupby('REGION')['RETURN_FLAG'].mean().reset_index()
        return_by_region['RETURN_RATE_PCT'] = return_by_region['RETURN_FLAG'] * 100
        return_by_region = return_by_region.sort_values(by='RETURN_RATE_PCT', ascending=False)

        # Vẽ biểu đồ Tỷ lệ trả hàng theo Ngành hàng (Bar Chart)
        plt.figure(figsize=(10, 6))
        plt.bar(return_by_prod['PRODUCT_CATEGORY'], return_by_prod['RETURN_RATE_PCT'], color='#d62728')
        plt.title('Tỷ Lệ Trả Hàng (%) Theo Danh Mục Sản Phẩm (Diagnostic)')
        plt.xlabel('Danh Mục Sản Phẩm')
        plt.ylabel('Tỷ Lệ Trả Hàng (%)')
        plt.xticks(rotation=15)
        plt.tight_layout()
        chart_ret_path = os.path.join(charts_dir, 'return_rate_by_product_category.png')
        plt.savefig(chart_ret_path)
        plt.close()

        # 4. Phân tích Chẩn Đoán (Diagnostic 2): Tại sao một số Đơn Hàng bị Thua Lỗ?
        # Chia làm 2 nhóm: Nhóm Lỗ (Profit < 0) và Nhóm Lãi (Profit >= 0)
        df['IS_LOSS'] = df['PROFIT'] < 0
        loss_diagnostic = df.groupby('IS_LOSS').agg(
            COUNT=('ORDER_ID', 'count'),
            AVG_REVENUE=('REVENUE', 'mean'),
            AVG_DISCOUNT_PCT=('DISCOUNT', 'mean'), # Giả định DISCOUNT là tỷ lệ % hoặc số tiền
            AVG_MARKETING_COST=('MARKETING_COST', 'mean'),
            AVG_COGS=('COGS', 'mean'),
            AVG_PROFIT=('PROFIT', 'mean')
        ).reset_index()
        
        # 5. Xuất file Excel Dashboard
        with pd.ExcelWriter(dashboard_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Data_Clean', index=False)
            stats_df.to_excel(writer, sheet_name='Thong_Ke_Mo_Ta', index=False)
            
            # Ghi tóm tắt doanh thu lợi nhuận
            prod_summary.to_excel(writer, sheet_name='Doanh_Thu_Loi_Nhuan', index=False)
            # Chèn chart Doanh thu
            workbook = writer.book
            worksheet_df = writer.sheets['Doanh_Thu_Loi_Nhuan']
            worksheet_df.insert_image('F2', chart_rev_path, {'x_scale': 0.7, 'y_scale': 0.7})
            
            # Ghi chẩn đoán trả hàng
            return_by_prod.to_excel(writer, sheet_name='Chan_Doan_Tra_Hang', index=False)
            worksheet_ret = writer.sheets['Chan_Doan_Tra_Hang']
            worksheet_ret.insert_image('D2', chart_ret_path, {'x_scale': 0.7, 'y_scale': 0.7})

            # Ghi chẩn đoán đơn lỗ
            loss_diagnostic.to_excel(writer, sheet_name='Chan_Doan_Don_Hang_Lo', index=False)

        print(f"[SUCCESS] Dashboard nâng cấp đã được lưu tại: {dashboard_path}")

    except Exception as e:
        print(f"[ERROR] Lỗi trong quá trình phân tích dữ liệu nâng cấp: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
