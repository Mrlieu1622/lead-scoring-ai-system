import os
import re
import pandas as pd
import requests
import streamlit as st
import io

# Core Lead Scoring Logic
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
    
    # Standardize columns to lower case for easy matching
    col_mapping = {str(col).strip().lower(): col for col in df.columns}
    
    # Resolve columns
    id_col = next((col_mapping[c] for c in ["mã kh", "mã khách hàng", "id"] if c in col_mapping), None)
    name_col = next((col_mapping[c] for c in ["họ tên", "tên khách hàng", "họ và tên", "name"] if c in col_mapping), None)
    phone_col = next((col_mapping[c] for c in ["số điện thoại", "sđt", "phone", "sdt"] if c in col_mapping), None)
    demand_col = next((col_mapping[c] for c in ["nhu cầu", "mô tả", "demand", "nhu cầu khách hàng"] if c in col_mapping), None)

    for idx, row in df.iterrows():
        lead_id = row.get(id_col, f"KH{idx+1:03d}") if id_col else f"KH{idx+1:03d}"
        name = row.get(name_col, "Chưa rõ") if name_col else "Chưa rõ"
        phone = row.get(phone_col, "") if phone_col else ""
        
        # Handle NaN phone values cleanly
        if pd.isna(phone):
            phone = "N/A"
        elif isinstance(phone, float):
            phone = str(int(phone))
        else:
            phone = str(phone)
            
        demand = row.get(demand_col, "") if demand_col else ""
        if pd.isna(demand):
            demand = ""
            
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
        for b in budgets:
            if b >= 20:
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
        
        # Check unrealistic price in central areas
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
    sheet_id_match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
    if not sheet_id_match:
        raise ValueError("Không thể tìm thấy ID Google Sheet từ URL.")
    
    sheet_id = sheet_id_match.group(1)
    gid_match = re.search(r'gid=(\d+)', url)
    gid = gid_match.group(1) if gid_match else "0"
    
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx&gid={gid}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    response = requests.get(export_url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        fallback_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
        response = requests.get(fallback_url, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            raise RuntimeError(f"Không thể tải Google Sheet (Mã lỗi: {response.status_code}). Vui lòng đảm bảo quyền truy cập công khai.")

# Streamlit App Config & Premium UI Customization (Techcombank Style)
st.set_page_config(page_title="AI Lead Scoring - Techcombank Premium", page_icon="🏦", layout="wide")

# CSS Injection for Techcombank Signature Premium Red & Dark Charcoal Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    /* Global App Container Override */
    .reportview-container {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Techcombank Corporate Premium Header */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .main-title span {
        color: #EB1F3A; /* Techcombank Red */
    }
    
    .subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        border-left: 3px solid #EB1F3A;
        padding-left: 12px;
        margin-bottom: 2rem;
    }
    
    /* Techcombank Obsidian Cards */
    .metric-card {
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 4px solid #EB1F3A; /* Top Red Line */
        border-radius: 12px;
        padding: 1.4rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 30px rgba(235, 31, 58, 0.15);
        border-color: rgba(235, 31, 58, 0.3);
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }
    
    .metric-val {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 0.4rem;
    }
    
    /* Techcombank Red Button Customization */
    .stButton>button {
        background: linear-gradient(135deg, #EB1F3A, #b91c1c) !important;
        color: white !important;
        border: 1px solid #EB1F3A !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 4px 12px rgba(235, 31, 58, 0.3) !important;
        text-transform: uppercase !important;
    }
    
    .stButton>button:hover {
        background: #EB1F3A !important;
        box-shadow: 0 6px 22px rgba(235, 31, 58, 0.5) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Sidebar customization (Techcombank Brand Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Styled widgets container */
    .stCheckbox {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Premium Header (Techcombank Brand Identity)
st.markdown("<div class='main-title'>🏦 TECHCOMBANK <span>PRIORITY</span></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Hệ thống Định hạng Khách hàng cao cấp và phân tích Tiềm năng AI Lead Scoring</div>", unsafe_allow_html=True)

# Sidebar Config
st.sidebar.markdown("### ⚙️ HỆ THỐNG GIAO DỊCH")
data_source = st.sidebar.radio("Hình thức nạp hồ sơ khách hàng:", ("Nhập link Google Sheets", "Tải lên tệp Excel (.xlsx)"))

def reset_data_state():
    if 'df_scored' in st.session_state:
        del st.session_state['df_scored']

df = None

# Logic to load data
if data_source == "Nhập link Google Sheets":
    sheet_url = st.sidebar.text_input("Đường dẫn Google Sheets:", "https://docs.google.com/spreadsheets/d/1hRvHE6RXm1peVG07avfApPEHocOcPld9IA94hE3vUGE/edit?gid=0#gid=0", on_change=reset_data_state)
    if st.sidebar.button("⚡ TẢI DỮ LIỆU & ĐỊNH HẠNG"):
        try:
            with st.spinner("Đang truy xuất thông tin từ mạng giao dịch..."):
                content = download_google_sheet(sheet_url)
                df = pd.read_excel(io.BytesIO(content))
                if len(df) > 0:
                    st.session_state.df_scored = run_lead_scoring(df)
                    st.success("Liên kết và phân tích dữ liệu Google Sheets thành công!")
                else:
                    st.error("Dữ liệu bảng tính trống.")
        except Exception as e:
            st.error(f"Không thể truy xuất: {str(e)}. Hãy đặt Google Sheet ở chế độ công khai để ứng dụng có quyền đọc.")
else:
    uploaded_file = st.sidebar.file_uploader("Nạp báo cáo Excel đầu vào:", type=["xlsx", "xls"], on_change=reset_data_state)
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            if len(df) > 0:
                if 'df_scored' not in st.session_state:
                    st.session_state.df_scored = run_lead_scoring(df)
                    st.success("Tải tệp và phân tách hồ sơ khách hàng thành công!")
            else:
                st.error("Tệp Excel không chứa thông tin.")
        except Exception as e:
            st.error(f"Lỗi phân tích tệp: {str(e)}")

# Process data if loaded in session state
if 'df_scored' in st.session_state:
    df_scored = st.session_state.df_scored
    
    # Beautiful Custom Cards for Stats (Techcombank Luxury Theme)
    total_leads = len(df_scored)
    vip_count = len(df_scored[df_scored["Phân loại"] == "VIP/Siêu tiềm năng"])
    pot_count = len(df_scored[df_scored["Phân loại"] == "Tiềm năng"])
    junk_count = len(df_scored[df_scored["Phân loại"] == "Không tiềm năng"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card' style='border-top: 4px solid #94a3b8;'><div class='metric-label'>👥 Tổng hồ sơ nạp</div><div class='metric-val'>{total_leads}</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card' style='border-top: 4px solid #fbbf24;'><div class='metric-label' style='color:#fbbf24;'>👑 Hạng VIP/Priority</div><div class='metric-val'>{vip_count}</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card' style='border-top: 4px solid #60a5fa;'><div class='metric-label' style='color:#60a5fa;'>✅ Khách Tiềm Năng</div><div class='metric-val'>{pot_count}</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card' style='border-top: 4px solid #f87171;'><div class='metric-label' style='color:#f87171;'>🗑️ Hồ Sơ Loại Trừ</div><div class='metric-val'>{junk_count}</div></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Premium Filter Layout inside an expander (Corporate Style)
    with st.expander("🔍 CÔNG CỤ TRUY VẤN VÀ LỌC THÔNG TIN", expanded=True):
        filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])
        with filter_col1:
            search_query = st.text_input("Tìm kiếm theo tên khách, SĐT, hoặc chi tiết nhu cầu:", "").lower().strip()
        with filter_col2:
            class_filter = st.selectbox("Lọc Hạng Khách Hàng:", ["Tất cả", "VIP/Siêu tiềm năng", "Tiềm năng", "Không tiềm năng"])
        with filter_col3:
            status_filter = st.selectbox("Trạng Thái Duyệt Hồ Sơ:", ["Tất cả", "Chờ duyệt", "Đã duyệt", "Bác bỏ"])
            
        only_valuable = st.checkbox("🔥 Chỉ lọc hiển thị Hạng Khách Hàng tiềm năng & VIP trở lên (Loại bỏ các Hồ Sơ Rác)", value=False)
    
    # Apply filtering criteria
    filtered_df = df_scored.copy()
    
    # Filter only valuable
    if only_valuable:
        filtered_df = filtered_df[filtered_df["Phân loại"].isin(["VIP/Siêu tiềm năng", "Tiềm năng"])]
        
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Họ tên"].astype(str).str.lower().str.contains(search_query) |
            filtered_df["Số điện thoại"].astype(str).str.lower().str.contains(search_query) |
            filtered_df["Nhu cầu"].astype(str).str.lower().str.contains(search_query)
        ]
        
    if class_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["Phân loại"] == class_filter]
        
    if status_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["Trạng thái duyệt"] == status_filter]
        
    # Actions right below the filter block (Techcombank Brand Action Group)
    st.markdown("##### ⚙️ GIAO DỊCH VIÊN PHÊ DUYỆT NHANH:")
    act_col1, act_col2, act_col3 = st.columns([1, 1, 4])
    with act_col1:
        if st.button("✅ Phê Duyệt"):
            for idx, row in filtered_df.iterrows():
                match_idx = st.session_state.df_scored[st.session_state.df_scored["Mã KH"] == row["Mã KH"]].index
                if len(match_idx) > 0:
                    st.session_state.df_scored.at[match_idx[0], "Trạng thái duyệt"] = "Đã duyệt"
            st.success("Đã chuyển toàn bộ hồ sơ đang hiển thị sang trạng thái Phê Duyệt!")
            st.rerun()
    with act_col2:
        if st.button("❌ Bác Bỏ"):
            for idx, row in filtered_df.iterrows():
                match_idx = st.session_state.df_scored[st.session_state.df_scored["Mã KH"] == row["Mã KH"]].index
                if len(match_idx) > 0:
                    st.session_state.df_scored.at[match_idx[0], "Trạng thái duyệt"] = "Bác bỏ"
            st.warning("Đã chuyển toàn bộ hồ sơ đang hiển thị sang trạng thái Bác Bỏ!")
            st.rerun()
            
    st.subheader(f"📊 Bảng dữ liệu định hạng phân loại ({len(filtered_df)} khách hàng)")
    
    # Render interactive editor
    edited_filtered_df = st.data_editor(filtered_df, use_container_width=True)
    
    # Safe cell update syncing to original session state
    for idx, row in edited_filtered_df.iterrows():
        match_idx = st.session_state.df_scored[st.session_state.df_scored["Mã KH"] == row["Mã KH"]].index
        if len(match_idx) > 0:
            for col in st.session_state.df_scored.columns:
                st.session_state.df_scored.at[match_idx[0], col] = row[col]
                
    # Export to Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.df_scored.to_excel(writer, index=False, sheet_name='Scored Leads')
    processed_data = output.getvalue()
    
    # Footer Action Buttons
    dl_col, tip_col = st.columns([1.5, 4])
    with dl_col:
        st.download_button(
            label="📥 Xuất File Excel Bàn Giao",
            data=processed_data,
            file_name="lead_scored_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with tip_col:
        st.info("💡 Bạn có thể trực tiếp nhấp vào ô bất kỳ trong bảng dữ liệu để chỉnh sửa điểm, sửa phân loại và duyệt hồ sơ trước khi xuất file.")
else:
    st.info("👋 Chào mừng bạn đến với hệ thống giao dịch Techcombank Priority. Vui lòng nạp thông tin khách hàng ở thanh cấu hình bên trái để bắt đầu.")
