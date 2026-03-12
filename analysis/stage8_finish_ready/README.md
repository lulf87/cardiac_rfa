
# stage8_fig128_export

This patch adds the three missing figures for the simulation paper:

- **Figure 1**: model geometry, boundary conditions, and workflow schematic
- **Figure 2**: representative temperature / damage field maps for the three protocols
- **Figure 8**: literature-derived benchmark plot (template-driven)

It also exports figures in **both PDF and PNG** so you can keep a journal-friendly vector copy and a high-resolution preview copy.

## Recommended local location

```text
cardiac_rfa/
└── analysis/
    └── stage8_fig128_export/
```

## What this package expects

Your existing project should already contain:

```text
cardiac_rfa/
└── simulation/
    └── stage3_uq_maps/
        ├── src/
        └── configs/
```

## Install once

```bash
cd ~/Projects/cardiac_rfa/analysis/stage8_fig128_export
python -m pip install -r requirements.txt
```

## Run Figure 1 + Figure 2 + Figure 8 skeleton

```bash
cd ~/Projects/cardiac_rfa/analysis/stage8_fig128_export

STAGE3_ROOT=../../simulation/stage3_uq_maps BASELINE_YAML=../../simulation/stage3_uq_maps/configs/baseline_50W_10s_4mm.yaml PROTOCOLS_YAML=../../simulation/stage3_uq_maps/configs/protocols.yaml BENCHMARK_CSV=example_data/benchmark_points.csv OUTDIR=example_outputs bash run_make_figures.sh
```

`benchmark_points.csv` is created automatically if it does not exist.

## Outputs

- `fig1_model_workflow.pdf/png`
- `fig2_representative_fields.pdf/png`
- `fig8_literature_benchmark.pdf/png`

## Figure 8 template columns

```csv
source_id,protocol_key,reported_depth_mm,simulated_depth_mm,reported_width_mm,simulated_width_mm,notes
```

Allowed `protocol_key` values:

- `standard_30W_30s`
- `hpsd_50W_10s`
- `vhpsd_90W_4s`


Finish patch updates:
- Figure 1 simplified to keyword-level workflow text.
- Figure 2 temperature colorbar relabelled and non-physical grid lines removed.
- PDF + PNG + TIFF export enabled.
