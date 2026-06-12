---
name: spatial-transcriptomics
description: >
  Orchestrator skill for spatial transcriptomics analysis. Routes to one of three personality
  modes (aristotle/plato/socrates) based on user intent. Covers platforms: Visium, Xenium,
  MERFISH, Slide-seq, Stereo-seq, CosMx, SpatialDB, Seq-Scope, DBiT-seq, STARmap. Frameworks:
  Scanpy, Squidpy, Giotto, Seurat, SpatialDE, BayesSpace, SPARK-X, SpaGCN, Cell2location,
  RCTD, Tangram. Trigger keywords: spatial transcriptomics, Visium, Xenium, MERFISH, Slide-seq,
  spatial gene expression, spatial omics, single-cell spatial, spatial analysis, spot deconvolution,
  spatial clustering, spatially variable genes, 空间转录组, 空间组学, 空间基因表达, 空间分析,
  空间聚类, 空间差异表达, 10x Visium, Stereo-seq, CosMx, seqFISH, FISSEQ.
---

# Spatial Transcriptomics — Mode Router

## Decision Tree

Route user requests to one of three personality modes. Detect intent from keywords in
the user's natural language question, then load the corresponding mode file.

```
User Question
    │
    ├── Contains Socrates markers?
    │   "全新" "颠覆" "换思路" "unconventional" "breakthrough"
    │   "rethink" "from scratch" "无预设" "paradigm shift"
    │   "abandon standard" "completely new direction"
    │       → YES → Load modes/socrates.md
    │
    ├── Contains Plato markers?
    │   "新方法" "前沿" "cutting-edge" "recent" "improved"
    │   "最新" "更好的方法" "state of the art" "alternative"
    │   "compare methods" "beyond standard" "最新进展"
    │       → YES → Load modes/plato.md
    │
    ├── Contains Aristotle markers?
    │   "标准流程" "常规分析" "standard pipeline" "routine analysis"
    │   "best practice" "tried and tested" "gold standard"
    │   "recommended workflow" "standard preprocessing" "QC"
    │       → YES → Load modes/aristotle.md
    │
    └── No clear markers (DEFAULT)
            → Load modes/aristotle.md (safety-first)
```

**Ambiguity resolution**: When markers from multiple modes are present, use this priority:
`socrates > plato > aristotle`. Novelty-seeking overrides safety defaults. If only
"novel" appears without stronger markers, route to plato mode.

## Mode Overview

### Aristotle (`modes/aristotle.md`)
Standard, reproducible spatial transcriptomics pipelines using well-established tools
(Scanpy, Squidpy, Seurat). Follows community-vetted best practices, built-in QC
thresholds, and published workflows. Aristotle was the empiricist who classified all of
nature — this mode inherits his systematic rigor. Appropriate for routine analysis,
benchmarking, and when reproducibility is paramount. No experimental methods are recommended.

### Plato (`modes/plato.md`)
Standard pipelines augmented with systematic literature search via BioMCP. Searches
PubMed for recent methods (last 2 years), compares alternatives, and recommends
improvements over the baseline pipeline. Plato was the dialectician who explored every
possibility — this mode inherits his breadth. Useful when the user wants to know about
newer approaches without abandoning the standard framework entirely.

### Socrates (`modes/socrates.md`)
Question-driven reverse design. Starts from the user's biological question, then
designs a custom analysis strategy from scratch — tool selection, parameter choices,
and interpretation framework are all derived from the question rather than from a
predefined pipeline. Socrates was the gadfly who questioned everything until truth
emerged — this mode inherits his relentless curiosity. No preset assumptions about
which tools should be used.

## BioMCP Integration

This skill uses the `biomcp_biomcp` MCP tool for biomedical queries. All modes may
invoke it, but Plato and Socrates modes rely on it heavily for literature-backed
method discovery.

| Command | Purpose | Used By |
|---|---|---|
| `search article -c "spatial transcriptomics" --date-from 2023` | Find recent methods | plato, socrates |
| `search article -c "<gene> spatial transcriptomics"` | Gene-specific literature | all modes |
| `get gene <symbol>` | Gene annotation, known roles | all modes |
| `search variant "<variant>" --review-status` | Variant annotation in spatial context | all modes |
| `discover "<biological question>"` | Concept resolution for question design | socrates |
| `enrich <gene1,gene2,...>` | Gene-set enrichment for spatial clusters | all modes |

**Usage rule**: Always trigger BioMCP when the user asks about a specific gene, pathway,
or disease context. For method discovery in Plato/Socrates modes, at least one
BioMCP literature search is mandatory before recommending a pipeline.

## Self-Evolution

This skill writes to `~/.spatial-transcriptomics-memory/` for persistent learning
across sessions:

- **Findings log**: `~/.spatial-transcriptomics-memory/findings.jsonl` — append
  insights from each analysis session (methods that worked, edge cases, platform-specific
  quirks).
- **Method catalog**: `reference/methods-catalog.md` — curated list of spatial methods
  with platform compatibility, performance notes, and citation anchors.
- **Personality memory**: Each mode file tracks its own session history in
  `~/.spatial-transcriptomics-memory/<mode>-sessions.jsonl` (aristotle/plato/socrates) for context continuity.

Before starting any analysis, the skill should briefly scan the findings log for
relevant past insights. After completing analysis, new findings are appended.

## Code Templates

Reusable analysis templates are stored in `templates/`. These are Python scripts
or Jupyter notebook stubs that each mode can customize:

| Template | File | Description |
|---|---|---|
| QC & Preprocessing | `templates/qc-template.py` | Scanpy/Squidpy-based QC with configurable thresholds |
| Spatial Clustering | `templates/clustering-template.py` | Leiden/Louvain with spatial neighborhood graph |
| SV Gene Detection | `templates/svg-template.py` | SpatialDE, SPARK-X, Moran's I wrappers |
| Deconvolution | `templates/deconv-template.py` | Cell2location, RCTD, Tangram spot deconvolution |
| Niche Analysis | `templates/niche-template.py` | Spatial neighborhood composition analysis |
| Visualization | `templates/viz-template.py` | Publication-ready spatial plots (UMAP, spatial heatmaps) |

Each template includes placeholder comments (`# TODO: CONFIGURE`) where mode-specific
decisions are injected. Aristotle mode fills these with default values; Plato
and Socrates modes replace them with literature-backed or question-driven choices.

## File Map

```
spatial-transcriptomics/
├── SKILL.md                  ← THIS FILE (router)
├── modes/
│   ├── aristotle.md          ← Standard pipeline mode
│   ├── plato.md              ← Literature-augmented mode
│   └── socrates.md           ← Question-driven reverse design mode
├── reference/
│   └── methods-catalog.md    ← Curated spatial methods reference
├── templates/
│   ├── qc-template.py
│   ├── clustering-template.py
│   ├── svg-template.py
│   ├── deconv-template.py
│   ├── niche-template.py
│   └── viz-template.py
└── memory/                   ← Session-level scratch (not persisted)
```
