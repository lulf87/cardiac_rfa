# Table 2 Final Methods Wording

## Scope

This note finalizes the **manuscript-facing Methods wording** for Table 2 using
the current source-of-truth only:

- `simulation/stage17_controlled_rebuild/`
- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`

It does **not** change scientific logic or parameter values.

## Final wording for the currently manual Table 2 rows

These rows are the ones that remained `MANUAL` in the current table exporter
and should be treated as the finalized Methods-facing wording for Table 2.

| Item | Final wording |
| --- | --- |
| `Controller sensor` | `Surface-adjacent temperature surrogate (implemented in the current stage17 code as the maximum temperature along the first interior depth row, i.e. T[1, :].max() for the production grid)` |
| `Primary interpretive outputs` | `Lesion depth, depth fraction, delivered energy, mean applied power, and peak temperature` |
| `Secondary internal proxies` | `Lesion width, lesion area, and overheat area (wall-only area with peak temperature >= 100 C over the energized-plus-latency run)` |
| `Calibration status` | `Contact-dependent source-gain and footprint-cooling surrogate coefficients were retained from the preceding reduced implementation; no formal re-estimation or identifiability analysis was performed in the current stage17 manuscript line` |
| `Supplementary UQ status` | `Reference uncertainty figures from the frozen fixed-power three-protocol formulation are retained for completeness only and are not the primary evidentiary basis for the current comparator-aware stage17 conclusions` |

## Current controller values not shown in Table 2 but relevant to reproducibility

The following current controller values are present in the active stage17
implementation and are relevant to reproducibility, even though they are not
currently surfaced in Table 2:

| Parameter | Current value | Unit | Source |
| --- | --- | --- | --- |
| `sensor_location` | `surface_adjacent` | N/A | `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml` |
| `target_temperature_C` | `70.0` | `C` | `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml` |
| `ceiling_temperature_C` | `80.0` | `C` | `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml` |
| `sample_period_s` | `0.05` | `s` | `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml` |
| `max_power_W` | `90.0` | `W` | `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml` |
| `min_power_W` | `15.0` | `W` | `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml` |
| `ramp_down_gain_W_per_C` | `6.0` | `W per C` | `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml` |

Current implementation note:

- The sensor is not merely labeled `surface_adjacent` in config.
- In the current solver, the measured controller temperature is computed by
  `_surface_adjacent_temperature_C(T)` in
  `simulation/stage17_controlled_rebuild/src/model_fd.py`, which returns the
  maximum temperature along the first interior depth row.

## Latency values relevant to Table 2

Current active latency values:

| Parameter | Current value | Unit | Source | Note |
| --- | --- | --- | --- | --- |
| `post_pulse_duration_s` | `8.0` | `s` | `simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml` | Active and used by the solver |
| `record_dt_s` | `0.05` | `s` | `simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml` | Present in config but not consumed by the current solver path |

## Recommended manuscript handling

- Keep the existing Table 2 rows for grid, time step, wall thickness levels,
  cooling levels, insertion levels, comparator set, controller target/ceiling,
  controller sample period, post-pulse latency window, and phase-preparation
  grid size.
- Replace or confirm the five rows above with the finalized wording in this
  file.
- If Table 2 must stay compact, the three most important reproducibility values
  that still need prose support outside the table are:
  - `max_power_W = 90.0`
  - `min_power_W = 15.0`
  - `ramp_down_gain_W_per_C = 6.0`

## Methods-safe note

This wording is intended for **Methods only**.

It does not:

- upgrade the benchmark into validation language
- imply catheter-specific control logic
- imply that the supplementary UQ figures belong to the current stage17
  comparator evidence chain
