# Handoff For Methods Writing

## 1) Current source-of-truth paths

- Authoritative simulation path:
  `simulation/stage17_controlled_rebuild/`
- Authoritative figure-generation path:
  `analysis/stage17_methodology_figs/`
- Authoritative manuscript packaging path:
  `papers/V13/`

Packaging note:

- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx` is the current
  manuscript file used by the recent audits.
- `manuscript/` remains a packaging/helper layer, not the primary text
  source-of-truth for current manuscript wording.

## 2) Scientific logic changes vs previous METHODS_PARAMETER_AUDIT

**NO SCIENTIFIC LOGIC CHANGE**

New stage17 provenance, figure, table, and environment work did **not** change:

- model equations
- parameter values
- controller settings
- latency settings
- lesion metric definitions
- benchmark values

Changes in this round were limited to:

- figure authority locking
- a stage17-native Figure 4 plotting path
- table-export automation
- environment and output-folder documentation

## 3) Figure authority status

- Figure 1: `CURRENT`
  Current authority is
  `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.{pdf,png,tiff}`.
- Figure 2: `UNRESOLVED`
  No stage17-native Figure 2 generator has been adopted; legacy packaged Figure
  2 remains in place pending an explicit editorial choice.
- Figure 3: `CURRENT`
  Current authority is
  `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.{pdf,png,tiff}`.
- Figure 4: `CURRENT`
  A stage17-native generator now exists at
  `analysis/stage17_methodology_figs/src/make_fig4_stage17_verification.py`
  and writes `fig4_stage17_verification.{pdf,png,tiff}` from current stage17
  convergence CSVs.
- Figure 5: `CURRENT`
  Current authority is
  `analysis/stage17_methodology_figs/example_outputs/fig5_depth_fraction_fixed_vs_controlled.{pdf,png,tiff}`.
- Figure 6: `CURRENT`
  Current authority is
  `analysis/stage17_methodology_figs/example_outputs/fig6_peak_temperature_fixed_vs_controlled.{pdf,png,tiff}`.
- Figure 7: `CURRENT`
  Current authority is
  `analysis/stage17_methodology_figs/example_outputs/fig7_controlled_minus_fixed_maps.{pdf,png,tiff}`.

Authority caution:

- `manuscript/figures/manifest.csv` still predates the current Figure 4 lock
  and therefore remains behind the current repository state for Figure 4.
- `docs/stage17/traceability/STAGE17_FIGURE_AUTHORITY.md` now reflects Figure 4
  as a current stage17-native figure source.

## 4) Figure 2 decision

- Chosen path: `Path A`
- Decision file: `docs/stage17/traceability/FIG2_DECISION.md`

Manuscript risk:

- Lower implementation risk, but it requires disciplined caption wording so the
  reader does not assume Figure 2 is stage17-native.

Exact implication for caption wording:

- Figure 2 should be described as a **legacy fixed-power reference figure**.
- Caption language should **not** imply that it comes from the current stage17
  comparator-aware line.
- Caption language should **not** imply that the temperature-limited comparator
  is represented in Figure 2.

## 5) Figure 4 verification status

Current input files:

- `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/grid_convergence.csv`
- `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/dt_convergence.csv`

Metrics plotted:

- relative error to the finest solution for `lesion_depth_mm`
- relative error to the finest solution for `peak_temperature_C`
- panel (a): grid refinement
- panel (b): time-step refinement

Current output files:

- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.pdf`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.png`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.tiff`

Stage17-native status:

- `YES` for the data path and output path
- Layout provenance note: panel structure was adapted from the legacy
  `analysis/stage7_freeze_final/` Figure 4 logic, but the script reads current
  stage17 convergence CSVs and recomputes the plotted relative errors from the
  raw exported metrics

## 6) Table status

### Table 1

Source file:

- `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`

Current export path:

- `export_table1_stage17_protocols.py`

Automated fields:

- protocol key
- `power_W`
- `duration_s`
- `use_controller`
- computed maximum nominal energy

Remaining `MANUAL` cells:

- protocol display labels
- role-in-comparison wording
- temp-limited display string `up to 360`

Manual trace source:

- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx` :: Table 1

### Table 2

Source files:

- `simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml`
- `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`
- `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml`
- `simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml`
- `simulation/stage17_controlled_rebuild/configs/phase_prep_stage17_fourway.yaml`

Current export path:

- `export_table2_stage17_controls.py`

Automated fields:

- production grid
- time step
- wall thickness levels
- nominal cooling coefficients
- nominal insertion levels
- comparator set
- controller target / ceiling
- controller sample period
- post-pulse latency window
- phase-preparation grid size

Remaining `MANUAL` cells:

- `Controller sensor`
- `Primary interpretive outputs`
- `Secondary internal proxies`
- `Calibration status`
- `Supplementary UQ status`

Manual trace source:

- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx` :: Table 2

### Table 3

Current export path:

- `export_table3_benchmark_trace.py`

Traceability status:

- `reported_depth_mm`: traced to current benchmark CSV
- `simulated_depth_mm`: traced to current benchmark CSV
- `reported_width_mm`: traced to current benchmark CSV
- `simulated_width_mm`: **not** in the current benchmark CSV; traced only via
  historical `benchmark_points_v3.csv`

Current benchmark-script source:

- `analysis/stage8_finish_ready/example_data/benchmark_points.csv`

Historical width trace:

- `papers/V7/tables/source_csv/benchmark_points_v3.csv`

Remaining `MANUAL` / non-current cells:

- none should be fabricated
- simulated-width provenance is still `HISTORICAL_TRACE`, not current
  single-source automation

## 7) Remaining unresolved items that still affect Methods writing

Only `AMBIGUOUS` / `NOT FOUND` items are listed here.

- `NOT FOUND`: analytic closed-form `q_reg(x,y)` formula
  Current implementation is algorithmic in
  `simulation/stage17_controlled_rebuild/src/model_fd.py`, not a standalone
  analytic formula.
- `AMBIGUOUS`: named time-stepping scheme label
  Current matrix form is consistent with a fully implicit finite-difference
  heat step, but no explicit scheme label is surfaced in
  `simulation/stage17_controlled_rebuild/src/model_fd.py`.
- `NOT FOUND`: solver tolerances
  No user-exposed tolerance setting was located in
  `simulation/stage17_controlled_rebuild/src/model_fd.py`.
- `NOT FOUND`: pinned library versions
  `simulation/stage17_controlled_rebuild/requirements.txt` and
  `analysis/stage17_methodology_figs/requirements.txt` do not pin versions.
- `AMBIGUOUS`: exact manuscript prose for some current controller and contact
  coefficients
  The current code/config values are recoverable, but some coefficient symbols
  and exact prose-level presentation are not cleanly recoverable from
  `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`.
- `AMBIGUOUS`: manuscript wording for the controller sensor
  Current implementation is specifically `T[1, :].max()` in
  `simulation/stage17_controlled_rebuild/src/model_fd.py`, while current Table
  2 wording remains manual.
- `NOT FOUND`: single current-source file for Table 3 simulated widths
  Current benchmark CSV does not contain simulated widths; the traced source is
  historical:
  `papers/V7/tables/source_csv/benchmark_points_v3.csv`.
- `AMBIGUOUS`: canonical-vs-observed stage17 output folder usage
  Current mapping is documented, but name drift still exists between script/docs
  targets and on-disk folders in
  `simulation/stage17_controlled_rebuild/outputs/`.

## 8) Path changes

- No files were renamed or moved in the stage17 provenance/figure/table/
  environment hardening work.
- New traceability-relevant files were added, including:
  - `analysis/stage17_methodology_figs/src/make_fig4_stage17_verification.py`
  - `analysis/stage17_methodology_figs/run_make_fig4_stage17_verification.sh`
  - `analysis/stage17_methodology_figs/requirements.txt`
  - `STAGE17_ENVIRONMENT.md`
