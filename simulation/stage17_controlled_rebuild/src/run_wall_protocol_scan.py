from __future__ import annotations

import argparse
from pathlib import Path
import yaml
import pandas as pd

from model_fd import CaseConfig, clone_cfg, rescale_ny, run_case, summarize_result, line_plot, bool_heatmap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-config', required=True)
    parser.add_argument('--protocols', required=True)
    parser.add_argument('--wall-scan', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())['protocols']
    wall_values = [float(v) for v in yaml.safe_load(Path(args.wall_scan).read_text())['wall_thickness_mm_values']]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for wall_mm in wall_values:
        for p in protocols:
            cfg = clone_cfg(
                base,
                power_W=float(p['power_W']),
                duration_s=float(p['duration_s']),
                wall_thickness_mm=wall_mm,
                ny=rescale_ny(base, wall_mm),
            )
            res = run_case(cfg)
            row = summarize_result(res)
            row['name'] = p['name']
            rows.append(row)
            print(f"wall={wall_mm:.1f} mm | {p['name']} | depth={row['lesion_depth_mm']:.3f} mm | frac={row['depth_fraction']:.3f} | transmural={row['transmural']}")

    df = pd.DataFrame(rows)
    df.to_csv(outdir / 'wall_protocol_summary.csv', index=False)
    line_plot(df, 'wall_thickness_mm', 'lesion_depth_mm', 'name', 'Lesion depth vs wall thickness', 'Wall thickness [mm]', 'Lesion depth [mm]', outdir / 'wall_vs_depth.png')
    line_plot(df, 'wall_thickness_mm', 'depth_fraction', 'name', 'Depth fraction vs wall thickness', 'Wall thickness [mm]', 'Depth fraction', outdir / 'wall_vs_depth_fraction.png')

    heat_df = df[['name', 'wall_thickness_mm', 'transmural']].copy()
    heat_df['transmural_int'] = heat_df['transmural'].astype(int)
    bool_heatmap(heat_df, wall_values, [p['name'] for p in protocols], 'wall_thickness_mm', 'name', 'transmural_int', 'Transmurality map', 'Wall thickness [mm]', 'Protocol', outdir / 'wall_transmurality_map.png')


if __name__ == '__main__':
    main()
