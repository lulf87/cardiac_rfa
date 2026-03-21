#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

OUTDIR=${OUTDIR:-example_outputs}

export PYTHONPATH=src
python src/make_fig1_stage17_workflow.py \
  --outdir "$OUTDIR"
