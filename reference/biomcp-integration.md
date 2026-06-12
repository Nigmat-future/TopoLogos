# BioMCP Integration Guide for Spatial Transcriptomics

This reference documents how the spatial transcriptomics skill uses BioMCP (`biomcp_biomcp`) across its three analysis modes. BioMCP provides read-only access to 15 biomedical sources including PubMed, ClinicalTrials.gov, ClinVar, gnomAD, Reactome, KEGG, and UniProt.

## Relevant BioMCP Commands

| Command | Example Syntax | Spatial Analysis Step | Mode Usage |
|---------|---------------|----------------------|------------|
| `search article` | `search article -c "spatial transcriptomics MERFISH"` | Literature review, method validation | All modes |
| `get gene` | `get gene BRAF` | Marker gene annotation, pathway mapping | All modes |
| `search variant` | `search variant "BRAF V600E"` | Genotype-phenotype linking | Conservative, Innovative |
| `discover` | `discover "tumor microenvironment"` | Concept exploration, hypothesis generation | Innovative, Radical |
| `enrich` | `enrich BRAF,CD68,COL1A1` | Pathway enrichment for gene clusters | Innovative, Radical |
| `search trial` | `search trial -c melanoma` | Clinical context for disease-focused studies | Conservative |
| `gene pathways` | `gene pathways BRAF` | Pathway context for spatial niches | Innovative, Radical |
| `gene trials` | `gene trials BRAF` | Clinical relevance of markers | Conservative |
| `gene drugs` | `gene drugs BRAF` | Therapeutic context for spatial findings | Conservative |

## Query Patterns

These are typical user queries and the corresponding BioMCP calls:

1. **"What is the function of gene X in the tumor microenvironment?"**
   - `get gene X` → `gene pathways X` → `search article -c "X spatial transcriptomics"`

2. **"Are there known variants associated with this spatial pattern?"**
   - `search variant "X Y"` (if specific variant known) or `discover "spatial pattern disease"`

3. **"What pathways are enriched in this cell cluster?"**
   - `enrich GENE1,GENE2,...` (cluster marker genes)

4. **"Has this method been used in breast cancer?"**
   - `search article -c "spatial transcriptomics breast cancer" --date-from 2023`

5. **"What clinical trials relate to these markers?"**
   - `gene trials MARKER1` → `search trial -c "disease marker"`

6. **"Discover novel cell-type markers for this niche"**
   - `discover "cell type tissue niche"` → `search article -c "novel marker spatial"`

## Mode-Specific Behavior

### Conservative Mode
- **Purpose**: Validate known biology, avoid speculative claims
- **BioMCP usage**:
  - `get gene` for canonical marker verification
  - `search article` with broad terms for background
  - `gene trials` and `gene drugs` for clinical anchoring
- **Constraint**: Only cite established pathways and well-documented markers

### Innovative Mode
- **Purpose**: Discover recent methods and contextualize findings
- **BioMCP usage**:
  - `search article --date-from 2024` for latest methods
  - `enrich` for pathway context on novel clusters
  - `gene pathways` to link spatial niches to biology
  - `discover` for emerging concept mapping (limited scope)
- **Constraint**: Cross-reference novel findings with at least one database source

### Radical Mode
- **Purpose**: Generate hypotheses and explore unconventional connections
- **BioMCP usage**:
  - `discover` freely for concept mapping across domains
  - `search article` across distant fields (e.g., neuroscience + cancer)
  - `enrich` on unexpected gene sets to find hidden pathways
  - `get gene` on non-obvious candidates
- **Constraint**: Flag all speculative claims; require manual review before publication

## Search Strategy

Effective BioMCP queries for spatial transcriptomics follow these principles:

- **Be specific**: Include technology (MERFISH, Visium, Xenium) and tissue type
- **Use date filters**: `--date-from 2023` for methods, omit for biology
- **Chain commands**: Start with `discover` or `get gene`, then `search article` for context
- **Batch where possible**: `enrich` accepts multiple genes; prefer it over repeated `get gene`
- **Interpret carefully**: BioMCP is read-only and returns source-grounded data; always map results back to spatial coordinates or clusters

## Notes

- BioMCP commands are natural-language-style but follow strict grammar (see tool schema)
- All BioMCP calls are read-only; no data is written to external databases
- When BioMCP returns zero results, retry with synonyms or broader terms
- For variant queries, use HGVS or common names (e.g., `"BRAF V600E"`)
