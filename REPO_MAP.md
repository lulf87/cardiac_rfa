# REPO_MAP

## Scope

This map audits the repository as it exists on disk and distinguishes current,
legacy, archive, and unknown areas for manuscript reproducibility work.

Status tags used here:

- `CURRENT`: active source-of-truth path for the present stage17 manuscript line.
- `LEGACY`: older or frozen implementation/figure path still present in the repo.
- `ARCHIVE`: delivery-only, packaged, copied, or temporary artifact layer.
- `UNKNOWN`: purpose or authority cannot be confirmed from current repo docs/code.

Note:

- The repository has a "frozen baseline" concept for `simulation/stage16_uq_metrics_ready/`,
  but the requested tag set does not include `FROZEN`. In this audit it is tagged
  `LEGACY` and called out explicitly as a frozen three-protocol baseline.

## Top-level tree

| Path | Status | Role | Notes |
| --- | --- | --- | --- |
| `simulation/stage17_controlled_rebuild/` | CURRENT | Canonical deterministic four-comparator implementation | Current stage17 line per [AGENTS.md](/Users/lulingfeng/Projects/cardiac_rfa/AGENTS.md) and [simulation/stage17_controlled_rebuild/README.md](/Users/lulingfeng/Projects/cardiac_rfa/simulation/stage17_controlled_rebuild/README.md). |
| `analysis/stage17_methodology_figs/` | CURRENT | Current stage17 figure-generation source scripts | Current methodology-rebuild figure line. |
| `docs/stage17/` | CURRENT | Current decision log, claim notes, audit notes | Documentation support for the stage17 branch. |
| `docs/stage17/traceability/` | CURRENT | Current detailed stage17 audit and provenance hub | Holds current figure/table/methods/verification traceability artifacts after the Task 6 safe reorganization. |
| `simulation/stage16_uq_metrics_ready/` | LEGACY | Frozen three-protocol UQ baseline | Still referenced by some current figure scripts, especially revision assets. |
| `simulation/stage0_minimal/` | LEGACY | Earliest minimal simulation stage | Sandbox/minimal baseline. |
| `simulation/stage1_deterministic/` | LEGACY | Deterministic three-protocol stage | Adds wall/cooling/convergence scans. |
| `simulation/stage1p5_contact/` | LEGACY | Deterministic stage with contact surrogate scans | Pre-phase-prep development stage. |
| `simulation/stage2_phase_ready/` | LEGACY | Deterministic stage with phase-prep support | Pre-UQ development stage. |
| `simulation/stage3_uq_maps/` | LEGACY | Three-protocol UQ map stage | Older UQ line still used by some legacy figure scripts. |
| `analysis/stage4_pubfigs_cmpb/` | LEGACY | Early split figure scripts for Figures 3-7 | Uses stage3-style deterministic/UQ CSVs. |
| `analysis/stage6_biorender_style/` | LEGACY | Restyled figure pipeline | Another old figure line over stage3-style outputs. |
| `analysis/stage7_freeze_ready/` | LEGACY | Frozen combined figure generator | Generates old three-protocol Figures 3-7 and supplements. |
| `analysis/stage7_freeze_final/` | LEGACY | Another frozen combined figure generator | Overlaps `stage7_freeze_ready`. |
| `analysis/stage7_polishing_patch/` | LEGACY | Patch variant of stage7 figure pack | Overlaps both stage7 freeze directories. |
| `analysis/stage8_fig128_export/` | LEGACY | Legacy Figure 1/2/8 generator | Uses `simulation/stage3_uq_maps/` conventions. |
| `analysis/stage8_finish_ready/` | LEGACY | Legacy Figure 1/2/8 generator | Overlaps `stage8_fig128_export`. |
| `analysis/stage16_revision_figs/` | LEGACY | Older copy of revision-assets generator | Duplicates the stage17 revision-assets script family. |
| `manuscript/` | ARCHIVE | Packaging-oriented figure and submission layer | Contains figure manifest, packaged figures, captions, and stage12 submission scripts. |
| `papers/V4/` to `papers/V12/` | ARCHIVE | Historical paper-version folders | Prior manuscript/delivery snapshots. |
| `papers/V13/` | ARCHIVE | Current delivery-facing manuscript folder | Contains the active DOCX deliverable and copied upload figures, but not authoritative generation code. |
| `data/literature_benchmark/` | UNKNOWN | Benchmark raw/processed data stash | Figure 8 scripts do not directly read these files in the traced current chain. |
| `experiments/` | UNKNOWN | Empty placeholder | No files found. |
| `tmp/` | ARCHIVE | Temporary QC/render outputs | Not authoritative sources. |
| `README.md` | CURRENT | Root navigation entry point | Points to the current stage17 reproducibility path and current-vs-legacy boundaries. |
| `AGENTS.md` | CURRENT | Repository operating rules | Sets the current traceability-first working rules for this repo. |
| `RUNBOOK.md` | CURRENT | Minimal current reproducibility path | Documents the smallest verified stage17 simulation and figure workflow. |
| `STAGE17_ENVIRONMENT.md` | CURRENT | Stage17 environment and output-path note | Documents canonical-vs-observed output folders and current environment anchors. |

## Simulation code map

### CURRENT

`simulation/stage17_controlled_rebuild/`

- Shell entry points:
  - `run_all.sh`
  - `run_phase_prep.sh`
  - `run_fixed_smoke.sh`
  - `run_controlled_smoke.sh`
  - `run_uq_fast.sh`
  - `run_uq_paper.sh`
  - `run_baseline_stage17.sh`
- Python entry points:
  - `src/run_case.py`
  - `src/run_protocol_scan.py`
  - `src/run_wall_protocol_scan.py`
  - `src/run_cooling_protocol_scan.py`
  - `src/run_contact_scan.py`
  - `src/run_convergence.py`
  - `src/run_phase_prep.py`
  - `src/run_uq_maps.py`
- Core implementation modules:
  - `src/model_fd.py`
  - `src/controller.py`
  - `src/latency.py`
- Config files:
  - `configs/baseline_90W_4s_4mm.yaml`
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols_stage17_fourway.yaml`
  - `configs/protocols.yaml`
  - `configs/protocols_generic_fixed.yaml`
  - `configs/controller_selected_stage17.yaml`
  - `configs/controller_generic_temp_limited.yaml`
  - `configs/controller_generic_temp_limited_enabled.yaml`
  - `configs/controller_trial_hard.yaml`
  - `configs/controller_trial_mid.yaml`
  - `configs/controller_trial_soft.yaml`
  - `configs/latency.yaml`
  - `configs/latency_enabled.yaml`
  - `configs/phase_prep_stage17_fourway.yaml`
  - `configs/phase_prep.yaml`
  - `configs/wall_scan_stage17.yaml`
  - `configs/wall_scan.yaml`
  - `configs/cooling_scan_stage17.yaml`
  - `configs/cooling_scan.yaml`
  - `configs/contact_scan_stage17.yaml`
  - `configs/contact_scan.yaml`
  - `configs/convergence.yaml`
  - `configs/uq_fast.yaml`
  - `configs/uq_paper.yaml`
- Output folders present:
  - `outputs/baseline_50W_10s_4mm/`
  - `outputs/contact_protocol_scan/`
  - `outputs/contact_scan_stage17_fourway/`
  - `outputs/convergence/`
  - `outputs/convergence_stage17_controlled_check/`
  - `outputs/cooling_protocol_scan/`
  - `outputs/cooling_scan_stage17_fourway/`
  - `outputs/phase_prep_stage17_fourway/`
  - `outputs/protocol_scan/`
  - `outputs/protocol_scan_stage17_fourway/`
  - `outputs/protocol_scan_stage17_fourway_check/`
  - `outputs/smoke_case*/`
  - `outputs/smoke_controlled_stage17/`
  - `outputs/smoke_fixed_stage17/`
  - `outputs/smoke_logs/`
  - `outputs/timing_single/`
  - `outputs/tune_*`
  - `outputs/uq_fast/`
  - `outputs/uq_paper/`
  - `outputs/wall_protocol_scan/`
  - `outputs/wall_scan_stage17_fourway/`
  - `outputs/baseline_stage17_fixed/` and `outputs/baseline_stage17_controlled/` were expected from `run_all.sh` and the stage17 README but were `NOT FOUND` in the current on-disk output inventory.

### LEGACY

`simulation/stage16_uq_metrics_ready/`

- Shell entry points:
  - `run_all.sh`
  - `run_phase_prep.sh`
  - `run_uq_fast.sh`
  - `run_uq_paper.sh`
- Python entry points:
  - `src/run_case.py`
  - `src/run_protocol_scan.py`
  - `src/run_wall_protocol_scan.py`
  - `src/run_cooling_protocol_scan.py`
  - `src/run_contact_scan.py`
  - `src/run_convergence.py`
  - `src/run_phase_prep.py`
  - `src/run_uq_maps.py`
- Core implementation module:
  - `src/model_fd.py`
- Config files:
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols.yaml`
  - `configs/wall_scan.yaml`
  - `configs/cooling_scan.yaml`
  - `configs/contact_scan.yaml`
  - `configs/convergence.yaml`
  - `configs/phase_prep.yaml`
  - `configs/uq_fast.yaml`
  - `configs/uq_paper.yaml`
- Output folders present:
  - `outputs/baseline_50W_10s_4mm/`
  - `outputs/protocol_scan/`
  - `outputs/wall_protocol_scan/`
  - `outputs/cooling_protocol_scan/`
  - `outputs/contact_protocol_scan/`
  - `outputs/convergence/`
  - `outputs/phase_prep/`
  - `outputs/uq_paper/`

`simulation/stage3_uq_maps/`

- Shell entry points:
  - `run_all.sh`
  - `run_phase_prep.sh`
  - `run_uq_fast.sh`
  - `run_uq_paper.sh`
- Python entry points:
  - `src/run_case.py`
  - `src/run_protocol_scan.py`
  - `src/run_wall_protocol_scan.py`
  - `src/run_cooling_protocol_scan.py`
  - `src/run_contact_scan.py`
  - `src/run_convergence.py`
  - `src/run_phase_prep.py`
  - `src/run_uq_maps.py`
- Core implementation module:
  - `src/model_fd.py`
- Config files:
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols.yaml`
  - `configs/wall_scan.yaml`
  - `configs/cooling_scan.yaml`
  - `configs/contact_scan.yaml`
  - `configs/convergence.yaml`
  - `configs/phase_prep.yaml`
  - `configs/uq_fast.yaml`
  - `configs/uq_paper.yaml`
- Output folders present:
  - `outputs/baseline_50W_10s_4mm/`
  - `outputs/protocol_scan/`
  - `outputs/wall_protocol_scan/`
  - `outputs/cooling_protocol_scan/`
  - `outputs/contact_protocol_scan/`
  - `outputs/convergence/`
  - `outputs/phase_prep/`
  - `outputs/uq_fast/`

`simulation/stage2_phase_ready/`

- Shell entry points:
  - `run_all.sh`
  - `run_phase_prep.sh`
- Python entry points:
  - `src/run_case.py`
  - `src/run_protocol_scan.py`
  - `src/run_wall_protocol_scan.py`
  - `src/run_cooling_protocol_scan.py`
  - `src/run_contact_scan.py`
  - `src/run_convergence.py`
  - `src/run_phase_prep.py`
- Core implementation module:
  - `src/model_fd.py`
- Config files:
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols.yaml`
  - `configs/wall_scan.yaml`
  - `configs/cooling_scan.yaml`
  - `configs/contact_scan.yaml`
  - `configs/convergence.yaml`
  - `configs/phase_prep.yaml`

`simulation/stage1p5_contact/`

- Shell entry point:
  - `run_all.sh`
- Python entry points:
  - `src/run_case.py`
  - `src/run_protocol_scan.py`
  - `src/run_wall_protocol_scan.py`
  - `src/run_cooling_protocol_scan.py`
  - `src/run_contact_scan.py`
  - `src/run_convergence.py`
- Core implementation module:
  - `src/model_fd.py`
- Config files:
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols.yaml`
  - `configs/wall_scan.yaml`
  - `configs/cooling_scan.yaml`
  - `configs/contact_scan.yaml`
  - `configs/convergence.yaml`

`simulation/stage1_deterministic/`

- Shell entry point:
  - `run_all.sh`
- Python entry points:
  - `src/run_case.py`
  - `src/run_protocol_scan.py`
  - `src/run_wall_protocol_scan.py`
  - `src/run_cooling_protocol_scan.py`
  - `src/run_convergence.py`
- Core implementation module:
  - `src/model_fd.py`
- Config files:
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols.yaml`
  - `configs/wall_scan.yaml`
  - `configs/cooling_scan.yaml`
  - `configs/convergence.yaml`

`simulation/stage0_minimal/`

- Shell entry point:
  - `run_all.sh`
- Python entry points:
  - `src/run_case.py`
  - `src/run_protocol_scan.py`
- Core implementation module:
  - `src/model_fd.py`
- Config files:
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols.yaml`

## Plotting and packaging entry points

| Script path | Status | Required input data | Output figure/table path | Likely manuscript target | Notes |
| --- | --- | --- | --- | --- | --- |
| `analysis/stage17_methodology_figs/run_make_fig1_stage17_workflow.sh` | CURRENT | No external CSV; script draws schematic directly | `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.{pdf,png,tiff}` | Figure 1 candidate for stage17 line | Output basename does not match `manuscript/figures/manifest.csv`. |
| `analysis/stage17_methodology_figs/run_make_fig4_stage17_verification.sh` | CURRENT | `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/grid_convergence.csv`; `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/dt_convergence.csv` | `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.{pdf,png,tiff}` | Figure 4 candidate for stage17 line | Stage17-native data path. Relative errors are recomputed from raw convergence metrics because the current CSV schema does not include legacy `*_relerr_pct` columns. Panel layout provenance is documented in the script header. |
| `analysis/stage17_methodology_figs/run_make_stage17_deterministic.sh` | CURRENT | `simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv` | `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.{pdf,png,tiff}` | Figure 3 candidate for stage17 line | Output basename does not match `fig3_deterministic_summary`. |
| `analysis/stage17_methodology_figs/run_make_phase_map_figures.sh` | CURRENT | `simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv` | `analysis/stage17_methodology_figs/example_outputs/fig5_depth_fraction_fixed_vs_controlled.{pdf,png,tiff}`; `fig6_peak_temperature_fixed_vs_controlled.{pdf,png,tiff}`; `fig7_controlled_minus_fixed_maps.{pdf,png,tiff}` | Figures 5-7 candidate set for stage17 line | Current stage17 filenames differ from `manuscript/figures/manifest.csv` and `papers/V13/CMBBE_figure_upload/`. |
| `analysis/stage17_methodology_figs/run_make_revision_assets.sh` | CURRENT | `simulation/stage16_uq_metrics_ready/outputs/phase_prep/phase_prep_summary.csv`; `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_summary.csv`; `simulation/stage16_uq_metrics_ready/configs/baseline_50W_10s_4mm.yaml`; `simulation/stage16_uq_metrics_ready/configs/uq_paper.yaml` | `analysis/stage17_methodology_figs/example_outputs/fig3_deterministic_summary_v2.{pdf,png,tiff}`; `figS3_probability_ci_halfwidths.{pdf,png,tiff}`; `table2_uncertainty_solver_settings.{csv,md}` | Revision assets / Table 2 / Figure S3 | Mixed-source workflow: current analysis dir but stage16 inputs. |
| `analysis/stage16_revision_figs/run_make_revision_assets.sh` | LEGACY | Same stage16 inputs as above | `analysis/stage16_revision_figs/example_outputs/fig3_deterministic_summary_v2.{pdf,png,tiff}`; `figS3_probability_ci_halfwidths.{pdf,png,tiff}`; `table2_uncertainty_solver_settings.{csv,md}` | Revision assets / Table 2 / Figure S3 | Explicit historical duplicate of the stage17 revision-assets script family. |
| `analysis/stage8_finish_ready/run_make_figures.sh` | LEGACY | `simulation/stage3_uq_maps/`; `simulation/stage3_uq_maps/configs/baseline_50W_10s_4mm.yaml`; `simulation/stage3_uq_maps/configs/protocols.yaml`; `analysis/stage8_finish_ready/example_data/benchmark_points.csv` | `analysis/stage8_finish_ready/example_outputs/fig1_model_workflow.{pdf,png,tiff}`; `fig2_representative_fields.{pdf,png,tiff}`; `fig8_literature_benchmark.{pdf,png,tiff}` | Legacy Figures 1, 2, and 8 | Figure 2 is stage3-based, not stage17-native. |
| `analysis/stage8_fig128_export/run_make_figures.sh` | LEGACY | Same stage3-style inputs as `stage8_finish_ready` | `analysis/stage8_fig128_export/example_outputs/fig1_model_workflow.{pdf,png,tiff}`; `fig2_representative_fields.{pdf,png,tiff}`; `fig8_literature_benchmark.{pdf,png,tiff}` | Legacy Figures 1, 2, and 8 | Overlapping predecessor of `stage8_finish_ready`. |
| `analysis/stage7_freeze_ready/run_make_figures.sh` | LEGACY | `phase_prep_summary.csv`; `grid_convergence.csv`; `dt_convergence.csv`; `uq_summary.csv` | `analysis/stage7_freeze_ready/example_outputs/fig3_deterministic_summary.*`; `fig4_verification.*`; `fig5_transmural_probability_maps.*`; `fig6_overheat_probability_maps.*`; `fig7_tradeoff_depthrisk.*`; `figS1_depth_fraction_p50_maps.*`; `figS2_tradeoff_ptrans_pover.*` | Legacy Figures 3-7, S1, S2 | Three-protocol figure pack. |
| `analysis/stage7_freeze_final/run_make_figures.sh` | LEGACY | Same CSV set as `stage7_freeze_ready` | Same figure family as above | Legacy Figures 3-7, S1, S2 | Overlapping freeze directory. |
| `analysis/stage7_polishing_patch/run_make_figures.sh` | LEGACY | Same CSV set as `stage7_freeze_ready` | Same figure family as above | Legacy Figures 3-7, S1, S2 | Another overlapping patch directory. |
| `analysis/stage6_biorender_style/run_make_figures.sh` | LEGACY | `phase_prep_summary.csv`; `grid_convergence.csv`; `dt_convergence.csv`; `uq_summary.csv` | `analysis/stage6_biorender_style/example_outputs/style_preview_palette.*`; `fig3_deterministic_summary.*`; `fig4_verification.*`; `fig5_transmural_probability_maps.*`; `fig6_overheat_probability_maps.*`; `fig7_tradeoff_scatter.*`; `figS1_depth_fraction_p50_maps.*` | Legacy figure styling line | Uses stage3-style deterministic/UQ inputs. |
| `analysis/stage4_pubfigs_cmpb/run_make_figures.sh` | LEGACY | `phase_prep_summary.csv`; `grid_convergence.csv`; `dt_convergence.csv`; `uq_summary.csv` | `analysis/stage4_pubfigs_cmpb/example_outputs/fig3_deterministic_summary.*`; `fig4_verification.*`; `fig5_transmural_probability_maps.*`; `fig6_overheat_probability_maps.*`; `fig7_tradeoff_scatter.*`; `figS1_depth_fraction_p50_maps.*` | Early legacy Figures 3-7 line | Earliest split figure-script pack found in `analysis/`. |
| `manuscript/scripts/run_stage12.sh` | ARCHIVE | `BENCHMARK_CSV`; `MAIN_DIR`; `SUPP_DIR`; `CAPTIONS`; `SUBMISSION_OUT`; `FIG8_OUTBASE` environment variables | `manuscript/figures/main/fig8_literature_benchmark.{pdf,png,tiff}`; `manuscript/submission_package/figure_manifest.csv`; packaged main/supp figure files | Packaging layer for Figure 8 and submission bundle | Delivery-oriented wrapper, not current source-of-truth figure generator. |
| `manuscript/scripts/make_fig8_final.py` | ARCHIVE | A benchmark CSV with `source_id`, `protocol_key`, `reported_depth_mm`, `simulated_depth_mm` | Arbitrary `--outbase.{pdf,png,tiff}` | Figure 8 packaging/regeneration | Overlaps `analysis/stage8_finish_ready/src/make_fig8_literature_benchmark.py`. |
| `manuscript/scripts/package_submission_figures.py` | ARCHIVE | `manuscript/figures/main/`; `manuscript/figures/supplement/`; captions file | `manuscript/submission_package/` plus `figure_manifest.csv` | Submission package only | Copies files; does not generate scientific content. |

## Manuscript assets

- Current delivery-facing manuscript assets:
  - `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`
  - `papers/V13/CMBBE_submission_checklist.docx`
  - `papers/V13/cover_letter.docx`
  - `papers/V13/title_page.docx`
  - `papers/V13/CMBBE_figure_upload/`
- Figure manifest and packaged figure layer:
  - `manuscript/figures/manifest.csv`
  - `manuscript/figures/main/`
  - `manuscript/figures/supplement/`
  - `manuscript/submission_package/`
- Caption stubs:
  - `manuscript/captions/figure_caption_stubs.md`
  - `manuscript/captions/figure_caption_stubs_v2.md`
  - `manuscript/captions/figure_caption_stubs_v3.md`
- Older manuscript drafts:
  - `manuscript/paper/V0/`
  - `manuscript/paper/V2/`
  - `manuscript/paper/V3/`
  - `papers/V4/` through `papers/V12/`

## Output folders

| Path | Status | Contents | Notes |
| --- | --- | --- | --- |
| `simulation/stage17_controlled_rebuild/outputs/` | CURRENT | Stage17 deterministic outputs plus non-canonical carry-over folders | Mixed canonical and unclear legacy-named outputs coexist; some documented stage17 output names were `NOT FOUND` on disk while similarly named alternatives were present. |
| `simulation/stage16_uq_metrics_ready/outputs/` | LEGACY | Frozen three-protocol deterministic + UQ outputs | Still referenced by current revision-assets scripts. |
| `simulation/stage0_minimal/outputs/` | LEGACY | Minimal baseline and protocol-scan outputs | Earliest stage outputs. |
| `simulation/stage1_deterministic/outputs/` | LEGACY | Deterministic scan outputs | Older stage outputs. |
| `simulation/stage1p5_contact/outputs/` | LEGACY | Contact-scan stage outputs | Older stage outputs. |
| `simulation/stage2_phase_ready/outputs/` | LEGACY | Phase-prep stage outputs | Older stage outputs. |
| `simulation/stage3_uq_maps/outputs/` | LEGACY | Three-protocol deterministic + UQ outputs | Used by legacy figure lines. |
| `analysis/*/example_outputs/` | LEGACY or CURRENT depending on parent | Example rendered figures/tables | Preview outputs, not authoritative alone. |
| `manuscript/figures/` | ARCHIVE | Stored figure deliverables | Delivery layer for packaged figures. |
| `manuscript/submission_package/` | ARCHIVE | Submission bundle with copied figures/captions/manifest | Packaging layer only. |
| `papers/V13/CMBBE_figure_upload/` | ARCHIVE | Upload-ready PNG figure copies | README states files were copied from `papers/V12/figure_refresh_png/`. |
| `tmp/figure_qc/` | ARCHIVE | Temporary QC renders | Useful for audit clues, not authoritative generation sources. |
| `tmp/docs/` | ARCHIVE | Temporary rendered manuscript PDFs/PNGs | Temporary rendering products only. |

## Notebooks

- `NOT FOUND`
- `rg --files -g '*.ipynb'` returned no notebook files in the repository.

## Duplicate or overlapping implementations

- `analysis/stage17_methodology_figs/src/make_revision_assets.py` and `analysis/stage16_revision_figs/src/make_revision_assets.py` are overlapping revision-assets implementations.
- `analysis/stage8_fig128_export/` and `analysis/stage8_finish_ready/` are overlapping Figure 1/2/8 generators using stage3-style inputs.
- `analysis/stage7_freeze_ready/`, `analysis/stage7_freeze_final/`, and `analysis/stage7_polishing_patch/` are overlapping combined figure-pack directories for Figures 3-7 and supplements.
- `analysis/stage4_pubfigs_cmpb/` and `analysis/stage6_biorender_style/` are earlier split/styled figure lines that cover much of the same figure family as the stage7 packs.
- `manuscript/scripts/make_fig8_final.py` overlaps the Figure 8 plotting role of `analysis/stage8_finish_ready/src/make_fig8_literature_benchmark.py` and `analysis/stage8_fig128_export/src/make_fig8_literature_benchmark.py`.
- `simulation/stage17_controlled_rebuild/` retains overlapping config families:
  - `protocols.yaml`
  - `protocols_generic_fixed.yaml`
  - `protocols_stage17_fourway.yaml`
  - `phase_prep.yaml`
  - `phase_prep_stage17_fourway.yaml`
  - `wall_scan.yaml`
  - `wall_scan_stage17.yaml`
  - `cooling_scan.yaml`
  - `cooling_scan_stage17.yaml`
  - `contact_scan.yaml`
  - `contact_scan_stage17.yaml`
- `simulation/stage17_controlled_rebuild/` also retains UQ scripts/configs (`run_uq_fast.sh`, `run_uq_paper.sh`, `configs/uq_fast.yaml`, `configs/uq_paper.yaml`) even though the current README says stage16 uncertainty outputs remain the authoritative baseline.
