# Legacy Drift Report

## Scope

This audit traces the manuscript figures and tables cited in
`papers/V13/CMBBE_RF_ablation_reduced_model_main.docx` back to repository
scripts, configs, intermediate CSVs, and packaged artifacts.

The goal here is provenance, not scientific reinterpretation.
If a link could not be located, it is marked `NOT FOUND`.

Status tags used below:

- `CURRENT`: matches the stage17 comparator-aware manuscript line
- `LEGACY`: earlier stage3/stage7/stage8/stage16 workflow
- `ARCHIVE`: historical paper/package material
- `DELIVERY_ONLY`: packaged output layer, not an authoritative source
- `AMBIGUOUS`: multiple candidates or an incomplete chain

## Highest-Risk Findings

1. **The current main figure pack is mostly legacy output.**
   - `manuscript/figures/main/fig1_model_workflow.png` is byte-identical to `manuscript/figures/source_exports/stage8_finish_ready/example_outputs/fig1_model_workflow.png`.
   - `manuscript/figures/main/fig2_representative_fields.png` is byte-identical to `manuscript/figures/source_exports/stage8_finish_ready/example_outputs/fig2_representative_fields.png`.
   - `manuscript/figures/main/fig3_deterministic_summary.png` through `fig7_tradeoff_depthrisk.png` are byte-identical to `manuscript/figures/source_exports/stage7_freeze_final/example_outputs/...`.
   - `Figure 8` is the only main figure that does not trace to the legacy stage8 source export by byte identity.

2. **The V13 manuscript captions for Figures 3 and 5-7 do not match the packaged figure files.**
   - The manuscript describes a four-way stage17 deterministic Figure 3, but the packaged figure is a legacy three-protocol stage7 summary.
   - The manuscript describes deterministic fixed-vs-temperature-limited maps in Figures 5 and 6, but the packaged figures are legacy `transmural_probability` and `overheat_probability` maps.
   - The manuscript describes controlled-minus-fixed difference maps in Figure 7, but the packaged figure is a legacy trade-off scatter.

3. **The workflow diagram drift is structural, not cosmetic.**
   - `analysis/stage8_finish_ready/src/make_fig1_model_workflow.py` includes a `Blood pool` domain, `cooling + perfusion`, and `probability maps`.
   - `analysis/stage17_methodology_figs/src/make_fig1_stage17_workflow.py` explicitly states `No explicit blood subdomain in stage17` and `perfusion term fixed at zero`.
   - The stage17 workflow also includes the generic controller and latency continuation, which the packaged legacy Figure 1 does not represent.

4. **The current stage17 figure directory still contains a mixed-source legacy branch.**
   - `analysis/stage17_methodology_figs/run_make_revision_assets.sh` points to:
     - `simulation/stage16_uq_metrics_ready/outputs/phase_prep/phase_prep_summary.csv`
     - `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_summary.csv`
     - `simulation/stage16_uq_metrics_ready/configs/baseline_50W_10s_4mm.yaml`
     - `simulation/stage16_uq_metrics_ready/configs/uq_paper.yaml`
   - This means the stage17 directory is not a purely stage17 provenance source.

5. **The tables in the V13 DOCX are not fully code-generated from the current repo state.**
   - `Table 1`: no current generator found for the four-protocol V13 version.
   - `Table 2`: the only table-generation script found writes `table2_uncertainty_solver_settings`, which is a stage16 UQ-style table and does not match the V13 controller/latency table.
   - `Table 3`: the current DOCX widths match historical `benchmark_points_v3.csv`, not the default benchmark CSV used by the current Figure 8 script.

6. **The delivery layer has drifted away from the source-export layer.**
   - `papers/V13/CMBBE_figure_upload/README.md` says `Figure1.png` to `Figure8.png` were copied from `papers/V12/figure_refresh_png/`.
   - Those upload PNGs are byte-different from `manuscript/figures/main/*.png`.
   - The README also names `papers/V13/CMBBE_main_document_blinded_final.docx`, which was not found; the visible manuscript file is `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`.

## Figure-by-Figure Drift

### Figure 1

- Packaged source: `LEGACY`
- Actual packaged generator path: `analysis/stage8_finish_ready/src/make_fig1_model_workflow.py`
- Current stage17 alternative: `analysis/stage17_methodology_figs/src/make_fig1_stage17_workflow.py`
- Drift:
  - packaged figure shows an explicit blood pool
  - packaged workflow mentions perfusion and probability maps
  - stage17 current script removes explicit blood subdomain and makes controller/latency visible

### Figure 2

- Packaged source: `LEGACY`
- Generator path: `analysis/stage8_finish_ready/src/make_fig2_representative_fields.py`
- Simulation dependency: `simulation/stage3_uq_maps/src/model_fd.py`
- Drift:
  - provenance is legacy stage3/stage8, not stage17
  - no stage17-native Figure 2 script was located
  - the caption is broadly compatible with a fixed-power three-protocol figure, but the implementation path is not current

### Figure 3

- Packaged source: `LEGACY`
- Actual packaged generator path: `analysis/stage7_freeze_final/src/make_figures.py`
- Current stage17 alternative: `analysis/stage17_methodology_figs/src/make_stage17_deterministic.py`
- Drift:
  - packaged figure is three-protocol, not four-protocol
  - packaged panel definitions differ from the V13 caption
  - current stage17 alternative exists, but it outputs `fig_stage17_deterministic_fourway` with a different panel set and is not wired into the manuscript package

### Figure 4

- Packaged source: `LEGACY`
- Actual packaged generator path: `analysis/stage7_freeze_final/src/make_figures.py`
- Candidate current data: `simulation/stage17_controlled_rebuild/outputs/convergence/*.csv`
- Drift:
  - packaged artifact is legacy stage7 output
  - no dedicated stage17-native Figure 4 plotting script was found
  - the repo can regenerate a verification figure from legacy code, but the current stage17 figure chain is incomplete

### Figures 5-7

- Packaged source: `LEGACY`
- Actual packaged generator path: `analysis/stage7_freeze_final/src/make_figures.py`
- Current stage17 alternatives:
  - `analysis/stage17_methodology_figs/src/make_phase_map_figures.py`
  - outputs `fig5_depth_fraction_fixed_vs_controlled`
  - outputs `fig6_peak_temperature_fixed_vs_controlled`
  - outputs `fig7_controlled_minus_fixed_maps`
- Drift:
  - packaged Figures 5-7 are legacy UQ/trade-off figures
  - current captions describe deterministic fixed-vs-controlled stage17 maps
  - current stage17 replacements exist but are not the files packaged into `manuscript/figures/main/`

### Figure 8

- Figure script path: `CURRENT`
- Generator path: `manuscript/scripts/make_fig8_final.py`
- Drift:
  - the current figure script is newer than the legacy stage8 export
  - the default input CSV is still `analysis/stage8_finish_ready/example_data/benchmark_points.csv`
  - the V13 table values appear to rely on older width-complete benchmark CSVs in `papers/V6` or `papers/V7`
  - figure generation is therefore newer, but the benchmark table/CSV chain is still partially historical

### Supplementary Figures S1-S2

- Packaged source: `LEGACY`
- Generator path: `analysis/stage7_freeze_final/src/make_figures.py`
- Drift:
  - low
  - the manuscript explicitly labels them as reference figures from the fixed-power three-protocol formulation

### Supplementary Figure S3

- Source status: `AMBIGUOUS`
- Candidate generators:
  - `analysis/stage17_methodology_figs/src/make_revision_assets.py`
  - `analysis/stage16_revision_figs/src/make_revision_assets.py`
- Observed artifact:
  - found in `analysis/stage16_revision_figs/example_outputs/`
  - `NOT FOUND` in `manuscript/submission_package/`
- Drift:
  - current manuscript references S3
  - active-vs-legacy generating location is unclear
  - packaging into the current submission layer is incomplete

## Table Drift

### Table 1

- Current DOCX content is a four-protocol stage17 table.
- Supporting config exists at `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`.
- `NOT FOUND`: a current code path that exports the V13 Table 1 directly.
- Historical CSV tables in `papers/V4` through `papers/V7` remain three-protocol and are not the same table.

### Table 2

- Current DOCX content is a stage17 control/latency/phase-prep table.
- Candidate code-generated table:
  - `analysis/stage17_methodology_figs/src/make_revision_assets.py::make_table2`
  - duplicate in `analysis/stage16_revision_figs/src/make_revision_assets.py`
- Drift:
  - candidate table script outputs UQ sample counts, distributions, and Wilson interval metadata
  - current DOCX Table 2 instead contains controller target/ceiling, sample period, latency, comparator set, and calibration status
  - these are not the same table

### Table 3

- Current DOCX content:
  - depths align with benchmark starter CSVs and historical benchmark CSVs
  - widths align with historical `benchmark_points_v3.csv`
- Current figure-input CSVs:
  - `analysis/stage8_finish_ready/example_data/benchmark_points.csv`
  - `manuscript/example_data/benchmark_points_v2.csv`
- Drift:
  - current figure-input CSVs leave `simulated_width_mm` blank
  - V13 Table 3 includes simulated widths
  - no current generator was found that produces the exact V13 Table 3 from repository inputs

## Manuscript Workflow vs Actual Code

### Workflow mismatch: blood pool and domain representation

- Current manuscript text says Figure 1 shows the `blood-pool boundary`.
- Legacy Figure 1 script draws an explicit `Blood pool` region.
- Current stage17 Figure 1 script says:
  - `No explicit blood subdomain in stage17`
  - `cooling enters through the top boundary profile`

This is not a naming issue. It is a model-representation change.

### Workflow mismatch: perfusion

- Legacy Figure 1 workflow text: `Transient bioheat T(x,t) with cooling + perfusion`
- Current stage17 Figure 1 workflow text: `perfusion term fixed at zero`

If the manuscript wants to represent stage17 current code, the legacy workflow wording is stale.

### Workflow mismatch: probability maps as primary outputs

- Legacy Figure 1 workflow advertises `probability maps`.
- Current stage17 manuscript line treats uncertainty figures as supplementary reference material.
- Stage17 main plotting scripts generate deterministic four-way and fixed-vs-controlled outputs, not primary UQ figures.

### Workflow mismatch: controller and latency

- Current stage17 protocols split:
  - `vhpsd_90W_4s_fixed`
  - `vhpsd_90W_4s_controlled`
- Current stage17 workflow figure includes:
  - generic controller
  - `70/80 C`
  - `0.05 s sample-hold`
  - latency continuation
- Legacy packaged workflow figure has none of those current stage17-specific components.

## Manuscript Terminology vs Variable Names

These mismatches are not necessarily errors, but they matter for traceability.

- Manuscript: `fixed-power 90 W / 4 s`
  - Code variable: `vhpsd_90W_4s_fixed`

- Manuscript: `temperature-limited 90 W / 4 s`
  - Code variable: `vhpsd_90W_4s_controlled`

- Manuscript: `surface-adjacent temperature surrogate`
  - Code implementation is more specific than the prose and is handled in the stage17 controller code path, not in figure assets

- Current manuscript captions for Figures 5-7 use deterministic comparator language
  - Packaged figure filenames still use:
    - `fig5_transmural_probability_maps`
    - `fig6_overheat_probability_maps`
    - `fig7_tradeoff_depthrisk`

- Current stage17 plotting scripts use a different filename vocabulary:
  - `fig1_stage17_geometry_workflow`
  - `fig_stage17_deterministic_fourway`
  - `fig5_depth_fraction_fixed_vs_controlled`
  - `fig6_peak_temperature_fixed_vs_controlled`
  - `fig7_controlled_minus_fixed_maps`

The filename vocabulary itself documents the drift between manuscript semantics
and packaged figure artifacts.

## Current Code vs Archived Code

### Protocol set

- `CURRENT`: `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`
  - `standard_30W_30s`
  - `hpsd_50W_10s`
  - `vhpsd_90W_4s_fixed`
  - `vhpsd_90W_4s_controlled`

- `LEGACY`: `simulation/stage16_uq_metrics_ready/configs/protocols.yaml`
  - `standard_30W_30s`
  - `hpsd_50W_10s`
  - `vhpsd_90W_4s`

This is a true branch split, not a cosmetic rename.

### Figure-script families

Overlapping figure implementations exist in at least these paths:

- `analysis/stage17_methodology_figs/`
- `analysis/stage16_revision_figs/`
- `analysis/stage8_finish_ready/`
- `analysis/stage7_freeze_final/`
- older stage4/stage6/stage7 variants

Only the stage17 directory is documented as the current methodology-rebuild
source, but the packaged manuscript outputs still resolve mostly to stage7 and
stage8 artifacts.

### Mixed-source wrappers

- `analysis/stage17_methodology_figs/run_make_revision_assets.sh` is located in
  a `CURRENT` directory but points to `LEGACY` stage16 inputs.
- This makes provenance ambiguous if a future audit assumes every script under
  `stage17_methodology_figs/` is stage17-native.

## Stale Intermediate Files

The following scripts use older or mixed-source intermediates:

- `analysis/stage17_methodology_figs/run_make_revision_assets.sh`
  - uses stage16 `phase_prep_summary.csv`
  - uses stage16 `uq_summary.csv`

- `analysis/stage8_finish_ready/run_make_figures.sh`
  - defaults to `simulation/stage3_uq_maps`

- `manuscript/scripts/run_stage12.sh`
  - defaults `BENCHMARK_CSV` to `analysis/stage8_finish_ready/example_data/benchmark_points.csv`

- `manuscript/figures/main/`
  - contains copied legacy exports for Figures 1-7

## Figures or Tables That Cannot Be Regenerated Cleanly Today

### Exact current submission figures not fully automated

- `Figure 3` as captioned in the V13 manuscript:
  - `NOT FOUND` as a single current script -> data -> packaged-output chain
- `Figure 4` as a stage17-native figure:
  - candidate data exist
  - dedicated current plotting script `NOT FOUND`
- `Figures 5-7` as currently captioned:
  - stage17 scripts exist
  - packaged outputs are still legacy
  - submission packaging does not currently point to the stage17 outputs

### Current manuscript tables not fully automated

- `Table 1` current four-protocol version: generator `NOT FOUND`
- `Table 2` current controller/latency version: exact generator `NOT FOUND`
- `Table 3` current width-complete benchmark version: exact generator `NOT FOUND`

### Supplement packaging gap

- `Figure S3` is cited in the V13 manuscript
- `Figure S3` package file in `manuscript/submission_package/` was `NOT FOUND`

## Candidate Files When the Exact Chain Was Not Found

- Current-stage17 Figure 3 candidate:
  - `analysis/stage17_methodology_figs/src/make_stage17_deterministic.py`

- Current-stage17 Figures 5-7 candidate:
  - `analysis/stage17_methodology_figs/src/make_phase_map_figures.py`

- Current-stage17 Figure 4 candidate plotting path:
  - `NOT FOUND`
  - nearest reusable legacy script: `analysis/stage7_freeze_final/src/make_figures.py`

- Table 1 current export path:
  - `NOT FOUND`

- Table 2 current export path:
  - candidate but mismatched script:
    `analysis/stage17_methodology_figs/src/make_revision_assets.py::make_table2`

- Table 3 current export path:
  - `NOT FOUND`
  - nearest historical sources:
    - `papers/V6/tables/source_csv/benchmark_points_v3.csv`
    - `papers/V7/tables/source_csv/benchmark_points_v3.csv`

## Bottom Line

The repository contains a real stage17 current implementation, but the
manuscript packaging layer has not fully caught up to it.

The highest-value cleanup target is not the solver. It is the provenance chain:

1. decide which figure scripts are authoritative for V13
2. route packaging to those outputs
3. either generate the current tables from code or mark them as manual
4. retire stale workflow language that still points to blood-pool/perfusion/UQ
   mainline logic that is no longer active in the current deterministic stage17
   implementation
