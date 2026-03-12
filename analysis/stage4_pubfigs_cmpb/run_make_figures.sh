#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH=src

python src/make_fig3_deterministic_summary.py \
  --phase-prep-csv ../../simulation/stage3_uq_maps/outputs/phase_prep/phase_prep_summary.csv \
  --outdir example_outputs

python src/make_fig4_verification.py \
  --grid-csv ../../simulation/stage3_uq_maps/outputs/convergence/grid_convergence.csv \
  --dt-csv ../../simulation/stage3_uq_maps/outputs/convergence/dt_convergence.csv \
  --outdir example_outputs

python src/make_fig5_uq_maps.py \
  --uq-summary-csv ../../simulation/stage3_uq_maps/outputs/uq_fast/uq_summary.csv \
  --outdir example_outputs

python src/make_fig6_tradeoff.py \
  --uq-summary-csv ../../simulation/stage3_uq_maps/outputs/uq_fast/uq_summary.csv \
  --outdir example_outputs