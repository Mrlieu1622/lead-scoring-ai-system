# Repair Protocols & Enrichment Engine

> Reference document for the `tao-ky-nang-moi` skill, Route 3 (OPTIMIZE).
> Contains deterministic fix recipes for all common skill quality failures.
> Agent MUST match failure dimension to protocol before executing repair.

---

## Protocol Index

| ID | Trigger Condition | Target Dimension | Severity |
| --- | --- | --- | --- |
| R1 | Description empty, weak, or truncated | D1 + D2 | High |
| R2 | Body unstructured, empty, or bullet-dump | D3 | High |
| R3 | SKILL.md > 500 lines (token bloat) | D5 | Medium |
| R4 | Broken reference links | D6 | High |
| E1 | Body empty (< 20 lines) — reconstruct | D3 | Critical |
| E2 | SKILL.md references files that don't exist | D6 | High |
| E3 | Reference files exist but are thin (< 20 lines) | D6 | Medium |
| E4 | Skill needs scripts/ but doesn't have any | D7 | Low |
| E5 | Skill needs evals but evals/ is missing or empty | QA | Medium |

---

## Repair Protocols

### R1: Description Repair (D1 + D2 Failures)

**Trigger:** D1 score < 10 OR D2 score < 10.

**Protocol:**

1. Read entire SKILL.md body to understand what the skill does.
2. Extract 4 elements:
   - **(a)** Domain — what field/topic does this skill operate in?
   - **(b)** User verbs — what would a user say to trigger this?
   - **(c)** Output type — what does the skill produce?
   - **(d)** Exclusions — when should this skill NOT trigger?
3. Rewrite description using the Pushy Template:

```yaml
description: >
  [One-line tagline: what the skill does, in target language].
  Kích hoạt khi người dùng nói [USER_VERB_1], [USER_VERB_2], [USER_VERB_3],
  [USER_VERB_4], [USER_VERB_5]. Cũng kích hoạt khi [IMPLICIT_CONTEXT].
  Also triggers when user says "[EN_PHRASE_1]", "[EN_PHRASE_2]".
  Even if the user doesn't use the word "[SKILL_NAME]", trigger when
  [SCENARIO_DESCRIPTION].
```

4. **Pushy Self-Test:** Re-read the description and ask: "If a user only reads this, do they know EXACTLY when to trigger?" If NO → rewrite again.

### R2: Body Structure Repair (D3 Failures)

**Trigger:** D3 score < 8.

**Protocol:**

1. If body is empty/skeleton → defer to **E1: Body Reconstruction**.
2. If body is a flat bullet dump → restructure to Canonical format:

```markdown
## ROLE           ← Who is this skill? Expert title + mandate
## PURPOSE        ← What goes wrong without this skill?
## WHEN TO CLARIFY ← Questions before executing
## PROCESS        ← Step-by-step workflow with decision points
## OUTPUT FORMAT  ← Exact output structure
## RESOURCES      ← Routing table: condition → file
## QA             ← Self-check checklist (≥3 items)
## RULES          ← Hard constraints (≥3 quan-ly-quy-tac, NEVER/ALWAYS)
```

3. Add at least 1 concrete example (input → expected output).
4. Add at least 1 decision table if skill has branching logic.
5. Ensure all instructions use imperative form ("Do X", not "You should try X").

### R3: Line Budget Repair (D5 Failures)

**Trigger:** SKILL.md > 500 lines.

**Protocol:**

1. Identify extractable content blocks (ranked by size):
   - Long examples (> 10 lines) → `references/examples.md`
   - Lookup tables / matrices → `references/[matrix-name].md`
   - Framework descriptions → `references/[framework].md`
   - Output templates → `assets/[template-name].md`
2. For each extracted block:
   a. Move content to target file.
   b. Replace original content in SKILL.md with a RESOURCES table entry:
      `| Need [context] | references/[filename].md |`
3. Verify: SKILL.md after extraction < 500 lines.
4. Verify: No duplicate content between SKILL.md and extracted files.

### R4: Broken Link Repair (D6 Failures)

**Trigger:** Referenced file in RESOURCES table does not exist on disk.

**Protocol:**

1. List all file references in SKILL.md (RESOURCES table + inline `references/` mentions).
2. For each reference, check if file exists.
3. If file missing:
   - If content can be reconstructed from SKILL.md context → route to **E2**.
   - If content cannot be inferred → comment out the broken reference, add TODO marker, flag in report.
4. Run grep across SKILL.md for any `references/` or `assets/` paths not in RESOURCES table → flag as undeclared dependencies.

---

## Enrichment Engine (5 Scenarios)

### Enrichment Threshold Decision

Before enriching a TYPE-C skill, run this decision tree:

```text
Q1: Does SKILL.md mention "references/" or contain a RESOURCES table?
    → YES: Clearly needs references. Proceed to enrichment.
    → NO: Go to Q2.

Q2: Does skill have complex workflow (> 3 phases, > 5 decision points)?
    → YES: References would help. Ask user for confirmation.
    → NO: Go to Q3.

Q3: Is SKILL.md > 300 lines?
    → YES: Should extract to references. Proceed to enrichment.
    → NO: TYPE-C is intentional. SKIP enrichment. Log decision in report.
```

### E1: Body Reconstruction (Empty → Minimal Viable Skill)

**Condition:** SKILL.md has < 20 lines of body content (frontmatter-only or skeleton).

**Action:**
1. Parse description to infer: domain, workflow type, output format.
2. Draft a minimal viable body:
   - `## ROLE` — infer expert persona from description domain
   - `## PURPOSE` — state what breaks without this skill
   - `## PROCESS` — draft 3-5 step workflow from description verbs
   - `## OUTPUT FORMAT` — infer from description output keywords
   - `## QA` — generate 3 self-check items
   - `## RULES` — generate 3 hard constraints
3. Present draft to user: "Body drafted from description. Review before I generate references."
4. DO NOT auto-commit. Wait for user approval on E1 output.

### E2: Missing Reference Generation

**Condition:** SKILL.md references files that don't exist on disk.

**Action per missing file type:**

| File Type | Artisanal Generation Strategy (No Batching!) |
| --- | --- |
| `framework.md` | Extract framework name from SKILL.md. Manually write a deep taxonomy, formulas, or explicit quan-ly-quy-tac using `write_to_file`. |
| `templates/*.md` | Handcraft strict markdown structures, data tables, or JSON/YAML schemas. Provide rigid bounds. |
| `examples/*.md` | Write 2-3 worked input→output examples based on real-world constraints. |
| `checklist.md` | Craft a structured numbered checklist with explicit PASS/FAIL logic. |
| `schemas.md` | Manually define JSON/YAML schemas. |
| `vietnamese-context.md` | Write deep cultural/regulatory context notes using explicit Vietnamese terminology. |

**BANNED:** You may NOT use a python loop/script to iterate over an array of missing files and create them automatically. You must process one file at a time, deeply.

**If insufficient context to generate meaningful content:** Create stub file with explicit TODO:

```markdown
# [Filename] — STUB (Requires Human Input)

> ⚠️ Auto-generated stub by tao-ky-nang-moi Route 3.
> TODO: [SPECIFIC_CONTENT_NEEDED — be precise about what's missing]

## Placeholder Sections
[List sections needed based on SKILL.md context]
```

### E3: Thin Reference Expansion

**Condition:** Reference file exists but has < 20 lines, only section headers, or contains generic boilerplate.

**Action (Artisanal Enhancement):**
1. Read the stub/thin file to understand the intended scope.
2. Read SKILL.md to understand the exact constraint or mechanism this reference must enforce.
3. Handcraft substantive content using domain knowledge: replace bullet points with decision tables, formulas, or strict quan-ly-quy-tac (e.g., "The Triangulation Rule: require 3 sources").
4. Do NOT use batch automated scripts. Use direct file I/O to craft the file.
5. Mark output as AI-generated, flag for human verification.

### E4: Script Generation

**Condition:** SKILL.md body mentions "chạy script", "execute", "automate", or has deterministic verification steps.

**Action:**
1. Identify which task should be scripted (validation, formatting, data processing).
2. Choose language: Python for data tasks, Bash for file operations.
3. Generate script stub with:
   - Docstring explaining purpose and I/O interface
   - Argument parsing
   - Core logic skeleton with TODOs for complex domain logic
   - Error handling
4. Save to `scripts/[task-name].py` and add RESOURCES pointer in SKILL.md.

### E5: Evals Generation

**Condition:** `evals/evals.json` is missing or empty or contains only generic placeholders.

**Action:**
1. Extract 5-10 trigger phrases from description.
2. Read `## PROCESS` to identify primary functions and edge cases.
3. Generate eval set:

```json
{
  "skill": "[skill-name]",
  "version": "1.0",
  "test_cases": [
    {
      "id": "TC-01",
      "type": "happy_path",
      "description": "[Domain-specific scenario description]",
      "input": "[Realistic user prompt that should trigger this skill]",
      "expected_output": "[Specific expected output format/content]",
      "pass_criteria": "[Measurable criteria]"
    },
    {
      "id": "TC-02",
      "type": "violation",
      "description": "[Edge case or rejection scenario]",
      "input": "[Input that should be rejected or handled differently]",
      "expected_output": "REJECT with specific error message",
      "pass_criteria": "[Rejection correctly triggered]"
    }
  ]
}
```

4. Save to `evals/evals.json`.
5. Ensure NO generic placeholders like "Execute skill with valid parameters".

---

## Batch Processing Priority Matrix

When optimizing ≥ 5 skills simultaneously, use this priority grid:

```text
                HIGH Impact           LOW Impact
              (D1, D2, D3 fails)   (D4, D5, D7, D8 fails)
  ┌─────────────────────────────┬──────────────────────────┐
  │      DO FIRST               │      BATCH LATER         │
  │  Description rewrite (R1)   │  Format cleanup (R3)     │
EASY│  Add missing RESOURCES     │  Add TOC to long files   │
FIX │  Fix broken links (R4)     │  Minor wording tweaks    │
  ├─────────────────────────────┼──────────────────────────┤
  │      PLAN + CONFIRM         │      DEFER               │
HARD│  Full body restructure(R2) │  Optional scripts (E4)   │
FIX │  Full rebuild (E1)         │  Optional enrichment     │
  │  Content extraction (R3)    │  Platform compatibility  │
  └─────────────────────────────┴──────────────────────────┘
```

**Critical Rule:** NEVER auto-execute a full rebuild (E1) without user confirmation. Present the draft and wait for approval.
