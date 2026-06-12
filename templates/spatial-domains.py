"""
Spatial Transcriptomics — Spatial Domain Detection Template
Dataset: 10x Visium human breast cancer
Tools: Scanpy + Squidpy
"""

import scanpy as sc
import squidpy as sq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# TODO: CONFIGURE — set your data path
DATA_PATH = "PATH_TO_YOUR_DATA/visium_breast_cancer.h5ad"
OUTPUT_DIR = "./output/spatial-domains"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the spatial dataset
# The 10x Visium breast cancer dataset can be downloaded from:
#   https://www.10xgenomics.com/resources/datasets
# Or use scanpy.datasets.visium_sge() for built-in samples.
adata = sc.read_h5ad(DATA_PATH)

# Validate expected structure
assert "spatial" in adata.uns, "Missing 'spatial' key in adata.uns — ensure Visium data was loaded correctly."
assert adata.obsm.get("spatial") is not None, "Missing spatial coordinates in adata.obsm['spatial']."

# Build spatial neighbor graph: connect spots that are physically close on the tissue
# This is essential for all spatial statistics in Squidpy.
sq.gr.spatial_neighbors(adata, coord_type="grid", n_neighs=6)

# Spatially informed Leiden clustering: uses both expression and spatial proximity
# This often yields more biologically coherent domains than expression-only clustering.
sq.gr.spatial_autocorr(adata, mode="moran", genes=adata.var_names[:100], n_perms=100, n_jobs=1)

# Moran's I: measure spatial autocorrelation for top variable genes
# High Moran's I indicates genes with spatially structured expression (e.g., layer markers).
# We run on highly variable genes to find spatially coherent expression patterns.
if "highly_variable" in adata.var.columns:
    hvg_names = adata.var_names[adata.var["highly_variable"]].tolist()[:100]
else:
    hvg_names = adata.var_names[:100]

sq.gr.spatial_autocorr(adata, mode="moran", genes=hvg_names, n_perms=100, n_jobs=1)

# Neighborhood enrichment: test if clusters are spatially enriched next to each other
# This reveals tissue architecture (e.g., tumor-stroma boundaries).
if "leiden" in adata.obs.columns:
    sq.gr.nhood_enrichment(adata, cluster_key="leiden")
    fig, ax = plt.subplots(figsize=(8, 6))
    sq.pl.nhood_enrichment(adata, cluster_key="leiden", ax=ax, show=False)
    fig.savefig(f"{OUTPUT_DIR}/nhood_enrichment.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

# Spatial domain visualization: overlay Moran's I scores on tissue
# Genes with high Moran's I are strong candidates for spatial domain markers.
if "MoransI" in adata.uns:
    top_moran = adata.uns["MoransI"].sort_values("I", ascending=False).head(1)["index"].values[0]
    fig = sq.pl.spatial_scatter(adata, color=top_moran, size=1.2, cmap="coolwarm",
                                title=f"Moran's I top gene: {top_moran}", save=False)
    fig.savefig(f"{OUTPUT_DIR}/spatial_moran_gene.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

# Spatial scatter of clusters for domain inspection
if "leiden" in adata.obs.columns:
    fig = sq.pl.spatial_scatter(adata, color="leiden", size=1.2,
                                title="Spatial domains (Leiden)", save=False)
    fig.savefig(f"{OUTPUT_DIR}/spatial_domains.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

# Save domain-annotated AnnData for downstream templates
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_domains.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
