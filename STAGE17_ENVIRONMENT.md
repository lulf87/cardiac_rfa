# Stage17 Environment

## Scope

This document hardens the current stage17 reproducibility path without changing
scientific logic, parameters, or output folder names.

It documents:

- current vs legacy vs archive paths
- environment anchors for the stage17 simulation and figure line
- canonical output folder names defined by current scripts
- observed on-disk folder names currently present in the repository

## Path status map

| Status | Path | Notes |
| --- | --- | --- |
| CURRENT | `simulation/stage17_controlled_rebuild/` | Canonical deterministic four-comparator simulation line |
| CURRENT | `analysis/stage17_methodology_figs/` | Current stage17 figure-generation scripts |
| CURRENT | `docs/stage17/` | Current stage17 notes, audits, and claim tracking |
| LEGACY | `simulation/stage16_uq_metrics_ready/` | Frozen three-protocol UQ baseline; still referenced by revision assets |
| LEGACY | `simulation/stage0_minimal/` through `simulation/stage3_uq_maps/` | Historical simulation stages |
| LEGACY | `analysis/stage4_pubfigs_cmpb/`, `analysis/stage6_biorender_style/`, `analysis/stage7_*`, `analysis/stage8_*`, `analysis/stage16_revision_figs/` | Historical figure-generation lines |
| ARCHIVE | `manuscript/` | Packaging layer, figure manifests, submission package helpers |
| ARCHIVE | `papers/V4/` through `papers/V13/` | Historical and delivery-facing paper folders |

## Environment anchors

Simulation environment anchor:

- `simulation/stage17_controlled_rebuild/requirements.txt`

Declared packages:

- `numpy`
- `scipy`
- `matplotlib`
- `pandas`
- `PyYAML`

Figure environment anchor:

- `analysis/stage17_methodology_figs/requirements.txt`

Declared packages:

- `matplotlib`
- `numpy`
- `pandas`
- `PyYAML`

Notes:

- The figure requirements file is aligned to the current import-inspected
  `stage17` figure scripts:
  - `make_fig1_stage17_workflow.py`
  - `make_fig4_stage17_verification.py`
  - `make_stage17_deterministic.py`
  - `make_phase_map_figures.py`
  - `make_revision_assets.py`
- No repo-wide `pyproject.toml`, `environment.yml`, `setup.py`, `Pipfile`, or
  `poetry.lock` was located.
- The verified current runbook path reused the simulation `.venv` for figure
  generation.

## Recommended setup

Verified current path:

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/simulation/stage17_controlled_rebuild
python3.12 -m venv .venv  # if unavailable, use python3
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Optional figure-only environment:

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/analysis/stage17_methodology_figs
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Environment note:

- The figure-only environment has not been separately verified in this document.
- The verified runbook path uses the simulation `.venv`.

## Canonical output folders vs observed on-disk folders

Canonical names below come from the current `stage17` simulation README and
`simulation/stage17_controlled_rebuild/run_all.sh`.

Observed names below come from the current on-disk
`simulation/stage17_controlled_rebuild/outputs/` inventory.

| Canonical output name | Defined by current script/docs | Observed on disk | Status | Notes |
| --- | --- | --- | --- | --- |
| `outputs/baseline_stage17_fixed/` | YES | `NOT FOUND` | CANONICAL_NOT_OBSERVED | Current smoke output exists separately at `outputs/smoke_fixed_stage17/`. |
| `outputs/baseline_stage17_controlled/` | YES | `NOT FOUND` | CANONICAL_NOT_OBSERVED | Current smoke output exists separately at `outputs/smoke_controlled_stage17/`. |
| `outputs/protocol_scan_stage17_fourway/` | YES | `outputs/protocol_scan_stage17_fourway/` | MATCH | Current canonical protocol-scan folder exists. |
| `outputs/wall_protocol_scan_stage17_fourway/` | YES | `NOT FOUND` | CANONICAL_NOT_OBSERVED | Observed nearby folder: `outputs/wall_scan_stage17_fourway/`. It contains `wall_protocol_summary.csv` but the folder basename differs from current script/docs. |
| `outputs/cooling_protocol_scan_stage17_fourway/` | YES | `NOT FOUND` | CANONICAL_NOT_OBSERVED | Observed nearby folder: `outputs/cooling_scan_stage17_fourway/`. It contains `cooling_protocol_summary.csv` but the folder basename differs from current script/docs. |
| `outputs/contact_protocol_scan_stage17_fourway/` | YES | `NOT FOUND` | CANONICAL_NOT_OBSERVED | Observed nearby folder: `outputs/contact_scan_stage17_fourway/`. It contains `contact_protocol_summary.csv` but the folder basename differs from current script/docs. |
| `outputs/convergence_stage17_controlled/` | YES | `NOT FOUND` | CANONICAL_NOT_OBSERVED | Observed nearby folder: `outputs/convergence_stage17_controlled_check/`. The verified stage17 Figure 4 path currently reads the `_check` folder because that is the checked dataset present on disk. |
| `outputs/phase_prep_stage17_fourway/` | YES | `outputs/phase_prep_stage17_fourway/` | MATCH | Current canonical phase-prep folder exists. |

Additional observed folders not named as canonical current outputs:

| Observed folder | Status | Notes |
| --- | --- | --- |
| `outputs/smoke_fixed_stage17/` | CURRENT_SUPPORTING | Verified smoke wrapper output |
| `outputs/smoke_controlled_stage17/` | CURRENT_SUPPORTING | Verified smoke wrapper output |
| `outputs/protocol_scan_stage17_fourway_check/` | OBSERVED_EXTRA | Present on disk but not named by current README or `run_all.sh` |
| `outputs/wall_scan_stage17_fourway/` | OBSERVED_NAME_DRIFT | Present on disk; basename differs from current `run_all.sh` target |
| `outputs/cooling_scan_stage17_fourway/` | OBSERVED_NAME_DRIFT | Present on disk; basename differs from current `run_all.sh` target |
| `outputs/contact_scan_stage17_fourway/` | OBSERVED_NAME_DRIFT | Present on disk; basename differs from current `run_all.sh` target |
| `outputs/convergence_stage17_controlled_check/` | OBSERVED_NAME_DRIFT | Present on disk; currently consumed by the verified stage17 Figure 4 generator |
| `outputs/uq_fast/` | LEGACY_OR_MIXED | Exists under stage17 directory, but the current stage17 README says stage16 remains the authoritative UQ baseline |
| `outputs/uq_paper/` | LEGACY_OR_MIXED | Exists under stage17 directory, but not part of the canonical deterministic current workflow |
| `outputs/baseline_50W_10s_4mm/` | LEGACY_OR_MIXED | Historical or exploratory output under the stage17 tree |
| `outputs/protocol_scan/`, `outputs/wall_protocol_scan/`, `outputs/cooling_protocol_scan/`, `outputs/contact_protocol_scan/`, `outputs/convergence/` | LEGACY_OR_MIXED | Legacy-style generic names retained on disk |

## Folder-handling rule

- Treat names defined in current scripts and current `stage17` docs as the
  canonical targets.
- Treat observed alternate names on disk as retained artifacts until a separate
  cleanup or rename task is explicitly approved.
- Do not rename folders only to make the tree look cleaner.
- If a script must consume an observed non-canonical folder, document that use
  explicitly, as was done for the current stage17 Figure 4 wrapper.

## Current figure environment note

Current stage17 figure wrappers:

- `run_make_fig1_stage17_workflow.sh`
- `run_make_fig4_stage17_verification.sh`
- `run_make_stage17_deterministic.sh`
- `run_make_phase_map_figures.sh`
- `run_make_revision_assets.sh`

Mixed-source caution:

- `run_make_revision_assets.sh` remains a mixed-source path because it still
  defaults to stage16 UQ inputs.
- The existence of `analysis/stage17_methodology_figs/requirements.txt` does not
  make the revision-assets path fully stage17-native.

## What this document does not do

- It does not rename any output folders.
- It does not delete legacy directories.
- It does not alter scientific parameters, protocol definitions, or benchmark
  values.
