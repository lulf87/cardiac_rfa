# Methods Final Audit

## Scope

Current source-of-truth only:

- `simulation/stage17_controlled_rebuild/`
- `analysis/stage17_methodology_figs/`
- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`

This audit is for manuscript writing. It does **not** change scientific logic,
parameter values, validation scope, or benchmark values.

Companion row-level table:

- `METHODS_FINAL_PARAMETER_TABLE.csv`

## High-level outcome

The current stage17 manuscript line is now traceable enough to write a
methods-accurate paper section, but several implementation-critical details are
still missing or under-specified in the manuscript text.

Highest-priority writing actions:

1. **Revise the dimensional interpretation.**
   The current implementation is a planar Cartesian 2D cross-sectional solver
   with per-depth source scaling; the manuscript still uses wording that can be
   read as an explicit electrode-blood-myocardium subdomain model.
2. **Add the algorithmic source construction explicitly.**
   The current `q_reg` is algorithmic, not analytic. Do not write a closed-form
   `q_reg(x,y)` formula unless one is actually introduced in code.
3. **Add the exact controller implementation.**
   The manuscript currently states the target, ceiling, update period, and
   sample-and-hold logic, but not the exact sensor implementation, piecewise
   control law, or power bounds.
4. **Revise the contact/cooling coefficient reporting.**
   The exact current coefficient values are in YAML/code and should be written
   explicitly if the Methods are meant to be reproducible.
5. **Revise the verification chain description.**
   The current stage17 Figure 4 path is now stage17-native and uses
   controller-enabled, latency-enabled convergence CSVs.
6. **Leave the benchmark-scope boundary unchanged in substance.**
   The current benchmark wording is already appropriately bounded and should
   not be upgraded into validation language.

## 1) Exact current dimensional interpretation of the model

Belongs primarily in:

- `2.1 Reduced two-dimensional electro-thermal lesion model`
- `2.2 Geometry and computational domain`
- `2.3 Boundary and initial conditions`

Current implementation:

- The computational domain is a **planar Cartesian** cross-section built by
  `make_grid`, with lateral coordinate `x` and depth coordinate `y`.
- Domain depth is `wall_thickness_mm + bottom_buffer_mm`.
- No axisymmetric terms or rotational factors are present in the electrical or
  thermal assembly.
- The current stage17 Figure 1 script states:
  `No explicit blood subdomain in stage17; cooling enters through the top boundary profile.`
- The current top boundary is implemented as an effective Robin cooling
  condition; the code does **not** define a separate explicit blood region.
- `lesion_area_mm2` is a **2D cross-sectional area** computed from the
  wall-only lesion mask.
- Applied power is mapped into the 2D source through
  `power_per_depth_scale_W_per_m_per_W`, so the current implementation should
  be described as a **per-depth scaled planar 2D reduced model**, not as a
  direct 3D watt-to-volume model.

Current writing consequence:

- The manuscript should be revised so that the geometry and boundary-condition
  wording matches the current code and current Figure 1 source.
- In particular, wording that implies an explicit blood subdomain should be
  removed or narrowed.

## 2) Exact current algorithmic source construction

Belongs primarily in:

- `2.1 Reduced two-dimensional electro-thermal lesion model`
- `2.4 Comparator definition, control logic, and contact surrogate implementation`

Current implementation:

1. Solve the unit-potential electrical subproblem with top electrode segment at
   unit potential and bottom boundary grounded.
2. Compute the unit Joule field:
   `q_unit = sigma_S_per_m * (dphi_dx**2 + dphi_dy**2)`.
3. If `source_smoothing_mm > 0`, apply Gaussian smoothing:
   `q_reg = gaussian_filter(q_unit, sigma=(sigma_y, sigma_x), mode="nearest")`.
4. Shift the smoothed source downward in depth using:
   `shift_m = source_shift_per_mm_insertion * insertion_depth_mm * 1e-3`
   and `shift_source_in_depth(...)`.
5. Compute
   `total_per_depth = sum(q_reg) * dx * dy`.
6. Apply contact-dependent source scaling:
   `contact_scale = max(0.5, 1.0 + contact_power_gain_per_mm * (insertion_depth_mm - reference_insertion_mm))`.
7. Form the final RF source:
   `q = power_per_depth_scale_W_per_m_per_W * power_W * contact_scale * q_reg / total_per_depth`.

Critical writing point:

- The current implementation does **not** expose an analytic closed-form
  `q_reg(x,y)`.
- `q_reg` remains **algorithmic** and should be described that way unless the
  code is changed.

## 3) Exact current controller implementation

Belongs primarily in:

- `2.4 Comparator definition, control logic, and contact surrogate implementation`

Current selected controller:

- File:
  `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml`
- `enabled = true`
- `sensor_location = surface_adjacent`
- `target_temperature_C = 70.0`
- `ceiling_temperature_C = 80.0`
- `max_power_W = 90.0`
- `min_power_W = 15.0`
- `ramp_down_gain_W_per_C = 6.0`
- `sample_period_s = 0.05`

Current sensor implementation:

- `_surface_adjacent_temperature_C(T)` returns `T[row, :].max()`
- `row = 1` if at least two depth rows exist, else `row = 0`
- In the current baseline/stage17 use case, this is effectively the **maximum
  temperature along the first interior depth row across the full lateral
  domain**

Current control law:

- If `measured_temp_C <= target_temperature_C`, apply the upper allowed power
- If `measured_temp_C >= ceiling_temperature_C`, apply the lower allowed power
- Otherwise apply a linear ramp-down from the requested power with slope
  `ramp_down_gain_W_per_C`
- The returned power is clipped between the effective lower and upper bounds

Current update/hold logic:

- `controller_steps = round(sample_period_s / dt_s)`
- The controller updates only when `step_idx % controller_steps == 0`
- Between update times, the previous `applied_power_W` is held constant

Current delivered-energy rule:

- `delivered_energy_J += applied_power_W * dt_s`

Current protocol usage:

- The controller is active only for
  `vhpsd_90W_4s_controlled` in
  `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`

## 4) Exact current contact/source/cooling coefficient values

Belongs primarily in:

- `2.4 Comparator definition, control logic, and contact surrogate implementation`

Current baseline/source/contact values from
`simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml`:

- `power_per_depth_scale_W_per_m_per_W = 6.8`
- `source_smoothing_mm = 0.20`
- `insertion_depth_mm = 1.0` for the nominal baseline case
- `reference_insertion_mm = 1.0`
- `contact_power_gain_per_mm = 0.16`
- `source_shift_per_mm_insertion = 0.25`
- `cooling_h_W_per_m2K = 1500.0`
- `contact_h_reduction_per_mm = 0.35`
- `min_contact_h_scale = 0.50`
- `max_contact_h_scale = 1.40`

Current cooling implementation:

- Outside the footprint:
  `h_top = cooling_h_W_per_m2K`
- On the footprint:
  `h_top = cooling_h_W_per_m2K * clip(1 - contact_h_reduction_per_mm * (insertion_depth_mm - reference_insertion_mm), min_contact_h_scale, max_contact_h_scale)`

Current writing consequence:

- The manuscript already states the reduced contact-surrogate idea, but the
  exact current coefficient values are not all explicit in the current text
  extraction and should be written out if reproducibility is the goal.

## 5) Exact current latency implementation

Belongs primarily in:

- `2.4 Comparator definition, control logic, and contact surrogate implementation`

Current enabled latency config:

- File:
  `simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml`
- `enabled = true`
- `post_pulse_duration_s = 8.0`
- `record_dt_s = 0.05`

Current implementation:

- After the energized pulse, the solver advances
  `extra_latency_steps(post_pulse_duration_s, dt_s)` zero-source steps.
- During the latency window, the heat equation still advances, Arrhenius damage
  still accumulates, and `peak_T` continues to update.

Current gap:

- `record_dt_s` is present in the YAML config, but no current stage17 solver
  path consumes it.

## 6) Exact current lesion metric extraction rules

Belongs primarily in:

- `2.5 Material parameters and lesion metrics`

Current rules:

- Lesion boundary:
  `lesion_mask = omega_report >= lesion_omega_threshold`, with
  `lesion_omega_threshold = 1.0`
- Lesion depth:
  centerline interpolation to the `Omega = 1` crossing within the physical wall
- Lesion width:
  maximum connected lesion width across wall rows; if multiple islands occur on
  a row, the component closest to the centerline is used
- Lesion area:
  `sum(lesion_mask) * dx * dy * 1e6`, reported in `mm^2`
- Depth fraction:
  `lesion_depth_mm / wall_thickness_mm`
- Transmurality:
  `lesion_depth_mm >= wall_thickness_mm - 1e-6`
- Overheat area:
  wall-only area where `peak_T_report >= 100.0`, computed over the full
  energized-plus-latency run

Current writing consequence:

- `Omega = 1` is already explicit in the manuscript.
- The exact code definitions for depth, width, transmurality, lesion area, and
  overheat-area semantics should be added or revised if the Methods are meant
  to be technically auditable.

## 7) Exact current verification evidence chain

Belongs primarily in:

- `2.6 Numerical implementation and verification`

Current verification configuration:

- File:
  `simulation/stage17_controlled_rebuild/configs/convergence.yaml`
- Grid cases:
  `201 x 101`, `281 x 141`, `361 x 181`
- Time-step values:
  `0.10 s`, `0.05 s`, `0.025 s`

Current execution/data chain:

1. `simulation/stage17_controlled_rebuild/src/run_convergence.py`
2. Base config:
   `simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml`
3. Controller config:
   `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml`
4. Latency config:
   `simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml`
5. Output CSVs:
   - `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/grid_convergence.csv`
   - `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/dt_convergence.csv`
6. Stage17-native figure generator:
   `analysis/stage17_methodology_figs/src/make_fig4_stage17_verification.py`
7. Current Figure 4 outputs:
   - `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.pdf`
   - `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.png`
   - `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.tiff`

Metrics plotted in current stage17 Figure 4:

- relative error to the finest solution for `lesion_depth_mm`
- relative error to the finest solution for `peak_temperature_C`

Current writing consequence:

- The manuscript already states the grid set, time-step set, and selected
  production settings.
- It should be revised if you want the current verification chain to reflect
  the present stage17-native Figure 4 path and the current controller-enabled,
  latency-enabled convergence outputs.

## 8) Exact current benchmark-scope statement

Belongs primarily in:

- `2.9 Reference literature benchmark`
- `3.6 Reference benchmark status`
- `4. Discussion`

Current manuscript statement:

- no geometry-matched experimental dataset was available
- external comparison remained limited to a protocol-level literature-derived
  benchmark
- the benchmark is trend-level context rather than validation
- it does not validate device-level prediction
- it does not validate the generic temperature-limited comparator
- it does not distinguish fixed-power and temperature-limited `90 W / 4 s` as
  separate computational objects

Current writing consequence:

- The benchmark-scope boundary is already appropriate and should be left
  unchanged in substance.
- Do **not** strengthen this into validation language.

Current scoped provenance gap:

- Within the current source-of-truth defined for this audit
  (`stage17` simulation, `stage17` figures, `papers/V13` manuscript), a current
  benchmark-generation code path is `NOT FOUND`.
- Therefore, the benchmark scope statement is supported by the current
  manuscript wording, but not by a stage17-native benchmark plotting chain
  inside the scoped paths.

## Remaining `NOT FOUND` items

- Analytic closed-form `q_reg(x,y)` formula:
  `NOT FOUND`
- Explicit named time-stepping scheme label in code:
  `AMBIGUOUS`
- Solver tolerances:
  `NOT FOUND`
- Pinned package versions:
  `NOT FOUND`
- Current benchmark-generation path inside the strict scoped source-of-truth:
  `NOT FOUND`

## Manuscript-writing bottom line

If the Methods are revised to match the current stage17 code path, the most
important additions are:

- planar Cartesian 2D / no explicit blood subdomain / per-depth scaling
- algorithmic `q_reg` construction
- exact controller sensor and piecewise control law
- exact current contact/cooling coefficient values
- exact lesion-width / transmurality / overheat-area rules
- stage17-native Figure 4 verification chain

What should **not** be added:

- a fabricated analytic `q_reg` formula
- a stronger validation claim for the benchmark
- fabricated current-source simulated widths for Table 3

