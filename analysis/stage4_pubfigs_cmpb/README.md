
# Stage 4 publication-figure package

This package converts the stage2/stage3 RFCA outputs into journal-style figures that are much closer
to CMPB/BPEX expectations than the default debugging plots.

## What it makes

- `fig3_deterministic_summary.(png|pdf)`
- `fig4_verification.(png|pdf)`
- `fig5_transmural_probability_maps.(png|pdf)`
- `fig6_overheat_probability_maps.(png|pdf)`
- `fig7_tradeoff_scatter.(png|pdf)`
- `figS1_depth_fraction_p50_maps.(png|pdf)`

## Recommended use with your local project

Place this folder under:

`~/Projects/cardiac_rfa/analysis/stage4_pubfigs_cmpb/`

Then edit the input paths in `run_make_figures.sh` so that they point to your local simulation outputs, e.g.

- `../../simulation/stage3_uq_maps/outputs/phase_prep/phase_prep_summary.csv`
- `../../simulation/stage3_uq_maps/outputs/convergence/grid_convergence.csv`
- `../../simulation/stage3_uq_maps/outputs/convergence/dt_convergence.csv`
- `../../simulation/stage3_uq_maps/outputs/uq_fast/uq_summary.csv`

## Why this version is better

- consistent journal-sized figure widths
- shared colorbars instead of one per panel
- shorter titles
- panel group structure
- conditional annotation (only transitional cells are labeled)
- PDF export for manuscript submission
- a dedicated trade-off figure, not just raw heatmaps

## Important note

Your current `uq_fast` results use only 8 samples per condition, so the probabilities appear quantized
(0.12, 0.38, 0.75, ...). These figures are good for exploration, but the final manuscript figures should
be regenerated from a denser run (recommended: 64 or 128 samples per cell).
