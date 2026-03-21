#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  if command -v python3.12 >/dev/null 2>&1; then
    echo "[INFO] create .venv with python3.12"
    python3.12 -m venv .venv
  else
    echo "[INFO] python3.12 not found, fallback to python3"
    python3 -m venv .venv
  fi
fi

source .venv/bin/activate

if ! python -c "import numpy, scipy, matplotlib, pandas, yaml" >/dev/null 2>&1; then
  echo "[ERROR] missing dependencies."
  echo "Please run these commands manually:"
  echo "  source .venv/bin/activate"
  echo "  python -m pip install -U pip"
  echo "  python -m pip install -i https://pypi.org/simple -r requirements.txt"
  exit 1
fi

export PYTHONPATH=src

BASE_CONFIG=${BASE_CONFIG:-configs/baseline_90W_4s_4mm.yaml}
LATENCY_CONFIG=${LATENCY_CONFIG:-configs/latency_enabled.yaml}
OUTDIR=${OUTDIR:-outputs/smoke_fixed_stage17}

python src/run_case.py \
  --config "$BASE_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir "$OUTDIR"
