#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
source .venv/bin/activate
export PYTHONPATH=src

python src/run_phase_prep.py   --base-config configs/baseline_50W_10s_4mm.yaml   --protocols configs/protocols.yaml   --phase-config configs/phase_prep.yaml   --outdir outputs/phase_prep
