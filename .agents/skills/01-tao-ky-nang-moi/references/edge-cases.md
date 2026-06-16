# Skill Audit & Optimize — Edge Cases

> Reference document for the `tao-ky-nang-moi` skill (Route 2 and Route 3).
> Load this when encountering non-standard inputs or unusual skill configurations.

---

## EC1: Inline Paste (No Filesystem)

**Scenario:** User pastes raw SKILL.md content directly into conversation instead of providing a path.

**Handling:**
1. Accept the paste as a virtual skill. Assign name `inline-skill-[timestamp]`.
2. Run full 8-Dimension audit against the pasted content.
3. For D6 (Reference Asset Completeness):
   - Cannot check filesystem → score D6 based on whether RESOURCES table entries are reasonable.
   - Flag as: "D6 scored on RESOURCES table consistency only — filesystem verification unavailable."
4. If repair is needed: output the repaired SKILL.md content inline.
5. Offer to save: "Tôi có thể tạo skill folder tại `.agents/skills/[inferred-name]/` nếu bạn muốn."

---

## EC2: Encoding Issues (Vietnamese Diacritics Corruption)

**Scenario:** SKILL.md contains garbled Vietnamese characters (mojibake).

**Detection Signals:**
- Sequences like `Ä'`, `Æ°`, `á»` in otherwise Vietnamese text
- Inconsistent character encoding within same file
- File reads correctly in some tools but corrupted in others

**Handling:**
1. Detect encoding by examining byte patterns.
2. Flag in audit report: "🔴 ENCODING ISSUE: File contains corrupted Vietnamese diacritics."
3. Do NOT attempt auto-repair of encoding in-place (risk of data loss).
4. Recommendation: "Convert file to UTF-8 before re-auditing."
5. Score the skill based on readable content — do not penalize for encoding (it's an infrastructure issue, not a content issue).

---

## EC3: Non-Standard Skill Structure

**Scenario:** Skill contains custom subdirectories beyond the canonical 4 (e.g., `formulas/`, `tools/`, `datasets/`).

**Handling:**
1. Treat non-standard subdirectories as **custom domain folders** — valid extensions of the skill.
2. **DO NOT penalize** structure score for having extra folders.
3. **DO audit** the content of custom folders:
   - Check if files inside are referenced from SKILL.md.
   - Check if files are substantive (> 500 bytes, not stubs).
4. In the report, list custom folders separately:
   ```
   Custom folders detected: formulas/ (3 files), tools/ (1 file)
   Status: Referenced ✅ | Content quality: OK
   ```
5. If custom folder content is unreferenced → flag as potential orphan asset (🟡 WARNING, not 🔴 FAIL).

---

## EC4: Circular References (Cross-Skill Dependencies)

**Scenario:** Skill A's SKILL.md references content from Skill B, or vice versa.

**Detection:**
- RESOURCES table entry points outside the skill's own directory (e.g., `../other-skill/references/shared-framework.md`)
- SKILL.md body mentions another skill by name with dependency language ("requires skill X to run first")

**Handling:**
1. Flag in audit report as: "📎 CROSS-SKILL DEPENDENCY: [skill-a] → [skill-b]."
2. **DO NOT penalize score** — cross-skill references are architecturally valid.
3. Verify the target file exists (broken cross-reference IS penalized under D6).
4. Recommend in report: "Consider extracting shared content into a common `references/` location if multiple skills depend on it."
5. Document the dependency graph in the batch report.

---

## EC5: Read-Only Skill Directories

**Scenario:** Skills are in a read-only location (e.g., `/mnt/skills/`, system-managed folders, or Git submodules).

**Handling:**
1. **AUDIT:** Proceed normally — read-only doesn't affect scoring.
2. **OPTIMIZE:** Cannot modify files in-place.
   - Copy the target skill to workspace `artifacts/skill-repairs/[skill-name]/`.
   - Execute all repairs on the copy.
   - Present repaired files to user with instructions:
     ```
     Repaired files saved to: artifacts/skill-repairs/[skill-name]/
     To install: copy contents back to [original-path]
     ```
3. NEVER attempt to write to a read-only location — fail gracefully with clear error message.
