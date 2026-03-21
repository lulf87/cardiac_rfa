# Stage17 Figure Authority

## Scope

This file locks the V13 manuscript figure source-of-truth to the current
stage17 figure line where a current stage17 generator and output can be located.

This is an authority decision, not a silent packaging replacement.

- Current authoritative figure source directory:
  `analysis/stage17_methodology_figs/`
- Legacy packaged main figures retained for reference:
  `papers/V13/CMBBE_figure_upload/`
- Legacy packaged supplementary figures retained for reference:
  `manuscript/submission_package/`

No legacy files were deleted, moved, or overwritten in this step.

## Status meanings

- `CURRENT`: use the stage17 figure output as the source-of-truth for the
  manuscript line
- `LEGACY_REFERENCE`: keep the existing packaged file as a retained reference;
  this step does not migrate it to stage17
- `UNRESOLVED`: do not guess a current replacement because a clean stage17
  figure path was not located

## Authority decisions

### CURRENT

- `Figure 1` -> `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.{pdf,png,tiff}`
- `Figure 3` -> `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.{pdf,png,tiff}`
- `Figure 4` -> `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.{pdf,png,tiff}`
- `Figure 5` -> `analysis/stage17_methodology_figs/example_outputs/fig5_depth_fraction_fixed_vs_controlled.{pdf,png,tiff}`
- `Figure 6` -> `analysis/stage17_methodology_figs/example_outputs/fig6_peak_temperature_fixed_vs_controlled.{pdf,png,tiff}`
- `Figure 7` -> `analysis/stage17_methodology_figs/example_outputs/fig7_controlled_minus_fixed_maps.{pdf,png,tiff}`

### UNRESOLVED

- `Figure 2`
  Current stage17 candidate: `NOT FOUND`

Figure 2 is intentionally left unresolved rather than patched by guesswork.

### LEGACY_REFERENCE

- `Figure 8`
  This authority lock does not migrate the benchmark figure into stage17.
  Retain the existing benchmark path outside `analysis/stage17_methodology_figs/`.
- `Figure S1`
  Retain as a legacy supplementary reference figure.
- `Figure S2`
  Retain as a legacy supplementary reference figure.

## Concise caption-vs-file mismatches

- `Figure 1`
  Legacy naming and legacy caption stubs refer to an explicit blood pool,
  perfusion, and probabilistic outputs. The current stage17 figure instead says
  `No explicit blood subdomain in stage17`, fixes perfusion at zero, and shows
  the generic controller plus latency continuation.

- `Figure 3`
  The legacy packaged file and manifest name `fig3_deterministic_summary`
  describe an older summary artifact. The current stage17 line uses
  `fig_stage17_deterministic_fourway`, which matches the four-protocol
  comparator framing rather than the older three-protocol summary.

- `Figure 4`
  The legacy packaged file predates the current stage17-native verification
  generator. The current stage17 line now uses
  `fig4_stage17_verification`, which reads the checked stage17 convergence CSVs
  directly and recomputes relative errors from the exported raw metrics.

- `Figure 5`
  The legacy packaged file name `fig5_transmural_probability_maps` implies a
  probability/UQ figure. The current stage17 replacement is
  `fig5_depth_fraction_fixed_vs_controlled`, a deterministic comparator map.

- `Figure 6`
  The legacy packaged file name `fig6_overheat_probability_maps` implies an
  overheating-probability figure. The current stage17 replacement is
  `fig6_peak_temperature_fixed_vs_controlled`, a deterministic peak-temperature
  map.

- `Figure 7`
  The legacy packaged file name `fig7_tradeoff_depthrisk` implies a trade-off
  scatter. The current stage17 replacement is
  `fig7_controlled_minus_fixed_maps`, a controlled-minus-fixed difference-map
  figure.

## Verified current stage17 outputs

The following current stage17 candidate files were confirmed to exist:

- `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.png`
- `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.png`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.png`
- `analysis/stage17_methodology_figs/example_outputs/fig5_depth_fraction_fixed_vs_controlled.png`
- `analysis/stage17_methodology_figs/example_outputs/fig6_peak_temperature_fixed_vs_controlled.png`
- `analysis/stage17_methodology_figs/example_outputs/fig7_controlled_minus_fixed_maps.png`

## Practical rule going forward

- When a manuscript-facing task asks for the current Figure 1, 3, 4, 5, 6, or 7,
  start from `analysis/stage17_methodology_figs/`, not from the packaged V13
  PNGs.
- Do not overwrite `papers/V13/CMBBE_figure_upload/Figure1.png` through
  `Figure7.png` silently.
- If the delivery package needs refreshing, that should be a separate explicit
  packaging step after caption and manuscript references are updated.
