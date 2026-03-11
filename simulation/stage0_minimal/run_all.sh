#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# 仅在虚拟环境不存在时创建
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

# 仅检查依赖是否存在，不在这里自动联网安装
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
  --outdir outputs/protocol_scan_stage0