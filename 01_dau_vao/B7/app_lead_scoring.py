import os
import sys
import re
import argparse
import pandas as pd
import requests

def clean_text(text):
    if not isinstance(text, str):
        return ""
    return text.strip().lower()

def extract_budget(text):
    # Match pattern like "20 tỷ", "35 tỷ", "20ty", etc.
    matches = re.findall(r'(\d+)\s*(?:tỷ|ty|tỉ)', text)
    if matches:
        return [int(m) for m in matches]
    return []

def run_lead_scoring(df):
    scored_leads = []
    
    for idx, row in df.iterrows():
        lead_id = row.get("Mã KH", row.get("Mã khách hàng", f"KH{idx+1:03d}"))
        name = row.get("Họ tên", row.get("Tên khách hàng", "Chưa rõ"))
        phone = row.get("Số điện thoại", row.get("SĐT", ""))
        demand = row.get("Nhu cầu", row.get("Mô tả", ""))
        
        demand_lower = clean_text(demand)
        
        # Scoring evaluation
        score = 100
        classification = "Tiềm năng"
        reasons = []
        
        # Check VIP criteria
        vip_keywords = {
            "loai_hinh_cao_cap": ["biệt thự đơn lập", "penthouse", "shophouse mặt đường lớn", "quỹ đất công nghiệp", "sàn văn phòng diện tích lớn"],
            "vi_tri_dac_dia": ["quận 1", "ven sông", "vinhomes ocean park", "phú mỹ hưng"],
            "doi_tuong_vip": ["chủ doanh nghiệp", "nhà đầu tư chuyên nghiệp", "mua sỉ", "mua số lượng lớn"],
            "phap_ly_minh_bach": ["pháp lý chuẩn 100%", "sổ hồng riêng", "muốn gặp trực tiếp chủ đầu tư để đàm phán"],
            "tai_chinh_manh": ["tài chính mạnh", "không thành vấn đề"]
        }
        
        matched_vip = []
        
        # Check budgets >= 20 billion
        budgets = extract_budget(demand_lower)
        large_budget = False
        for b in budgets:
            if b >= 20:
                large_budget = True
                matched_vip.append(f"Ngân sách lớn: {b} tỷ")
                
        for key, words in vip_keywords.items():
            for w in words:
                if w in demand_lower:
                    matched_vip.append(w)
                    
        # Check Junk criteria
        junk_keywords = {
            "khong_nhu_cau": ["nhầm số", "không có nhu cầu", "dữ liệu cũ", "nhầm ngành"],
            "khong_thien_chi": ["hỏi giá cho vui", "chưa có ý định mua", "thái độ không hợp tác"],
            "spam_quang_cao": ["bảo hiểm", "vay vốn", "mời chào dịch vụ"],
            "lien_lac_loi": ["thuê bao", "gọi nhiều lần không bắt máy", "không phản hồi zalo", "gọi nhiều lần không nghe"]
        }
        
        matched_junk = []
        
        # Check unrealistic price in central areas (Q1, Trung tâm and low price like 1-2 tỷ or vài trăm triệu)
        has_central = any(x in demand_lower for x in ["quận 1", "q1", "trung tâm"])
        has_low_price = any(x in demand_lower for x in ["1 tỷ", "2 tỷ", "1-2 tỷ", "vài trăm triệu", "vài trăm tr"])
        if has_central and has_low_price:
            matched_junk.append("yêu cầu phi thực tế (nhà Q1/trung tâm giá rẻ)")
            
        for key, words in junk_keywords.items():
            for w in words:
                if w in demand_lower:
                    matched_junk.append(w)
                    
        # Apply Score
        if matched_vip and not matched_junk:
            score = 150
            classification = "VIP/Siêu tiềm năng"
            reasons.append("Phát hiện tiêu chí VIP: " + ", ".join(matched_vip))
        elif matched_junk:
            score = 50
            classification = "Không tiềm năng"
            reasons.append("Phát hiện dấu hiệu loại trừ: " + ", ".join(matched_junk))
        else:
            score = 100
            classification = "Tiềm năng"
            # Default potential checks
            potential_reasons = []
            if any(x in demand_lower for x in ["chung cư", "căn hộ", "nhà phố"]):
                potential_reasons.append("Chung cư/nhà phố tầm trung")
            if "vay" in demand_lower or "ngân hàng" in demand_lower:
                potential_reasons.append("Cần vay/cân nhắc chính sách ngân hàng")
            if "tư vấn" in demand_lower or "pháp lý" in demand_lower or "vị trí" in demand_lower:
                potential_reasons.append("Cần tư vấn thêm pháp lý/vị trí")
            
            if potential_reasons:
                reasons.append(" / ".join(potential_reasons))
            else:
                reasons.append("Khách hàng tầm trung/Nhu cầu thực")
                
        scored_leads.append({
            "Mã KH": lead_id,
            "Họ tên": name,
            "Số điện thoại": phone,
            "Nhu cầu": demand,
            "Điểm số": score,
            "Phân loại": classification,
            "Lý do chấm điểm": "; ".join(reasons),
            "Trạng thái duyệt": "Chờ duyệt"
        })
        
    return pd.DataFrame(scored_leads)

def download_google_sheet(url):
    # Match standard spreadsheet ID pattern
    sheet_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    if not sheet_id_match:
        raise ValueError("Không thể tìm thấy ID Google Sheet từ URL.")
    
    sheet_id = sheet_id_match.group(1)
    
    # Check if there is a specific gid/sheet parameter
    gid_match = re.search(r'gid=(\d+)', url)
    gid = gid_match.group(1) if gid_match else "0"
    
    # Download as XLSX
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(export_url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        # Fallback to general export
        fallback_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        response = requests.get(fallback_url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            raise RuntimeError(f"Không thể tải Google Sheet (Mã lỗi: {response.status_code}). Vui lòng đảm bảo quyền truy cập công khai.")

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass # Python 3.7+ support
        
    parser = argparse.ArgumentParser(description="AI Lead Scoring Automation Tool")
    parser.add_argument("source", help="Path to raw excel file or Google Sheets URL")
    parser.add_argument("--output", default="lead_scored_report.xlsx", help="Path to output Excel file")
    
    args = parser.parse_args()
    
    print(f"Bắt đầu xử lý dữ liệu từ nguồn: {args.source}")
    
    try:
        if args.source.startswith("http://") or args.source.startswith("https://"):
            print("Đang tải dữ liệu từ Google Sheets...")
            sheet_content = download_google_sheet(args.source)
            # Read from memory
            df = pd.read_excel(sheet_content)
        else:
            if not os.path.exists(args.source):
                raise FileNotFoundError(f"Không tìm thấy file nguồn cục bộ: {args.source}")
            print("Đang đọc tệp Excel cục bộ...")
            df = pd.read_excel(args.source)
            
        print(f"Đã nạp {len(df)} dòng dữ liệu.")
        
        # Run Lead Scoring logic
        df_scored = run_lead_scoring(df)
        
        # Export to Excel
        df_scored.to_excel(args.output, index=False)
        print(f"Đã chấm điểm hoàn tất! Kết quả được ghi lại tại: {args.output}")
        
    except Exception as e:
        print(f"Lỗi trong quá trình thực hiện: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
