# stage16_uq_metrics_ready

Place at:

`~/Projects/cardiac_rfa/simulation/stage16_uq_metrics_ready/`

This stage extends the earlier stage3 model by adding:

- maximum lesion width
- lesion area
- depth-to-width ratio
- paper-level UQ config with 64 samples per cell
- Wilson-score confidence intervals for transmurality and overheating probabilities

Recommended local run order:

```bash
cd ~/Projects/cardiac_rfa/simulation/stage16_uq_metrics_ready
bash run_all.sh
bash run_phase_prep.sh
bash run_uq_paper.sh
```

Key outputs:

- `outputs/phase_prep/phase_prep_summary.csv`
- `outputs/uq_paper/uq_summary.csv`
- `outputs/uq_paper/uq_samples.csv`
- `outputs/uq_paper/uq_overview.csv`
