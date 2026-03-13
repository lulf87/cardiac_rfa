#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PHASE_CSV=${PHASE_CSV:-../../simulation/stage16_uq_metrics_ready/outputs/phase_prep/phase_prep_summary.csv}
UQ_CSV=${UQ_CSV:-../../simulation/stage16_uq_metrics_ready/outputs/uq_paper/uq_summary.csv}
BASELINE_YAML=${BASELINE_YAML:-../../simulation/stage16_uq_metrics_ready/configs/baseline_50W_10s_4mm.yaml}
UQ_YAML=${UQ_YAML:-../../simulation/stage16_uq_metrics_ready/configs/uq_paper.yaml}
OUTDIR=${OUTDIR:-example_outputs}
export PYTHONPATH=src
python src/make_revision_assets.py   --phase-csv "$PHASE_CSV"   --uq-csv "$UQ_CSV"   --baseline-yaml "$BASELINE_YAML"   --uq-yaml "$UQ_YAML"   --outdir "$OUTDIR"
