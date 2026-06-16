# Canonical 4-Tier Skill Specification

> Reference document for the `tao-ky-nang-moi` skill.
> Defines the complete 4-Tier directory structure, evals schema, and migration guide from legacy formats.

---

## 4-Tier Directory Structure

Every production skill MUST have this exact structure:

```text
.agents/skills/[skill-name]/
├── SKILL.md              # Tier 0: Orchestrator (routing logic, < 500 lines)
├── references/            # Tier 1: Domain knowledge (SOPs, matrices, formulas)
│   ├── [topic-1].md
│   └── [topic-2].md
├── assets/                # Tier 2: Output templates & schemas
│   ├── [template-1].md
│   └── [schema-1].yaml
├── evals/                 # Tier 3: Deterministic test cases
│   └── evals.json
└── scripts/               # Tier 4: Helper scripts (optional)
    └── [script].py
```

---

## 💎 The Artisanal Development Protocol

When creating or modifying payload files (`references/` and `assets/`), you MUST operate as an artisanal watchmaker. 

**BANNED BEHAVIORS (Lazy Output):**
- **Batch Scripting:** Using Python generator scripts to mass-produce 5 skeletal files at once.
- **Hollow Skeletons / Dummy Files:** Creating a file that merely fulfills directory structure quan-ly-quy-tac but lacks dense intelligence (e.g. 9-line files). Any file violating the **Data Volume Quotas** below must be instantly flagged as a `VOLUME_VIOLATION`.
- **Surface-Level References:** Writing a reference that is just a bulleted list of generic LLM advice ("It's important to be clear").

**REQUIRED BEHAVIORS (Handcrafted Precision):**
- **Single-File Execution:** Load context, write ONE file using explicit tools like `write_to_file`. Verify it. Then move to the next.
- **Deep Taxonomies:** A reference must contain formulas, scoring metrics, exact thresholds, or explicit classifications (e.g., "The 4-tier Fact-Check Pyramid", "The 4-variable Matrix").
- **Rigid Templates:** An asset must have exact Markdown structural boundaries, data tables, or JSON/YAML schemas that strictly limit the executing agent's hallucination space.

---

## ⚖️ Data Volume Quotas (Length & Density Bounds)

To prevent LLM superficial generation ("Lazy Writing"), every artifact generated during skill creation MUST respect strict quantitative thresholds. 

| Component Tier | Minimum Bound (Floor) | Maximum Bound (Ceiling) | Density Requirement (Pattern Lock) |
|---|---|---|---|
| **`SKILL.md` (Tier 0)** | **100 Lines / ~1,500 Tokens** | **500 Lines / ~8,000 Tokens** | If under min length, the prompt lacks sufficient Edge-Case handling or explicit pushy persona commands. REWORK internally before outputting. |
| **`references/*.md` (Tier 1)** | **500 Words / ~2,500 Tokens** | **2,000 Words / ~10,000 Tokens** | 9-line bulleted lists are strictly ILLEGAL. Must contain ≥ 3 sections: (1) Core Rationale, (2) Execution Bounds (Rules), and (3) Anti-Patterns. |
| **`assets/*.md` (Tier 2)** | **30 Lines / ~500 Tokens** | **300 Lines / ~4,000 Tokens** | Asset cannot be empty prose. Must be explicitly structured (Markdown Tables `\|`, Checkboxes `[ ]`, or specific YAML/JSON data schemas). |
| **`evals/evals.json` (Tier 3)** | **2 Test Cases** | - | Must contain at least 1 `happy_path` and 1 `violation` edge-case. |

*Self-Correction Trigger:* Before terminating the creation of a payload file, count the words/lines. If underneath the Minimum Bound, DO NOT stop. Pause, nghien-cuu-thi-truong deeper into the domain, and explicitly add "Anti-Patterns" or "Granular Use-Cases" to reach the density quota.

---

## SKILL.md Canonical Sections

| # | Section | Required | Purpose |
|---|---|---|---|
| 1 | YAML Front Matter (`---`) | ✅ MUST | `name:` + `description:` (≥10 words, Pushy tone, "Even if..." ending) |
| 2 | `## ROLE` | ✅ MUST | Expert persona title + 1-2 sentence mandate |
| 3 | `## PURPOSE` | ✅ MUST | What goes wrong without this skill |
| 4 | `## ACTIVATION SIGNALS` | Optional | Explicit trigger phrases |
| 5 | `## WHEN TO CLARIFY` | ✅ MUST | Questions to ask before executing |
| 6 | `## PROCESS` | ✅ MUST | Sequential routes with imperative steps |
| 7 | `## OUTPUT FORMAT` | ✅ MUST | Exact format/template of skill outputs |
| 8 | `## RESOURCES` | ✅ MUST | Routing table: `Situation → Load [file]` |
| 9 | `## QA` | ✅ MUST | Self-check checklist (≥3 items) |
| 10 | `## RULES` | ✅ MUST | Hard constraints with NEVER/ALWAYS (≥3 quan-ly-quy-tac) |

---

## evals.json Schema

```json
{
  "skill": "[skill-name]",
  "version": "1.0",
  "test_cases": [
    {
      "id": "TC-01",
      "type": "happy_path",
      "description": "Brief description of what this tests",
      "input": "Description of valid input scenario",
      "expected_output": "Description of expected correct output",
      "pass_criteria": "Measurable criteria for PASS (e.g., 'output contains X', 'file created at Y')"
    },
    {
      "id": "TC-02",
      "type": "violation",
      "description": "Brief description of invalid scenario",
      "input": "Description of invalid/edge-case input",
      "expected_output": "REJECT or specific error message",
      "pass_criteria": "Rejection correctly triggered, error message matches expected"
    }
  ]
}
```

**Minimum Requirements**:
- ≥ 1 `happy_path` test case
- ≥ 1 `violation` test case
- Each test must have ALL 5 fields (id, type, input, expected_output, pass_criteria)

---

## Pushy Persona Rules

### DO (Imperative Language):
- "You are a Senior [Domain] Auditor"
- "REJECT if input lacks..."
- "Execute X, then Y"
- "Load `references/Z.md` and apply Rule 3"
- "CẤM: Không chấp nhận output không có scoring matrix"

### DON'T (Passive Language):
- ~~"You should try to..."~~
- ~~"Consider doing..."~~
- ~~"It might be helpful to..."~~
- ~~"The agent could potentially..."~~

---

## Migration Guide: Legacy → 4-Tier

### Scenario 1: Flat `skill-name.md` (No SKILL.md)

1. Rename `skill-name.md` → `SKILL.md` (or create new SKILL.md from content).
2. Extract domain knowledge (>4 lines) → `references/[topic].md`.
3. Extract output templates → `assets/[template].md`.
4. Create `evals/evals.json` with ≥2 test cases.
5. Create empty `scripts/` directory.
6. Delete the legacy `skill-name.md` after migration.
7. Run `grep_search` for old filename across workflows/agents → update references.

### Scenario 2: SKILL.md exists but missing subdirectories

1. Create missing directories: `references/`, `assets/`, `evals/`, `scripts/`.
2. Scan SKILL.md for embedded domain knowledge (>4 lines inline).
3. Extract to appropriate subdirectory.
4. Add RESOURCES routing table pointing to extracted files.
5. Generate `evals/evals.json`.

### Scenario 3: SKILL.md exists in legacy format (Description + Instructions)

1. Rewrite to Canonical format using the 10-section table above.
2. Map `## Description` → `## ROLE` + `## PURPOSE`.
3. Map `## Instructions` → `## PROCESS` (split into routes if multi-function).
4. Add missing sections: `## WHEN TO CLARIFY`, `## RESOURCES`, `## QA`, `## RULES`.
5. Apply Pushy Persona quan-ly-quy-tac to all content.
