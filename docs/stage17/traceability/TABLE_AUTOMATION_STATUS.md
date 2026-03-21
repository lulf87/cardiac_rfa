# Table Automation Status

## Scope

This audit checks the current V13 manuscript tables against repository configs,
data files, and exportable automation paths.

Created automation scripts:

- `export_table1_stage17_protocols.py`
- `export_table2_stage17_controls.py`
- `export_table3_benchmark_trace.py`

Default generated outputs:

- `tmp/table_exports/table1_stage17_protocols.csv`
- `tmp/table_exports/table1_stage17_protocols.md`
- `tmp/table_exports/table2_stage17_controls.csv`
- `tmp/table_exports/table2_stage17_controls.md`
- `tmp/table_exports/table3_benchmark_trace.csv`
- `tmp/table_exports/table3_benchmark_trace.md`

## Summary

| Table | Status | What is automated | What remains manual |
| --- | --- | --- | --- |
| Table 1 | PARTIAL | Power, duration, controller flag, and computed maximum nominal energy from `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml` | Manuscript-facing protocol labels, role text, and the temp-limited row display string `up to 360` |
| Table 2 | PARTIAL | Grid, time step, wall/cooling/insertion levels, comparator set, controller target/ceiling, controller sample period, latency window, and phase-grid size from current stage17 configs | Controller sensor wording, primary outputs wording, secondary proxies wording, calibration-status sentence, supplementary-UQ sentence |
| Table 3 | PARTIAL | Reported depth, simulated depth, and reported width trace to the current benchmark CSV used by the Figure 8 script | Simulated widths do not exist in the current benchmark CSV and are only traceable through historical `benchmark_points_v3.csv` files |

## Current manuscript evidence

Current V13 manuscript table source:

- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`

Observed current table content:

- Table 1 has 4 protocol rows for the stage17 four-comparator line.
- Table 2 has 15 item/value rows.
- Table 3 has 3 benchmark rows for `Nakagawa2021`.

## Table 1

### Automated source

- `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`

### Export coverage

The Table 1 exporter reads:

- protocol key
- `power_W`
- `duration_s`
- `use_controller`

It computes:

- `computed_max_energy_J = power_W * duration_s`

### Manual fields

The following current manuscript-facing fields are not stored in the protocol
config and are therefore marked `MANUAL` in the exporter output:

- `Protocol` display label
- `Role in comparison`
- the temperature-limited row display string `up to 360`

Manual source file used for trace:

- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx` :: Table 1

## Table 2

### Automated sources

- `simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml`
- `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`
- `simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml`
- `simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml`
- `simulation/stage17_controlled_rebuild/configs/phase_prep_stage17_fourway.yaml`

### Rows exported automatically

- `Deterministic production grid`
- `Time step`
- `Wall thickness levels`
- `Nominal cooling coefficients`
- `Nominal insertion levels`
- `Comparator set`
- `Controller target / ceiling`
- `Controller sample period`
- `Post-pulse latency window`
- `Phase-preparation grid size`

### Rows still manual

- `Controller sensor`
- `Primary interpretive outputs`
- `Secondary internal proxies`
- `Calibration status`
- `Supplementary UQ status`

Manual source file used for trace:

- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx` :: Table 2

Notes:

- `Controller sensor` is only stored in config as `surface_adjacent`; the exact
  manuscript phrase `Surface-adjacent temperature surrogate` is not stored
  verbatim in a current config file.
- The current controller config also contains values not surfaced in Table 2,
  including:
  - `min_power_W`
  - `max_power_W`
  - `ramp_down_gain_W_per_C`
- The current latency config also contains `record_dt_s`, which is not exposed
  in Table 2.

## Table 3

### Current figure-script source

Current Figure 8 benchmark script default:

- `manuscript/scripts/run_stage12.sh`

Current default benchmark CSV used by that script:

- `analysis/stage8_finish_ready/example_data/benchmark_points.csv`

Observed duplicate with identical benchmark depths/widths but still blank
simulated widths:

- `manuscript/example_data/benchmark_points_v2.csv`

### What the current benchmark CSV does cover

The current benchmark CSV covers:

- `reported_depth_mm`
- `simulated_depth_mm`
- `reported_width_mm`

for the three fixed-power protocol keys:

- `standard_30W_30s`
- `hpsd_50W_10s`
- `vhpsd_90W_4s`

### What it does not cover

The current benchmark CSV does **not** contain:

- `simulated_width_mm`

### Historical width trace

The current V13 Table 3 simulated widths match:

- `papers/V7/tables/source_csv/benchmark_points_v3.csv`

Identical duplicates were also found at:

- `papers/V6/tables/source_csv/benchmark_points_v3.csv`
- `papers/V7/tables/main/table3_literature_benchmark_points.csv`

Because the repository does not expose a current code path that assembles V13
Table 3 from one single source file, the exporter marks simulated-width cells as
`HISTORICAL_TRACE` rather than pretending they come from the current Figure 8
benchmark CSV.

## Dependency note

The exporters rely on:

- `PyYAML`
- `python-docx`

`python-docx` is required because the current manuscript table text is stored in
`papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`.
