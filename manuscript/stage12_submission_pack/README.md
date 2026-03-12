# Stage 12: final benchmark and submission package

This bundle does two things:

1. Rebuilds `fig8_literature_benchmark` from `benchmark_points.csv` using a cleaner, final plotting style.
2. Creates a manuscript-facing submission package with separated PDF/TIFF/PNG files and a caption file.

## Recommended placement

Unzip this folder into:

```text
~/Projects/cardiac_rfa/manuscript/stage12_submission_pack
```

## Files

- `scripts/make_fig8_final.py` — rebuild Figure 8 from benchmark CSV
- `scripts/package_submission_figures.py` — collect frozen figures into a submission package
- `scripts/run_stage12.sh` — convenience wrapper
- `captions/figure_caption_stubs_v3.md` — updated caption draft
- `example_data/benchmark_points_v2.csv` — starter literature benchmark rows

## Typical workflow

Copy the starter benchmark CSV into the Stage 8 figure directory:

```bash
cp ~/Projects/cardiac_rfa/manuscript/stage12_submission_pack/example_data/benchmark_points_v2.csv \
   ~/Projects/cardiac_rfa/analysis/stage8_finish_ready/example_data/benchmark_points.csv
```

Copy the caption file into the manuscript caption directory:

```bash
cp ~/Projects/cardiac_rfa/manuscript/stage12_submission_pack/captions/figure_caption_stubs_v3.md \
   ~/Projects/cardiac_rfa/manuscript/captions/figure_caption_stubs_v3.md
```

Run the wrapper:

```bash
cd ~/Projects/cardiac_rfa/manuscript/stage12_submission_pack

PROJECT_ROOT=~/Projects/cardiac_rfa \
BENCHMARK_CSV=~/Projects/cardiac_rfa/analysis/stage8_finish_ready/example_data/benchmark_points.csv \
MAIN_DIR=~/Projects/cardiac_rfa/manuscript/figures/main \
SUPP_DIR=~/Projects/cardiac_rfa/manuscript/figures/supplement \
CAPTIONS=~/Projects/cardiac_rfa/manuscript/captions/figure_caption_stubs_v3.md \
SUBMISSION_OUT=~/Projects/cardiac_rfa/manuscript/submission_package \
FIG8_OUTBASE=~/Projects/cardiac_rfa/manuscript/figures/main/fig8_literature_benchmark \
./scripts/run_stage12.sh
```

This will refresh Figure 8 and build:

```text
manuscript/submission_package/
├── main_pdf/
├── main_tiff/
├── main_png_preview/
├── supp_pdf/
├── supp_tiff/
├── supp_png_preview/
├── figure_manifest.csv
└── figure_captions_v3.md
```
