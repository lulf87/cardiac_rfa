# Minimal Reproducibility Runbook

## Scope

This runbook documents the smallest current reproducibility path that can be
located in the repository after the current safe stage17 traceability
reorganization.

The current manuscript-facing implementation is the stage17 deterministic branch:

- Simulation: `simulation/stage17_controlled_rebuild/`
- Figure generation: `analysis/stage17_methodology_figs/`

This runbook does not treat older stage folders as the primary path unless
explicitly noted as a blocker or legacy dependency.

Detailed current stage17 audits and provenance notes now live under:

- `docs/stage17/traceability/`

## Current authoritative locations

- Current nominal simulation case:
  `simulation/stage17_controlled_rebuild/run_fixed_smoke.sh`
- Current all-in-one deterministic workflow:
  `simulation/stage17_controlled_rebuild/run_all.sh`
- Current data-linked figure script:
  `analysis/stage17_methodology_figs/run_make_stage17_deterministic.sh`
- Current workflow figure script:
  `analysis/stage17_methodology_figs/run_make_fig1_stage17_workflow.sh`
- Current stage17-native verification figure script:
  `analysis/stage17_methodology_figs/run_make_fig4_stage17_verification.sh`

## Environment setup

The repository does not currently expose a single repo-wide environment file.
The smallest declared environment for the current implementation is:

- `simulation/stage17_controlled_rebuild/requirements.txt`

The stage17 shell wrappers already expect a local virtual environment in
`simulation/stage17_controlled_rebuild/.venv` and prefer `python3.12` if it is
available.

Minimum setup:

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/simulation/stage17_controlled_rebuild
python3.12 -m venv .venv  # if python3.12 is unavailable, use python3
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Wrapper behavior:

- `run_fixed_smoke.sh`, `run_controlled_smoke.sh`, `run_phase_prep.sh`, and
  `run_all.sh` create `.venv` if it does not exist.
- These wrappers do not auto-install packages.
- If imports fail, they stop and print the manual `pip install` commands.

## Package and dependency discovery

Repository-wide package metadata discovery found:

- `requirements.txt` files in multiple stage directories
- `NOT FOUND` for a repo-wide `pyproject.toml`
- `NOT FOUND` for a repo-wide `environment.yml`
- `NOT FOUND` for a repo-wide `setup.py`
- `NOT FOUND` for a repo-wide `Pipfile`
- `NOT FOUND` for a repo-wide `poetry.lock`

Current stage17 simulation requirements:

- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `PyYAML`

Current stage17 figure requirements:

- Dedicated file: `analysis/stage17_methodology_figs/requirements.txt`
- Import-inspected minimum for `make_fig1_stage17_workflow.py`: `matplotlib`
- Import-inspected minimum for `make_fig4_stage17_verification.py`: `matplotlib`,
  `numpy`, `pandas`
- Import-inspected minimum for `make_stage17_deterministic.py`: `matplotlib`,
  `pandas`
- Import-inspected minimum for `make_phase_map_figures.py`: `matplotlib`,
  `numpy`, `pandas`
- Import-inspected minimum for `make_revision_assets.py`: `matplotlib`,
  `numpy`, `pandas`, `PyYAML`

Practical current recommendation:

- Reuse `simulation/stage17_controlled_rebuild/.venv` for both stage17
  simulation and stage17 figure scripts.
- A dedicated figure requirements file now exists for
  `analysis/stage17_methodology_figs/`, but the shared stage17 simulation `.venv`
  remains the verified current path.

Notebook discovery:

- `NOT FOUND` for any `.ipynb` files outside virtual environments.
- No notebook is required for the minimal current path documented below.

## Minimum command: one nominal simulation case

This is the shortest verified current simulation entry point.

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/simulation/stage17_controlled_rebuild
bash run_fixed_smoke.sh
```

What it runs:

- Base config: `configs/baseline_90W_4s_4mm.yaml`
- Latency config: `configs/latency_enabled.yaml`
- No controller config
- Python entry point: `src/run_case.py`

Expected outputs:

- `simulation/stage17_controlled_rebuild/outputs/smoke_fixed_stage17/summary.yaml`
- `simulation/stage17_controlled_rebuild/outputs/smoke_fixed_stage17/case_fields.png`

Observed runtime on the current machine:

- `real 2.69 s`

Notes:

- This is a nominal `90 W / 4 s` fixed-power case with latency enabled.
- The shell wrapper is the preferred entry point because it handles `.venv`
  creation and import checks.

## Minimum command: one main figure

This is the shortest verified current main-figure entry point.

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/analysis/stage17_methodology_figs
source ../../simulation/stage17_controlled_rebuild/.venv/bin/activate
bash run_make_fig1_stage17_workflow.sh
```

What it runs:

- Python entry point: `src/make_fig1_stage17_workflow.py`
- No simulation CSV input is required

Expected outputs:

- `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.pdf`
- `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.png`
- `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.tiff`

Observed runtime on the current machine:

- `real 2.16 s`

## Smallest data-linked figure path

The previous figure is a workflow schematic. The smallest current path that
links stage17 simulation output to a manuscript-facing main figure is:

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/simulation/stage17_controlled_rebuild
bash run_phase_prep.sh

cd /Users/lulingfeng/Projects/cardiac_rfa/analysis/stage17_methodology_figs
source ../../simulation/stage17_controlled_rebuild/.venv/bin/activate
bash run_make_stage17_deterministic.sh
```

What it uses:

- Base config: `configs/baseline_90W_4s_4mm.yaml`
- Protocols: `configs/protocols_stage17_fourway.yaml`
- Phase-prep sweep: `configs/phase_prep_stage17_fourway.yaml`
- Controller: `configs/controller_selected_stage17.yaml`
- Latency: `configs/latency_enabled.yaml`

Expected intermediate output:

- `simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv`

Expected figure outputs:

- `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.pdf`
- `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.png`
- `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.tiff`

Observed runtime on the current machine:

- Figure render only, once `phase_prep_summary.csv` already exists: `real 2.67 s`
- Full `run_phase_prep.sh`: `NOT FOUND` as a measured runtime in this runbook

Sweep size if defaults are unchanged:

- `5 wall values x 3 cooling values x 4 insertion values x 4 protocols = 240 cases`

## Stage17-native Figure 4 path

The current stage17-native verification figure reads the checked convergence
exports directly.

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/analysis/stage17_methodology_figs
source ../../simulation/stage17_controlled_rebuild/.venv/bin/activate
bash run_make_fig4_stage17_verification.sh
```

Default inputs:

- `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/grid_convergence.csv`
- `simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/dt_convergence.csv`

Expected outputs:

- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.pdf`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.png`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.tiff`

Observed runtime on the current machine:

- `real 2.09 s`

Notes:

- The current stage17 convergence CSVs store raw metrics rather than legacy
  `*_relerr_pct` columns.
- The stage17-native Figure 4 script therefore recomputes relative error to the
  finest solution from `lesion_depth_mm` and `peak_temperature_C`.
- The panel layout is adapted from the legacy stage7 Figure 4 script, but the
  data source is the current stage17 convergence output.

## Expected output paths

Minimal sanity-check outputs:

- `simulation/stage17_controlled_rebuild/outputs/smoke_fixed_stage17/summary.yaml`
- `simulation/stage17_controlled_rebuild/outputs/smoke_fixed_stage17/case_fields.png`
- `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.pdf`
- `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.png`
- `analysis/stage17_methodology_figs/example_outputs/fig1_stage17_geometry_workflow.tiff`

First data-linked outputs:

- `simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv`
- `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.pdf`
- `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.png`
- `analysis/stage17_methodology_figs/example_outputs/fig_stage17_deterministic_fourway.tiff`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.pdf`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.png`
- `analysis/stage17_methodology_figs/example_outputs/fig4_stage17_verification.tiff`

## Known blockers

- No repo-wide lockfile or unified environment file was located, so the
  verified current path still relies on local stage-specific requirements.
- Canonical stage17 output names and observed on-disk folder names do not yet
  fully match. See `STAGE17_ENVIRONMENT.md` for the current mapping.
- The current stage17 figure folder still includes
  `run_make_revision_assets.sh`, which defaults to stage16 inputs rather than
  stage17 deterministic outputs.
- Package version pinning is `NOT FOUND` in the current repository metadata.
- Full phase-prep runtime is `NOT FOUND` in repository documentation or logs.
- TIFF export works in the current environment, but an explicit repository-level
  declaration for any backend-specific image dependency is `NOT FOUND`.

## What this runbook does not claim

- It does not claim that every manuscript figure is reproducible from the
  current stage17 path.
- It does not claim that legacy stage folders are obsolete; it only identifies
  the smallest current reproducibility path that could be verified here.
- It does not claim that the full manuscript delivery package under `papers/`
  is regenerated by the commands above.
