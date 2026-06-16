import http.server
import socketserver
import json
import pandas as pd
import time
import webbrowser
import os
import urllib.parse
import threading

PORT = 9090
EXCEL_FILE = "TH_ngan_sach_phong_ban.xlsx"

class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Serve dashboard.html at root
        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            try:
                with open("dashboard.html", "r", encoding="utf-8") as f:
                    self.wfile.write(f.read().encode("utf-8"))
            except Exception as e:
                self.wfile.write(f"<h3>Lỗi tải trang: {str(e)}</h3>".encode("utf-8"))
                
        # Serve data API
        elif path == "/api/data":
            try:
                # Read the excel file
                if not os.path.exists(EXCEL_FILE):
                    raise FileNotFoundError(f"Không tìm thấy file {EXCEL_FILE}")
                
                df = pd.read_excel(EXCEL_FILE)
                max_rows = len(df)
                start_rows = 150  # Phù hợp với cỡ mẫu 300 của tệp ngân sách
                
                # Dynamic simulation: loops between 150 and 300 rows
                # Step up by 1 row every 2 seconds. Total steps = 150. Total cycle = 300 seconds.
                cycle_length = (max_rows - start_rows) * 2  # 300 seconds
                elapsed_in_cycle = int(time.time()) % cycle_length
                simulated_rows = start_rows + (elapsed_in_cycle // 2)
                
                # Bound check
                if simulated_rows > max_rows:
                    simulated_rows = max_rows
                
                df_slice = df.iloc[:simulated_rows]
                
                # Đọc tham số bộ lọc từ Query String
                query = urllib.parse.parse_qs(parsed_path.query)
                quy_filter = query.get("quy", [None])[0]
                phong_ban_filter = query.get("phong_ban", [None])[0]
                
                # Áp dụng lọc dữ liệu
                df_filtered = df_slice
                if quy_filter and quy_filter != "All" and quy_filter != "undefined":
                    # Lọc mềm theo từ khóa (Ví dụ: "Q1" sẽ khớp với "Q1-2026")
                    df_filtered = df_filtered[df_filtered["Quy"].str.contains(quy_filter, case=False, na=False)]
                if phong_ban_filter and phong_ban_filter != "All" and phong_ban_filter != "undefined":
                    df_filtered = df_filtered[df_filtered["Phong_Ban"] == phong_ban_filter]
                
                # 1. Calculate KPIs dựa trên dữ liệu đã lọc
                tong_ngan_sach = float(df_filtered["Ngan_Sach_Duyet"].sum())
                tong_chi_tieu = float(df_filtered["Chi_Tieu_Thuc_Te"].sum())
                chenh_lech = float(df_filtered["Chenh_Lech"].sum())
                so_giao_dich_vuot = int((df_filtered["Trang_Thai"] == "Vuot Ngan Sach").sum())
                
                # Khai thác thông tin thâm hụt và tỷ lệ tuân thủ
                tong_tien_vuot = float(df_filtered[df_filtered["Trang_Thai"] == "Vuot Ngan Sach"]["Chenh_Lech"].abs().sum())
                total_txn = len(df_filtered)
                ty_le_vuot = round((so_giao_dich_vuot / total_txn * 100), 1) if total_txn > 0 else 0.0
                
                # Thống kê phân phối trạng thái giao dịch
                status_counts = df_filtered["Trang_Thai"].value_counts().to_dict()
                status_tiet_kiem = int(status_counts.get("Tiet Kiem", 0))
                status_vuot = int(status_counts.get("Vuot Ngan Sach", 0))
                
                # Logic phân tích xu hướng liên quý (Q-o-Q) dựa trên quý được chọn hoặc quý gần nhất khi chọn "All"
                curr_quy_trend = None
                prev_quy_trend = None
                
                if quy_filter and quy_filter != "All" and quy_filter != "undefined":
                    if "Q2" in quy_filter:
                        curr_quy_trend = "Q2-2026"
                        prev_quy_trend = "Q1-2026"
                    elif "Q3" in quy_filter:
                        curr_quy_trend = "Q3-2026"
                        prev_quy_trend = "Q2-2026"
                    elif "Q4" in quy_filter:
                        curr_quy_trend = "Q4-2026"
                        prev_quy_trend = "Q3-2026"
                    elif "Q1" in quy_filter:
                        curr_quy_trend = "Q1-2026"
                        prev_quy_trend = None
                else:
                    curr_quy_trend = "Q4-2026"
                    prev_quy_trend = "Q3-2026"
                
                # Hàm tính toán % thay đổi
                def get_pct_change(curr, prev):
                    if prev == 0:
                        return 0.0
                    return round(((curr - prev) / prev) * 100, 1)
                
                tong_ngan_sach_curr = 0.0
                tong_chi_tieu_curr = 0.0
                chenh_lech_curr = 0.0
                so_giao_dich_vuot_curr = 0
                
                tong_ngan_sach_prev = 0.0
                tong_chi_tieu_prev = 0.0
                chenh_lech_prev = 0.0
                so_giao_dich_vuot_prev = 0
                
                if curr_quy_trend:
                    df_curr = df_slice[df_slice["Quy"] == curr_quy_trend]
                    if phong_ban_filter and phong_ban_filter != "All" and phong_ban_filter != "undefined":
                        df_curr = df_curr[df_curr["Phong_Ban"] == phong_ban_filter]
                    tong_ngan_sach_curr = float(df_curr["Ngan_Sach_Duyet"].sum())
                    tong_chi_tieu_curr = float(df_curr["Chi_Tieu_Thuc_Te"].sum())
                    chenh_lech_curr = float(df_curr["Chenh_Lech"].sum())
                    so_giao_dich_vuot_curr = int((df_curr["Trang_Thai"] == "Vuot Ngan Sach").sum())
                
                if prev_quy_trend:
                    df_prev = df_slice[df_slice["Quy"] == prev_quy_trend]
                    if phong_ban_filter and phong_ban_filter != "All" and phong_ban_filter != "undefined":
                        df_prev = df_prev[df_prev["Phong_Ban"] == phong_ban_filter]
                    tong_ngan_sach_prev = float(df_prev["Ngan_Sach_Duyet"].sum())
                    tong_chi_tieu_prev = float(df_prev["Chi_Tieu_Thuc_Te"].sum())
                    chenh_lech_prev = float(df_prev["Chenh_Lech"].sum())
                    so_giao_dich_vuot_prev = int((df_prev["Trang_Thai"] == "Vuot Ngan Sach").sum())
                
                # Tính toán baseline cho Q1 (trung bình của năm)
                df_yearly = df_slice
                if phong_ban_filter and phong_ban_filter != "All" and phong_ban_filter != "undefined":
                    df_yearly = df_yearly[df_yearly["Phong_Ban"] == phong_ban_filter]
                
                by_q_avg = df_yearly.groupby("Quy").agg({
                    "Ngan_Sach_Duyet": "sum",
                    "Chi_Tieu_Thuc_Te": "sum",
                    "Chenh_Lech": "sum"
                }).mean()
                
                avg_ngan_sach = float(by_q_avg.get("Ngan_Sach_Duyet", 0.0))
                avg_chi_tieu = float(by_q_avg.get("Chi_Tieu_Thuc_Te", 0.0))
                avg_chenh_lech = float(by_q_avg.get("Chenh_Lech", 0.0))
                avg_giao_dich_vuot = float(df_yearly[df_yearly["Trang_Thai"] == "Vuot Ngan Sach"].groupby("Quy").size().mean()) if len(df_yearly) > 0 else 0.0
                
                if prev_quy_trend:
                    ngan_sach_change = get_pct_change(tong_ngan_sach_curr, tong_ngan_sach_prev)
                    chi_tieu_change = get_pct_change(tong_chi_tieu_curr, tong_chi_tieu_prev)
                    chenh_lech_change = get_pct_change(chenh_lech_curr, chenh_lech_prev)
                    giao_dich_vuot_change = int(so_giao_dich_vuot_curr - so_giao_dich_vuot_prev)
                    prev_quy_label_val = prev_quy_trend.split("-")[0]
                else:
                    ngan_sach_change = get_pct_change(tong_ngan_sach_curr, avg_ngan_sach)
                    chi_tieu_change = get_pct_change(tong_chi_tieu_curr, avg_chi_tieu)
                    chenh_lech_change = get_pct_change(chenh_lech_curr, avg_chenh_lech)
                    giao_dich_vuot_change = int(so_giao_dich_vuot_curr - avg_giao_dich_vuot)
                    prev_quy_label_val = "TB Năm"
                
                # Tính toán chuỗi lịch sử Sparkline (luôn theo 4 Quý Q1 -> Q4)
                quarters_list = ["Q1-2026", "Q2-2026", "Q3-2026", "Q4-2026"]
                sparkline_data = {
                    "ngan_sach": [],
                    "chi_tieu": [],
                    "chenh_lech": [],
                    "giao_dich_vuot": []
                }
                for q in quarters_list:
                    df_q = df_slice[df_slice["Quy"] == q]
                    if phong_ban_filter and phong_ban_filter != "All" and phong_ban_filter != "undefined":
                        df_q = df_q[df_q["Phong_Ban"] == phong_ban_filter]
                    sparkline_data["ngan_sach"].append(float(df_q["Ngan_Sach_Duyet"].sum()))
                    sparkline_data["chi_tieu"].append(float(df_q["Chi_Tieu_Thuc_Te"].sum()))
                    sparkline_data["chenh_lech"].append(float(df_q["Chenh_Lech"].sum()))
                    sparkline_data["giao_dich_vuot"].append(int((df_q["Trang_Thai"] == "Vuot Ngan Sach").sum()))
                
                # 2. Column Chart & Line Chart data (Quarterly) - Không bị lọc bởi Quý, chỉ lọc bởi Bộ phận để giữ nguyên bối cảnh so sánh
                df_quarterly_trend = df_slice
                if phong_ban_filter and phong_ban_filter != "All" and phong_ban_filter != "undefined":
                    df_quarterly_trend = df_quarterly_trend[df_quarterly_trend["Phong_Ban"] == phong_ban_filter]
                
                by_quarter = df_quarterly_trend.groupby("Quy").agg({
                    "Ngan_Sach_Duyet": "sum",
                    "Chi_Tieu_Thuc_Te": "sum",
                    "Chenh_Lech": "sum"
                }).reset_index()
                
                by_quarter = by_quarter.sort_values("Quy")
                quarters = by_quarter["Quy"].tolist()
                ngan_sach_by_quarter = by_quarter["Ngan_Sach_Duyet"].map(float).tolist()
                chi_tieu_by_quarter = by_quarter["Chi_Tieu_Thuc_Te"].map(float).tolist()
                chenh_lech_by_quarter = by_quarter["Chenh_Lech"].map(float).tolist()
                
                # 3. Department Chart data
                by_department = df_filtered.groupby("Phong_Ban").agg({
                    "Ngan_Sach_Duyet": "sum",
                    "Chi_Tieu_Thuc_Te": "sum"
                }).reset_index()
                departments = by_department["Phong_Ban"].tolist()
                ngan_sach_by_department = by_department["Ngan_Sach_Duyet"].map(float).tolist()
                chi_tieu_by_department = by_department["Chi_Tieu_Thuc_Te"].map(float).tolist()
                
                # 3.1 Department budget vs actual table data (with ratios)
                dept_table_data = []
                for _, row in by_department.iterrows():
                    budget = float(row["Ngan_Sach_Duyet"])
                    spend = float(row["Chi_Tieu_Thuc_Te"])
                    diff = budget - spend
                    ratio = round((spend / budget * 100), 1) if budget > 0 else 0.0
                    dept_table_data.append({
                        "phong_ban": row["Phong_Ban"],
                        "ngan_sach": budget,
                        "chi_tieu": spend,
                        "chenh_lech": diff,
                        "ty_le": ratio
                    })
                
                # 4. Top 5 Hạng Mục Chi Tiêu Lớn Nhất
                by_item = df_filtered.groupby("Hang_Muc_Chi").agg({
                    "Ngan_Sach_Duyet": "sum",
                    "Chi_Tieu_Thuc_Te": "sum",
                    "Chenh_Lech": "sum"
                }).reset_index()
                by_item = by_item.sort_values("Chi_Tieu_Thuc_Te", ascending=False).head(5)
                
                top_hang_muc = []
                for _, row in by_item.iterrows():
                    top_hang_muc.append({
                        "hang_muc": row["Hang_Muc_Chi"],
                        "ngan_sach": float(row["Ngan_Sach_Duyet"]),
                        "chi_tieu": float(row["Chi_Tieu_Thuc_Te"]),
                        "chenh_lech": float(row["Chenh_Lech"])
                    })
                
                # 4.1 Spend breakdown by category (donut)
                by_cat_spend = df_filtered.groupby("Hang_Muc_Chi")["Chi_Tieu_Thuc_Te"].sum().reset_index()
                cat_spend_labels = by_cat_spend["Hang_Muc_Chi"].tolist()
                cat_spend_series = by_cat_spend["Chi_Tieu_Thuc_Te"].map(float).tolist()
                
                # 5. Top 5 Giao Dịch Vượt Ngân Sách Nghiêm Trọng Nhất
                df_over = df_filtered[df_filtered["Trang_Thai"] == "Vuot Ngan Sach"].copy()
                df_over["Chenh_Lech_Abs"] = df_over["Chenh_Lech"].abs()
                df_over = df_over.sort_values("Chenh_Lech_Abs", ascending=False).head(5)
                top_giao_dich_vuot = []
                for _, row in df_over.iterrows():
                    top_giao_dich_vuot.append({
                        "ma_gd": row["Ma_Giao_Dich"],
                        "phong_ban": row["Phong_Ban"],
                        "hang_muc": row["Hang_Muc_Chi"],
                        "ngan_sach": float(row["Ngan_Sach_Duyet"]),
                        "chi_tieu": float(row["Chi_Tieu_Thuc_Te"]),
                        "chenh_lech": float(row["Chenh_Lech"])
                    })
                
                # 6. Compliance Status counts by Department
                comp_dept = df_filtered.groupby(["Phong_Ban", "Trang_Thai"]).size().unstack(fill_value=0)
                comp_dept_depts = comp_dept.index.tolist()
                comp_dept_tiet_kiem = comp_dept.get("Tiet Kiem", pd.Series(0, index=comp_dept.index)).map(int).tolist()
                comp_dept_vuot = comp_dept.get("Vuot Ngan Sach", pd.Series(0, index=comp_dept.index)).map(int).tolist()
                
                # 7. Compliance Status counts by Expense Category
                comp_cat = df_filtered.groupby(["Hang_Muc_Chi", "Trang_Thai"]).size().unstack(fill_value=0)
                comp_cat_cats = comp_cat.index.tolist()
                comp_cat_tiet_kiem = comp_cat.get("Tiet Kiem", pd.Series(0, index=comp_cat.index)).map(int).tolist()
                comp_cat_vuot = comp_cat.get("Vuot Ngan Sach", pd.Series(0, index=comp_cat.index)).map(int).tolist()
                
                response_data = {
                    "kpis": {
                        "tong_ngan_sach": tong_ngan_sach,
                        "tong_chi_tieu": tong_chi_tieu,
                        "ty_le_chi_tieu": round((tong_chi_tieu / tong_ngan_sach * 100), 1) if tong_ngan_sach > 0 else 0.0,
                        "chenh_lech": chenh_lech,
                        "so_giao_dich_vuot": so_giao_dich_vuot,
                        "tong_tien_vuot": tong_tien_vuot,
                        "ty_le_vuot": ty_le_vuot,
                        "compliance": {
                            "tiet_kiem": status_tiet_kiem,
                            "vuot": status_vuot
                        },
                        "sparklines": sparkline_data,
                        "trends": {
                            "has_trend": True,
                            "ngan_sach_change": ngan_sach_change,
                            "chi_tieu_change": chi_tieu_change,
                            "chenh_lech_change": chenh_lech_change,
                            "giao_dich_vuot_change": giao_dich_vuot_change,
                            "prev_quy_label": prev_quy_label_val
                        }
                    },
                    "charts": {
                        "quarters": quarters,
                        "ngan_sach_by_quarter": ngan_sach_by_quarter,
                        "chi_tieu_by_quarter": chi_tieu_by_quarter,
                        "chenh_lech_by_quarter": chenh_lech_by_quarter,
                        "departments": departments,
                        "ngan_sach_by_department": ngan_sach_by_department,
                        "chi_tieu_by_department": chi_tieu_by_department,
                        "cat_spend_labels": cat_spend_labels,
                        "cat_spend_series": cat_spend_series
                    },
                    "compliance_charts": {
                        "departments": comp_dept_depts,
                        "dept_tiet_kiem": comp_dept_tiet_kiem,
                        "dept_vuot": comp_dept_vuot,
                        "categories": comp_cat_cats,
                        "cat_tiet_kiem": comp_cat_tiet_kiem,
                        "cat_vuot": comp_cat_vuot
                    },
                    "phong_ban_data": dept_table_data,
                    "top_hang_muc": top_hang_muc,
                    "top_giao_dich_vuot": top_giao_dich_vuot,
                    "simulated_rows": simulated_rows,
                    "total_rows": max_rows
                }
                
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def open_browser():
    time.sleep(1.5)
    print(">>> Dang mo trinh duyet tai: http://localhost:9090")
    webbrowser.open("http://localhost:9090")

if __name__ == "__main__":
    handler = DashboardHandler
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"*** Server dang chay tai: http://localhost:{PORT}")
        
        # Start browser thread
        threading.Thread(target=open_browser, daemon=True).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n*** Da dung server.")
            httpd.server_close()
