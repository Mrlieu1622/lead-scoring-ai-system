import sys
import os
import glob
import pandas as pd

# UTF-8 Encoding Handler
sys.stdout.reconfigure(encoding='utf-8')

def main():
    if len(sys.argv) < 5:
        print("Usage: python generate_report.py <input_insights_txt_path> <charts_dir> <output_report_path> <dashboard_excel_path>")
        sys.exit(1)

    insights_path = sys.argv[1]
    charts_dir = sys.argv[2]
    output_path = sys.argv[3]
    excel_path = sys.argv[4]

    print(f"[INFO] Bắt đầu tổng hợp báo cáo nâng cấp từ: {insights_path}")
    
    if not os.path.exists(insights_path):
        print(f"[ERROR] Không tìm thấy file chứa insights: {insights_path}")
        sys.exit(1)
        
    try:
        # Đọc insights từ file tạm
        with open(insights_path, 'r', encoding='utf-8') as f:
            insights_content = f.read()
            
        kpis_html = ""
        desc_md = ""
        diag_ret_md = ""
        diag_loss_md = ""
        
        if os.path.exists(excel_path):
            try:
                # 1. Đọc Thống kê mô tả từ Data_Clean để tính KPI tổng
                raw_df = pd.read_excel(excel_path, sheet_name='Data_Clean')
                
                total_orders = len(raw_df)
                total_qty = int(raw_df['QUANTITY'].sum())
                total_revenue = float(raw_df['REVENUE'].sum())
                total_discount = float(raw_df['DISCOUNT'].sum())
                total_marketing = float(raw_df['MARKETING_COST'].sum())
                total_cogs = float(raw_df['COGS'].sum())
                total_profit = float(raw_df['PROFIT'].sum())
                
                avg_margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0
                avg_delivery = float(raw_df['DELIVERY_TIME_DAYS'].mean())
                return_rate = float(raw_df['RETURN_FLAG'].mean()) * 100
                
                # Tạo KPI Card Table
                kpis_html += "### 📊 Chỉ Số KPI Doanh Nghiệp Cốt Lõi (Descriptive KPIs)\n\n"
                kpis_html += "| Chỉ số KPI | Giá trị Thực tế | Phân loại / Đánh giá | Trạng thái |\n"
                kpis_html += "|---|---|---|---|\n"
                kpis_html += f"| 📦 **Tổng Sản Lượng Đã Bán** | {total_qty:,} sản phẩm | Quy mô sản xuất | Ổn định |\n"
                kpis_html += f"| 💰 **Tổng Doanh Thu (Revenue)** | ${total_revenue:,.2f} | Quy mô tài chính | Đạt mục tiêu |\n"
                kpis_html += f"| 💵 **Tổng Chiết Khấu (Discount)** | ${total_discount:,.2f} | Tỷ lệ giảm giá: {(total_discount/total_revenue*100):.1f}% | Cần giám sát |\n"
                kpis_html += f"| 📢 **Tổng Chi Phí Marketing** | ${total_marketing:,.2f} | Hiệu quả quảng cáo | Bình thường |\n"
                kpis_html += f"| ⚙️ **Tổng Giá Vốn Hàng Bán (COGS)** | ${total_cogs:,.2f} | Giá thành sản xuất | Chiếm {(total_cogs/total_revenue*100):.1f}% Doanh thu |\n"
                kpis_html += f"| 💎 **Tổng Lợi Nhuận (Profit)** | ${total_profit:,.2f} | Biên lợi nhuận gộp: **{avg_margin:.1f}%** | Khá tốt |\n"
                kpis_html += f"| ⚠️ **Tỷ Lệ Trả Hàng (Return Rate)** | **{return_rate:.1f}%** | Biên độ trả hàng | 🚨 Báo động đỏ |\n"
                kpis_html += f"| 🚚 **Thời Gian Giao Hàng TB** | {avg_delivery:.2f} ngày | Tốc độ logistics | ⚠️ Cần cải thiện |\n\n"
                
                # 2. Đọc Doanh_Thu_Loi_Nhuan (Descriptive Table)
                prod_df = pd.read_excel(excel_path, sheet_name='Doanh_Thu_Loi_Nhuan')
                desc_md += "### 🛒 Phân Tích Doanh Thu & Lợi Nhuận Theo Ngành Hàng (Descriptive Table)\n\n"
                desc_md += "| Ngành Hàng | Tổng Sản Lượng | Tổng Doanh Thu ($) | Tổng Lợi Nhuận ($) | Biên Lợi Nhuận TB (%) |\n"
                desc_md += "|---|---|---|---|---|\n"
                for idx, row in prod_df.iterrows():
                    desc_md += f"| {row['PRODUCT_CATEGORY']} | {row['TOTAL_QUANTITY']:,} | ${row['TOTAL_REVENUE']:,.2f} | ${row['TOTAL_PROFIT']:,.2f} | {row['AVG_MARGIN_PCT']:.1f}% |\n"
                desc_md += "\n"
                
                # 3. Đọc Chan_Doan_Tra_Hang (Diagnostic Table 1)
                ret_df = pd.read_excel(excel_path, sheet_name='Chan_Doan_Tra_Hang')
                diag_ret_md += "### 🔍 Chẩn Đoán 1: Phân Tích Tỷ Lệ Trả Hàng Theo Danh Mục Sản Phẩm\n\n"
                diag_ret_md += "| Danh Mục Sản Phẩm | Tỷ Lệ Trả Hàng (%) | Mức Độ Rủi Ro | Đánh Giá Nguyên Nhân |\n"
                diag_ret_md += "|---|---|---|---|\n"
                for idx, row in ret_df.iterrows():
                    rate = row['RETURN_RATE_PCT']
                    risk = "🚨 Cực cao" if rate > 25 else "⚠️ Cao" if rate > 15 else "✅ Bình thường"
                    diag_ret_md += f"| {row['PRODUCT_CATEGORY']} | {rate:.1f}% | {risk} | Cần kiểm tra kỹ mô tả & QA sản phẩm |\n"
                diag_ret_md += "\n"
                
                # 4. Đọc Chan_Doan_Don_Hang_Lo (Diagnostic Table 2)
                loss_df = pd.read_excel(excel_path, sheet_name='Chan_Doan_Don_Hang_Lo')
                diag_loss_md += "### 🔍 Chẩn Đoán 2: Chẩn Đoán Nguyên Nhân Giao Dịch Thua Lỗ (Profit < 0)\n\n"
                diag_loss_md += "| Nhóm Giao Dịch (Có Lỗ hay Không) | Số Lượng Đơn | Doanh Thu Trung Bình | Chiết Khấu TB ($) | CP Marketing TB ($) | Lợi Nhuận TB ($) |\n"
                diag_loss_md += "|---|---|---|---|---|---|\n"
                for idx, row in loss_df.iterrows():
                    group_name = "🔴 Nhóm Giao Dịch Bị Lỗ" if row['IS_LOSS'] == True else "🟢 Nhóm Giao Dịch Có Lãi"
                    diag_loss_md += f"| {group_name} | {row['COUNT']} | ${row['AVG_REVENUE']:,.2f} | ${row['AVG_DISCOUNT_PCT']:,.2f} | ${row['AVG_MARKETING_COST']:,.2f} | ${row['AVG_PROFIT']:,.2f} |\n"
                diag_loss_md += "\n"
                diag_loss_md += "> **Phân tích nguyên nhân chẩn đoán:** So sánh chiết khấu và chi phí tiếp thị của nhóm lỗ so với nhóm lãi để xem có phải do chính sách chiết khấu quá cao kết hợp chi phí marketing lớn hay không.\n\n"

            except Exception as e:
                print(f"[WARNING] Lỗi trích xuất số liệu từ Excel: {e}")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Xử lý cho định dạng Markdown
        if output_path.endswith('.md'):
            md_content = "# Báo Cáo Phân Tích Hiệu Suất Kinh Doanh (BI Executive Report)\n\n"
            md_content += "## 1. Executive Summary & KPIs Dashboard\n"
            md_content += kpis_html
            md_content += "\n"
            
            md_content += "## 2. Phân Tích Mô Tả (Descriptive Analytics)\n"
            md_content += desc_md
            md_content += "### 📈 Biểu Đồ Phân Bổ Doanh Thu\n"
            md_content += "![Doanh thu theo sản phẩm](charts/revenue_by_product_category.png)\n\n"
            
            md_content += "## 3. Phân Tích Chẩn Đoán Nguyên Nhân (Diagnostic Analytics)\n"
            md_content += diag_ret_md
            md_content += "### 📈 Biểu Đồ Tỷ Lệ Trả Hàng Theo Danh Mục\n"
            md_content += "![Tỷ lệ trả hàng](charts/return_rate_by_product_category.png)\n\n"
            md_content += diag_loss_md
            
            md_content += "## 4. Nhận Định Kinh Doanh Chuyên Sâu & Khuyến Nghị (OEIA Insights)\n"
            md_content += insights_content + "\n"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            print(f"[SUCCESS] Báo cáo BI Markdown chi tiết đã được lưu tại: {output_path}")

        elif output_path.endswith('.docx'):
            print("[INFO] Fallback sang MD theo chuẩn BI.")
            md_path = output_path.replace('.docx', '.md')
            sys.argv[3] = md_path
            main()

    except Exception as e:
        print(f"[ERROR] Lỗi tạo báo cáo BI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
