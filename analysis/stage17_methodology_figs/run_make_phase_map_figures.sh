#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PHASE_CSV=${PHASE_CSV:-../../simulation/stage17_controlled_rebuild/outputs/phase_prep_stage17_fourway/phase_prep_summary.csv}
OUTDIR=${OUTDIR:-example_outputs}

export PYTHONPATH=src
python src/make_phase_map_figures.py \
  --phase-csv "$PHASE_CSV" \
  --outdir "$OUTDIR"
