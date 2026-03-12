#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

export PYTHONPATH=src

STAGE3_ROOT="${STAGE3_ROOT:-../../simulation/stage3_uq_maps}"
BASELINE_YAML="${BASELINE_YAML:-$STAGE3_ROOT/configs/baseline_50W_10s_4mm.yaml}"
PROTOCOLS_YAML="${PROTOCOLS_YAML:-$STAGE3_ROOT/configs/protocols.yaml}"
BENCHMARK_CSV="${BENCHMARK_CSV:-example_data/benchmark_points.csv}"
OUTDIR="${OUTDIR:-example_outputs}"

python src/make_fig1_model_workflow.py --outdir "$OUTDIR"

python src/make_fig2_representative_fields.py \
  --stage3-root "$STAGE3_ROOT" \
  --baseline-yaml "$BASELINE_YAML" \
  --protocols-yaml "$PROTOCOLS_YAML" \
  --outdir "$OUTDIR"

python src/make_fig8_literature_benchmark.py \
  --benchmark-csv "$BENCHMARK_CSV" \
  --outdir "$OUTDIR"

echo "Saved Figure 1 / 2 / 8 outputs to $OUTDIR"
