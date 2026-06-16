# Skill Audit & Optimize Report Templates

> Asset file for the `tao-ky-nang-moi` skill.
> Used by Route 2 (AUDIT) for output formatting and Route 3 (OPTIMIZE) for delta reporting.

---

## Template 1: Batch Scorecard (Route 2 Output)

```markdown
# SKILL LIBRARY AUDIT REPORT — [WORKSPACE_NAME] — [DATE]

## Executive Summary

- **Skills Scanned:** [N]
- **Library Health Score:** [AVG]/100
- **Library Status:** [HEALTHY / AT_RISK / DEGRADED]
- **Critical Issues:** [COUNT]
- **Requested by:** [WORKFLOW_NAME] (e.g., `/audit-workspace Phase 2d`)

## Scorecard

| # | Skill Name | Type | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | Total | Grade | Top Issue |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [name] | [A-E] | [/20] | [/20] | [/15] | [/10] | [/10] | [/10] | [/10] | [/5] | [/100] | [A-F] | [brief] |

## Priority Queue

### 🔴 CRITICAL (Grade D/F — Fix immediately)
- [skill-name]: [Score] — [Top failing dimensions]

### ⚠️ REPAIR QUEUE (Grade C — Fix this session)
- [skill-name]: [Issue summary]

### 🔶 ENRICH QUEUE (Missing assets despite need)
- [skill-name]: [What's missing]

### ✅ MONITOR ONLY (Grade A/B)
- [skill-name]: [Minor note if any]

## Dimension Distribution

| Dimension | Avg Score | Weakest Skill | Notes |
|---|---|---|---|
| D1 Frontmatter | [avg]/20 | [skill] | |
| D2 Trigger Power | [avg]/20 | [skill] | |
| D3 Body Structure | [avg]/15 | [skill] | |
| D4 Progressive Disclosure | [avg]/10 | [skill] | |
| D5 Token Budget | [avg]/10 | [skill] | |
| D6 Reference Assets | [avg]/10 | [skill] | |
| D7 Platform Compat. | [avg]/10 | [skill] | |
| D8 Output Clarity | [avg]/5 | [skill] | |
```

---

## Template 2: Single Skill Deep Audit (Route 2 — Detail Mode)

```markdown
# SKILL AUDIT — [skill-name]

## Classification
- **Type:** [A-E]
- **Total Lines:** [N]
- **Has references/:** [Yes (X files) / No]
- **Has assets/:** [Yes (X files) / No]
- **Has evals/:** [Yes / No]
- **Has scripts/:** [Yes / No]

## Scoring Breakdown

| Dim | Dimension | Score | Max | Evidence |
|---|---|---|---|---|
| D1 | Frontmatter Quality | [X] | 20 | [brief finding] |
| D2 | Trigger Power | [X] | 20 | [brief finding] |
| D3 | Body Structure | [X] | 15 | [brief finding] |
| D4 | Progressive Disclosure | [X] | 10 | [brief finding] |
| D5 | Token Budget | [X] | 10 | [brief finding] |
| D6 | Reference Assets | [X] | 10 | [brief finding] |
| D7 | Platform Compat. | [X] | 10 | [brief finding] |
| D8 | Output Clarity | [X] | 5 | [brief finding] |
| | **TOTAL** | **[X]** | **100** | **Grade: [A-F]** |

## Findings

### 🔴 Critical
- [Finding with evidence]

### 🟡 Warning
- [Finding with evidence]

### ✅ Strengths
- [What the skill does well]

## Recommended Actions
1. [Action] — Protocol [R1/R2/R3/R4/E1-E5]
2. [Action] — Protocol [ID]
```

---

## Template 3: Delta Report (Route 3 Output — After Repair)

```markdown
# SKILL REPAIR REPORT — [skill-name]

## Before / After

| Metric | Before | After | Delta |
|---|---|---|---|
| **Total Score** | [X]/100 ([Grade]) | [Y]/100 ([Grade]) | [+Z] |
| **D1 Frontmatter** | [X]/20 | [Y]/20 | [+Z] |
| **D2 Trigger Power** | [X]/20 | [Y]/20 | [+Z] |
| **D3 Body Structure** | [X]/15 | [Y]/15 | [+Z] |
| **D4 Disclosure** | [X]/10 | [Y]/10 | [+Z] |
| **D5 Budget** | [X]/10 | [Y]/10 | [+Z] |
| **D6 References** | [X]/10 | [Y]/10 | [+Z] |
| **D7 Platform** | [X]/10 | [Y]/10 | [+Z] |
| **D8 Output** | [X]/5 | [Y]/5 | [+Z] |

## Changes Made
- ✅ [Protocol ID]: [What was done]
- ✅ [Protocol ID]: [What was done]

## Files Created/Modified
- [MODIFIED] `SKILL.md` — [summary]
- [NEW] `references/[file].md` — [summary]
- [NEW] `assets/[file].md` — [summary]

## Remaining TODOs (Human Action Required)
- ⚠️ [What AI could not resolve and why]
```
