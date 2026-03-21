# Verification Audit

## Scope

This audit reviews repository evidence for:

- mesh / grid refinement
- time-step refinement
- domain-size / buffer sensitivity
- solver convergence checks
- parameter sensitivity
- uncertainty analysis
- benchmark / external comparison
- validation-oriented data scaffolds

The goal is to separate:

1. evidence that exists in code or data
2. evidence referenced in the manuscript but not reproducible from the repo
3. analyses that appear to be missing entirely

`VERIFICATION_CASES.csv` records the case families and evidence artifacts found.

## Evidence That Exists in Code/Data

### 1. Grid and time-step refinement evidence exists

Current-stage17 convergence code exists at:

- `simulation/stage17_controlled_rebuild/src/run_convergence.py`
- `simulation/stage17_controlled_rebuild/configs/convergence.yaml`

Observed current-style convergence data exist at:

- `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/grid_convergence.csv`
- `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/dt_convergence.csv`

What this supports:

- three-grid refinement at `201 x 101`, `281 x 141`, `361 x 181`
- three-step refinement at `0.10 s`, `0.05 s`, `0.025 s`
- raw output comparison for lesion depth, width, area, depth fraction, peak temperature, delivered energy, and mean applied power

What it does not provide:

- solver residual histories
- iterative stopping criteria
- domain-size or buffer sensitivity
- worst-case convergence outside the nominal 4-mm baseline

Legacy duplicate convergence families also exist in:

- `simulation/stage1_deterministic/`
- `simulation/stage1p5_contact/`
- `simulation/stage2_phase_ready/`
- `simulation/stage3_uq_maps/`
- `simulation/stage16_uq_metrics_ready/`

These are real historical evidence artifacts, not placeholders.

### 2. Comparator and latency contrast evidence exists

The current manuscript's short high-power methodological claims are supported by
paired summary outputs in the repo.

Latency contrast for fixed `90 W / 4 s`:

- without latency:
  `simulation/stage17_controlled_rebuild/outputs/protocol_scan/vhpsd_90W_4s/summary.yaml`
- with `8 s` latency:
  `simulation/stage17_controlled_rebuild/outputs/protocol_scan_stage17_fourway/vhpsd_90W_4s_fixed/summary.yaml`

This pair reproduces the manuscript's key latency result:

- depth increases from about `1.302 mm` to `1.695 mm`
- area increases from about `3.486 mm^2` to `4.599 mm^2`
- peak temperature remains unchanged at about `83.46 C`

Fixed-vs-temperature-limited baseline contrast:

- fixed:
  `simulation/stage17_controlled_rebuild/outputs/smoke_fixed_stage17/summary.yaml`
- controlled:
  `simulation/stage17_controlled_rebuild/outputs/smoke_controlled_stage17/summary.yaml`

This supports the current comparator claim that the generic temperature-limited
case slightly reduces delivered energy and peak temperature with only a small
depth reduction.

Important limitation:

- these contrasts exist as paired outputs, not as a dedicated sensitivity or
  verification runner

### 3. Deterministic parameter-sweep evidence exists

Current-stage17 deterministic sweep outputs exist at:

- `simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv`
- `simulation/stage17_controlled_rebuild/outputs/wall_scan_stage17_fourway/wall_protocol_summary.csv`
- `simulation/stage17_controlled_rebuild/outputs/cooling_scan_stage17_fourway/cooling_protocol_summary.csv`
- `simulation/stage17_controlled_rebuild/outputs/contact_scan_stage17_fourway/contact_protocol_summary.csv`

These vary:

- wall thickness
- nominal cooling coefficient
- insertion depth
- protocol / comparator

They output:

- lesion depth
- lesion width
- lesion area
- depth fraction
- transmurality
- overheat area
- peak temperature
- delivered energy
- mean applied power

Interpretation:

- this is strong deterministic parameter-variation evidence
- it is not a formal sensitivity analysis with effect sizes, ranking, or UQ on
  parameter influence

### 4. Frozen three-protocol uncertainty evidence exists

The strongest uncertainty-analysis evidence in the repo is still the frozen
stage16 three-protocol line:

- code:
  `simulation/stage16_uq_metrics_ready/src/run_uq_maps.py`
- config:
  `simulation/stage16_uq_metrics_ready/configs/uq_paper.yaml`
- outputs:
  `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_summary.csv`
  `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_samples.csv`
  `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_overview.csv`

What it does:

- treats insertion depth and cooling coefficient as uncertain inputs
- uses `64` samples per nominal cell
- computes Wilson confidence intervals for transmurality and overheating
  probabilities
- stores depth-fraction quantiles and mean lesion metrics

This is complete as legacy uncertainty evidence.

The main uncertainty-stability summary artifact also exists:

- `analysis/stage16_revision_figs/example_outputs/figS3_probability_ci_halfwidths.png`

This is backed by:

- `analysis/stage16_revision_figs/src/make_revision_assets.py`
- `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_summary.csv`

### 5. Exploratory uncertainty evidence exists

Earlier exploratory UQ outputs exist in stage3:

- `simulation/stage3_uq_maps/src/run_uq_maps.py`
- `simulation/stage3_uq_maps/outputs/uq_fast/uq_summary.csv`
- `simulation/stage3_uq_maps/outputs/uq_fast/uq_overview.csv`

Stage3 README explicitly frames these as an initial uncertainty layer and quick
testing path, not the final paper-grade evidence.

### 6. Benchmark / external comparison evidence exists, but only at trend level

Current benchmark figure code exists at:

- `manuscript/scripts/make_fig8_final.py`
- `manuscript/scripts/run_stage12.sh`

Current benchmark figure input exists at:

- `analysis/stage8_finish_ready/example_data/benchmark_points.csv`

Historical width-complete benchmark tables also exist at:

- `papers/V6/tables/source_csv/benchmark_points_v3.csv`
- `papers/V7/tables/source_csv/benchmark_points_v3.csv`

What this supports:

- three-protocol benchmark comparison
- trend-level depth comparison
- current Figure 8 generation path

What it does not support:

- geometry-matched validation
- validation of the temperature-limited `90 W / 4 s` comparator
- a structured current benchmark dataset populated under
  `data/literature_benchmark/processed/`

### 7. Validation scaffolding exists, but it is empty

The repository contains structured benchmark scaffolds:

- `data/literature_benchmark/processed/calibration_points.csv`
- `data/literature_benchmark/processed/validation_points.csv`
- `docs/stage17/02_benchmark_sources.md`

However:

- both CSV files contain headers only
- no populated calibration rows were found
- no populated validation rows were found

This is scaffolding, not actual validation evidence.

### 8. Exploratory controller-tuning evidence exists

The repository contains controller trial configs:

- `simulation/stage17_controlled_rebuild/configs/controller_trial_soft.yaml`
- `simulation/stage17_controlled_rebuild/configs/controller_trial_mid.yaml`
- `simulation/stage17_controlled_rebuild/configs/controller_trial_hard.yaml`

Observed trial outputs exist at:

- `simulation/stage17_controlled_rebuild/outputs/tune_soft_controller_only/summary.yaml`
- `simulation/stage17_controlled_rebuild/outputs/tune_mid_controller_only/summary.yaml`
- `simulation/stage17_controlled_rebuild/outputs/tune_hard_controller_only/summary.yaml`

This is the closest thing to controller-parameter sensitivity found in the
repo, but it is clearly exploratory:

- no dedicated runner was found
- no summary table or sweep manifest was found
- the soft and mid trial outputs collapse back to the nominal fixed-power-like
  result in the observed baseline case

## Evidence Referenced in Manuscript but Not Reproducible From Repo

### 1. Current four-way uncertainty evidence is not reproducible

The current V13 manuscript keeps uncertainty figures as supplementary context,
but the repo does not contain a reproducible four-way uncertainty workflow for
the stage17 comparator-aware line.

Why:

- `simulation/stage17_controlled_rebuild/run_uq_paper.sh` exists
- but it still points to:
  - `configs/baseline_50W_10s_4mm.yaml`
  - `configs/protocols.yaml`
- that protocol file is the old three-protocol set:
  - `standard_30W_30s`
  - `hpsd_50W_10s`
  - `vhpsd_90W_4s`
- `simulation/stage17_controlled_rebuild/outputs/uq_paper/` is empty in the
  current workspace

Conclusion:

- a current four-way comparator-aware uncertainty analysis is referenced
  indirectly by scope language, but is not reproducible from the repo

### 2. The exact current Figure 4 evidence chain is incomplete

Current code/data for stage17 convergence do exist, but the current artifact
chain is incomplete:

- README and `run_all.sh` expect `outputs/convergence_stage17_controlled/`
- the observed current artifact is `outputs/convergence_stage17_controlled_check/`
- legacy `outputs/convergence/` also exists in the same stage17 directory

Conclusion:

- stage17 verification evidence exists
- the exact current manuscript-facing artifact chain is not fully consolidated

### 3. Supplementary Figure S3 support exists only through the legacy line

The current manuscript references Supplementary Figure S3 as legacy context.
The repository does contain the CI half-width figure logic and a legacy output,
but not a clean current package path:

- script family:
  `analysis/stage16_revision_figs/src/make_revision_assets.py`
  and duplicate
  `analysis/stage17_methodology_figs/src/make_revision_assets.py`
- observed artifact:
  `analysis/stage16_revision_figs/example_outputs/figS3_probability_ci_halfwidths.png`

Conclusion:

- the evidence exists
- the current submission-facing packaging is incomplete

### 4. The manuscript's benchmark table is not fully generated from current code

Current Figure 8 generation uses:

- `manuscript/scripts/make_fig8_final.py`
- `analysis/stage8_finish_ready/example_data/benchmark_points.csv`

But the current manuscript's width-complete Table 3 aligns with the historical
`benchmark_points_v3.csv` files, not the current starter CSV.

Conclusion:

- the benchmark comparison exists
- the exact current benchmark table is not reproducible from a single current
  code path in the repo

### 5. Generalized-polynomial-chaos wording is not supported by current code

The current V13 manuscript refers to the supplementary uncertainty workflow as
reflecting a prior generalized-polynomial-chaos treatment.

Repo search did not find a generalized-polynomial-chaos implementation.
What was found instead:

- `simulation/stage3_uq_maps/src/run_uq_maps.py`
- `simulation/stage16_uq_metrics_ready/src/run_uq_maps.py`
- `simulation/stage17_controlled_rebuild/src/run_uq_maps.py`

These implement:

- stratified / Latin-hypercube-style normal sampling with clipping
- Wilson confidence intervals

Conclusion:

- the current repository does not reproduce a generalized-polynomial-chaos UQ
  workflow

## Analyses That Appear to Be Missing Entirely

### 1. Domain-size or buffer sensitivity

I found no evidence of:

- bottom-buffer variation
- domain-width variation
- electrical-ground depth variation
- explicit domain-size sensitivity study

Repo-wide search only found `bottom_buffer_mm: 4.0` as a fixed setting across
the simulation stages and outputs.

### 2. Formal solver-convergence diagnostics

The code uses direct sparse linear algebra:

- `spsolve`
- `factorized`

in:

- `simulation/stage17_controlled_rebuild/src/model_fd.py`
- `simulation/stage16_uq_metrics_ready/src/model_fd.py`

But I found no repository evidence of:

- residual tracking
- solver tolerance reporting
- stopping-criterion logging
- matrix-condition analysis

So the repo has discretization refinement evidence, but not a separate
solver-convergence audit.

### 3. Formal parameter sensitivity analysis

I found no formal:

- local sensitivity study
- global sensitivity study
- Sobol / Morris / variance-based sensitivity
- sensitivity ranking for source/contact/controller parameters

In particular, I found no systematic sensitivity study for:

- `power_per_depth_scale_W_per_m_per_W`
- `contact_power_gain_per_mm`
- `contact_h_reduction_per_mm`
- controller target / ceiling / min power / ramp-down gain
- latency duration

The closest evidence is the deterministic parameter sweeps and ad hoc controller
trial outputs, which are exploratory rather than formal sensitivity analyses.

### 4. Current four-way uncertainty analysis

No complete uncertainty-analysis artifact was found for the current stage17
four-way comparator line that distinguishes:

- `vhpsd_90W_4s_fixed`
- `vhpsd_90W_4s_controlled`

### 5. Geometry-matched validation

I found no:

- geometry-matched experimental dataset
- device-specific comparator validation
- validation notebook
- validation result table for the temperature-limited comparator

The benchmark remains protocol-level and trend-level only.

### 6. Validation notebooks

Running a repository-wide search outside `.venv` returned no `.ipynb` files.

Conclusion:

- no validation notebooks were found
- no dedicated notebook-style verification reports were found

## Bottom Line

The repository has real verification and uncertainty evidence, but it is split
across two different evidentiary lines:

- `CURRENT` stage17 deterministic comparator-aware evidence:
  convergence checks, latency contrast, fixed-vs-controlled baseline contrast,
  deterministic sweeps
- `FROZEN / LEGACY` three-protocol evidence:
  paper-level UQ, Wilson CI summaries, legacy benchmark tables

The strongest missing pieces are:

1. no formal domain-size / buffer sensitivity
2. no formal parameter sensitivity
3. no current four-way uncertainty analysis
4. no geometry-matched validation
5. no structured populated validation dataset

So the repository supports:

- baseline discretization verification
- deterministic comparator comparisons
- legacy three-protocol UQ and trend-level benchmarking

But it does not yet support:

- a fully closed VVUQ chain for the current four-way comparator-aware stage17
  manuscript line
