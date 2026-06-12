# Spatial Transcriptomics: Analysis Decision Tree

## Quick Reference

| Platform | Resolution | Typical Genes | Best For | Limitations |
|----------|-----------|---------------|----------|-------------|
| 10x Visium | ~55um spots | ~20K (whole transcriptome) | Tissue architecture, broad patterns | Spots mix multiple cells; no single-cell resolution |
| Xenium | Subcellular | ~300-5K (targeted) | Cell typing, niche mapping in known systems | Gene panel limits discovery; tissue prep critical |
| MERFISH | Subcellular | ~100-1K (targeted) | Validation, spatial mapping with morphology | Lower throughput; complex image analysis |
| Slide-seq | ~10um spots | ~20K (whole transcriptome) | Fine-grained domains, near-single-cell | Higher noise than Visium; newer ecosystem |

## Decision Tree

```
START: What resolution is your data?
|
|---> Spot-based (Visium, Slide-seq)
|     |
|     |---> Cell type identification?
|     |     |---> Deconvolution: SPOTlight, RCTD, Cell2location
|     |           (needs single-cell reference; Cell2location is Bayesian, slower)
|     |
|     |---> Spatial domain detection?
|     |     |---> Graph-based: Squidpy (leiden on spatial graph)
|     |     |---> Deep: STAGATE (GPU recommended), SpaGCN
|     |
|     |---> Cell-cell communication?
|     |     |---> Niche-based: CellPhoneDB + Squidpy spatial neighbors
|     |     |---> Deconvolve first, then run LIANA or CellChat
|     |
|     |---> Differential expression?
|     |     |---> Spot-level: MAST, edgeR with spatial covariates
|     |     |---> Domain-level: Aggregate spots, then standard DE
|     |
|     |---> Trajectory inference?
|     |     |---> Map to scRNA-seq reference: scArches, Tangram
|     |     |---> Spatial-aware: SPATA2 (R; note R dependency)
|     |
|     |---> Niche analysis?
|     |     |---> Squidpy spatial statistics (Ripley, co-occurrence)
|     |     |---> MISTy for multi-view spatial interactions
|     |
|---> Single-cell resolution (Xenium, MERFISH)
      |
      |---> Cell type identification?
      |     |---> Direct clustering: Scanpy/Leiden (no deconvolution needed)
      |     |---> Transfer labels: scArches, scANVI (if reference exists)
      |
      |---> Spatial domain detection?
      |     |---> Cell-type composition: Squidpy, STAGATE
      |     |---> Morphology-aware: Baysor (MERFISH; uses cell shape)
      |
      |---> Cell-cell communication?
      |     |---> Direct neighbor methods: CellPhoneDB, LIANA
      |     |---> Distance-based: CellChat with spatial weights
      |
      |---> Differential expression?
      |     |---> Standard single-cell: Scanpy rank_genes_groups, MAST
      |     |---> Spatially-aware: SpatialDE2 (detects spatially variable genes)
      |
      |---> Trajectory inference?
      |     |---> Standard: scVelo, Palantir, Monocle3 (R; note R dependency)
      |     |---> Spatial-aware: SPATA2, stLearn (GPU recommended)
      |
      |---> Niche analysis?
      |     |---> Cell-type co-occurrence: Squidpy, custom radius analysis
      |     |---> Functional niches: MISTy, NCEM (deep learning, GPU)
```

## Platform-Specific Method Recommendations

### 10x Visium
- **Best workflow**: QC -> normalization -> H&E integration -> Squidpy spatial graph -> deconvolution -> niche analysis
- **Key packages**: Scanpy, Squidpy, scVI-tools (for deconvolution)

### Xenium
- **Best workflow**: Cell segmentation QC -> clustering with morphology features -> niche mapping -> targeted DE
- **Key packages**: Scanpy, Squidpy, Baysor (alternative segmentation)

### MERFISH
- **Best workflow**: Image-based cell segmentation -> clustering -> spatial registration to atlas -> validation
- **Key packages**: Scanpy, Baysor (segmentation), Squidpy

### Slide-seq
- **Best workflow**: Similar to Visium but with smaller spot logic; treat as "noisy single-cell"
- **Key packages**: Scanpy, Squidpy, RCTD for deconvolution if needed

## Common Pitfalls

1. **Visium spot mixing**: A 55um spot contains 1-10 cells. Never report "cell-type expression" without deconvolution.
2. **Xenium panel bias**: Targeted panels miss unknown markers. DE results are only valid for panel genes.
3. **MERFISH segmentation errors**: Cell boundary errors create false doublets. Always visualize segmentation on image.
4. **Slide-seq noise**: 10um spots have high dropout. Use larger neighborhoods for domain detection.
5. **Platform comparison**: Never directly compare expression magnitudes across platforms. Compare relative patterns only.
6. **Spatial autocorrelation**: Standard DE assumes independent samples. Use spatial-aware methods or block by domain.
7. **GPU requirements**: STAGATE, stLearn, NCEM need GPU. Note this in compute planning.
8. **R dependencies**: SPATA2, Monocle3 are R-only. If skill targets Python, flag these explicitly.
