// Lead Scoring Web App State
let leadsData = [];

// Realistic Mock Data for Instant Preview
const mockLeads = [
    { "Mã KH": "KH001", "Họ tên": "Nguyễn Văn A", "Số điện thoại": "0912345678", "Nhu cầu": "Cần tìm mua Biệt thự đơn lập tại Vinhomes Ocean Park, tài chính khoảng 35 tỷ, yêu cầu pháp lý chuẩn 100% có sổ hồng riêng. Muốn gặp trực tiếp chủ đầu tư để đàm phán.", "Điểm số": 150, "Phân loại": "VIP/Siêu tiềm năng", "Lý do chấm điểm": "Ngân sách lớn: 35 tỷ (>= 20 tỷ); Từ khóa VIP phát hiện: biệt thự đơn lập, vinhomes ocean park, pháp lý chuẩn 100%, sổ hồng riêng, muốn gặp trực tiếp chủ đầu tư để đàm phán", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH002", "Họ tên": "Trần Thị B", "Số điện thoại": "0987654321", "Nhu cầu": "Tìm kiếm căn Penthouse ven sông khu Phú Mỹ Hưng, Quận 1. Tài chính mạnh không thành vấn đề. Tôi là nhà đầu tư chuyên nghiệp muốn mua sỉ.", "Điểm số": 150, "Phân loại": "VIP/Siêu tiềm năng", "Lý do chấm điểm": "Từ khóa VIP phát hiện: penthouse, quận 1, ven sông, phú mỹ hưng, tài chính mạnh, không thành vấn đề, nhà đầu tư chuyên nghiệp, mua sỉ", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH003", "Họ tên": "Phạm Minh C", "Số điện thoại": "0901234567", "Nhu cầu": "Là chủ doanh nghiệp cần tìm mua Quỹ đất công nghiệp hoặc sàn văn phòng diện tích lớn khu vực TP.HCM. Pháp lý sổ hồng riêng rõ ràng.", "Điểm số": 150, "Phân loại": "VIP/Siêu tiềm năng", "Lý do chấm điểm": "Từ khóa VIP phát hiện: quỹ đất công nghiệp, sàn văn phòng diện tích lớn, chủ doanh nghiệp, sổ hồng riêng", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH004", "Họ tên": "Lê Văn D", "Số điện thoại": "0934567890", "Nhu cầu": "Cần mua nhà mặt phố Quận 1 giá 1-2 tỷ có sân vườn hồ bơi.", "Điểm số": 50, "Phân loại": "Không tiềm năng", "Lý do chấm điểm": "Yêu cầu phi thực tế (Nhà Q1/Trung tâm giá rẻ)", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH005", "Họ tên": "Hoàng Thị E", "Số điện thoại": "0945678901", "Nhu cầu": "Nhầm số rồi em ơi, chị không có nhu cầu mua bán bất động sản gì đâu nhé, dữ liệu cũ rồi.", "Điểm số": 50, "Phân loại": "Không tiềm năng", "Lý do chấm điểm": "Dấu hiệu không tiềm năng: nhầm số, không có nhu cầu, dữ liệu cũ", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH006", "Họ tên": "Nguyễn Văn F", "Số điện thoại": "0956789012", "Nhu cầu": "Mời chào gói bảo hiểm nhân thọ và hỗ trợ vay vốn ngân hàng lãi suất thấp 5%.", "Điểm số": 50, "Phân loại": "Không tiềm năng", "Lý do chấm điểm": "Dấu hiệu không tiềm năng: bảo hiểm, vay vốn, mời chào dịch vụ", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH007", "Họ tên": "Trần Văn G", "Số điện thoại": "0967890123", "Nhu cầu": "Khách này gọi nhiều lần không bắt máy, thuê bao không liên lạc được, không phản hồi Zalo.", "Điểm số": 50, "Phân loại": "Không tiềm năng", "Lý do chấm điểm": "Dấu hiệu không tiềm năng: thuê bao, gọi nhiều lần không bắt máy, không phản hồi zalo", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH008", "Họ tên": "Phạm Thị H", "Số điện thoại": "0978901234", "Nhu cầu": "Cần tìm mua căn hộ chung cư 2 phòng ngủ khoảng 3.5 tỷ tại Quận 7. Cần vay ngân hàng hỗ trợ 70%.", "Điểm số": 100, "Phân loại": "Tiềm năng", "Lý do chấm điểm": "Khách hàng tầm trung/Nhu cầu thực", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH009", "Họ tên": "Vũ Văn I", "Số điện thoại": "0989012345", "Nhu cầu": "Tìm nhà phố phân khúc 5-7 tỷ ở Bình Thạnh, đang cân nhắc chính sách thanh toán của chủ đầu tư.", "Điểm số": 100, "Phân loại": "Tiềm năng", "Lý do chấm điểm": "Khách hàng tầm trung/Nhu cầu thực", "Trạng thái duyệt": "Chờ duyệt" },
    { "Mã KH": "KH010", "Họ tên": "Đặng Thị J", "Số điện thoại": "0990123456", "Nhu cầu": "Nhu cầu thực tìm mua đất nền vùng ven tầm 2 tỷ, cần tư vấn thêm về pháp lý và quy hoạch vị trí.", "Điểm số": 100, "Phân loại": "Tiềm năng", "Lý do chấm điểm": "Khách hàng tầm trung/Nhu cầu thực", "Trạng thái duyệt": "Chờ duyệt" }
];

// Elements
const tableBody = document.getElementById('table-body');
const uploadInput = document.getElementById('excel-upload');
const searchInput = document.getElementById('search-input');
const filterClassification = document.getElementById('filter-classification');
const filterStatus = document.getElementById('filter-status');
const exportBtn = document.getElementById('export-excel-btn');

// Initialize App
window.addEventListener('DOMContentLoaded', () => {
    leadsData = [...mockLeads];
    renderApp();
    showToast("Đã nạp dữ liệu mẫu thành công!");
});

// Main render function
function renderApp() {
    updateKPIs();
    renderTable();
}

// Update KPI stats card
function updateKPIs() {
    const total = leadsData.length;
    const vip = leadsData.filter(d => d["Phân loại"] === 'VIP/Siêu tiềm năng').length;
    const potential = leadsData.filter(d => d["Phân loại"] === 'Tiềm năng').length;
    const junk = leadsData.filter(d => d["Phân loại"] === 'Không tiềm năng').length;

    document.getElementById('val-total').innerText = total;
    document.getElementById('val-vip').innerText = vip;
    document.getElementById('val-potential').innerText = potential;
    document.getElementById('val-junk').innerText = junk;
}

// Render dynamic rows to table
function renderTable() {
    const searchQuery = searchInput.value.toLowerCase();
    const classificationFilter = filterClassification.value;
    const statusFilter = filterStatus.value;

    const filtered = leadsData.filter(lead => {
        const matchesSearch = 
            (lead["Họ tên"] || "").toLowerCase().includes(searchQuery) ||
            (lead["Số điện thoại"] || "").toLowerCase().includes(searchQuery) ||
            (lead["Nhu cầu"] || "").toLowerCase().includes(searchQuery);

        const matchesClass = classificationFilter === 'all' || lead["Phân loại"] === classificationFilter;
        const matchesStatus = statusFilter === 'all' || lead["Trạng thái duyệt"] === statusFilter;

        return matchesSearch && matchesClass && matchesStatus;
    });

    tableBody.innerHTML = '';

    if (filtered.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="9" style="text-align: center; padding: 40px; color: var(--text-muted);">
                    Không tìm thấy bản ghi nào khớp bộ lọc.
                </td>
            </tr>
        `;
        return;
    }

    filtered.forEach((lead, index) => {
        const tr = document.createElement('tr');
        
        // Dynamic badge style
        let classBadge = 'badge-potential';
        if (lead["Phân loại"] === 'VIP/Siêu tiềm năng') classBadge = 'badge-vip';
        if (lead["Phân loại"] === 'Không tiềm năng') classBadge = 'badge-junk';

        // Select approved state class
        let statusClass = 'status-pending';
        if (lead["Trạng thái duyệt"] === 'Đã duyệt') statusClass = 'status-approved';
        if (lead["Trạng thái duyệt"] === 'Bác bỏ') statusClass = 'status-rejected';

        tr.innerHTML = `
            <td><strong>${lead["Mã KH"] || `KH${index+1}`}</strong></td>
            <td>${lead["Họ tên"] || ''}</td>
            <td>${lead["Số điện thoại"] || ''}</td>
            <td class="text-truncate" title="${lead["Nhu cầu"] || ''}">${lead["Nhu cầu"] || ''}</td>
            <td>
                <input type="number" class="score-input" value="${lead["Điểm số"]}" 
                    onchange="updateScore('${lead["Mã KH"]}', this.value)">
            </td>
            <td><span class="badge ${classBadge}">${lead["Phân loại"]}</span></td>
            <td style="font-size: 12px; color: var(--text-muted); max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${lead["Lý do chấm điểm"] || ''}">
                ${lead["Lý do chấm điểm"] || 'Khách hàng tầm trung'}
            </td>
            <td>
                <select class="status-select ${statusClass}" onchange="updateStatus('${lead["Mã KH"]}', this.value)">
                    <option value="Chờ duyệt" ${lead["Trạng thái duyệt"] === 'Chờ duyệt' ? 'selected' : ''}>Chờ duyệt</option>
                    <option value="Đã duyệt" ${lead["Trạng thái duyệt"] === 'Đã duyệt' ? 'selected' : ''}>Đã duyệt</option>
                    <option value="Bác bỏ" ${lead["Trạng thái duyệt"] === 'Bác bỏ' ? 'selected' : ''}>Bác bỏ</option>
                </select>
            </td>
            <td>
                <div class="action-btn-group">
                    <button class="action-btn action-approve" onclick="quickAction('${lead["Mã KH"]}', 'Đã duyệt')" title="Duyệt nhanh">
                        <i class="fa-solid fa-check"></i>
                    </button>
                    <button class="action-btn action-reject" onclick="quickAction('${lead["Mã KH"]}', 'Bác bỏ')" title="Bác bỏ nhanh">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                </div>
            </td>
        `;
        tableBody.appendChild(tr);
    });
}

// Update Score handler
window.updateScore = function(code, newScoreVal) {
    const score = parseInt(newScoreVal) || 0;
    const lead = leadsData.find(d => d["Mã KH"] === code);
    if (lead) {
        lead["Điểm số"] = score;
        // Dynamically adjust classification based on customized score
        if (score >= 150) {
            lead["Phân loại"] = "VIP/Siêu tiềm năng";
        } else if (score <= 50) {
            lead["Phân loại"] = "Không tiềm năng";
        } else {
            lead["Phân loại"] = "Tiềm năng";
        }
        lead["Lý do chấm điểm"] = "Sửa đổi thủ công bởi Người vận hành";
        renderApp();
        showToast(`Đã cập nhật điểm cho khách hàng ${code}: ${score}`);
    }
};

// Update Status handler
window.updateStatus = function(code, newStatus) {
    const lead = leadsData.find(d => d["Mã KH"] === code);
    if (lead) {
        lead["Trạng thái duyệt"] = newStatus;
        renderApp();
        showToast(`Khách hàng ${code} được đặt sang: ${newStatus}`);
    }
};

// Quick action buttons (Approve/Reject)
window.quickAction = function(code, status) {
    updateStatus(code, status);
};

// AI Lead Scoring scoring rules in JS
function scoreLeadInJS(demand) {
    const demandLower = (demand || "").toString().toLowerCase().trim();
    let score = 100;
    let classification = "Tiềm năng";
    let reasons = [];

    // VIP criteria
    const vipKeywords = {
        "loai_hinh_cao_cap": ["biệt thự đơn lập", "penthouse", "shophouse mặt đường lớn", "quỹ đất công nghiệp", "sàn văn phòng diện tích lớn"],
        "vi_tri_dac_dia": ["quận 1", "ven sông", "vinhomes ocean park", "phú mỹ hưng"],
        "doi_tuong_vip": ["chủ doanh nghiệp", "nhà đầu tư chuyên nghiệp", "mua sỉ", "mua số lượng lớn"],
        "phap_ly_minh_bach": ["pháp lý chuẩn 100%", "sổ hồng riêng", "muốn gặp trực tiếp chủ đầu tư để đàm phán"],
        "tai_chinh_manh": ["tài chính mạnh", "không thành vấn đề"]
    };

    let matchedVip = [];
    
    // Extract budgets >= 20 billion
    const budgetRegex = /(\d+)\s*(?:tỷ|ty|tỉ)/g;
    let budgetMatch;
    while ((budgetMatch = budgetRegex.exec(demandLower)) !== null) {
        const val = parseInt(budgetMatch[1]);
        if (val >= 20) {
            matchedVip.push(`Ngân sách lớn: ${val} tỷ`);
        }
    }

    for (const [key, words] of Object.entries(vipKeywords)) {
        for (const w of words) {
            if (demandLower.includes(w)) {
                matchedVip.push(w);
            }
        }
    }

    // Junk criteria
    const junkKeywords = {
        "khong_nhu_cau": ["nhầm số", "không có nhu cầu", "dữ liệu cũ", "nhầm ngành"],
        "khong_thien_chi": ["hỏi giá cho vui", "chưa có ý định mua", "thái độ không hợp tác"],
        "spam_quang_cao": ["bảo hiểm", "vay vốn", "mời chào dịch vụ"],
        "lien_lac_loi": ["thuê bao", "gọi nhiều lần không bắt máy", "không phản hồi zalo", "gọi nhiều lần không nghe"]
    };

    let matchedJunk = [];

    // Low price in central areas (Q1, Trung tâm and price < 3 billion)
    const hasCentral = ["quận 1", "q1", "trung tâm"].some(x => demandLower.includes(x));
    const hasLowPrice = ["1 tỷ", "2 tỷ", "1-2 tỷ", "vài trăm triệu", "vài trăm tr"].some(x => demandLower.includes(x));
    if (hasCentral && hasLowPrice) {
        matchedJunk.push("yêu cầu phi thực tế (nhà Q1/trung tâm giá rẻ)");
    }

    for (const [key, words] of Object.entries(junkKeywords)) {
        for (const w of words) {
            if (demandLower.includes(w)) {
                matchedJunk.push(w);
            }
        }
    }

    // Apply logic
    if (matchedVip.length > 0 && matchedJunk.length === 0) {
        score = 150;
        classification = "VIP/Siêu tiềm năng";
        reasons.push("Phát hiện tiêu chí VIP: " + matchedVip.join(", "));
    } else if (matchedJunk.length > 0) {
        score = 50;
        classification = "Không tiềm năng";
        reasons.push("Phát hiện dấu hiệu loại trừ: " + matchedJunk.join(", "));
    } else {
        score = 100;
        classification = "Tiềm năng";
        let potentialReasons = [];
        if (["chung cư", "căn hộ", "nhà phố"].some(x => demandLower.includes(x))) {
            potentialReasons.push("Chung cư/nhà phố tầm trung");
        }
        if (demandLower.includes("vay") || demandLower.includes("ngân hàng")) {
            potentialReasons.push("Cần vay/cân nhắc chính sách ngân hàng");
        }
        if (demandLower.includes("tư vấn") || demandLower.includes("pháp lý") || demandLower.includes("vị trí")) {
            potentialReasons.push("Cần tư vấn thêm pháp lý/vị trí");
        }

        if (potentialReasons.length > 0) {
            reasons.push(potentialReasons.join(" / "));
        } else {
            reasons.push("Khách hàng tầm trung/Nhu cầu thực");
        }
    }

    return {
        score: score,
        classification: classification,
        reason: reasons.join("; ")
    };
}

// Process and Score all leads
function processAndScoreLeads(rawLeads) {
    leadsData = rawLeads.map((item, idx) => {
        const demand = item["Nhu cầu"] || item["Mô tả"] || item["Nhu cầu khách hàng"] || "";
        const scoring = scoreLeadInJS(demand);
        
        return {
            "Mã KH": item["Mã KH"] || item["Mã khách hàng"] || `KH${idx+1:03d}`,
            "Họ tên": item["Họ tên"] || item["Tên khách hàng"] || "Chưa rõ",
            "Số điện thoại": item["Số điện thoại"] || item["SĐT"] || item["Sdt"] || "N/A",
            "Nhu cầu": demand,
            "Điểm số": scoring.score,
            "Phân loại": scoring.classification,
            "Lý do chấm điểm": scoring.reason,
            "Trạng thái duyệt": item["Trạng thái duyệt"] || "Chờ duyệt"
        };
    });
    renderApp();
}

// Google Sheets Fetch Handler
const gsheetFetchBtn = document.getElementById('gsheet-fetch-btn');
const gsheetUrlInput = document.getElementById('gsheet-url');

if (gsheetFetchBtn) {
    gsheetFetchBtn.addEventListener('click', async () => {
        const url = gsheetUrlInput.value.trim();
        if (!url) {
            showToast("Vui lòng nhập link Google Sheets!", "danger");
            return;
        }
        
        const sheetIdMatch = url.match(/\/d\/([a-zA-Z0-9-_]+)/);
        if (!sheetIdMatch) {
            showToast("Định dạng link Google Sheets không đúng!", "danger");
            return;
        }
        
        const sheetId = sheetIdMatch[1];
        const gidMatch = url.match(/gid=(\d+)/);
        const gid = gidMatch ? gidMatch[1] : "0";
        
        const exportUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=csv&gid=${gid}`;
        
        gsheetFetchBtn.disabled = true;
        gsheetFetchBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Đang tải...`;
        
        try {
            const response = await fetch(exportUrl);
            if (!response.ok) throw new Error("Không thể tải sheet. Hãy kiểm tra cài đặt chia sẻ.");
            const csvText = await response.text();
            
            const workbook = XLSX.read(csvText, { type: 'string' });
            const sheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[sheetName];
            const json = XLSX.utils.sheet_to_json(worksheet);
            
            if (json.length === 0) {
                showToast("Bảng tính rỗng hoặc không đúng cấu trúc!", "danger");
                return;
            }
            
            processAndScoreLeads(json);
            showToast("Đã tải dữ liệu Google Sheets & chấm điểm tự động thành công!");
        } catch (err) {
            console.error(err);
            showToast("Lỗi CORS hoặc link Sheets không công khai. Hãy xuất Excel và nạp thủ công!", "danger");
        } finally {
            gsheetFetchBtn.disabled = false;
            gsheetFetchBtn.innerHTML = `<i class="fa-solid fa-cloud-arrow-down"></i> Tải & Chấm Điểm`;
        }
    });
}

// Import Excel Handler
uploadInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(evt) {
        try {
            const data = evt.target.result;
            const workbook = XLSX.read(data, { type: 'binary' });
            const firstSheetName = workbook.SheetNames[0];
            const worksheet = workbook.Sheets[firstSheetName];
            const json = XLSX.utils.sheet_to_json(worksheet);

            if (json.length === 0) {
                showToast("Tệp tải lên rỗng!", "danger");
                return;
            }

            processAndScoreLeads(json);
            showToast("Nạp tệp Excel & chạy thuật toán chấm điểm tự động thành công!");
        } catch (error) {
            console.error(error);
            showToast("Lỗi khi đọc file Excel!", "danger");
        }
    };
    reader.readAsBinaryString(file);
});

// Search & Filter Events
searchInput.addEventListener('input', renderTable);
filterClassification.addEventListener('change', renderTable);
filterStatus.addEventListener('change', renderTable);

// Export Excel Final Handler
exportBtn.addEventListener('click', () => {
    try {
        const worksheet = XLSX.utils.json_to_sheet(leadsData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Final Scored Leads");
        
        // Export file name
        XLSX.writeFile(workbook, "data_final.xlsx");
        showToast("Xuất file Excel thành công! Đã sẵn sàng bàn giao.");
    } catch (error) {
        console.error(error);
        showToast("Lỗi khi xuất file Excel!", "danger");
    }
});

// Toast notification helper
function showToast(message, type = "success") {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <i class="fa-solid ${type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation'}"></i>
        <span>${message}</span>
    `;
    container.appendChild(toast);
    
    // Auto remove
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
