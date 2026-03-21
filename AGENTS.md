# AGENTS.md

## Purpose

This repository supports a CMBBE manuscript on a reduced 2D electro-thermal
radiofrequency ablation model comparing fixed-power and temperature-limited
protocols.

The primary goal for future Codex work is:

> recover a full reproducibility chain from manuscript claim -> simulation
> config -> code implementation -> figure/table output

This file defines repository-level working rules for all future tasks in this
repo.

---

## Core principles

1. Do not invent missing scientific details.
2. If a parameter, formula, unit, boundary condition, controller rule, workflow
   detail, or provenance link cannot be located, record it exactly as
   `NOT FOUND`.
3. Distinguish explicitly between:
   - current implementation
   - frozen baseline
   - legacy/archived code
   - delivery-only artifacts
4. During the audit phase, do not delete legacy files.
5. Do not rename or move files unless the user explicitly asks.
6. Prefer markdown and CSV audit artifacts over speculative refactoring.
7. Flag every mismatch between manuscript wording and current implementation.
8. Do not upgrade a trend-level benchmark into validation language unless the
   supporting evidence is present in the repository.
9. Do not make device-specific QDOT or catheter-specific claims unless the user
   explicitly provides evidence that supports them.
10. Preserve traceability. Every substantive conclusion should cite files,
    scripts, configs, outputs, or user-provided material.

---

## Current project map

### Current implementation

Use these directories first when tracing the present comparator-aware manuscript
line:

- `simulation/stage17_controlled_rebuild/`
  Canonical deterministic four-comparator implementation.
- `analysis/stage17_methodology_figs/`
  Current figure scripts for the stage17 methodology-rebuild branch.
- `docs/stage17/`
  Current decision log, claim tracking, and methodology notes.
- `docs/stage17/traceability/`
  Current detailed audit, provenance, verification, figure, and table
  traceability records for the stage17 manuscript line.

Current stage17 scope:

- `standard_30W_30s`
- `hpsd_50W_10s`
- `vhpsd_90W_4s_fixed`
- `vhpsd_90W_4s_controlled`

### Frozen baseline

- `simulation/stage16_uq_metrics_ready/`
  Frozen three-protocol UQ baseline with 64-sample paper-level uncertainty
  outputs.

Treat stage16 as a frozen baseline unless the user explicitly asks for changes.

### Legacy and archived lines

Treat these as historical development stages unless the user explicitly asks to
 audit or revive them:

- `simulation/stage0_minimal/`
- `simulation/stage1_deterministic/`
- `simulation/stage1p5_contact/`
- `simulation/stage2_phase_ready/`
- `simulation/stage3_uq_maps/`
- `analysis/stage4_pubfigs_cmpb/`
- `analysis/stage6_biorender_style/`
- `analysis/stage7_freeze_ready/`
- `analysis/stage7_freeze_final/`
- `analysis/stage7_polishing_patch/`
- `analysis/stage8_fig128_export/`
- `analysis/stage8_finish_ready/`
- `analysis/stage16_revision_figs/`
- `manuscript/paper/V0/`
- `manuscript/paper/V2/`
- `manuscript/paper/V3/`
- `papers/V4/` through `papers/V12/`

Do not assume these directories match the current stage17 implementation.

### Delivery-only artifacts

Treat these as outputs or packaging layers, not authoritative generation
sources:

- `papers/V13/CMBBE_figure_upload/`
- `papers/V13/*.docx`
- `manuscript/submission_package/`
- `manuscript/figures/main/`
- `manuscript/figures/supplement/`

If a delivery artifact conflicts with a current source script or config, flag
the mismatch explicitly.

---

## Working assumptions that are already supported

These points may be referenced when they match the current files:

- The current deterministic line is stage17, not stage16.
- Stage17 is reduced, planar 2D, comparator-aware, and assumption-bounded.
- The temperature-limited `90 W / 4 s` case is generic, not catheter-specific.
- Lesion depth and depth fraction are primary outputs.
- Width and overheating are secondary proxies unless stronger evidence is added.

If any of these become inconsistent with the files you inspect, flag the
mismatch instead of forcing the narrative.

---

## How to run the project

### Canonical stage17 deterministic workflow

Run from:

```bash
cd simulation/stage17_controlled_rebuild
bash run_fixed_smoke.sh
bash run_controlled_smoke.sh
bash run_all.sh
```

Canonical stage17 configs:

- `configs/baseline_90W_4s_4mm.yaml`
- `configs/protocols_stage17_fourway.yaml`
- `configs/controller_selected_stage17.yaml`
- `configs/latency_enabled.yaml`
- `configs/phase_prep_stage17_fourway.yaml`
- `configs/wall_scan_stage17.yaml`
- `configs/cooling_scan_stage17.yaml`
- `configs/contact_scan_stage17.yaml`

Expected stage17 outputs:

- `outputs/baseline_stage17_fixed/summary.yaml`
- `outputs/baseline_stage17_controlled/summary.yaml`
- `outputs/protocol_scan_stage17_fourway/protocol_summary.csv`
- `outputs/wall_protocol_scan_stage17_fourway/wall_protocol_summary.csv`
- `outputs/cooling_protocol_scan_stage17_fourway/cooling_protocol_summary.csv`
- `outputs/contact_protocol_scan_stage17_fourway/contact_protocol_summary.csv`
- `outputs/convergence_stage17_controlled/grid_convergence.csv`
- `outputs/convergence_stage17_controlled/dt_convergence.csv`
- `outputs/phase_prep_stage17_fourway/phase_prep_summary.csv`

### Frozen stage16 UQ workflow

Run from:

```bash
cd simulation/stage16_uq_metrics_ready
bash run_all.sh
bash run_phase_prep.sh
bash run_uq_paper.sh
```

Expected stage16 outputs:

- `outputs/phase_prep/phase_prep_summary.csv`
- `outputs/uq_paper/uq_summary.csv`
- `outputs/uq_paper/uq_samples.csv`
- `outputs/uq_paper/uq_overview.csv`

### Current figure generation workflow

Run from:

```bash
cd analysis/stage17_methodology_figs
bash run_make_fig1_stage17_workflow.sh
bash run_make_fig4_stage17_verification.sh
bash run_make_stage17_deterministic.sh
bash run_make_phase_map_figures.sh
bash run_make_revision_assets.sh
```

Default inputs:

- `simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv`
- `simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_summary.csv`

Important:

- `run_make_revision_assets.sh` currently mixes stage17 deterministic inputs and
  stage16 UQ inputs.
- Treat this as an explicit mixed-source workflow, not as a single unified
  simulation stage.

### Submission packaging

The submission/package layer is managed from:

- `manuscript/scripts/make_fig8_final.py`
- `manuscript/scripts/package_submission_figures.py`
- `manuscript/submission_package/`
- `papers/V13/`

Do not treat packaged figures or DOCX files as authoritative generation sources
without tracing them back to code and inputs.

---

## Audit workflow

For any non-trivial scientific or reproducibility task, use this sequence.

1. Identify the target claim, figure, table, or manuscript sentence.
2. Classify the referenced asset as:
   - current implementation
   - frozen baseline
   - legacy/archived
   - delivery-only
3. Trace the chain in order:
   - manuscript or notes
   - figure/table artifact
   - generating script
   - input CSV/YAML/output directory
   - code implementation
4. Record every unresolved link as `NOT FOUND`.
5. Record every wording/implementation discrepancy as `MISMATCH`.
6. Prefer adding audit artifacts in markdown or CSV rather than rewriting code.
7. Only propose refactors after the traceability audit is complete.

Suggested audit artifact locations:

- `docs/stage17/traceability/` for durable current stage17 audit notes
- `docs/` for broader durable notes outside the current stage17 line
- `tmp/` for temporary exploratory outputs

If the user asks for a formal audit artifact and no location is specified,
prefer:

- `docs/stage17/traceability/*.md`
- `docs/stage17/traceability/*.csv`

---

## Required mismatch checks

Always check for these classes of mismatch when relevant:

1. Manuscript protocol set vs actual protocol config
2. Manuscript parameter values vs YAML/config values
3. Manuscript formulas vs implemented algorithm
4. Manuscript units vs code/output units
5. Figure caption wording vs figure content
6. Figure labels vs generating script inputs
7. Claimed validation vs actual benchmark scope
8. Current-stage wording vs legacy-stage outputs

When a mismatch exists, do not silently harmonize it. Report it.

---

## File safety and modification rules

1. During audit work, do not delete legacy files.
2. Do not rename or move files yet unless explicitly asked.
3. Do not modify `simulation/stage16_uq_metrics_ready/` during routine current
   stage17 work unless the user explicitly asks.
4. Do not assume `papers/` directories are source-of-truth for computation.
5. If a directory appears to be a delivery package or frozen handoff, treat it
   as read-only unless explicitly asked to edit it.

---

## What to do when something is missing

If you cannot locate a needed detail:

- write `NOT FOUND`
- say what was searched
- say which files or directories were checked
- say what downstream claim remains unsupported because of the missing detail

Do not infer a formula, unit, control law, or calibration rationale from vague
manuscript prose when the implementation is missing or inconsistent.

---

## Definition of completion

A future Codex task in this repository is complete only when all relevant items
below are satisfied.

### For audit tasks

- every inspected claim is mapped to exact files
- current vs frozen vs legacy vs delivery-only status is stated
- every missing detail is marked `NOT FOUND`
- every wording/implementation discrepancy is flagged
- no speculative scientific detail is introduced

### For code or figure update tasks

- the modified file set is minimal and traceable
- the affected run command is documented
- the expected output files are named
- verification was actually run, or the response clearly states it was not run
- any remaining gaps in reproducibility are listed explicitly

### For manuscript-support tasks

- every scientific statement added or revised is backed by repository evidence
- claims are bounded to the actual implementation
- trend-level benchmark language is not upgraded to validation language without
  new evidence

---

## Practical summary

- Current deterministic source of truth: `simulation/stage17_controlled_rebuild/`
- Frozen UQ baseline: `simulation/stage16_uq_metrics_ready/`
- Current figure source of truth: `analysis/stage17_methodology_figs/`
- Delivery-only layer: `papers/V13/` and `manuscript/submission_package/`
- Missing detail: write `NOT FOUND`
- Conflict between wording and implementation: write `MISMATCH`
- During audit: do not delete, rename, or move legacy files
