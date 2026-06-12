# Spatial Transcriptomics Methods Catalog

Quick reference for method selection across major analysis tasks. Methods marked with ⭐ are recommended for Aristotle mode (well-tested, broad compatibility, stable APIs).

---

## Quick Selection Guide

| Analysis Goal | First Choice | Alternative | Avoid When |
|---------------|--------------|-------------|------------|
| Domain detection with H&E | SpaGCN | STAGATE | No histology image available |
| Domain detection without image | STAGATE | GraphST | Tissue has very few spots |
| Cell type deconvolution | Cell2location | Tangram | No single-cell reference exists |
| Fast deconvolution | SPOTlight | RCTD | Need continuous state estimates |
| Ligand-receptor inference | LIANA+ | CellChat | No cell type labels available |
| Spatial variable genes | SpatialDE | SPARK-X | Dataset exceeds 100k spots |
| Batch correction | Harmony | scVI | Only one batch exists |
| Slice alignment | PASTE | Seurat v5 | Slices are non-adjacent |

---

## Spatial Domain Detection

Identify tissue regions with coherent gene expression patterns. These methods cluster spots or cells while respecting spatial proximity.

| Method | Year | Description | Platforms | Package | Best For | Template |
|--------|------|-------------|-----------|---------|----------|----------|
| ⭐ SpaGCN | 2021 | Graph convolutional network integrating histology image features with gene expression to detect domains; excels when morphology and transcription are correlated. | Visium, Xenium | Python (`spagcn`) | H&E-guided domain detection | `templates/clustering.py` |
| STAGATE | 2022 | Graph attention autoencoder learning low-dimensional embeddings via adaptive neighbor aggregation; handles irregular tissue architectures better than fixed-radius methods. | Visium, MERFISH, Slide-seq | Python (`stagate`) | Complex tissue shapes, attention-based weighting | `templates/clustering.py` |
| GraphST | 2023 | Contrastive learning on spatial graphs with data augmentation; strong performance on noisy datasets and when batch effects dominate. | Visium, Xenium, MERFISH | Python (`graphst`) | Noisy data, batch correction before clustering | `templates/clustering.py` |
| BANKSY | 2024 | Neighborhood-informed clustering using polar coordinates and principal component analysis; designed for subcellular resolution where cell types mix within spots. | Xenium, MERFISH, CosMx | Python/R (`banksy`) | Subcellular data, microenvironment-aware domains | `templates/clustering.py` |
| BayesSpace | 2021 | Bayesian nonparametric clustering with spatial priors; R-only but remains gold standard for Visium when probabilistic uncertainty matters. | Visium | R (`BayesSpace`) | Uncertainty quantification, R workflows | `templates/clustering.R` |
| BASS | 2022 | Bayesian alignment of single-cell and spatial data for joint domain detection; useful when you want cell type and spatial domain learned together. | Visium, MERFISH | R (`BASS`) | Joint cell type + domain modeling | `templates/clustering.R` |

**When to choose:** Use SpaGCN when you have good H&E staining and want morphology-informed domains. Pick STAGATE for irregular tissue boundaries or when fixed spatial windows fail. Choose GraphST if batch effects are severe. Use BANKSY exclusively for subcellular platforms where spots contain mixed cell types. BayesSpace is the fallback for R users needing probabilistic outputs. BASS fits when you want cell type composition and spatial domain learned in a single joint model.

---

## Deconvolution

Estimate cell type proportions within each spatial spot or pixel. These methods require a single-cell reference atlas.

| Method | Year | Description | Platforms | Package | Best For | Template |
|--------|------|-------------|-----------|---------|----------|----------|
| ⭐ Cell2location | 2022 | Bayesian model mapping single-cell references to spatial data via variational inference; accounts for platform-specific sensitivity and ambient RNA. | Visium, Slide-seq | Python (`cell2location`) | Large references, sensitivity correction | `templates/deconv.py` |
| RCTD | 2021 | Robust cell type decomposition using Poisson regression and platform-effect normalization; designed explicitly for Visium spot sizes. | Visium | R (`spacexr`) | Visium-specific, R ecosystem | `templates/deconv.R` |
| SPOTlight | 2021 | Nonnegative matrix factorization coupled with archetypal analysis; fast and lightweight for exploratory deconvolution. | Visium | R (`SPOTlight`) | Quick exploration, NMF-based workflows | `templates/deconv.R` |
| Tangram | 2021 | Deep learning framework aligning single-cell and spatial data via optimal transport; supports mapping genes and cell types simultaneously. | Visium, MERFISH, Xenium | Python (`tangram-sc`) | Gene imputation + deconvolution together | `templates/deconv.py` |
| DestVI | 2022 | Conditional variational autoencoder modeling continuous cell state variation; captures gradations better than discrete-type methods. | Visium | Python (`scvi-tools`) | Continuous states, developmental gradients | `templates/deconv.py` |
| CARD | 2022 | Conditional autoregressive model using cell type-specific expression profiles; explicitly models spatial correlation in deconvolution results. | Visium | R (`CARD`) | Spatially aware deconvolution | `templates/deconv.R` |

**When to choose:** Cell2location is the default for large single-cell references and when you need sensitivity correction. RCTD fits R workflows focused strictly on Visium. SPOTlight wins for speed and simplicity. Tangram is unique when you also need to impute unmeasured genes into spatial coordinates. DestVI handles continuous phenotypes like activation gradients where discrete labels fail. CARD adds explicit spatial correlation modeling when you expect cell types to cluster beyond what the reference captures.

---

## Cell-Cell Communication

Infer ligand-receptor interactions from spatial context. These methods typically require cell type labels and spatial coordinates.

| Method | Year | Description | Platforms | Package | Best For | Template |
|--------|------|-------------|-----------|---------|----------|----------|
| ⭐ LIANA+ | 2023 | Unified framework wrapping multiple ligand-receptor methods with consensus scoring and spatial prioritization; modular and extensible. | Visium, Xenium, MERFISH | Python/R (`liana`) | Consensus scoring, method comparison | `templates/niche.py` |
| CellPhoneDB | 2020 | Statistical testing of ligand-receptor pairs using permutation analysis; remains gold standard despite age due to curated database quality. | Visium, Xenium | Python (`cellphonedb`) | Curated database, statistical rigor | `templates/niche.py` |
| CellChat | 2021 | Probabilistic modeling of signaling networks with pathway-level aggregation and visualization tools; strong for biological interpretation. | Visium, Xenium, MERFISH | R (`CellChat`) | Pathway analysis, network visualization | `templates/niche.R` |
| MISTy | 2022 | Explainable machine learning decomposing interactions into intra-view, juxta-view, and para-view components; reveals multi-scale signaling. | Visium, Xenium, MERFISH | Python/R (`mistyR`) | Multi-scale interactions, explainability | `templates/niche.py` |
| NCEM | 2022 | Neural cell-cell interaction model learning differential equations from spatial data; captures nonlinear and conditional interactions. | Visium, MERFISH | Python (`ncem`) | Nonlinear interactions, deep learning | `templates/niche.py` |

**When to choose:** LIANA+ is the safest starting point because it aggregates multiple methods and filters by spatial proximity. CellPhoneDB remains the benchmark when you need the most curated database and statistical testing. CellChat adds pathway-level summaries that biologists prefer. MISTy is the choice when you suspect signaling acts at multiple spatial scales beyond immediate neighbors. NCEM fits when you expect nonlinear or conditional interactions that simple ligand-receptor models miss.

---

## Spatially Variable Genes

Detect genes with expression patterns that depend on spatial coordinates. These are the spatial equivalent of differential expression.

| Method | Year | Description | Platforms | Package | Best For | Template |
|--------|------|-------------|-----------|---------|----------|----------|
| ⭐ SpatialDE | 2018 | Gaussian process regression identifying spatially variable genes with automatic covariance structure selection; pre-2020 but still the gold standard benchmark. | Visium, MERFISH | Python (`SpatialDE`) | Benchmark comparisons, interpretable kernels | `templates/svg.py` |
| SPARK-X | 2021 | Nonparametric test using kernel-based variance decomposition; faster than SpatialDE and handles larger datasets without Gaussian process overhead. | Visium, Slide-seq | R (`SPARK`) | Large datasets, speed-critical workflows | `templates/svg.R` |
| Moran's I | 1950 | Classic spatial autocorrelation statistic; included because it is the simplest sanity check and works on any coordinate system without model fitting. | All | Python (`pysal`)/R (`ape`) | Sanity checks, any platform, no assumptions | `templates/svg.py` |
| ⭐ Squidpy | 2021 | Comprehensive spatial analysis toolkit including spatial variable gene detection, neighborhood enrichment, and graph analysis; ecosystem anchor. | Visium, Xenium, MERFISH, Slide-seq | Python (`squidpy`) | End-to-end Python workflows | `templates/svg.py` |
| Sepal | 2021 | Wavelet-based approach detecting spatial patterns at multiple scales; useful when you expect gene expression to vary at different resolutions. | Visium | Python (`sepal`) | Multi-resolution patterns | `templates/svg.py` |

**When to choose:** SpatialDE is the benchmark when you need interpretable spatial covariance structures and can afford the compute. SPARK-X replaces it for large datasets where runtime matters. Moran's I is the mandatory first pass because it is assumption-free and instant. Squidpy wraps multiple SVG approaches and is the default Python toolkit when you want one package for many tasks. Sepal adds wavelet decomposition when you expect patterns at multiple spatial frequencies.

---

## Integration and Alignment

Combine multiple slices, modalities, or experiments into a shared coordinate system.

| Method | Year | Description | Platforms | Package | Best For | Template |
|--------|------|-------------|-----------|---------|----------|----------|
| ⭐ Harmony | 2019 | Fast integration of single-cell and spatial datasets via iterative soft clustering; remains the gold standard for batch correction despite age. | All | R (`harmony`)/Python (`harmonypy`) | Batch correction, scRNA-seq integration | `templates/qc.py` |
| scVI | 2018 | Deep generative model for probabilistic integration of heterogeneous single-cell data; extends naturally to spatial when coupled with deconvolution. | All | Python (`scvi-tools`) | Probabilistic modeling, multimodal data | `templates/qc.py` |
| PASTE | 2022 | Optimal transport-based alignment of adjacent tissue slices preserving spatial geometry; explicitly models slice-to-slice mapping. | Visium | Python (`paste-bio`) | 3D reconstruction, adjacent slices | `templates/qc.py` |
| ⭐ Seurat v5 | 2023 | Weighted nearest neighbors and sketch-based integration scaling to millions of cells; the default R ecosystem anchor for multimodal mapping. | All | R (`Seurat`) | R workflows, multimodal reference mapping | `templates/qc.R` |
| Scanorama | 2019 | Panoramic stitching of heterogeneous single-cell datasets using mutual nearest neighbors; simple and effective for batch correction. | All | Python (`scanorama`) | Lightweight batch correction | `templates/qc.py` |

**When to choose:** Harmony is the first choice for simple batch correction across replicates or technologies. scVI adds probabilistic uncertainty when data is highly heterogeneous. PASTE is the only option specifically built for physical slice alignment and 3D reconstruction. Seurat v5 is the default for R users integrating single-cell references with spatial data at scale. Scanorama provides a lightweight Python alternative when you want minimal configuration.

---

## Visualization

Render spatial data and analysis results for exploration and publication.

| Method | Year | Description | Platforms | Package | Best For | Template |
|--------|------|-------------|-----------|---------|----------|----------|
| ⭐ Squidpy | 2021 | Spatial data visualization with neighborhood graphs, spatial statistics plots, and image overlays; tightly integrated with Scanpy and AnnData. | Visium, Xenium, MERFISH, Slide-seq | Python (`squidpy`) | Python ecosystem, programmatic plots | `templates/viz.py` |
| Seurat v5 | 2023 | Spatial plotting with image alignment, feature overlays, and dimensional reduction embeddings; the standard for R-based spatial visualization. | Visium, Xenium | R (`Seurat`) | R ecosystem, publication-ready figures | `templates/viz.R` |
| napari-spatialdata | 2024 | Interactive multi-dimensional viewer for SpatialData objects; supports large-scale image pyramids and annotation layers. | Visium, Xenium, MERFISH | Python (`napari-spatialdata`) | Interactive exploration, manual annotation | `templates/viz.py` |
| vitessce | 2023 | Web-based visualization of spatial and single-cell data with linked views; ideal for sharing results with collaborators. | Visium, MERFISH | Python/R/JS (`vitessce`) | Web sharing, collaborative viewing | `templates/viz.py` |

**When to choose:** Squidpy is the default for Python users who want programmatic, reproducible figures tied to Scanpy workflows. Seurat v5 is the equivalent for R users and produces publication-quality plots with less code. napari-spatialdata replaces static plotting when you need interactive exploration, manual region annotation, or large image pyramid navigation. vitessce is the choice when you need to share interactive visualizations with collaborators who do not code.

---

## Platform Compatibility Summary

| Method | Visium | Xenium | MERFISH | Slide-seq | CosMx |
|--------|--------|--------|---------|-----------|-------|
| SpaGCN | ✅ | ✅ | ❌ | ❌ | ❌ |
| STAGATE | ✅ | ❌ | ✅ | ✅ | ❌ |
| GraphST | ✅ | ✅ | ✅ | ❌ | ❌ |
| BANKSY | ❌ | ✅ | ✅ | ❌ | ✅ |
| Cell2location | ✅ | ❌ | ❌ | ✅ | ❌ |
| Tangram | ✅ | ✅ | ✅ | ❌ | ❌ |
| LIANA+ | ✅ | ✅ | ✅ | ❌ | ❌ |
| SpatialDE | ✅ | ❌ | ✅ | ❌ | ❌ |
| SPARK-X | ✅ | ❌ | ❌ | ✅ | ❌ |
| Squidpy | ✅ | ✅ | ✅ | ✅ | ❌ |
| Harmony | ✅ | ✅ | ✅ | ✅ | ✅ |
| PASTE | ✅ | ❌ | ❌ | ❌ | ❌ |
| Seurat v5 | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Version Notes

All methods listed are current as of June 2026. APIs and default parameters change frequently in this field. Always verify the latest documentation before running production analyses. Conservative mode prioritizes methods with stable releases (v1.0+) and broad community adoption.

**Starred methods (⭐):** SpaGCN, Cell2location, LIANA+, SpatialDE, Squidpy, Harmony, Seurat v5 — selected for Aristotle mode based on maturity, documentation quality, and cross-platform compatibility.

**Pre-2020 exceptions:** SpatialDE (2018), Harmony (2019), scVI (2018), Moran's I (1950), and CellPhoneDB (2020) are included because they remain gold standards or foundational sanity checks that newer methods are benchmarked against.

**Template cross-reference:** All `templates/*.py` and `templates/*.R` files mentioned above live in `~/.opencode/skills/spatial-transcriptomics/templates/`. Each template includes the specific package imports, parameter defaults, and output formats expected by Aristotle mode workflows.

**Update policy:** This catalog is reviewed quarterly. New methods are added after they demonstrate reproducible benchmarks across at least two spatial platforms. Deprecated methods are moved to an archive file rather than deleted, preserving historical references for reproducibility.

**Feedback:** If you encounter a method that should be added or a compatibility note that needs updating, append a finding to `~/.spatial-transcriptomics-memory/findings.jsonl` with the method name, platform tested, and outcome.
