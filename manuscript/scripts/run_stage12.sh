#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$(dirname "$0")/../../.." && pwd)}"
BENCHMARK_CSV="${BENCHMARK_CSV:-$PROJECT_ROOT/analysis/stage8_finish_ready/example_data/benchmark_points.csv}"
MAIN_DIR="${MAIN_DIR:-$PROJECT_ROOT/manuscript/figures/main}"
SUPP_DIR="${SUPP_DIR:-$PROJECT_ROOT/manuscript/figures/supplement}"
CAPTIONS="${CAPTIONS:-$PROJECT_ROOT/manuscript/captions/figure_caption_stubs_v3.md}"
SUBMISSION_OUT="${SUBMISSION_OUT:-$PROJECT_ROOT/manuscript/submission_package}"
FIG8_OUTBASE="${FIG8_OUTBASE:-$MAIN_DIR/fig8_literature_benchmark}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

python "$SCRIPT_DIR/make_fig8_final.py" --csv "$BENCHMARK_CSV" --outbase "$FIG8_OUTBASE"
python "$SCRIPT_DIR/package_submission_figures.py" \
  --project-root "$PROJECT_ROOT" \
  --main-dir "$MAIN_DIR" \
  --supp-dir "$SUPP_DIR" \
  --captions "$CAPTIONS" \
  --outdir "$SUBMISSION_OUT"

echo "[DONE] Stage 12 benchmark figure refreshed and submission package built."
