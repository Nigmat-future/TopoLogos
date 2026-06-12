"""
Spatial Transcriptomics — Cell Type Deconvolution Template
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
REF_PATH = "PATH_TO_YOUR_DATA/reference_scrna_breast.h5ad"  # scRNA-seq reference with cell type labels
OUTPUT_DIR = "./output/deconvolution"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load the spatial dataset
# The 10x Visium breast cancer dataset can be downloaded from:
#   https://www.10xgenomics.com/resources/datasets
# Or use scanpy.datasets.visium_sge() for built-in samples.
adata = sc.read_h5ad(DATA_PATH)

# Validate expected structure
assert "spatial" in adata.uns, "Missing 'spatial' key in adata.uns — ensure Visium data was loaded correctly."
assert adata.obsm.get("spatial") is not None, "Missing spatial coordinates in adata.obsm['spatial']."

# Load reference scRNA-seq dataset with annotated cell types
# The reference must have a 'cell_type' column in adata.obs for deconvolution.
# Example public references: Tabula Sapiens, Human Cell Atlas, or breast cancer atlases.
if os.path.exists(REF_PATH):
    adata_ref = sc.read_h5ad(REF_PATH)
    assert "cell_type" in adata_ref.obs.columns, "Reference missing 'cell_type' annotation in obs."
else:
    raise FileNotFoundError(f"Reference scRNA-seq not found at {REF_PATH}. Provide a reference with cell_type labels.")

# Deconvolution setup: identify shared genes between spatial and reference data
# Shared genes ensure that cell type signatures are comparable across modalities.
shared_genes = list(set(adata.var_names) & set(adata_ref.var_names))
adata = adata[:, shared_genes].copy()
adata_ref = adata_ref[:, shared_genes].copy()

# Normalize reference to match spatial data preprocessing
sc.pp.normalize_total(adata_ref, target_sum=1e4)
sc.pp.log1p(adata_ref)

# Compute average expression profile per cell type in reference
# These profiles serve as signatures for deconvolution.
cell_type_profiles = pd.DataFrame(
    {ct: adata_ref[adata_ref.obs["cell_type"] == ct].X.mean(axis=0).A1
     for ct in adata_ref.obs["cell_type"].unique()},
    index=adata_ref.var_names
)

# Simple deconvolution: non-negative least squares per spot
# For production, replace with Cell2location (cell2location) or RCTD (spacexr).
from scipy.optimize import nnls
proportions = pd.DataFrame(
    index=adata.obs_names,
    columns=cell_type_profiles.columns,
    data=[nnls(cell_type_profiles.values, spot)[0] for spot in adata.X.toarray()]
)
# Normalize proportions to sum to 1 per spot
proportions = proportions.div(proportions.sum(axis=1), axis=0).fillna(0)
adata.obsm["cell_type_proportions"] = proportions.values

# Visualize per-spot cell type proportions on tissue
# Stacked bar or spatial scatter of dominant cell type per spot.
dominant_cell_type = proportions.idxmax(axis=1)
adata.obs["dominant_cell_type"] = dominant_cell_type
fig = sq.pl.spatial_scatter(adata, color="dominant_cell_type", size=1.2,
                            title="Dominant cell type per spot", save=False)
fig.savefig(f"{OUTPUT_DIR}/spatial_dominant_celltype.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Proportion heatmap: show all cell type proportions across spots
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(proportions.values.T, aspect="auto", cmap="YlOrRd")
ax.set_xlabel("Spots")
ax.set_ylabel("Cell types")
ax.set_title("Cell type proportions per spot")
plt.colorbar(im, ax=ax, label="Proportion")
fig.savefig(f"{OUTPUT_DIR}/proportion_heatmap.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Save deconvoluted AnnData for downstream templates
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_deconvoluted.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
