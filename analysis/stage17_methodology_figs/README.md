
# stage17_methodology_figs

This directory contains the final methodology-rebuild figure scripts used for the stage17 four-way manuscript branch.

Final sources in this folder:

- `src/make_fig1_stage17_workflow.py` for the stage17 geometry/workflow schematic aligned to the canonical four-way implementation
- `src/make_stage17_deterministic.py` for the four-way deterministic comparison figure
- `src/make_phase_map_figures.py` for the fixed-vs-temperature-limited 90 W / 4 s phase-map figures
- `src/make_revision_assets.py` for `figS3_probability_ci_halfwidths`

Historical duplicate:

- `analysis/stage16_revision_figs/` contains an earlier copy of the revision-assets script. Keep `stage17_methodology_figs/` as the active source for the methodology-rebuild paper line.

Default inputs:

- `simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv`
- `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_summary.csv`

Helper scripts:

- `run_make_fig1_stage17_workflow.sh`
- `run_make_stage17_deterministic.sh`
- `run_make_phase_map_figures.sh`
- `run_make_revision_assets.sh`
