#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACK_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$HOME/Projects/cardiac_rfa}"

mkdir -p "$PROJECT_ROOT/manuscript/captions"
mkdir -p "$PROJECT_ROOT/analysis/stage8_finish_ready/example_data"

cp "$PACK_ROOT/captions/figure_caption_stubs_v3.md" \
   "$PROJECT_ROOT/manuscript/captions/figure_caption_stubs_v3.md"
cp "$PACK_ROOT/example_data/benchmark_points_v2.csv" \
   "$PROJECT_ROOT/analysis/stage8_finish_ready/example_data/benchmark_points.csv"

echo "[DONE] Installed caption stub and benchmark starter into project: $PROJECT_ROOT"
