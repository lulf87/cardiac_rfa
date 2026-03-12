# Cardiac RFA unified BioRender-like figure style

This package updates the figure pipeline to a unified style inspired by:
1. BioRender-like schematic hierarchy (soft muted palette, rounded label chips, generous spacing)
2. Clean quantitative modeling figures (white background, restrained grids, shared legends/colorbars)

## Inputs
- `phase_prep_summary.csv`
- `grid_convergence.csv`
- `dt_convergence.csv`
- `uq_summary.csv`

## Outputs
- `fig3_deterministic_summary.{png,pdf}`
- `fig4_verification.{png,pdf}`
- `fig5_transmural_probability_maps.{png,pdf}`
- `fig6_overheat_probability_maps.{png,pdf}`
- `fig7_tradeoff_scatter.{png,pdf}`
- `figS1_depth_fraction_p50_maps.{png,pdf}`
- `style_preview_palette.{png,pdf}`

## Run with bundled example data
```bash
bash run_make_figures.sh
```

## Run with your stage3 outputs
```bash
PHASE_CSV=../../simulation/stage3_uq_maps/outputs/phase_prep/phase_prep_summary.csv GRID_CSV=../../simulation/stage3_uq_maps/outputs/convergence/grid_convergence.csv DT_CSV=../../simulation/stage3_uq_maps/outputs/convergence/dt_convergence.csv UQ_CSV=../../simulation/stage3_uq_maps/outputs/uq_fast/uq_summary.csv OUTDIR=example_outputs bash run_make_figures.sh
```
