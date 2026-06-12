"""
Spatial Transcriptomics — Cell-Cell Communication Template
Dataset: 10x Visium human breast cancer
Tools: Scanpy + Squidpy + LIANA
"""

import scanpy as sc
import squidpy as sq
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# TODO: CONFIGURE — set your data path
DATA_PATH = "PATH_TO_YOUR_DATA/visium_breast_cancer.h5ad"
OUTPUT_DIR = "./output/cci"
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

# LIANA+ multi-method ligand-receptor analysis
# LIANA aggregates predictions from multiple LR methods (e.g., CellPhoneDB, NATMI, SingleCellSignalR)
# to produce a robust consensus of cell-cell communication.
try:
    import liana as li
except ImportError:
    raise ImportError("liana is required. Install with: pip install liana")

# Run LIANA on cluster-level aggregated expression
# We use the 'rank_aggregate' method which combines multiple LR tools into a single score.
li.mt.rank_aggregate(adata, groupby="leiden", expr_prop=0.1, n_perms=100,
                     use_raw=False, verbose=True)

# Extract and save the consensus ligand-receptor results
liana_results = adata.uns["liana_rank_aggregate"]
liana_results.to_csv(f"{OUTPUT_DIR}/liana_consensus_lr.csv", index=False)

# Summary dotplot: visualize top interactions across cluster pairs
# Dot color = interaction score; dot size = expression proportion.
fig, ax = plt.subplots(figsize=(10, 8))
li.pl.dotplot(adata, colour="magnitude", size="specificity", source_labels=liana_results["source"].unique()[:5].tolist(),
              target_labels=liana_results["target"].unique()[:5].tolist(),
              filter_fun=lambda x: x["specificity_rank"] <= 0.05, ax=ax, show=False)
fig.savefig(f"{OUTPUT_DIR}/liana_dotplot.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# Spatial visualization of top interaction
# Identify the strongest ligand-receptor pair and overlay ligand expression on tissue.
if not liana_results.empty:
    top_lr = liana_results.iloc[0]
    ligand = top_lr["ligand"]
    if ligand in adata.var_names:
        fig = sq.pl.spatial_scatter(adata, color=ligand, size=1.2, cmap="magma",
                                    title=f"Top ligand: {ligand} ({top_lr['source']}→{top_lr['target']})", save=False)
        fig.savefig(f"{OUTPUT_DIR}/spatial_top_ligand.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

# Save CCI-annotated AnnData for downstream templates
adata.write_h5ad(f"{OUTPUT_DIR}/visium_breast_cancer_cci.h5ad")

print(f"Analysis complete. Output saved to {OUTPUT_DIR}")
