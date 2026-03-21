# Stage17 Methods Reproducibility Notes

This note records the implementation details that are currently encoded in the
stage17 rebuild and should be reflected explicitly in the Methods text.

## Canonical stage17 execution path

- Base geometry/material config:
  `simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml`
- Four-way protocol list:
  `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`
- Selected generic controller:
  `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml`
- Enabled post-pulse latency:
  `simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml`
- Canonical phase-preparation driver:
  `simulation/stage17_controlled_rebuild/run_phase_prep.sh`
- Canonical full deterministic driver:
  `simulation/stage17_controlled_rebuild/run_all.sh`

## Reduced source construction

The implemented source is not an analytic `q_reg(x, y)` expression. Instead, it
is generated from the reduced electrical subproblem in the following sequence:

1. Solve the unit-potential Laplace problem on the planar 2D grid.
2. Compute the unit Joule field
   `q_unit = sigma * (dphi_dx^2 + dphi_dy^2)`.
3. Apply Gaussian smoothing with `source_smoothing_mm`.
4. Shift the smoothed source downward by
   `source_shift_per_mm_insertion * insertion_depth_mm`.
5. Normalize by the 2D area integral of the shifted field.
6. Scale by
   `power_per_depth_scale_W_per_m_per_W * power_W * max(0.5, 1 + beta_P * (d_ins - d_ref))`.

Current canonical values in the baseline stage17 config:

- `power_per_depth_scale_W_per_m_per_W = 6.8`
- `source_smoothing_mm = 0.20`
- `reference_insertion_mm = 1.0`
- `contact_power_gain_per_mm = 0.16`
- `source_shift_per_mm_insertion = 0.25`

## Cooling surrogate

The top boundary cooling coefficient is spatially piecewise:

- Outside the electrode footprint: `h_top = cooling_h_W_per_m2K`
- On the electrode footprint:
  `h_top = cooling_h_W_per_m2K * clip(1 - beta_h * (d_ins - d_ref), h_min, h_max)`

Current canonical values:

- `contact_h_reduction_per_mm = 0.35`
- `min_contact_h_scale = 0.50`
- `max_contact_h_scale = 1.40`

## Generic temperature-limited comparator

The selected generic controller in stage17 is:

- `sensor_location = surface_adjacent`
- `target_temperature_C = 70.0`
- `ceiling_temperature_C = 80.0`
- `max_power_W = 90.0`
- `min_power_W = 15.0`
- `ramp_down_gain_W_per_C = 6.0`
- `sample_period_s = 0.05`

The current implementation measures the sensor temperature as the maximum value
on the first interior temperature row. The power law is piecewise:

- if `T_meas <= target`, apply `min(requested_power, max_power)`
- if `T_meas >= ceiling`, apply `min_power` clipped by `max_power`
- otherwise, linearly ramp down from the requested power with slope
  `ramp_down_gain_W_per_C`

Between update times, the previously applied power is held constant.

## Latency window

The enabled latency config adds an `8.0 s` post-pulse thermal continuation using
the same heat step with zero RF source. Arrhenius accumulation continues during
this window.

## Reported metrics and extraction rules

- Lesion depth: centerline interpolation to `Omega = 1` within the physical wall
- Lesion width: maximum connected `Omega >= 1` width across wall rows
- Lesion area: 2D lesion-mask area in `mm^2`
- Depth fraction: `lesion_depth_mm / wall_thickness_mm`
- Transmurality: `lesion_depth_mm >= wall_thickness_mm`
- Overheat area: physical-wall area where `peak_temperature_C >= 100`
- Delivered energy: discrete sum of `applied_power_W * dt_s`
- Mean applied power: delivered energy divided by energized pulse duration

## Remaining manuscript-only gaps

These items are still not solved by code consolidation alone and must be handled
explicitly in the manuscript:

- the planar 2D per-depth interpretation and unit closure for applied wattage
- calibration provenance for the retained source/cooling coefficients
- the validation boundary, which remains trend-level rather than geometry-matched
