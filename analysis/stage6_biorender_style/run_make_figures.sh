#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

: "${PHASE_CSV:=example_data/phase_prep_summary.csv}"
: "${GRID_CSV:=example_data/grid_convergence.csv}"
: "${DT_CSV:=example_data/dt_convergence.csv}"
: "${UQ_CSV:=example_data/uq_summary.csv}"
: "${OUTDIR:=example_outputs}"

export PYTHONPATH=src
mkdir -p "$OUTDIR"
python src/make_style_preview.py --outdir "$OUTDIR"
python src/make_fig3_deterministic_summary.py --phase-prep-csv "$PHASE_CSV" --outdir "$OUTDIR"
python src/make_fig4_verification.py --grid-csv "$GRID_CSV" --dt-csv "$DT_CSV" --outdir "$OUTDIR"
python src/make_fig5_uq_maps.py --uq-summary-csv "$UQ_CSV" --outdir "$OUTDIR"
python src/make_fig7_tradeoff.py --uq-summary-csv "$UQ_CSV" --outdir "$OUTDIR"
