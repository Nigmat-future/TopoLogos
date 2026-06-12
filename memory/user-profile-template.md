# Self-Evolution Memory Mechanism

## Directory Structure

`~/.spatial-transcriptomics-memory/`

```
~/.spatial-transcriptomics-memory/
├── user-profile.md          # YAML frontmatter + markdown body
├── findings.jsonl           # Append-only JSON Lines log
├── sessions/
│   ├── aristotle/            # One file per session: YYYY-MM-DD-HHMMSS.md
│   ├── plato/
│   └── socrates/
└── methods-catalog.md         # Auto-updated method registry
```

## User Profile Format (`user-profile.md`)

```yaml
---
preferred_platform: "scanpy"        # scanpy | seurat | squidpy | spatialde2
frequent_genes:
  - "EPCAM"
  - "CD68"
  - "COL1A1"
preferred_mode: "plato"              # aristotle | plato | socrates
analysis_depth: "standard"          # quick | standard | deep
past_decisions:
  - timestamp: "2026-06-12T10:30:00Z"
    context: "breast cancer ST"
    choice: "used SpatialDE2 over Moran's I"
    outcome: "better spatial pattern detection"
---

# Notes (freeform markdown below the frontmatter)
```

## Findings Log Format (`findings.jsonl`)

Append-only. One JSON object per line. Schema:

```json
{"timestamp": "2026-06-12T14:30:00Z", "mode": "plato", "gene": "EPCAM", "analysis_type": "spatial_variation", "method_used": "SpatialDE2", "outcome": "success", "lesson": "SpatialDE2 outperformed Moran's I for gradient detection in this tissue type"}
```

Fields:
- `timestamp`: ISO 8601 UTC
- `mode`: aristotle | plato | socrates
- `gene`: gene symbol or "multiple" or "none"
- `analysis_type`: e.g. "clustering", "deconvolution", "niche_analysis", "svg_detection"
- `method_used`: specific method or tool name
- `outcome`: "success" | "partial" | "failure" | "unexpected"
- `lesson`: free-text insight for future sessions

## Reflection Cycle

After completing any analysis:

1. Evaluate outcome against user expectation
2. If result doesn't match expectation → record lesson in `findings.jsonl`
3. Suggest alternative method for next time (append to `past_decisions` in profile)
4. If method succeeded unexpectedly well → add to `methods-catalog.md`

## Mode-Specific Session Logs

Each mode writes to its own subdirectory. File naming: `YYYY-MM-DD-HHMMSS.md`

Content template:
```markdown
# Session: 2026-06-12-143000
## Mode: plato
## Genes: EPCAM, CD68
## Methods Used: SpatialDE2, leiden clustering
## Outcome: partial
## Key Lesson: SpatialDE2 parameters needed tuning for this tissue density
```

## Data Extraction Trigger Rules

Write to memory when:
- Every analysis session completes (outcome + lesson)
- User changes method or overrides suggestion
- User expresses dissatisfaction ("that didn't work", "try something else")
- Method produces unexpected result (good or bad)
- User confirms a method worked well ("this is great")

## Reading from Memory

Before starting any new analysis:

1. Check if `~/.spatial-transcriptomics-memory/` exists. If not, initialize it.
2. Read `user-profile.md` for preferences and past decisions
3. Scan `findings.jsonl` for entries matching current gene / analysis type / mode
4. Load relevant `methods-catalog.md` entries
5. Incorporate past lessons into method selection and parameter defaults

## Initialization Procedure

If `~/.spatial-transcriptomics-memory/` does not exist:

1. Create the directory and all subdirectories
2. Write `user-profile.md` with empty YAML frontmatter and placeholder body
3. Create empty `findings.jsonl`
4. Create empty `methods-catalog.md` with header template
5. Create `sessions/` subdirectories for all three modes

## Methods Catalog (`methods-catalog.md`)

Auto-updated registry. Format:

```markdown
# Methods Catalog

## spatial_variation
- **SpatialDE2**: Good for gradient detection. Tissue density sensitive.
- **Moran's I**: Fast. Good for binary spatial patterns.

## clustering
- **Leiden**: Default. Resolution parameter 0.4-1.2 typical range.
```

Updated when reflection cycle identifies a method success or failure.
