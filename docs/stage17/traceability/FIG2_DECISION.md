# Figure 2 Decision

## Recommendation

Recommend `Path A`: keep Figure 2 as a legacy reference figure.

This is the lower-risk option for the current manuscript state because the
existing Figure 2 is well traced to a concrete legacy generator, while a
stage17-native rebuild would force an unresolved manuscript decision about
whether Figure 2 should remain a three-protocol fixed-power comparison or be
expanded to include the stage17 temperature-limited comparator.

## Why this decision

Three constraints make `Path A` the safer choice now:

1. **Figure 2 is currently a fully traced legacy artifact.**
   The current packaged figure can be mapped exactly to a repository generator,
   inputs, and protocol set.

2. **A stage17-native rebuild is technically possible but editorially
   underdetermined.**
   The stage17 code can produce the needed field arrays, but the manuscript does
   not currently resolve whether Figure 2 should stay three-column
   `Standard/HPSD/vHPSD fixed` or become a four-column
   `Standard/HPSD/90 W fixed/90 W controlled` figure.

3. **The manuscript risk is higher than the implementation effort.**
   The coding work for a minimal rebuild is moderate. The scientific-framing
   risk is larger, because a rebuilt Figure 2 would change what the figure is
   claiming about the current stage17 line.

## Current Figure 2 provenance

Current packaged figure:

- `papers/V13/CMBBE_figure_upload/Figure2.png`

Current repository generation path:

- Script:
  `analysis/stage8_finish_ready/src/make_fig2_representative_fields.py`
- Wrapper:
  `analysis/stage8_finish_ready/run_make_figures.sh`
- Upstream simulation code:
  `simulation/stage3_uq_maps/src/model_fd.py`
- Baseline config:
  `simulation/stage3_uq_maps/configs/baseline_50W_10s_4mm.yaml`
- Protocol list:
  `simulation/stage3_uq_maps/configs/protocols.yaml`

Hard-coded representative case in the script defaults:

- wall thickness: `4.0 mm`
- cooling coefficient: `1500 W m^-2 K^-1`
- insertion depth: `1.0 mm`

Protocol set used by the legacy Figure 2 generator:

- `standard_30W_30s`
- `hpsd_50W_10s`
- `vhpsd_90W_4s`

Fields plotted by the legacy script:

- temperature field: `peak_T_C`
- damage field: `omega`
- lesion contour: contour at `omega = 1`
- axes support: `x_m`, `y_m`
- electrode-width annotation: `res["cfg"].electrode_width_mm`

Repository evidence for this legacy status:

- `analysis/stage8_finish_ready/README.md` explicitly describes Figure 2 as
  `representative temperature / damage field maps for the three protocols`.
- `FIGURE_PROVENANCE.csv` already records Figure 2 as a `LEGACY` generator with
  no stage17-native Figure 2 generator located.
- `STAGE17_FIGURE_AUTHORITY.md` currently leaves Figure 2 as `UNRESOLVED`.

## Path A

### Meaning

Treat Figure 2 as a retained legacy reference figure that illustrates the older
three-protocol fixed-power formulation rather than the stage17 comparator-aware
line.

### Scientific meaning

Pros:

- Preserves the already established interpretation of Figure 2 as a
  representative temperature/damage field visualization for the legacy
  fixed-power three-protocol comparison.
- Avoids implying that the current stage17 comparator split has already been
  propagated into every manuscript figure.

Cons:

- Figure 2 would remain semantically different from the now-current stage17
  Figures 1, 3, 4, 5, 6, and 7.

### Implementation effort

Low.

No new scientific plotting code is needed. The work is documentation and caption
discipline only.

### Manuscript risk

Low to moderate.

The main risk is wording drift, not computational reproducibility.
That risk can be controlled by caption language that explicitly marks Figure 2
as a legacy fixed-power reference figure.

### Recommended caption language for Path A

Recommended wording:

> **Figure 2. Legacy reference temperature and damage fields for the fixed-power three-protocol formulation.** Representative deterministic case from the earlier fixed-power model line with wall thickness 4.0 mm, cooling coefficient 1500 W m^-2 K^-1, and insertion depth 1.00 mm. Panel (a) shows temperature fields for the Standard, HPSD, and 90 W / 4 s fixed-power protocols, with the lesion boundary defined by Omega = 1 overlaid. Panel (b) shows the corresponding damage fields as log10(Omega). This figure is retained as a reference visualization from the legacy fixed-power workflow and should not be interpreted as a stage17-native comparator figure.

Why this wording:

- It does not call the figure stage17-native.
- It keeps the exact protocol interpretation tied to fixed-power protocols.
- It avoids implying that the temperature-limited comparator is represented in
  Figure 2.

## Path B

### Meaning

Define a new stage17-native Figure 2 that is regenerated from the current
stage17 model implementation rather than from the legacy stage3/stage8 path.

### Smallest stage17-native rebuild path

The smallest code-level rebuild path already supported by repository code would
use:

- model entry point:
  `simulation/stage17_controlled_rebuild/src/model_fd.py::run_case_with_fields`
- current config anchor:
  `simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml`
- current protocol list:
  `simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml`

The exact representative-case settings already present in the baseline config
and current manuscript language are:

- wall thickness: `4.0 mm`
- cooling coefficient: `1500 W m^-2 K^-1`
- insertion depth: `1.0 mm`

Existing stage17 field arrays available from `run_case_with_fields`:

- `x_m`
- `y_m`
- `peak_T_C`
- `omega`
- `lesion_mask`
- `phi`
- `q_unit`
- `q`

Existing stage17 metadata already available through the returned `result` or
`cfg`:

- `cfg.electrode_width_mm`
- `lesion_depth_mm`
- `lesion_width_mm`

Existing stage17 plotting logic already available for reuse:

- `simulation/stage17_controlled_rebuild/src/model_fd.py::plot_case`
  already plots:
  - `peak_T_C`
  - `log10(omega)`
  - horizontal wall-thickness marker

Smallest new plotting script that would be needed:

- a dedicated Figure 2 generator under
  `analysis/stage17_methodology_figs/`
- it would call `run_case_with_fields` for each selected protocol and then
  compose a multi-panel figure using:
  - top row: `peak_T_C`
  - bottom row: `log10(omega)`
  - contour overlay at `omega = 1`
  - axes from `x_m`, `y_m`
  - electrode rectangle from `cfg.electrode_width_mm`

### Critical unresolved choice inside Path B

Path B is blocked not by missing fields, but by an unresolved figure definition:

- **Option B1:** keep the old three-column scientific meaning and rebuild only
  the fixed-power subset
  - `standard_30W_30s`
  - `hpsd_50W_10s`
  - `vhpsd_90W_4s_fixed`

- **Option B2:** make Figure 2 truly stage17-native in comparator terms and use
  all four protocols
  - `standard_30W_30s`
  - `hpsd_50W_10s`
  - `vhpsd_90W_4s_fixed`
  - `vhpsd_90W_4s_controlled`

Both options are implementable from current code, but they do not mean the same
thing scientifically.

### Scientific meaning

Pros:

- Would align Figure 2 with the current stage17 implementation rather than with
  the legacy stage3/stage8 chain.
- Would remove the provenance mismatch now attached to the packaged Figure 2.

Cons:

- A three-protocol rebuild would still be only partially stage17-native because
  it would intentionally exclude the new controlled comparator.
- A four-protocol rebuild would change the figure’s narrative and likely its
  panel count, which is a manuscript-level decision, not just a plotting task.

### Implementation effort

Moderate.

The required fields already exist, but there is no current stage17-native Figure
2 plotting script, no saved stage17 field-data product for reuse, and no agreed
panel definition for the comparator-aware line.

### Manuscript risk

Moderate to high.

The main risk is editorial drift:

- if rebuilt as three protocols, the figure remains visually close to the legacy
  interpretation but still sidesteps the new controlled comparator
- if rebuilt as four protocols, the figure becomes a new scientific object that
  the manuscript text and possibly layout would need to absorb

## A vs B comparison

| Criterion | Path A: keep legacy reference | Path B: smallest stage17-native rebuild |
| --- | --- | --- |
| Scientific meaning | Stable, explicit legacy fixed-power reference | Potentially better alignment with stage17, but figure meaning must be re-decided |
| Implementation effort | Low | Moderate |
| Manuscript risk | Low to moderate | Moderate to high |
| Provenance clarity after action | Good if caption is explicit | Good only after an additional figure-definition decision |
| Immediate suitability | Better | Not yet ready without a manuscript framing choice |

## Final recommendation

Choose `Path A` now.

Why:

- The current Figure 2 is already reproducible and fully traceable as a legacy
  reference figure.
- The smallest stage17-native rebuild path is technically available, but the
  repository evidence does not tell us whether the intended current Figure 2
  should be three-protocol fixed-power or four-protocol comparator-aware.
- That ambiguity is a manuscript decision, not a missing-code problem.

If you later decide to migrate Figure 2 into the stage17 line, the rebuild
should start only after choosing explicitly between:

1. a three-protocol fixed-power stage17 refresh, or
2. a four-protocol comparator-aware stage17 figure.
