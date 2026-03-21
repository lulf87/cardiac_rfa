#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

GRID_CSV=${GRID_CSV:-../../simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/grid_convergence.csv}
DT_CSV=${DT_CSV:-../../simulation/stage17_controlled_rebuild/outputs/convergence_stage17_controlled_check/dt_convergence.csv}
OUTDIR=${OUTDIR:-example_outputs}

export PYTHONPATH=src
python src/make_fig4_stage17_verification.py \
  --grid-csv "$GRID_CSV" \
  --dt-csv "$DT_CSV" \
  --outdir "$OUTDIR"
