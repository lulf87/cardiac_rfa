# V14 Integrated Package

## Scope

This folder integrates the latest manuscript-facing figures and tables without
changing scientific logic or the current source-of-truth paths.

Current scientific source-of-truth remains:

- `simulation/stage17_controlled_rebuild/`
- `analysis/stage17_methodology_figs/`
- `papers/V13/`

This `V14（整合）` folder is a packaging/integration layer.

## Contents

### Main figures

Stored in:

- `figures/main/`

Current composition:

- `Figure1.*` from the current stage17 source
- `Figure2.png` from the retained legacy fixed-power reference figure
- `Figure3.*` from the current stage17 source
- `Figure4.*` from the current stage17-native verification source
- `Figure5.*` from the current stage17 source
- `Figure6.*` from the current stage17 source
- `Figure7.*` from the current stage17 source
- `Figure8.png` from the retained benchmark packaging path

### Supplementary figures

Stored in:

- `figures/supplement/`

Current composition:

- `FigureS1.png` retained as legacy/reference supplementary figure
- `FigureS2.png` retained as legacy/reference supplementary figure

### Tables

Stored in:

- `tables/`

Current composition:

- `table1_stage17_protocols.{csv,md}`
- `table2_stage17_controls.{csv,md}`
- `TABLE2_FINAL_METHODS_WORDING.md`
- `table3_benchmark_trace.{csv,md}`
- `TABLE3_METHODS_SCOPE.md`
- `table3_depth_only.csv`

### Manuscript file

Existing file retained at package root:

- `CMBBE_RF_ablation_reduced_model_main.docx`

Note:

- This integration step did not overwrite that DOCX.

## Current vs legacy status inside this package

### Current stage17 figures

- `Figure1`
- `Figure3`
- `Figure4`
- `Figure5`
- `Figure6`
- `Figure7`

### Legacy or retained reference figures

- `Figure2`
- `Figure8`
- `FigureS1`
- `FigureS2`

### Table status

- `Table 1`: current stage17 export
- `Table 2`: current stage17 export plus finalized Methods wording
- `Table 3`: benchmark trace export plus a Methods-safe depth-only export

Critical benchmark note:

- `table3_depth_only.csv` is the Methods-safe benchmark export
- simulated widths were **not** fabricated
- if width values are retained, they remain historical-trace only

## Provenance summary

See:

- `ASSET_MANIFEST.csv`

