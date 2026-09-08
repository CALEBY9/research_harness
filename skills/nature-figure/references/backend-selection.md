# Backend Selection

## Contents

- [Quick decision table](#quick-decision-table)
- [Backend exclusivity rule](#backend-exclusivity-rule)
- [Default stacks](#default-stacks)
- [Mixed workflow rule](#mixed-workflow-rule)
- [Recommendation language](#recommendation-language)


Backend selection, task-local defaults, and persistent preference writes are
owned by `../static/core/contract.md`. Use the table below when comparing
backends is requested or materially affects the deliverable.

## Quick decision table

| Recommend R when | Recommend Python when |
|---|---|
| The user brings R scripts, RData/RDS, Seurat objects, DESeq2/limma outputs, survival models, or ggplot templates | The data pipeline is already Python, NumPy/Pandas arrays, PyTorch/TensorFlow outputs, image arrays, or simulation output |
| The target plot is `ggplot2`, `patchwork`, `ComplexHeatmap`, `ggtree`, `circlize`, `survminer`, `maftools`, or Seurat/UMAP-heavy | The target plot needs low-level custom layout, Matplotlib patches, image plates, subplot mosaics, or custom drawing primitives |
| The user provides an R template collection or an existing R plotting workflow | The user wants a self-contained script with matplotlib/seaborn/statsmodels and no R dependency |
| Heatmap annotations are biologically rich and multi-layered | Image panels and quantitative panels need tight pixel/axis control |

If either backend can do the job, honor the user's saved preference. Do not switch
backends for aesthetics alone. Save a new default only when the user establishes
or changes a persistent preference.

## Backend exclusivity rule

Follow `../static/core/contract.md` for backend-exclusive rendering, missing
runtimes, and non-visual cross-language utilities.

## Default stacks

### R

- Core plotting: `ggplot2`
- Multi-panel assembly: `patchwork`
- Heatmaps: `ComplexHeatmap`, `circlize`
- Direct labels: `ggrepel`
- Survival/clinical: `survival`, `survminer`, `forestplot`, `ggplot2`
- Single-cell/omics: `Seurat`, `SingleCellExperiment`, `ComplexHeatmap`, `ggtree`
- Export: `svglite`, `grDevices::cairo_pdf`, `ragg`

### Python

- Core plotting: `matplotlib`
- Statistical plots: `seaborn`
- Layout: `subplot_mosaic`, `GridSpec`
- Tables/model output: `pandas`, `numpy`, `statsmodels`
- Images: `matplotlib.imshow`, `skimage`, `tifffile` when needed
- Export: `fig.savefig(... .svg/.pdf/.tiff)`, `svg.fonttype='none'`,
  `pdf.fonttype=42`

## Mixed workflow rule

Use the selected plotting backend for final assembly and all visual output. A mixed
workflow is reasonable only when the non-selected language performs non-visual data
preparation and the selected backend assembles the figure. In that case:

1. Export clean source data as CSV/TSV with stable column names.
2. Assemble the final figure in the selected backend.
3. Keep the source-data file next to the plotting script.
4. Do not stitch, preview, QA-render, or export final image/vector outputs from the
   non-selected backend unless the user explicitly changes the selected backend.

## Recommendation language

Use direct language:

```text
For this figure I recommend R because the main burden is ComplexHeatmap-style
omics annotation and patchwork assembly. I will still keep the export contract
SVG/PDF/TIFF with editable text.
```

```text
For this figure I recommend Python because the key panel is a custom image plate
with quantitative overlays and a subplot_mosaic layout. Matplotlib gives tighter
control over the raster and vector layers.
```
