# cardiac_rfa

This repository supports a CMBBE manuscript on a reduced 2D electro-thermal RF
ablation model comparing fixed-power and temperature-limited protocols.

The current manuscript-facing implementation is the `stage17` deterministic
line. If you are trying to reproduce or audit the current paper branch, start
there rather than from older stage directories or packaged manuscript assets.

## Status map

| Status | Path | Role |
| --- | --- | --- |
| CURRENT | `simulation/stage17_controlled_rebuild/` | Canonical comparator-aware deterministic simulation path |
| CURRENT | `analysis/stage17_methodology_figs/` | Current stage17 figure-generation path |
| CURRENT | `docs/stage17/` | Current decision log, claim notes, and methodology notes |
| LEGACY | `simulation/stage16_uq_metrics_ready/` | Frozen three-protocol UQ baseline still referenced by some revision assets |
| LEGACY | `simulation/stage0_minimal/` through `simulation/stage3_uq_maps/` | Historical simulation stages |
| LEGACY | `analysis/stage4_pubfigs_cmpb/`, `analysis/stage6_biorender_style/`, `analysis/stage7_*`, `analysis/stage8_*`, `analysis/stage16_revision_figs/` | Historical figure-generation lines |
| ARCHIVE | `manuscript/` | Packaging layer, manifests, captions, submission bundle helpers |
| ARCHIVE | `papers/V4/` through `papers/V13/` | Historical and delivery-facing paper-version folders |

## Current reproducibility path

Simulation:

- `simulation/stage17_controlled_rebuild/`

Figures:

- `analysis/stage17_methodology_figs/`

Most useful audit/navigation docs:

- `AGENTS.md`
- `RUNBOOK.md`
- `STAGE17_ENVIRONMENT.md`
- `REPO_MAP.md`

## Quick start

Minimum verified simulation check:

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/simulation/stage17_controlled_rebuild
bash run_fixed_smoke.sh
```

Minimum verified figure check:

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/analysis/stage17_methodology_figs
source ../../simulation/stage17_controlled_rebuild/.venv/bin/activate
bash run_make_fig1_stage17_workflow.sh
```

Current stage17-native Figure 4 check:

```bash
cd /Users/lulingfeng/Projects/cardiac_rfa/analysis/stage17_methodology_figs
source ../../simulation/stage17_controlled_rebuild/.venv/bin/activate
bash run_make_fig4_stage17_verification.sh
```

## Environment notes

- The current simulation environment anchor is
  `simulation/stage17_controlled_rebuild/requirements.txt`.
- The current figure environment anchor is
  `analysis/stage17_methodology_figs/requirements.txt`.
- No repo-wide lockfile or unified environment file was found.
- The verified current path reused the stage17 simulation `.venv` for figure
  generation.

See `STAGE17_ENVIRONMENT.md` for:

- environment setup guidance
- canonical output folder names vs observed on-disk names
- current vs legacy vs archive path boundaries

## Output-folder caution

The current stage17 scripts define canonical output names, but the repository
also contains older or check-run output folders on disk. Do not infer authority
from folder presence alone.

For example:

- canonical names such as `outputs/baseline_stage17_fixed/` are defined by
  `simulation/stage17_controlled_rebuild/run_all.sh`
- observed folders such as `outputs/convergence_stage17_controlled_check/` are
  present on disk and currently used by the verified stage17 Figure 4 path

The full canonical-vs-observed mapping is documented in
`STAGE17_ENVIRONMENT.md`.

## What this README does not claim

- It does not claim that every legacy directory is obsolete.
- It does not claim that delivery artifacts under `papers/` are authoritative
  generation sources.
- It does not rename or reconcile any existing output folders on disk.
