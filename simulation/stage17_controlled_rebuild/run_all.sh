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
PROTOCOLS=${PROTOCOLS:-configs/protocols_stage17_fourway.yaml}
PHASE_CONFIG=${PHASE_CONFIG:-configs/phase_prep_stage17_fourway.yaml}
WALL_SCAN=${WALL_SCAN:-configs/wall_scan_stage17.yaml}
COOLING_SCAN=${COOLING_SCAN:-configs/cooling_scan_stage17.yaml}
CONTACT_SCAN=${CONTACT_SCAN:-configs/contact_scan_stage17.yaml}
CONTROLLER_CONFIG=${CONTROLLER_CONFIG:-configs/controller_selected_stage17.yaml}
LATENCY_CONFIG=${LATENCY_CONFIG:-configs/latency_enabled.yaml}
CONVERGENCE_CONFIG=${CONVERGENCE_CONFIG:-configs/convergence.yaml}

echo "[INFO] Stage17 canonical workflow"
echo "  base config:        $BASE_CONFIG"
echo "  protocols:          $PROTOCOLS"
echo "  controller config:  $CONTROLLER_CONFIG"
echo "  latency config:     $LATENCY_CONFIG"

python src/run_case.py \
  --config "$BASE_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/baseline_stage17_fixed

python src/run_case.py \
  --config "$BASE_CONFIG" \
  --controller-config "$CONTROLLER_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/baseline_stage17_controlled

python src/run_protocol_scan.py \
  --base-config "$BASE_CONFIG" \
  --protocols "$PROTOCOLS" \
  --controller-config "$CONTROLLER_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/protocol_scan_stage17_fourway

python src/run_wall_protocol_scan.py \
  --base-config "$BASE_CONFIG" \
  --protocols "$PROTOCOLS" \
  --wall-scan "$WALL_SCAN" \
  --controller-config "$CONTROLLER_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/wall_protocol_scan_stage17_fourway

python src/run_cooling_protocol_scan.py \
  --base-config "$BASE_CONFIG" \
  --protocols "$PROTOCOLS" \
  --cooling-scan "$COOLING_SCAN" \
  --controller-config "$CONTROLLER_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/cooling_protocol_scan_stage17_fourway

python src/run_contact_scan.py \
  --base-config "$BASE_CONFIG" \
  --protocols "$PROTOCOLS" \
  --contact-scan "$CONTACT_SCAN" \
  --controller-config "$CONTROLLER_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/contact_protocol_scan_stage17_fourway

python src/run_convergence.py \
  --base-config "$BASE_CONFIG" \
  --convergence-config "$CONVERGENCE_CONFIG" \
  --controller-config "$CONTROLLER_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/convergence_stage17_controlled

python src/run_phase_prep.py \
  --base-config "$BASE_CONFIG" \
  --protocols "$PROTOCOLS" \
  --phase-config "$PHASE_CONFIG" \
  --controller-config "$CONTROLLER_CONFIG" \
  --latency-config "$LATENCY_CONFIG" \
  --outdir outputs/phase_prep_stage17_fourway
