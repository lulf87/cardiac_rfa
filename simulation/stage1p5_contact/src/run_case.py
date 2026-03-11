from __future__ import annotations

import argparse
from pathlib import Path

from model_fd import CaseConfig, run_case, plot_case, save_summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    cfg = CaseConfig.from_yaml(args.config)
    result = run_case(cfg)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plot_case(result, outdir / 'case_fields.png')
    save_summary(result, outdir / 'summary.yaml')
    print(f'Saved results to {outdir}')
    print(f"Lesion depth: {result['lesion_depth_mm']:.3f} mm")
    print(f"Peak temperature: {result['peak_T_C'].max():.2f} C")
    print(f"Overheat area >=100C: {result['overheat_area_mm2']:.4f} mm^2")


if __name__ == '__main__':
    main()
