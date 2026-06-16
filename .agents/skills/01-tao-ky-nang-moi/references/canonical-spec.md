# Claude Agent Skill — Canonical Spec
> Chuẩn thiết kế skill cho Claude agent. Dùng làm reference khi viết, review, hoặc audit bất kỳ SKILL.md nào.

---

## 1. ANATOMY OF A SKILL

```
skill-name/
├── SKILL.md                  ← bắt buộc — orchestrator chính
├── evals/
│   └── evals.json            ← test cases
├── references/               ← knowledge chunks — load on demand
│   ├── topic-a.md
│   └── topic-b.md
├── assets/                   ← templates, output blueprints, icons
│   └── default-template.md
└── scripts/                  ← executable code — chạy không cần load vào context
    └── verify-output.py
```

**Nguyên tắc tách layer:**
- `SKILL.md` = orchestration logic, role, process, output format, resource routing
- `references/` = domain knowledge sâu — chỉ load khi task cần
- `assets/` = output templates — copy sang output, không phân tích
- `scripts/` = deterministic operations — chạy trực tiếp, không chiếm context window

---

## 2. PROGRESSIVE DISCLOSURE — 3 CẤP LOADING

| Cấp | Nội dung | Luôn trong context? | Kích thước lý tưởng |
|---|---|---|---|
| 1 | `name` + `description` (YAML) | ✅ Luôn luôn | ~50–150 words |
| 2 | Body của `SKILL.md` | ✅ Khi skill trigger | < 500 lines |
| 3 | `references/`, `assets/`, `scripts/` | ❌ Load khi cần | Không giới hạn |

**Rule quan trọng:** Nếu SKILL.md đang chạm 500 lines, đó là tín hiệu cần tách thêm
companion files. Không nên nhồi knowledge vào body.

---

## 3. YAML FRONTMATTER — CHỈ 2 FIELDS BẮT BUỘC

```yaml
---
name: skill-identifier           # kebab-case, unique
description: >
  [Mô tả ngắn việc skill làm].
  [Khi nào nên dùng — liệt kê trigger phrases cụ thể].
  Make sure to use this skill whenever the user mentions [X, Y, Z]
  — even if they don't use the exact term.
---
```

**KHÔNG dùng:**
```yaml
# ❌ Các fields này không được support và tốn tokens vô ích
metadata:
  owner: ...
  version: ...
  category: ...
  execution_level: ...
  review_status: ...
  priority: ...
```

`compatibility` là field tùy chọn duy nhất được hỗ trợ (khi skill cần tool cụ thể).

---

## 4. DESCRIPTION — NGUYÊN TẮC "PUSHY"

Claude có xu hướng **undertrigger** — không dùng skill dù phù hợp. Description phải
chủ động đẩy Claude dùng skill đúng lúc.

**Pattern chuẩn:**

```
[Một câu mô tả skill làm gì].
Use this skill whenever the user mentions [list trigger keywords/phrases].
Also trigger when [edge cases hoặc implicit signals].
Even if the user doesn't say "[exact skill name]", trigger when [scenario].
```

**Ví dụ tốt:**
> Design practical multi-layer folder structures. Use this skill whenever the user mentions
> shared drive, folder mess, naming convention, file organization, "where to put files",
> or asks about archiving — even if they don't use the words "folder architecture".

**Ví dụ kém:**
> Use this skill when the user needs a folder structure.

---

## 5. BODY STRUCTURE — PHẦN CỐT LÕI

Đây là các section được khuyến nghị, **theo thứ tự**:

```markdown
## ROLE           ← Skill là ai, hành xử như thế nào
## PURPOSE        ← Dùng cho gì / không dùng cho gì
## ACTIVATION SIGNALS  ← Trigger phrases bổ sung (nếu cần)
## WHEN TO CLARIFY     ← Khi nào hỏi user, hỏi gì
## PROCESS        ← Workflow step-by-step
## OUTPUT FORMAT  ← Template output bắt buộc
## RESOURCES      ← Routing table: situation → file
## QA             ← Checklist trước khi deliver
## RULES          ← Constraints không được vi phạm
```

**Không nên có trong SKILL.md body:**
- `EVALUATION HOOKS` / `MAINTENANCE` → đây là metadata của skill owner, không phải instruction cho Claude
- `SOURCE OF TRUTH` với 5 cấp priority → overkill cho Claude skill
- `REFERENCES TO CONSULT` nếu đã có `RESOURCES` routing table → trùng lặp
- Bất kỳ nội dung domain knowledge nào dài hơn 3–4 dòng → chuyển sang `references/`

---

## 6. RESOURCE ORCHESTRATION — NGUYÊN TẮC RETRIEVAL

```markdown
## RESOURCES — LOAD ONLY WHAT'S NEEDED

| Situation | Load |
|---|---|
| [trigger condition] | `references/file.md` |
| [trigger condition] | `assets/template.md` |
```

**Rules:**
- Load minimum necessary — không load tất cả references mặc định
- Nếu chỉ cần một section của reference file lớn (>300 lines), chỉ load section đó
- Reference files >300 lines cần có table of contents ở đầu file
- Scripts chạy trực tiếp, không cần load vào context

---

## 7. OUTPUT CONTRACT

Mọi skill cần định nghĩa rõ output format. Dùng template cứng khi có thể:

```markdown
## OUTPUT FORMAT
ALWAYS use this structure:

1. SECTION A — [mô tả]
2. SECTION B — [mô tả]
3. SECTION C — [mô tả]
```

Output quality bar nên nằm trong QA checklist, không phải prose dài.

---

## 8. WRITING STYLE — 5 NGUYÊN TẮC

| # | Nguyên tắc | Ví dụ |
|---|---|---|
| 1 | Dùng imperative form | "Load only what's needed" không phải "You should try to load..." |
| 2 | Giải thích *tại sao* thay vì dùng MUST nhiều | "Avoid deep nesting — it hurts retrieval" tốt hơn "MUST NOT nest > 4 levels" |
| 3 | Không viết quá narrow / example-specific | Rule chung, không hardcode từng case |
| 4 | Dùng table thay vì bullet list dài | Dễ scan, tốn ít dòng hơn |
| 5 | Viết xong đọc lại với "fresh eyes" | Xóa bất cứ thứ gì Claude không cần biết để làm task |

---

## 9. COMPANION FILES — KHI NÀO TÁCH

| Tín hiệu | Hành động |
|---|---|
| Body > 300 lines | Tách section dài nhất ra `references/` |
| Có nhiều ví dụ / case / variant | → `references/examples.md` |
| Có naming quan-ly-quy-tac / standards dài | → `references/naming-convention.md` |
| Có nhiều work model / framework | → `references/work-models.md`, mỗi model 1 section |
| Có template output phức tạp | → `assets/default-template.md` |
| Có step deterministic / verifiable | → `scripts/verify.py` |

**Vàng rule:** Nếu Claude không cần đọc thứ đó để quyết định *làm gì tiếp theo*,
đừng để nó trong SKILL.md body.

---

## 10. EVALS — CẤU TRÚC TEST CASE

```json
{
  "skill_name": "folder-architecture-design",
  "evals": [
    {
      "id": 1,
      "prompt": "We're a 5-person marketing team on Google Drive. Help us organize our files.",
      "expected_output": "Folder tree + naming quan-ly-quy-tac + archive logic",
      "files": []
    }
  ]
}
```

Test prompts phải đủ phức tạp — simple 1-step queries sẽ không trigger skill.
Viết prompts như real user thực sự nói.

---

## 11. CHECKLIST AUDIT — DÙNG KHI REVIEW SKILL.MD

```
YAML
[ ] Chỉ có name + description (+ compatibility nếu cần)
[ ] Description có trigger phrases cụ thể
[ ] Description có "even if they don't use the word X"

BODY
[ ] Body < 500 lines
[ ] Không có EVALUATION HOOKS / MAINTENANCE trong body
[ ] Không có domain knowledge dài hơn 4 dòng trong body
[ ] Có ROLE, PURPOSE, PROCESS, OUTPUT FORMAT, RESOURCES, QA

COMPANION FILES
[ ] references/ chứa knowledge dài
[ ] assets/ chứa output templates
[ ] scripts/ chứa logic deterministic

RESOURCES
[ ] Có routing table: situation → file
[ ] Không có "load all references"
[ ] Files >300 lines có table of contents

OUTPUT
[ ] Template output được định nghĩa rõ
[ ] QA checklist cụ thể, có thể verify

WRITING
[ ] Dùng imperative form
[ ] Không có section trùng lặp
[ ] Đọc lại: xóa thứ gì Claude không cần để làm task
```

---

## 12. TOKEN BUDGET — ƯỚC LƯỢNG

| Thành phần | Token ước tính |
|---|---|
| YAML frontmatter (chuẩn) | 80–150 |
| SKILL.md body (lean) | 500–900 |
| SKILL.md body (standard) | 900–1,500 |
| Mỗi reference file được load | 300–800 |
| Script chạy (không load) | ~0 |

**Target:** Core SKILL.md (YAML + body) dưới 1,500 tokens cho hầu hết skills thông thường.
Skills phức tạp có thể lên 2,000–2,500 nếu justified.
