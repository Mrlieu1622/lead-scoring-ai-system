# Skill Audit Scoring Engine — 8-Dimension Rubric (100-Point Scale)

> Reference document for the `tao-ky-nang-moi` skill, Route 2 (ASSESS).
> Contains the complete scoring algorithm for evaluating any Claude Agent skill.
> Agent MUST load this file when executing batch audit or single-skill deep scan.
>
> **Framework Position:** This engine provides DEEPER scoring than CQS Tầng 2.
> CQS gates (in `kiem-dinh-chat-luong/references/cqs-validation-engine.md`) MUST pass BEFORE this engine runs.
> D3 body structure aligns with the Canonical 10-section spec in `references/canonical-4tier-spec.md`.
> D7 Epistemic Wiring aligns with CQS Tầng 2 Physical Structure checks (A1-A4).

---

## Structural Classification (Pre-Scoring)

Before scoring, classify each skill folder into one of 5 types:

| Type | Structure | Description |
| --- | --- | --- |
| **TYPE-A** | `SKILL.md` + `references/` (with content) + optional `assets/`, `scripts/`, `evals/` | Full structure — production-grade |
| **TYPE-B** | `SKILL.md` + `references/` (broken links or thin content) | Partial — scaffolded but incomplete |
| **TYPE-C** | `SKILL.md` only (no subdirectories) | Single-file — may be intentional for simple skills |
| **TYPE-D** | `SKILL.md` (< 20 lines body or frontmatter-only) + empty dirs | Skeleton — empty shell |
| **TYPE-E** | Raw text (inline paste, no filesystem) | Virtual — audit inline then offer to save |

> TYPE-C and TYPE-D are NOT automatically bad. TYPE-C is valid for simple skills that genuinely don't need references. The scoring dimensions will determine if the simplicity is intentional vs. negligent.

---

## 8-Dimension Scoring

### D1 — Frontmatter Quality (20 pts)

```text
+5  : `name` field exists AND matches folder name (kebab-case)
+5  : `description` field exists AND is not empty
+5  : description >= 80 words (sufficient context for trigger matching)
+5  : YAML syntax valid (no broken indentation, no missing --- delimiters)

Penalties:
-5  : description cuts off mid-sentence (truncation detected)
-5  : name contains spaces or special characters (non-kebab-case)
-10 : description is empty or only contains skill name as placeholder
```

### D2 — Description Trigger Power (20 pts)

```text
+5  : Contains ≥ 5 specific trigger phrases (keywords/verbs user would say)
+5  : "Pushy" language — specifies WHEN to trigger including edge cases
+5  : Explains what skill DOES (not just what it IS) — action-oriented
+5  : Language consistency: bilingual if serving VN users, OR consistently EN

Penalties:
-5  : Description is just a paraphrase of the name (zero added value)
-10 : Description empty or placeholder ("TODO", "TBD")
-3  : Missing "Even if..." or "Also trigger when..." clause (under-triggers)
```

**Pushy Test (Mental Check):** Read only the description. Ask: "If a user says these words, will Claude DEFINITELY trigger this skill?" If ambiguous → D2 fails.

### D3 — Body Structure (15 pts)

> Cross-reference: Canonical 10-section spec in `references/canonical-4tier-spec.md`.
> Sections checked: ROLE, PURPOSE, WHEN TO CLARIFY, PROCESS, OUTPUT FORMAT, RESOURCES, QA, RULES.

```text
+5  : Has ≥ 6 of the 8 mandatory sections from Canonical Spec
+5  : PROCESS section has ≥ 1 decision point (if/then, table routing, gate)
+3  : Has ≥ 1 concrete example (input → output pair)
+2  : Has error handling or edge case guidance

Penalties:
-3  : Body is just a flat bullet list without section headings
-5  : Body empty or < 5 meaningful lines
-2  : Missing RESOURCES section (breaks Progressive Disclosure)
```

### D4 — Progressive Disclosure (10 pts)

```text
+5  : SKILL.md has pointer(s) to references/ via RESOURCES routing table
+3  : Does NOT load all content upfront — uses lazy-load/on-demand pattern
+2  : Has table of contents if SKILL.md > 200 lines

Penalties:
-3  : All knowledge crammed into SKILL.md despite being extractable
-5  : References exist on disk but SKILL.md has no pointer to them (disconnected)
-2  : ## RESOURCES section missing entirely
```

### D5 — Token Budget Discipline (10 pts)

```text
+10 : SKILL.md < 300 lines (optimal — lean orchestrator)
+7  : SKILL.md 300-500 lines (acceptable)
+3  : SKILL.md 500-700 lines (borderline bloat)
0   : SKILL.md > 700 lines (bloated — mandatory extraction needed)

Penalties:
-3  : Duplicate content between SKILL.md and references/ (detected via text overlap > 10 lines)
```

### D6 — Reference Asset Completeness (10 pts)

```text
# Only applies if skill HAS or NEEDS references
+5  : Every file referenced in SKILL.md's RESOURCES table physically exists on disk
+3  : Reference files have substantive content (not empty stubs — each > 500 bytes)
+2  : Filenames are descriptive and typo-free

Penalties:
-5  : Broken link detected (referenced file does not exist)
-5  : TYPE-C skill that CLEARLY needs references (see Enrichment Threshold below)
N/A : TYPE-C skill that genuinely doesn't need references (simple skill) → skip D6
```

**Enrichment Threshold Decision Tree (determines if TYPE-C is OK):**
```text
Q1: Does SKILL.md mention "references/" or "xem file" or contain a RESOURCES table?
    → YES: Clearly needs references. Penalize D6.
    → NO: Go to Q2.

Q2: Does skill have complex workflow (> 3 phases, > 5 decision points)?
    → YES: Would benefit from references. Flag as 🟡 suggestion, don't hard-penalize.
    → NO: Go to Q3.

Q3: Is SKILL.md > 300 lines?
    → YES: Should extract to references. Penalize D6.
    → NO: TYPE-C is intentional. D6 = N/A (full marks or skip).
```

### D7 — Epistemic Wiring Integrity (10 pts)

> Cross-reference: Aligns with CQS Tầng 2 Physical Structure checks A1-A4
> in `kiem-dinh-chat-luong/references/cqs-validation-engine.md`.

```text
+4  : RESOURCES routing table exists with ≥1 entry pointing to physical reference files
+3  : ALL RESOURCES entries have corresponding physical files on disk (no broken links)
+3  : evals/evals.json exists with ≥2 domain-specific (not generic) test cases

Penalties:
-5  : RESOURCES table present but ≥50% entries point to non-existent files (broken wiring)
-3  : No evals at all (skill behavior is untested and non-deterministic)
-2  : Evals exist but are generic placeholders (per CQS Evals Quality Gate)
```

> In MAS context: Epistemic Wiring ensures knowledge flows correctly from references → SKILL.md → agent.
> A skill with broken wiring will load zero domain knowledge and operate on assumptions.

### D8 — Output Clarity (5 pts)

```text
+3  : User can predict the output format before execution (## OUTPUT FORMAT section exists)
+2  : Has example output or template demonstrating the format

Penalties:
-2  : Output format is vague or missing
-3  : No ## OUTPUT FORMAT section at all
```

---

## Grade Thresholds

| Score | Grade | Label | Recommended Action |
| --- | --- | --- | --- |
| 85–100 | **A** | ✅ Production-ready | Monitor only |
| 70–84 | **B** | 🔶 Good, minor gaps | Quick patch (auto-fixable) |
| 55–69 | **C** | ⚠️ Functional but weak | Repair needed → Route 3 |
| 40–54 | **D** | 🔴 Significant issues | Full rework → Route 3 |
| < 40 | **F** | ❌ Non-functional | Rebuild from scratch → Route 1 |

---

## Batch Scan Aggregation

When auditing multiple skills, compute **Library Health Score**:

```text
LIBRARY_HEALTH = SUM(all_skill_scores) / COUNT(skills)

CRITICAL_COUNT = count(skills with Grade D or F)
HEALTHY_COUNT  = count(skills with Grade A or B)
REPAIR_NEEDED  = count(skills with Grade C)

Library Status:
  HEALTHY   : CRITICAL_COUNT == 0 AND LIBRARY_HEALTH >= 75
  AT_RISK   : CRITICAL_COUNT <= 2 OR LIBRARY_HEALTH 60-74
  DEGRADED  : CRITICAL_COUNT > 2 OR LIBRARY_HEALTH < 60
```
