# Gap Brief Schema — Handoff Contract

> Asset file for the `tao-ky-nang-moi` skill (Route 3, Step 5: Enrichment Gate).
> Defines the JSON contract used to delegate knowledge nghien-cuu-thi-truong to the `knowledge-forge` skill.
> Generate one Gap Brief per missing reference asset.

---

## JSON Schema

```json
{
  "skill_name": "string — exact folder name in .agents/skills/",
  "gap_id": "G001 — sequential ID per audit session",
  "gap_type": "framework | example | schema | process | context | tool | checklist",
  "missing_asset_path": "references/[filename].md — where the generated file should go",
  "domain": "string — specific domain description (e.g., 'Vietnamese SME GenAI adoption')",
  "knowledge_needed": "string — precise description of what knowledge is missing",
  "depth": "overview | standard | deep",
  "target_audience": "Claude operating as [ROLE from skill's ## ROLE section]",
  "language": "vi | en | bilingual",
  "output_format": "methodology | example | process | context | checklist | framework-breakdown",
  "constraints": ["array of strings — e.g., 'no proprietary content', 'focus on VN context'"],
  "related_assets": ["array — existing reference files for context"],
  "source_hints": ["array — suggested sources or keywords, optional"]
}
```

## Example Gap Brief

```json
{
  "skill_name": "clo-writer",
  "gap_id": "G001",
  "gap_type": "framework",
  "missing_asset_path": "references/bloom-taxonomy-revised.md",
  "domain": "Higher education curriculum design",
  "knowledge_needed": "Bloom's Revised Taxonomy (Anderson & Krathwohl 2001) — 6 cognitive levels with action verbs, application protocol for writing Course Learning Outcomes",
  "depth": "standard",
  "target_audience": "Claude operating as Curriculum Design Specialist",
  "language": "bilingual",
  "output_format": "methodology",
  "constraints": ["Focus on Vietnamese higher education context", "Include action verb lists per level"],
  "related_assets": ["references/clo-writing-guide.md"],
  "source_hints": ["Anderson Krathwohl 2001", "AUN-QA guidelines"]
}
```

## Usage in tao-ky-nang-moi Route 3

```text
Step 5 (Enrichment Gate):
  1. For each E2/E3 finding → generate Gap Brief JSON
  2. Present to user: "Cần nghien-cuu-thi-truong [N] reference files. Chuyển sang knowledge-forge?"
  3. If approved → invoke knowledge-forge with Gap Brief(s)
  4. Receive generated files → integrate into skill directory
  5. Update RESOURCES table in SKILL.md → add pointers to new files
```
