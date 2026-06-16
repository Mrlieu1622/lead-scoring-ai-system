import os
import sys
import re
import pandas as pd

# Force UTF-8 stdout for Windows terminals to avoid UnicodeEncodeErrors
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

RAW_DATA_PATH = os.path.join("01_dau_vao", "data_raw.xlsx")
CLEAN_DATA_PATH = os.path.join("04_ban_thao", "data_clean.xlsx")

# Rule definitions based on tieu_chi_cham_diem (1).txt
VIP_KEYWORDS = [
    "tài chính mạnh", "không thành vấn đề",
    "biệt thự đơn lập", "penthouse", "shophouse mặt đường lớn", "quỹ đất công nghiệp", "sàn văn phòng diện tích lớn",
    "quận 1", "ven sông", "vinhomes ocean park", "phú mỹ hưng",
    "chủ doanh nghiệp", "nhà đầu tư chuyên nghiệp", "mua sỉ", "mua số lượng lớn",
    "pháp lý chuẩn 100%", "sổ hồng riêng", "muốn gặp trực tiếp chủ đầu tư để đàm phán"
]

GARBAGE_KEYWORDS = [
    "nhầm số", "không có nhu cầu", "dữ liệu cũ", "nhầm ngành",
    "hỏi giá cho vui", "chưa có ý định mua", "thái độ không hợp tác",
    "bảo hiểm", "vay vốn", "mới chào dịch vụ",
    "thuê bao", "gọi nhiều lần không bắt máy", "không phản hồi zalo"
]

def score_lead(text):
    if not isinstance(text, str):
        return 100, "Tiềm năng", "Không có thông tin nhu cầu."
    
    text_lower = text.lower()
    score = 100  # Base score
    reasons = []
    
    # Pre-check garbage flags to prevent VIP bonus
    dist1_low_price = ("quận 1" in text_lower or "trung tâm" in text_lower) and (any(x in text_lower for x in ["1 tỷ", "2 tỷ", "vài trăm triệu", "1-2 tỷ", "1 - 2 tỷ", "vài trăm triệu"]) or re.search(r'\b[1-2]\s*tỷ\b', text_lower))
    matched_garbage_kws = [kw for kw in GARBAGE_KEYWORDS if kw in text_lower]
    is_garbage = dist1_low_price or len(matched_garbage_kws) > 0
    
    # 1. Check VIP Criteria (+50) - Only if NOT garbage
    is_vip = False
    if not is_garbage:
        budget_match = re.search(r'(\d+)\s*tỷ', text_lower)
        if budget_match:
            billion_value = int(budget_match.group(1))
            if billion_value >= 20:
                score += 50
                is_vip = True
                reasons.append(f"Ngân sách lớn: {billion_value} tỷ (>= 20 tỷ)")
                
        matched_vip_kws = [kw for kw in VIP_KEYWORDS if kw in text_lower]
        if matched_vip_kws:
            if not is_vip:
                score += 50
                is_vip = True
            reasons.append(f"Từ khóa VIP phát hiện: {', '.join(matched_vip_kws)}")
            
    # 2. Check Garbage Criteria (-50)
    if dist1_low_price:
        score -= 50
        reasons.append("Yêu cầu phi thực tế (Nhà Q1/Trung tâm giá rẻ)")
    if matched_garbage_kws:
        score -= 50
        reasons.append(f"Dấu hiệu không tiềm năng: {', '.join(matched_garbage_kws)}")
        
    # Classify based on score
    if score >= 150:
        classification = "VIP/Siêu tiềm năng"
    elif score <= 50:
        classification = "Không tiềm năng"
    else:
        classification = "Tiềm năng"
        
    reason_str = "; ".join(reasons) if reasons else "Khách hàng tầm trung/Nhu cầu thực"
    return score, classification, reason_str

def main():
    print("Executing score_leads...")
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Không tìm thấy file {RAW_DATA_PATH}. Đang chạy fetch_leads để nạp dữ liệu...")
        # Add skill folder to path dynamically to import fetch_leads
        import sys
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.append(script_dir)
        import fetch_leads
        fetch_leads.main()
        
    df = pd.read_excel(RAW_DATA_PATH)
    
    scores = []
    classifications = []
    reasons = []
    
    for _, row in df.iterrows():
        demand_text = row.get("Nhu cầu", "")
        score, classification, reason = score_lead(demand_text)
        scores.append(score)
        classifications.append(classification)
        reasons.append(reason)
        
    df["Điểm số"] = scores
    df["Phân loại"] = classifications
    df["Lý do chấm điểm"] = reasons
    df["Trạng thái duyệt"] = "Chờ duyệt"
    
    os.makedirs(os.path.dirname(CLEAN_DATA_PATH), exist_ok=True)
    df.to_excel(CLEAN_DATA_PATH, index=False)
    print(f"Chấm điểm thành công! Dữ liệu đã được lưu vào: {CLEAN_DATA_PATH}")

if __name__ == "__main__":
    main()
