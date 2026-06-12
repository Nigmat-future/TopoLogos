"""
Spatial Transcriptomics — Quality Control Template
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
OUTPUT_DIR = "./output/qc"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the spatial dataset
# The 10x Visium breast cancer dataset can be downloaded from:
#   https://www.10xgenomics.com/resources/datasets
# Or use scanpy.datasets.visium_sge() for built-in samples.
adata = sc.read_h5ad(DATA_PATH)

# Validate expected structure for Visium data
assert "spatial" in adata.uns, "Missing 'spatial' key in adata.uns — ensure Visium data was loaded correctly."
assert adata.obsm.get("spatial") is not None, "Missing spatial coordinates in adata.obsm['spatial']."

# Calculate QC metrics: total counts, genes per spot, and mitochondrial percentage
# Mitochondrial genes are prefixed with 'MT-' in human data; high MT% indicates damaged cells.
adata.var["mt"] = adata.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)

# Filter spots (cells) with too few genes or too many counts — removes empty/damaged tissue regions
sc.pp.filter_cells(adata, min_genes=200)   # Keep spots expressing at least 200 genes
sc.pp.filter_cells(adata, max_genes=8000)  # Remove potential doublets or artifacts

# Filter genes expressed in too few spots — removes noise from extremely rare transcripts
sc.pp.filter_genes(adata, min_cells=10)    # Keep genes detected in at least 10 spots

# Filter spots with excessive mitochondrial content (>20% is a common threshold for tissue damage)
adata = adata[adata.obs.pct_counts_mt < 20, :].copy()

# QC violin plots: visualize distributions after filtering
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
sc.pl.violin(adata, ["n_genes_by_counts"], jitter=0.4, ax=axes[0], show=False)
sc.pl.violin(adata, ["total_counts"], jitter=0.4, ax=axes[1], show=False)
sc.pl.violin(adata, ["pct_counts_mt"], jitter=0.4, ax=axes[2], show=False)
fig.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/qc_violins.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Spatial QC scatter: overlay total counts on tissue image to detect regional artifacts
fig = sq.pl.spatial_scatter(adata, color="total_counts", size=1.2, cmap="viridis",
                            title="Total counts per spot", save=False)
fig.savefig(f"{OUTPUT_DIR}/qc_spatial_total_counts.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Save filtered AnnData for downstream templates
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_qc.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
