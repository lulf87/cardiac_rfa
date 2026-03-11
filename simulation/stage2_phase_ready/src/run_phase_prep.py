
from __future__ import annotations

import argparse
from pathlib import Path
import yaml
import pandas as pd
import matplotlib.pyplot as plt

from model_fd import CaseConfig, clone_cfg, rescale_ny, run_case, summarize_result


def save_protocol_heatmap(df: pd.DataFrame, protocol_name: str, value_col: str, title: str, outpath: Path) -> None:
    sub = df[df['name'] == protocol_name].copy()
    pivot = sub.pivot_table(
        index='wall_thickness_mm',
        columns=['cooling_h_W_per_m2K', 'insertion_depth_mm'],
        values=value_col,
        aggfunc='mean',
    ).sort_index()

    fig, ax = plt.subplots(figsize=(10.0, 4.8), constrained_layout=True)
    im = ax.imshow(pivot.values, aspect='auto', origin='lower')
    ax.set_title(f'{protocol_name}: {title}')
    ax.set_xlabel('(cooling h, insertion)')
    ax.set_ylabel('Wall thickness [mm]')
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels([f'{v:.1f}' for v in pivot.index])

    xticks = range(len(pivot.columns))
    xlabels = [f'{c[0]:.0f},{c[1]:.1f}' for c in pivot.columns]
    ax.set_xticks(list(xticks))
    ax.set_xticklabels(xlabels, rotation=45, ha='right', fontsize=8)

    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.values[i, j]
            if pd.notna(val):
                text = f'{val:.2f}' if value_col != 'transmural_int' else f'{int(val)}'
                ax.text(j, i, text, ha='center', va='center', fontsize=7)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(value_col)
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-config', required=True)
    parser.add_argument('--protocols', required=True)
    parser.add_argument('--phase-config', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())['protocols']
    phase_cfg = yaml.safe_load(Path(args.phase_config).read_text())

    wall_values = [float(v) for v in phase_cfg['wall_thickness_mm_values']]
    cooling_values = [float(v) for v in phase_cfg['cooling_h_W_per_m2K_values']]
    insertion_values = [float(v) for v in phase_cfg['insertion_depth_mm_values']]

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for wall_mm in wall_values:
        for h in cooling_values:
            for ins in insertion_values:
                for p in protocols:
                    cfg = clone_cfg(
                        base,
                        power_W=float(p['power_W']),
                        duration_s=float(p['duration_s']),
                        wall_thickness_mm=wall_mm,
                        cooling_h_W_per_m2K=h,
                        insertion_depth_mm=ins,
                        ny=rescale_ny(base, wall_mm),
                    )
                    res = run_case(cfg)
                    row = summarize_result(res)
                    row['name'] = p['name']
                    rows.append(row)
                    print(
                        f"wall={wall_mm:.1f} | h={h:.0f} | ins={ins:.2f} | {p['name']} | "
                        f"depth={row['lesion_depth_mm']:.3f} mm | frac={row['depth_fraction']:.3f} | "
                        f"Tmax={row['peak_temperature_C']:.2f} C | transmural={row['transmural']}"
                    )

    df = pd.DataFrame(rows)
    df['transmural_int'] = df['transmural'].astype(int)
    df.to_csv(outdir / 'phase_prep_summary.csv', index=False)

    for protocol_name in df['name'].unique():
        save_protocol_heatmap(
            df, protocol_name, 'depth_fraction',
            'Depth fraction across wall/cooling/contact',
            outdir / f'{protocol_name}_depth_fraction_heatmap.png'
        )
        save_protocol_heatmap(
            df, protocol_name, 'transmural_int',
            'Deterministic transmural map',
            outdir / f'{protocol_name}_transmural_heatmap.png'
        )

    overview = (
        df.groupby('name')[['lesion_depth_mm', 'depth_fraction', 'peak_temperature_C', 'transmural_int']]
        .agg(['mean', 'min', 'max'])
    )
    overview.to_csv(outdir / 'phase_prep_overview.csv')
    print("\nSaved phase-prep results to", outdir)


if __name__ == '__main__':
    main()
