#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PHASE_CSV="${PHASE_CSV:-example_data/phase_prep_summary.csv}"
GRID_CSV="${GRID_CSV:-example_data/grid_convergence.csv}"
DT_CSV="${DT_CSV:-example_data/dt_convergence.csv}"
UQ_CSV="${UQ_CSV:-example_data/uq_summary.csv}"
OUTDIR="${OUTDIR:-example_outputs}"

python3 src/make_figures.py   --phase-csv "$PHASE_CSV"   --grid-csv "$GRID_CSV"   --dt-csv "$DT_CSV"   --uq-csv "$UQ_CSV"   --outdir "$OUTDIR"   --style styles/cardiac_biorender_light.mplstyle   --palette styles/palette.yaml
