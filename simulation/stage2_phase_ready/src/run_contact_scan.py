from __future__ import annotations

import argparse
from pathlib import Path
import yaml
import pandas as pd

from model_fd import CaseConfig, clone_cfg, run_case, summarize_result, line_plot, bool_heatmap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-config', required=True)
    parser.add_argument('--protocols', required=True)
    parser.add_argument('--contact-scan', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())['protocols']
    insertion_values = [float(v) for v in yaml.safe_load(Path(args.contact_scan).read_text())['insertion_depth_mm_values']]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for ins in insertion_values:
        for p in protocols:
            cfg = clone_cfg(base, power_W=float(p['power_W']), duration_s=float(p['duration_s']), insertion_depth_mm=ins)
            res = run_case(cfg)
            row = summarize_result(res)
            row['name'] = p['name']
            rows.append(row)
            print(f"ins={ins:.2f} mm | {p['name']} | depth={row['lesion_depth_mm']:.3f} mm | Tmax={row['peak_temperature_C']:.2f} C | transmural={row['transmural']}")

    df = pd.DataFrame(rows)
    df.to_csv(outdir / 'contact_protocol_summary.csv', index=False)
    line_plot(df, 'insertion_depth_mm', 'lesion_depth_mm', 'name', 'Lesion depth vs contact surrogate', 'Insertion depth surrogate [mm]', 'Lesion depth [mm]', outdir / 'contact_vs_depth.png')
    line_plot(df, 'insertion_depth_mm', 'peak_temperature_C', 'name', 'Peak temperature vs contact surrogate', 'Insertion depth surrogate [mm]', 'Peak temperature [°C]', outdir / 'contact_vs_peakT.png')
    heat_df = df[['name', 'insertion_depth_mm', 'transmural']].copy()
    heat_df['transmural_int'] = heat_df['transmural'].astype(int)
    bool_heatmap(heat_df, insertion_values, [p['name'] for p in protocols], 'insertion_depth_mm', 'name', 'transmural_int', 'Transmurality vs contact surrogate', 'Insertion depth [mm]', 'Protocol', outdir / 'contact_transmurality_map.png')


if __name__ == '__main__':
    main()
