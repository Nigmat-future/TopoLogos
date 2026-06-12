"""
Spatial Transcriptomics — Publication-Ready Visualization Template
Dataset: 10x Visium human breast cancer
Tools: Scanpy + Squidpy + Matplotlib
"""

import scanpy as sc
import squidpy as sq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# TODO: CONFIGURE — set your data path
DATA_PATH = "PATH_TO_YOUR_DATA/visium_breast_cancer.h5ad"
OUTPUT_DIR = "./output/visualization"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the spatial dataset
# The 10x Visium breast cancer dataset can be downloaded from:
#   https://www.10xgenomics.com/resources/datasets
# Or use scanpy.datasets.visium_sge() for built-in samples.
adata = sc.read_h5ad(DATA_PATH)

# Validate expected structure
assert "spatial" in adata.uns, "Missing 'spatial' key in adata.uns — ensure Visium data was loaded correctly."
assert adata.obsm.get("spatial") is not None, "Missing spatial coordinates in adata.obsm['spatial']."
assert "leiden" in adata.obs.columns, "Missing cluster labels — run clustering.py first."

# Spatial feature plot: overlay gene expression on tissue image
# Feature plots are the primary visualization for spatial transcriptomics publications.
feature_gene = "ESR1" if "ESR1" in adata.var_names else adata.var_names[0]
fig = sq.pl.spatial_scatter(adata, color=feature_gene, size=1.2, cmap="viridis",
                            title=f"Expression of {feature_gene}", save=False)
fig.savefig(f"{OUTPUT_DIR}/spatial_feature_{feature_gene}.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# UMAP overlay: clusters and a key gene on the same embedding
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sc.pl.umap(adata, color="leiden", ax=axes[0], show=False, title="UMAP — Clusters")
sc.pl.umap(adata, color=feature_gene, ax=axes[1], show=False, title=f"UMAP — {feature_gene}")
fig.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/umap_overlay.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# Cluster composition barplot: show relative abundance of each cluster
# Useful for comparing tissue composition across samples or regions.
cluster_counts = adata.obs["leiden"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 5))
cluster_counts.plot(kind="bar", color="steelblue", ax=ax)
ax.set_xlabel("Cluster")
ax.set_ylabel("Number of spots")
ax.set_title("Cluster composition")
fig.savefig(f"{OUTPUT_DIR}/cluster_composition.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# Multi-panel figure assembly: combine spatial, UMAP, and dotplot in one figure
# This is the standard format for publication supplementary figures.
fig = plt.figure(figsize=(16, 12))
# Panel A: spatial clusters
ax1 = fig.add_subplot(2, 2, 1)
sq.pl.spatial_scatter(adata, color="leiden", size=1.0, ax=ax1, show=False)
ax1.set_title("A. Spatial clusters")
# Panel B: UMAP
ax2 = fig.add_subplot(2, 2, 2)
sc.pl.umap(adata, color="leiden", ax=ax2, show=False)
ax2.set_title("B. UMAP clusters")
# Panel C: dotplot of top markers
top_markers = sc.get.rank_genes_groups_df(adata, group=None).groupby("group").head(3)["names"].unique().tolist()
ax3 = fig.add_subplot(2, 2, 3)
sc.pl.dotplot(adata, var_names=top_markers, groupby="leiden", ax=ax3, show=False)
ax3.set_title("C. Top markers")
# Panel D: spatial feature
ax4 = fig.add_subplot(2, 2, 4)
sq.pl.spatial_scatter(adata, color=feature_gene, size=1.0, cmap="plasma", ax=ax4, show=False)
ax4.set_title(f"D. Spatial {feature_gene}")
fig.tight_layout()
fig.savefig(f"{OUTPUT_DIR}/multi_panel_figure.png", dpi=300, bbox_inches="tight")
plt.close(fig)

# Export all key plots to PNG at 300 DPI for publication
# (Individual plots above already saved at 300 DPI; this block confirms the export.)
print(f"All publication-ready figures exported to {OUTPUT_DIR} at 300 DPI.")

# Save final annotated AnnData
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_viz.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
