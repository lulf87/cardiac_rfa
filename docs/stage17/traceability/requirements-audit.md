# Requirements Audit

## Scope

This audit summarizes dependency declarations and dependency gaps relevant to
the current manuscript-facing reproducibility path.

Current primary path:

- Simulation: `simulation/stage17_controlled_rebuild/`
- Figure generation: `analysis/stage17_methodology_figs/`

This document does not invent missing environment details. When a dependency
source cannot be located, it is marked `NOT FOUND`.

## Repository-wide dependency metadata discovery

Discovered package metadata files:

- `analysis/stage4_pubfigs_cmpb/requirements.txt`
- `analysis/stage6_biorender_style/requirements.txt`
- `analysis/stage7_freeze_final/requirements.txt`
- `analysis/stage7_freeze_ready/requirements.txt`
- `analysis/stage7_polishing_patch/requirements.txt`
- `analysis/stage8_fig128_export/requirements.txt`
- `analysis/stage8_finish_ready/requirements.txt`
- `simulation/stage0_minimal/requirements.txt`
- `simulation/stage16_uq_metrics_ready/requirements.txt`
- `simulation/stage17_controlled_rebuild/requirements.txt`
- `simulation/stage1_deterministic/requirements.txt`
- `simulation/stage1p5_contact/requirements.txt`
- `simulation/stage2_phase_ready/requirements.txt`
- `simulation/stage3_uq_maps/requirements.txt`

Not found anywhere in the repository search:

- `pyproject.toml`
- `environment.yml`
- `setup.py`
- `Pipfile`
- `poetry.lock`

Implication:

- The repository is stage-local rather than repo-global in its dependency
  declarations.
- There is no single pinned environment for the full manuscript workflow.

## Current environment anchor

The closest thing to a current authoritative environment file is:

- `simulation/stage17_controlled_rebuild/requirements.txt`

Declared packages:

- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `PyYAML`

Status:

- `CURRENT`

Notes:

- Stage17 wrapper scripts create `.venv` if needed.
- Stage17 wrapper scripts do not install requirements automatically.
- The wrappers prefer `python3.12` if available, otherwise `python3`.
- Python version pinning is `NOT FOUND`.
- Package version pinning is `NOT FOUND`.

## Stage17 figure dependency status

Dedicated requirements file for current stage17 figures:

- `analysis/stage17_methodology_figs/requirements.txt`

Import-inspected dependencies by script:

| Script | Imported non-stdlib packages | Status |
| --- | --- | --- |
| `analysis/stage17_methodology_figs/src/make_fig1_stage17_workflow.py` | `matplotlib` | COVERED by local requirements file |
| `analysis/stage17_methodology_figs/src/make_fig4_stage17_verification.py` | `matplotlib`, `numpy`, `pandas` | COVERED by local requirements file |
| `analysis/stage17_methodology_figs/src/make_stage17_deterministic.py` | `matplotlib`, `pandas` | COVERED by local requirements file |
| `analysis/stage17_methodology_figs/src/make_phase_map_figures.py` | `matplotlib`, `numpy`, `pandas` | COVERED by local requirements file |
| `analysis/stage17_methodology_figs/src/make_revision_assets.py` | `matplotlib`, `numpy`, `pandas`, `yaml` | COVERED by local requirements file |

Practical implication:

- The simplest current setup is to run stage17 figure scripts from the stage17
  simulation virtual environment.
- The stage17 figure directory now has a local requirements file for the
  current figure scripts.
- The shared simulation virtual environment remains the verified current path.

## Current vs legacy dependency files

| Path | Tag | Notes |
| --- | --- | --- |
| `simulation/stage17_controlled_rebuild/requirements.txt` | CURRENT | Best current environment anchor for stage17 deterministic runs |
| `analysis/stage17_methodology_figs/requirements.txt` | CURRENT | Current figure-environment anchor for stage17 figure scripts |
| `simulation/stage16_uq_metrics_ready/requirements.txt` | FROZEN BASELINE | Relevant for stage16 UQ and legacy revision assets |
| `analysis/stage8_finish_ready/requirements.txt` | LEGACY | Old figure-generation branch |
| `analysis/stage7_freeze_final/requirements.txt` | LEGACY | Older freeze/final figure branch |
| `analysis/stage7_freeze_ready/requirements.txt` | LEGACY | Older freeze-ready figure branch |
| `analysis/stage7_polishing_patch/requirements.txt` | LEGACY | Older figure patch branch |
| `analysis/stage8_fig128_export/requirements.txt` | LEGACY | Older export branch |
| `analysis/stage6_biorender_style/requirements.txt` | LEGACY | Older styling branch |
| `analysis/stage4_pubfigs_cmpb/requirements.txt` | LEGACY | Older publication-figure branch |
| `simulation/stage0_minimal/requirements.txt` | LEGACY | Historical simulation stage |
| `simulation/stage1_deterministic/requirements.txt` | LEGACY | Historical simulation stage |
| `simulation/stage1p5_contact/requirements.txt` | LEGACY | Historical simulation stage |
| `simulation/stage2_phase_ready/requirements.txt` | LEGACY | Historical simulation stage |
| `simulation/stage3_uq_maps/requirements.txt` | LEGACY | Historical simulation stage |

## Notebook requirement check

Notebook discovery result:

- `NOT FOUND` for any `.ipynb` files outside virtual environments

Implication:

- No notebook appears to be required for the minimal current reproducibility
  path.
- If a workflow step depends on notebook execution, that dependency is `NOT
  FOUND` in the current repository scan.

## Dependency gaps and ambiguities

### Gap 1: no repo-wide environment lock

Status:

- `NOT FOUND`

Impact:

- Full manuscript reproduction cannot currently rely on one pinned environment.
- Reproducing legacy and current figure paths may require manual environment
  reconciliation.

### Gap 2: no repo-wide unified environment for simulation + figures

Status:

- `NOT FOUND`

Impact:

- Stage17 simulation and stage17 figure paths are now both declared locally, but
  they are still not unified by one repo-wide environment file or lockfile.

### Gap 3: version pinning absent

Status:

- `NOT FOUND`

Impact:

- Package resolution may drift over time.
- Manuscript figure rendering and TIFF export behavior may vary by environment.

### Gap 4: current figure folder still contains a stage16-driven path

Files:

- `analysis/stage17_methodology_figs/run_make_revision_assets.sh`
- `analysis/stage17_methodology_figs/src/make_revision_assets.py`

Impact:

- Not every script under the current figure directory is stage17-native.
- Dependency and provenance boundaries remain mixed for revision assets.

### Gap 5: backend/image dependency declaration is incomplete

Status:

- Explicit requirement for backend-specific image support is `NOT FOUND`

Observed behavior:

- TIFF export succeeded in the current environment for
  `run_make_fig1_stage17_workflow.sh` and `run_make_stage17_deterministic.sh`.

Impact:

- Repository metadata does not state whether additional image libraries are
  required beyond the declared packages.

## Minimum known-good package set for the verified current path

Verified current path:

- `simulation/stage17_controlled_rebuild/run_fixed_smoke.sh`
- `analysis/stage17_methodology_figs/run_make_fig1_stage17_workflow.sh`
- `analysis/stage17_methodology_figs/run_make_stage17_deterministic.sh`

Minimum declared or import-inspected packages for that path:

- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `PyYAML`

This package set comes from:

- the declared stage17 simulation requirements file
- import inspection of the current figure scripts

It is a practical minimum for the current verified path, not a repo-wide lock.
