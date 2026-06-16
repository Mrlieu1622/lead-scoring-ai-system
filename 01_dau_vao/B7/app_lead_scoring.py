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
            "Số điện thoại": str(phone),
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

# Streamlit App UI
st.set_page_config(page_title="AI Lead Scoring System", page_icon="🤖", layout="wide")

st.title("🤖 AI Lead Scoring & Automation System")
st.markdown("Hệ thống tự động chấm điểm khách hàng tiềm năng ngành Bất động sản dựa trên mô tả nhu cầu.")

# Sidebar configuration
st.sidebar.header("Cấu hình nguồn dữ liệu")
data_source = st.sidebar.radio("Chọn hình thức nạp dữ liệu:", ("Nhập link Google Sheets", "Tải lên tệp Excel (.xlsx)"))

# Reset state helper if data source or file changes
def reset_data_state():
    if 'df_scored' in st.session_state:
        del st.session_state['df_scored']

df = None

if data_source == "Nhập link Google Sheets":
    sheet_url = st.sidebar.text_input("Link Google Sheets:", "https://docs.google.com/spreadsheets/d/1hRvHE6RXm1peVG07avfApPEHocOcPld9IA94hE3vUGE/edit?gid=0#gid=0", on_change=reset_data_state)
    if st.sidebar.button("Nạp dữ liệu từ Sheets"):
        try:
            with st.spinner("Đang tải dữ liệu từ Google Sheets..."):
                content = download_google_sheet(sheet_url)
                df = pd.read_excel(io.BytesIO(content))
                st.session_state.df_scored = run_lead_scoring(df)
                st.success("Tải dữ liệu và chạy chấm điểm tự động từ Google Sheets thành công!")
        except Exception as e:
            st.error(f"Lỗi: {str(e)}. Hãy chắc chắn rằng Google Sheet đã được cài đặt chế độ chia sẻ công khai.")
else:
    uploaded_file = st.sidebar.file_uploader("Chọn tệp Excel:", type=["xlsx", "xls"], on_change=reset_data_state)
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            if 'df_scored' not in st.session_state:
                st.session_state.df_scored = run_lead_scoring(df)
                st.success("Tải tệp Excel lên và chạy chấm điểm tự động thành công!")
        except Exception as e:
            st.error(f"Lỗi đọc file: {str(e)}")

# Process data if loaded in session state
if 'df_scored' in st.session_state:
    df_scored = st.session_state.df_scored
    
    # Show Metrics
    total_leads = len(df_scored)
    vip_count = len(df_scored[df_scored["Phân loại"] == "VIP/Siêu tiềm năng"])
    pot_count = len(df_scored[df_scored["Phân loại"] == "Tiềm năng"])
    junk_count = len(df_scored[df_scored["Phân loại"] == "Không tiềm năng"])
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số Lead", total_leads)
    col2.metric("VIP/Siêu Tiềm Năng", vip_count)
    col3.metric("Tiềm Năng", pot_count)
    col4.metric("Không Tiềm Năng", junk_count)
    
    st.markdown("---")
    
    # Filtering Section
    st.subheader("🔍 Bộ lọc và tìm kiếm dữ liệu")
    filter_col1, filter_col2, filter_col3 = st.columns([2, 1, 1])
    
    with filter_col1:
        search_query = st.text_input("Tìm kiếm theo Họ tên, SĐT hoặc Nhu cầu:", "").lower().strip()
        
    with filter_col2:
        class_filter = st.selectbox("Lọc theo phân loại:", ["Tất cả", "VIP/Siêu tiềm năng", "Tiềm năng", "Không tiềm năng"])
        
    with filter_col3:
        status_filter = st.selectbox("Lọc theo trạng thái duyệt:", ["Tất cả", "Chờ duyệt", "Đã duyệt", "Bác bỏ"])
    
    # Filter the dataframe
    filtered_df = df_scored.copy()
    
    # Apply text search
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Họ tên"].astype(str).str.lower().str.contains(search_query) |
            filtered_df["Số điện thoại"].astype(str).str.lower().str.contains(search_query) |
            filtered_df["Nhu cầu"].astype(str).str.lower().str.contains(search_query)
        ]
        
    # Apply classification filter
    if class_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["Phân loại"] == class_filter]
        
    # Apply status filter
    if status_filter != "Tất cả":
        filtered_df = filtered_df[filtered_df["Trạng thái duyệt"] == status_filter]
        
    st.subheader(f"🎯 Kết quả chấm điểm ({len(filtered_df)} dòng hiển thị)")
    
    # Interactive data editor
    edited_filtered_df = st.data_editor(filtered_df, use_container_width=True)
    
    # Sync edited changes back to session state to prevent loss
    for idx, row in edited_filtered_df.iterrows():
        # Update matching row in original session state
        st.session_state.df_scored.loc[st.session_state.df_scored["Mã KH"] == row["Mã KH"]] = row
        
    # Export all results to Excel in memory for download
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        st.session_state.df_scored.to_excel(writer, index=False, sheet_name='Scored Leads')
    processed_data = output.getvalue()
    
    # Export and download button group
    dl_col1, dl_col2 = st.columns([1, 4])
    with dl_col1:
        st.download_button(
            label="📥 Tải xuống kết quả bàn giao",
            data=processed_data,
            file_name="lead_scored_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    with dl_col2:
        st.info("Bấm vào các ô trong bảng để trực tiếp chỉnh sửa điểm số, phân loại hoặc trạng thái duyệt (Human-in-the-loop).")
else:
    st.info("Vui lòng cấu hình nguồn dữ liệu ở thanh bên (Sidebar) và nhấn nút Nạp dữ liệu để bắt đầu.")
