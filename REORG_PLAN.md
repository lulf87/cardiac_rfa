# Reorganization Plan For Task 6

## Purpose

This plan proposes a **safe reorganization only** to improve methods
traceability for the **current stage17 manuscript line**.

It does **not** change:

- scientific logic
- parameter values
- protocol definitions
- controller behavior
- lesion metrics
- benchmark values
- validation scope

This is an approval-gated plan. No reorganization beyond creation of this plan
has been applied yet.

## Current source-of-truth that must remain unchanged

These paths stay authoritative and are **not** candidates for relocation:

- `simulation/stage17_controlled_rebuild/`
- `analysis/stage17_methodology_figs/`
- `papers/V13/`

Additional fixed rule:

- Figure 2 remains a **legacy fixed-power reference figure**
- Table 3 will **not** gain fabricated current-source simulated widths

## Reorganization goal

Make the current stage17 methods traceability easier to follow by reducing
top-level audit sprawl and making the current traceability documents easier to
find, while preserving existing scientific source paths.

## Problems observed in the current layout

1. Many stage17-specific audit artifacts are scattered at the repository root.
2. `docs/stage17/` already holds current stage17 notes, but many newer
   provenance/methods/figure/table audits live outside it.
3. A few documentation files are now stale relative to the latest stage17
   traceability work, especially around Figure 4.
4. Current, legacy, archive, and mixed-source paths are documented, but the
   documentation is not yet organized around one clear stage17 traceability hub.

## Proposed safe reorganization scope

### A. Keep these top-level navigation files in place

These should remain at the repository root because they serve as entry points:

- `AGENTS.md`
- `README.md`
- `REPO_MAP.md`
- `RUNBOOK.md`
- `STAGE17_ENVIRONMENT.md`
- `FINAL_PATH_CHANGE_SUMMARY.md` after the reorganization is applied

### B. Create one stage17 traceability hub under docs

Proposed new directory:

- `docs/stage17/traceability/`

Purpose:

- hold the detailed stage17 provenance/methods/verification/figure/table audit
  artifacts
- reduce root-level clutter
- make `docs/stage17/` the clear home for current stage17 traceability

### C. Move only documentation/audit artifacts, not scientific source paths

Candidate files to move into `docs/stage17/traceability/`:

- `METHODS_PARAMETER_AUDIT.md`
- `METHODS_PARAMETER_TABLE.csv`
- `FIG2_DECISION.md`
- `STAGE17_FIGURE_AUTHORITY.md`
- `OLD_VS_CURRENT_FIGURES.csv`
- `FIGURE_PROVENANCE.csv`
- `LEGACY_DRIFT_REPORT.md`
- `SIM_CASE_MANIFEST.csv`
- `REPRO_GAPS.md`
- `VERIFICATION_AUDIT.md`
- `VERIFICATION_CASES.csv`
- `TABLE_AUTOMATION_STATUS.md`
- `HANDOFF_FOR_METHODS_WRITING.md`
- `requirements-audit.md`

Rationale:

- these are audit/traceability artifacts, not authoritative scientific source
  code
- they are stage17-facing or manuscript-traceability-facing
- moving them is lower risk than moving simulation, analysis, or manuscript
  source directories

### D. Do not move these paths in Task 6

No move/rename for:

- `simulation/stage17_controlled_rebuild/`
- `analysis/stage17_methodology_figs/`
- `papers/V13/`
- `manuscript/`
- `tmp/table_exports/`
- any `outputs/` directory
- any YAML config
- any Python scientific implementation module

### E. Sync documentation that is currently behind the latest traceability state

After approval, update these documents so they reflect the reorganized
locations and latest stage17 status:

- `AGENTS.md`
- `REPO_MAP.md`
- `RUNBOOK.md`

Planned content syncs:

- point to `docs/stage17/traceability/` as the detailed audit location
- keep the current stage17 source-of-truth paths explicit
- keep Figure 2 marked as legacy reference
- reflect that Figure 4 now has a stage17-native generator/output path
- keep current vs legacy vs archive boundaries explicit

### F. Produce one explicit path-change summary

After approval and after the moves are complete, add:

- `FINAL_PATH_CHANGE_SUMMARY.md`

This file should record:

- every file moved
- old path -> new path
- reason for move
- confirmation that no scientific source directory was moved

## Proposed path-change table

| Current path | Proposed new path | Type | Notes |
| --- | --- | --- | --- |
| `METHODS_PARAMETER_AUDIT.md` | `docs/stage17/traceability/METHODS_PARAMETER_AUDIT.md` | move | Stage17 methods audit artifact |
| `METHODS_PARAMETER_TABLE.csv` | `docs/stage17/traceability/METHODS_PARAMETER_TABLE.csv` | move | Paired audit table |
| `FIG2_DECISION.md` | `docs/stage17/traceability/FIG2_DECISION.md` | move | Figure 2 decision record |
| `STAGE17_FIGURE_AUTHORITY.md` | `docs/stage17/traceability/STAGE17_FIGURE_AUTHORITY.md` | move + sync | Needs Figure 4 status sync |
| `OLD_VS_CURRENT_FIGURES.csv` | `docs/stage17/traceability/OLD_VS_CURRENT_FIGURES.csv` | move + sync | Should reflect current Figure 4 status if updated |
| `FIGURE_PROVENANCE.csv` | `docs/stage17/traceability/FIGURE_PROVENANCE.csv` | move | Figure provenance matrix |
| `LEGACY_DRIFT_REPORT.md` | `docs/stage17/traceability/LEGACY_DRIFT_REPORT.md` | move | Manuscript/code drift audit |
| `SIM_CASE_MANIFEST.csv` | `docs/stage17/traceability/SIM_CASE_MANIFEST.csv` | move | Simulation case manifest |
| `REPRO_GAPS.md` | `docs/stage17/traceability/REPRO_GAPS.md` | move | Reproducibility gaps |
| `VERIFICATION_AUDIT.md` | `docs/stage17/traceability/VERIFICATION_AUDIT.md` | move | Verification/validation audit |
| `VERIFICATION_CASES.csv` | `docs/stage17/traceability/VERIFICATION_CASES.csv` | move | Verification case table |
| `TABLE_AUTOMATION_STATUS.md` | `docs/stage17/traceability/TABLE_AUTOMATION_STATUS.md` | move | Table automation audit |
| `HANDOFF_FOR_METHODS_WRITING.md` | `docs/stage17/traceability/HANDOFF_FOR_METHODS_WRITING.md` | move | Writer handoff note |
| `requirements-audit.md` | `docs/stage17/traceability/requirements-audit.md` | move | Environment/dependency audit |

## Explicit non-goals

Task 6 should **not** do any of the following:

- change scientific values
- change controller or latency behavior
- change simulation outputs
- run new simulations
- recalibrate against Table 3
- create new validation language
- replace Figure 2 with a stage17-native rebuild
- invent a current-source simulated-width field for Table 3
- rename `outputs/` folders
- delete legacy directories

## Verification plan after approval

If approved, verification should stay lightweight and traceability-focused:

1. Confirm every moved file exists at its new path.
2. Confirm old paths no longer appear in current navigation docs unless they are
   intentionally listed as historical paths.
3. Update internal links in:
   - `AGENTS.md`
   - `REPO_MAP.md`
   - `RUNBOOK.md`
   - any moved markdown files that reference each other
4. Confirm no scientific source directories were moved.
5. Confirm the current source-of-truth paths remain unchanged:
   - `simulation/stage17_controlled_rebuild/`
   - `analysis/stage17_methodology_figs/`
   - `papers/V13/`
6. Confirm Figure 2 remains documented as legacy fixed-power reference only.
7. Confirm Table 3 simulated widths remain historical trace only.

## Stop conditions

Stop and ask for confirmation if any of the following becomes necessary:

- moving or renaming anything under `simulation/stage17_controlled_rebuild/`
- moving or renaming anything under `analysis/stage17_methodology_figs/`
- moving or renaming anything under `papers/V13/`
- renaming output folders to resolve canonical-vs-observed drift
- touching benchmark source values or manuscript scientific claims

## Approval checkpoint

Current status:

- `REORG_PLAN.md` created
- no reorganization applied yet

If approved, the next step is:

1. create `docs/stage17/traceability/`
2. move the selected audit artifacts there
3. update `AGENTS.md`, `REPO_MAP.md`, and `RUNBOOK.md`
4. write `FINAL_PATH_CHANGE_SUMMARY.md`

