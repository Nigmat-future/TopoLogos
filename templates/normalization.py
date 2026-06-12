"""
Spatial Transcriptomics — Normalization Template
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
OUTPUT_DIR = "./output/normalization"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the spatial dataset
# The 10x Visium breast cancer dataset can be downloaded from:
#   https://www.10xgenomics.com/resources/datasets
# Or use scanpy.datasets.visium_sge() for built-in samples.
adata = sc.read_h5ad(DATA_PATH)

# Validate expected structure
assert "spatial" in adata.uns, "Missing 'spatial' key in adata.uns — ensure Visium data was loaded correctly."
assert adata.obsm.get("spatial") is not None, "Missing spatial coordinates in adata.obsm['spatial']."

# Library-size normalization: scale each spot to 10,000 total counts
# This removes technical variation from differing sequencing depth across spots.
sc.pp.normalize_total(adata, target_sum=1e4)

# Log1p transform: stabilize variance and make data approximately normal
# Log transformation compresses high-expression outliers and improves downstream PCA.
sc.pp.log1p(adata)

# Highly variable gene selection (top 2000): focus analysis on informative genes
# HVGs capture biological heterogeneity while reducing noise from constitutive genes.
sc.pp.highly_variable_genes(adata, n_top_genes=2000, subset=True, flavor="seurat_v3")

# Scale to unit variance: give each gene equal weight in distance-based methods (PCA, UMAP)
# Centering at zero mean is standard; max_value=10 clips extreme outliers.
sc.pp.scale(adata, max_value=10)

# Visualize HVG selection
fig, ax = plt.subplots(figsize=(8, 6))
sc.pl.highly_variable_genes(adata, ax=ax, show=False)
fig.savefig(f"{OUTPUT_DIR}/highly_variable_genes.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Save normalized AnnData for downstream templates
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_normalized.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
