# MASTER-INDEX.md — Bản đồ Chỉ mục Hệ thống (SSoT)

Tệp này là Nguồn Sự thật Duy nhất (Single Source of Truth) định nghĩa toàn bộ cấu trúc thư mục, quy tắc, quy trình và kỹ năng vận hành hệ thống trong Workspace này.

---

## 1. Thư mục Vận hành Dự án (Active Directories)
*   `00_ke_hoach/`: Lưu trữ Task Brief và Success Criteria (Pha PLAN).
*   `01_dau_vao/`: Lưu trữ dữ liệu thô đầu vào và Source Registry (Pha DO 1).
*   `02_nhat_ky_va_nhap/`: Nhật ký hoạt động (`pdca_log.md`), ghi chú kiểm tra (`check_notes.md`) và log lỗi.
*   `03_cong_cu/`: Chứa các script Python, prompt phụ, tài liệu tham chiếu (Công cụ hỗ trợ).
*   `04_ban_thao/`: Chứa các bản nháp báo cáo, tệp code nháp, dữ liệu sạch trung gian (WIP).
*   `05_san_pham/`: Chứa báo cáo chính thức, mã nguồn hoàn thiện, bảng Dashboard (Sản phẩm hoàn thiện).
*   `06_ban_giao/`: Lưu trữ các gói bàn giao nén ZIP, tệp PDF xuất bản và tóm tắt nộp bài (Bàn giao).
*   `99_luu_tru/`: Lưu trữ lịch sử dữ liệu của các chu kỳ PDCA cũ.

---

## 2. Bản đồ Thành phần Hệ thống (System Components Map)

| Lớp (Layer) | Tên Tệp tin | Vai trò & Chức năng | Phím tắt kích hoạt (Triggers) |
| :--- | :--- | :--- | :--- |
| **Cấu hình Lõi** | [AGENTS.md](AGENTS.md) | Định nghĩa ranh giới an toàn và phân vai Agent | Nạp tự động |
| **Cấu hình Lõi** | [GEMINI.md](GEMINI.md) | Persona sư phạm Socratic và chu trình PDCA | Nạp tự động |
| **Luật lệ (Rules)** | `.agents/rules/00_workspace_boundaries.md` | Giới hạn ranh giới ghi tệp, cấm lệnh phá hủy | Luôn bật (`always_on`) |
| **Luật lệ (Rules)** | `.agents/rules/01_pdca_operating_rules.md` | Bắt buộc thực hiện kỷ luật 4 bước PDCA tuần tự | Luôn bật (`always_on`) |
| **Luật lệ (Rules)** | `.agents/rules/02_data_safety_rules.md` | Bảo vệ thông tin cá nhân (PII), chống bịa dữ liệu | Luôn bật (`always_on`) |
| **Luật lệ (Rules)** | `.agents/rules/03_output_quality_rules.md` | Chuẩn hóa định dạng Excel, Word, viết Insight OEIA | Luôn bật (`always_on`) |
| **Luật lệ (Rules)** | `.agents/rules/04_safety_gates_and_rules.md` | Cổng an toàn, phân loại rủi ro, phòng prompt injection | Luôn bật (`always_on`) |
| **Luật lệ (Rules)** | `.agents/rules/05_phuong_phap_su_pham.md` | Hướng dẫn Socratic Coaching, 5 cấp độ giá đỡ nhận thức | Luôn bật (`always_on`) |
| **Luật lệ (Rules)** | `.agents/rules/06_chi_so_do_luong.md` | Đo lường tải nhận thức, tốc độ chuẩn hóa, tỷ lệ lỗi | Luôn bật (`always_on`) |
| **Quy trình (Workflows)** | `.agents/workflows/00-quan-tri-workspace.md` | Quản trị, quét sức khỏe hệ thống và dọn dẹp lưu trữ | `/00-quan-tri`, `quan tri workspace` |
| **Quy trình (Workflows)** | `.agents/workflows/01-lap-ke-hoach.md` | Hướng dẫn pha PLAN lập Task Brief & tiêu chí đo lường | `/01-lap-ke-hoach`, `lap ke hoach` |
| **Quy trình (Workflows)** | `.agents/workflows/02-thu-thap-du-lieu.md` | Hướng dẫn pha DO tìm kiếm thông tin và tạo data_raw | `/02-thu-thap`, `thu thap du lieu` |
| **Quy trình (Workflows)** | `.agents/workflows/03-lam-sach-du-lieu.md` | Hướng dẫn viết script Python chuẩn hóa dữ liệu sạch | `/03-lam-sach`, `lam sach du lieu` |
| **Quy trình (Workflows)** | `.agents/workflows/04-phan-tich-va-bao-cao.md` | Tạo dashboard Excel và viết báo cáo Word theo OEIA | `/04-phan-tich`, `phan tich va bao cao` |
| **Quy trình (Workflows)** | `.agents/workflows/05-danh-gia-va-cai-tien.md` | Chấm điểm độc lập (rubric) và lên kế hoạch ACT 2 | `/05-danh-gia`, `danh gia va cai tien` |
| **Kỹ năng (Skills)** | `.agents/skills/01-planner/SKILL.md` | Lập kế hoạch, sinh các tệp Brief tự động | Được gọi bởi Quy trình 01 |
| **Biểu mẫu (Templates)** | `.agents/skills/01-planner/templates/task_card_template.md` | Biểu mẫu Thẻ công việc (Task Card) lập kế hoạch | Nạp bởi Quy trình 01 |
| **Kỹ năng (Skills)** | `.agents/skills/03-cleaner/SKILL.md` | Viết code Python làm sạch dữ liệu tự động | Được gọi bởi Quy trình 03 |
| **Kỹ năng (Skills)** | `.agents/skills/04-writer/SKILL.md` | Diễn giải Insights phân tích dựa trên bằng chứng | Được gọi bởi Quy trình 04 |
| **Kỹ năng (Skills)** | `.agents/skills/05-reviewer/SKILL.md` | Chấm điểm tự động toàn diện dự án thang 100 | Được gọi bởi Quy trình 05 |
| **Biểu mẫu (Templates)** | `.agents/skills/05-reviewer/templates/check_report_template.md` | Biểu mẫu Báo cáo kiểm duyệt chất lượng đầu ra | Nạp bởi Quy trình 05 |
| **Biểu mẫu (Templates)** | `.agents/skills/05-reviewer/templates/act_patch_spec_template.md` | Biểu mẫu Đặc tả bản sửa lỗi để cải tiến quy trình | Nạp bởi Quy trình 05 |
