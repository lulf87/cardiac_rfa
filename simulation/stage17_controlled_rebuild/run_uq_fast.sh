#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate
export PYTHONPATH=src
python src/run_uq_maps.py \
  --base-config configs/baseline_50W_10s_4mm.yaml \
  --protocols configs/protocols.yaml \
  --uq-config configs/uq_fast.yaml \
  --outdir outputs/uq_fast
