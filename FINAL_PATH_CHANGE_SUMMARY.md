# Final Path Change Summary

## Scope

This file records the **approved Task 6 safe reorganization** that was applied
to improve methods traceability for the current stage17 manuscript line.

This reorganization did **not** change:

- scientific logic
- parameter values
- simulation code behavior
- protocol definitions
- benchmark values
- current source-of-truth scientific directories

## Current source-of-truth preserved

These authoritative paths were **not** moved or renamed:

- `simulation/stage17_controlled_rebuild/`
- `analysis/stage17_methodology_figs/`
- `papers/V13/`

Figure policy preserved:

- Figure 2 remains a legacy fixed-power reference figure
- Table 3 simulated widths remain historical-trace only

## New traceability hub

Created:

- `docs/stage17/traceability/`

Purpose:

- collect current stage17 audit, provenance, verification, figure, table, and
  methods-traceability artifacts in one place

## File moves applied

| Old path | New path | Reason |
| --- | --- | --- |
| `METHODS_PARAMETER_AUDIT.md` | `docs/stage17/traceability/METHODS_PARAMETER_AUDIT.md` | Move detailed stage17 methods audit into the current traceability hub |
| `METHODS_PARAMETER_TABLE.csv` | `docs/stage17/traceability/METHODS_PARAMETER_TABLE.csv` | Keep paired methods parameter table with its audit note |
| `FIG2_DECISION.md` | `docs/stage17/traceability/FIG2_DECISION.md` | Keep Figure 2 decision record with current stage17 provenance docs |
| `STAGE17_FIGURE_AUTHORITY.md` | `docs/stage17/traceability/STAGE17_FIGURE_AUTHORITY.md` | Keep figure authority record in the traceability hub |
| `OLD_VS_CURRENT_FIGURES.csv` | `docs/stage17/traceability/OLD_VS_CURRENT_FIGURES.csv` | Keep old-vs-current figure comparison next to figure authority |
| `FIGURE_PROVENANCE.csv` | `docs/stage17/traceability/FIGURE_PROVENANCE.csv` | Keep figure provenance matrix in the traceability hub |
| `LEGACY_DRIFT_REPORT.md` | `docs/stage17/traceability/LEGACY_DRIFT_REPORT.md` | Keep manuscript/code drift audit in the traceability hub |
| `SIM_CASE_MANIFEST.csv` | `docs/stage17/traceability/SIM_CASE_MANIFEST.csv` | Keep simulation case manifest with current reproducibility docs |
| `REPRO_GAPS.md` | `docs/stage17/traceability/REPRO_GAPS.md` | Keep reproducibility gaps list with current audits |
| `VERIFICATION_AUDIT.md` | `docs/stage17/traceability/VERIFICATION_AUDIT.md` | Keep verification/validation audit in the traceability hub |
| `VERIFICATION_CASES.csv` | `docs/stage17/traceability/VERIFICATION_CASES.csv` | Keep verification case table with verification audit |
| `TABLE_AUTOMATION_STATUS.md` | `docs/stage17/traceability/TABLE_AUTOMATION_STATUS.md` | Keep table automation audit in the traceability hub |
| `HANDOFF_FOR_METHODS_WRITING.md` | `docs/stage17/traceability/HANDOFF_FOR_METHODS_WRITING.md` | Keep writer handoff note with the supporting traceability documents |
| `requirements-audit.md` | `docs/stage17/traceability/requirements-audit.md` | Keep stage17 dependency audit in the traceability hub |

## Documentation updates applied

Updated root/navigation files:

- `AGENTS.md`
- `REPO_MAP.md`
- `RUNBOOK.md`

Updates made:

- added `docs/stage17/traceability/` as the current detailed audit/provenance
  location
- kept the current stage17 source-of-truth paths explicit
- updated figure-generation workflow notes to include the stage17-native Figure
  4 generator where relevant
- corrected outdated root-README status in `REPO_MAP.md`

Additional traceability sync applied:

- `docs/stage17/traceability/STAGE17_FIGURE_AUTHORITY.md`
  now marks Figure 4 as `CURRENT`
- `docs/stage17/traceability/OLD_VS_CURRENT_FIGURES.csv`
  now marks Figure 4 as `CURRENT`
- `docs/stage17/traceability/HANDOFF_FOR_METHODS_WRITING.md`
  was synchronized to that Figure 4 update

## Files intentionally not moved

These files remain at the repository root because they serve as entry points,
newer manuscript-writing outputs, or approved-scope exceptions:

- `README.md`
- `AGENTS.md`
- `REORG_PLAN.md`
- `REPO_MAP.md`
- `RUNBOOK.md`
- `STAGE17_ENVIRONMENT.md`
- `FINAL_PATH_CHANGE_SUMMARY.md`
- `METHODS_FINAL_AUDIT.md`
- `TABLE2_FINAL_METHODS_WORDING.md`
- `TABLE3_METHODS_SCOPE.md`

These non-document scientific source paths were also intentionally not moved:

- `simulation/stage17_controlled_rebuild/`
- `analysis/stage17_methodology_figs/`
- `papers/V13/`
- all `outputs/` directories
- all YAML configs
- all Python scientific implementation modules

## No deletions and no scientific-source renames

- No legacy directories were deleted.
- No current scientific source directory was renamed.
- No output folder was renamed.
- No benchmark file was rewritten.

## Result

The repository now has a clearer split between:

- root navigation and execution docs
- current stage17 scientific source-of-truth paths
- detailed stage17 traceability/audit artifacts under
  `docs/stage17/traceability/`

This improves methods traceability without changing the current stage17
scientific implementation.

