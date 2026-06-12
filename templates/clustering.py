"""
Spatial Transcriptomics — Clustering Template
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
OUTPUT_DIR = "./output/clustering"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the spatial dataset
# The 10x Visium breast cancer dataset can be downloaded from:
#   https://www.10xgenomics.com/resources/datasets
# Or use scanpy.datasets.visium_sge() for built-in samples.
adata = sc.read_h5ad(DATA_PATH)

# Validate expected structure
assert "spatial" in adata.uns, "Missing 'spatial' key in adata.uns — ensure Visium data was loaded correctly."
assert adata.obsm.get("spatial") is not None, "Missing spatial coordinates in adata.obsm['spatial']."
assert "X_pca" in adata.obsm, "Missing PCA — run normalization.py first or compute PCA before this script."

# PCA: reduce dimensionality to 50 components for efficient neighbor graph construction
# PCA captures the major axes of gene expression variance across spots.
sc.pp.pca(adata, n_comps=50)

# Neighborhood graph: connect spots with similar expression profiles
# This graph is the foundation for UMAP, Leiden clustering, and trajectory inference.
sc.pp.neighbors(adata, n_neighbors=15, n_pcs=30)

# UMAP embedding: 2D visualization preserving local and global structure
# UMAP is non-linear and better than PCA for visualizing complex tissue architectures.
sc.tl.umap(adata)

# Leiden clustering at multiple resolutions to explore granularity
# Resolution controls cluster granularity: low = broad domains, high = fine subtypes.
for res in [0.3, 0.5, 1.0]:
    sc.tl.leiden(adata, resolution=res, key_added=f"leiden_res_{res}")

# UMAP plot colored by Leiden clusters (default resolution 0.5)
fig, ax = plt.subplots(figsize=(8, 7))
sc.pl.umap(adata, color="leiden_res_0.5", ax=ax, show=False, title="UMAP — Leiden clusters (res=0.5)")
fig.savefig(f"{OUTPUT_DIR}/umap_leiden.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Spatial scatter: overlay clusters on tissue image to see spatial organization
fig = sq.pl.spatial_scatter(adata, color="leiden_res_0.5", size=1.2,
                            title="Spatial clusters (Leiden res=0.5)", save=False)
fig.savefig(f"{OUTPUT_DIR}/spatial_clusters.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Save clustered AnnData for downstream templates
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_clustered.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
