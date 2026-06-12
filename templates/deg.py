"""
Spatial Transcriptomics — Differential Expression Template
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
OUTPUT_DIR = "./output/deg"
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

# Differential expression: Wilcoxon rank-sum test per cluster
# Wilcoxon is non-parametric and robust for spatial transcriptomics spot-level data.
sc.tl.rank_genes_groups(adata, groupby="leiden", method="wilcoxon", corr_method="benjamini-hochberg")

# Extract and filter significant markers: adjusted p < 0.05 and log2FC > 1
# These thresholds balance sensitivity and specificity for marker discovery.
result = adata.uns["rank_genes_groups"]
groups = result["names"].dtype.names
markers = []
for group in groups:
    genes = result["names"][group]
    logfc = result["logfoldchanges"][group]
    pvals_adj = result["pvals_adj"][group]
    df = pd.DataFrame({"gene": genes, "log2FC": logfc, "pvals_adj": pvals_adj})
    df = df[(df["pvals_adj"] < 0.05) & (df["log2FC"] > 1)].copy()
    df["cluster"] = group
    markers.append(df)
markers_df = pd.concat(markers)
markers_df.to_csv(f"{OUTPUT_DIR}/significant_markers.csv", index=False)

# Top marker dotplot: visualize expression of top 5 markers per cluster across all clusters
# Dotplots show both expression level (color) and fraction of expressing spots (size).
fig, ax = plt.subplots(figsize=(12, 6))
sc.pl.dotplot(adata, var_names=sc.get.rank_genes_groups_df(adata, group=None).groupby("group").head(5)["names"].unique().tolist(),
              groupby="leiden", ax=ax, show=False)
fig.savefig(f"{OUTPUT_DIR}/marker_dotplot.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Rank genes groups plot: violin-style visualization of top markers per cluster
fig = sc.pl.rank_genes_groups(adata, n_genes=10, sharey=False, show=False)
fig.savefig(f"{OUTPUT_DIR}/rank_genes_groups.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Spatial visualization of top marker: overlay expression of the strongest cluster marker
# This confirms that marker genes have spatially coherent expression patterns.
top_marker = markers_df.sort_values("log2FC", ascending=False).iloc[0]["gene"]
fig = sq.pl.spatial_scatter(adata, color=top_marker, size=1.2, cmap="plasma",
                            title=f"Top marker: {top_marker}", save=False)
fig.savefig(f"{OUTPUT_DIR}/spatial_top_marker.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Save DEG-annotated AnnData for downstream templates
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_deg.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
