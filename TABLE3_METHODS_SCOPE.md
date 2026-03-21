# Table 3 Methods Scope

## Scope

This note defines a **Methods-safe benchmark scope** for Table 3 using the
current repository evidence without fabricating simulated widths.

Current benchmark source used for the depth-safe chain:

- `analysis/stage8_finish_ready/example_data/benchmark_points.csv`

Historical-trace width source:

- `papers/V7/tables/source_csv/benchmark_points_v3.csv`

Current manuscript source:

- `papers/V13/CMBBE_RF_ablation_reduced_model_main.docx`

## Methods-safe split

### A. Current benchmark fields traced to the current CSV

These fields are traced directly to the current benchmark CSV:

- `source_id`
- `protocol_key`
- `reported_depth_mm`
- `simulated_depth_mm`
- `reported_width_mm`
- `notes`

Current CSV:

- `analysis/stage8_finish_ready/example_data/benchmark_points.csv`

Meaning:

- These values support a **protocol-level, trend-context benchmark**.
- They are appropriate for a methods-safe description of the benchmark as a
  depth-oriented external context dataset.
- They do **not** validate the generic temperature-limited comparator.
- They do **not** establish geometry-matched validation.

### B. Historical-trace width fields

These fields are **not** traced to the current benchmark CSV:

- `simulated_width_mm`

Current status:

- `simulated_width_mm` is blank in
  `analysis/stage8_finish_ready/example_data/benchmark_points.csv`
- The values currently shown in manuscript Table 3 are traced only through the
  historical file:
  `papers/V7/tables/source_csv/benchmark_points_v3.csv`

Meaning:

- Simulated widths are **historical-trace values**, not current single-source
  benchmark exports.
- If widths are retained in the manuscript, they should be marked as
  **historical-trace** and not treated as primary validation targets.
- They should not be used as the main evidentiary basis for the Methods
  benchmark description.

## Recommended Methods description

Recommended Methods-safe description:

> External comparison was limited to a protocol-level literature-derived
> benchmark. For the current reproducible chain, the benchmark fields directly
> traced to the current CSV are source label, protocol key, reported lesion
> depth, simulated lesion depth, and reported lesion width. Simulated lesion
> widths shown in the retained manuscript table are historical-trace values from
> an earlier table-source CSV and should not be interpreted as current
> single-source benchmark exports or as primary validation targets.

## Recommended handling in manuscript Table 3

### Preferred Methods-safe option

- Use the depth-oriented benchmark only:
  - `Source / matched point`
  - `Protocol`
  - `Reported depth (mm)`
  - `Simulated depth (mm)`

This export is provided in:

- `table3_depth_only.csv`

### If width columns are retained

Use explicit trace labeling:

- `Reported width (mm)`:
  current benchmark CSV trace
- `Simulated width (mm)`:
  historical-trace only

Recommended caption or footnote language:

> Simulated width values are retained as historical-trace benchmark fields from
> an earlier table-source CSV and are not treated here as primary validation
> targets or as current single-source benchmark exports.

## What this scope does not allow

- No fabricated `simulated_width_mm`
- No upgrade from benchmark context to validation claim
- No claim that Table 3 is fully stage17-native

