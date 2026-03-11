#!/usr/bin/env bash
set -e
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

python src/run_case.py \
  --config configs/baseline_50W_10s_4mm.yaml \
  --outdir outputs/baseline_50W_10s_4mm

python src/run_protocol_scan.py \
  --base-config configs/baseline_50W_10s_4mm.yaml \
  --protocols configs/protocols.yaml \
  --outdir outputs/protocol_scan

python src/run_wall_protocol_scan.py \
  --base-config configs/baseline_50W_10s_4mm.yaml \
  --protocols configs/protocols.yaml \
  --wall-scan configs/wall_scan.yaml \
  --outdir outputs/wall_protocol_scan

python src/run_cooling_protocol_scan.py \
  --base-config configs/baseline_50W_10s_4mm.yaml \
  --protocols configs/protocols.yaml \
  --cooling-scan configs/cooling_scan.yaml \
  --outdir outputs/cooling_protocol_scan

python src/run_convergence.py \
  --base-config configs/baseline_50W_10s_4mm.yaml \
  --convergence-config configs/convergence.yaml \
  --outdir outputs/convergence
