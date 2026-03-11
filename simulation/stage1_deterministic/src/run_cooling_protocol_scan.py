from __future__ import annotations

import argparse
from pathlib import Path
import yaml
import pandas as pd

from model_fd import CaseConfig, clone_cfg, run_case, summarize_result, line_plot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-config', required=True)
    parser.add_argument('--protocols', required=True)
    parser.add_argument('--cooling-scan', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())['protocols']
    h_values = [float(v) for v in yaml.safe_load(Path(args.cooling_scan).read_text())['cooling_h_W_per_m2K_values']]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for h in h_values:
        for p in protocols:
            cfg = clone_cfg(
                base,
                power_W=float(p['power_W']),
                duration_s=float(p['duration_s']),
                cooling_h_W_per_m2K=h,
            )
            res = run_case(cfg)
            row = summarize_result(res)
            row['name'] = p['name']
            rows.append(row)
            print(f"h={h:.0f} | {p['name']} | depth={row['lesion_depth_mm']:.3f} mm | Tmax={row['peak_temperature_C']:.2f} C")

    df = pd.DataFrame(rows)
    df.to_csv(outdir / 'cooling_protocol_summary.csv', index=False)
    line_plot(
        df=df,
        x_col='cooling_h_W_per_m2K',
        y_col='lesion_depth_mm',
        group_col='name',
        title='Lesion depth vs cooling',
        xlabel='Cooling coefficient h [W/m²K]',
        ylabel='Lesion depth [mm]',
        outpath=outdir / 'cooling_vs_depth.png',
    )
    line_plot(
        df=df,
        x_col='cooling_h_W_per_m2K',
        y_col='peak_temperature_C',
        group_col='name',
        title='Peak temperature vs cooling',
        xlabel='Cooling coefficient h [W/m²K]',
        ylabel='Peak temperature [°C]',
        outpath=outdir / 'cooling_vs_peakT.png',
    )


if __name__ == '__main__':
    main()
