from __future__ import annotations

import argparse
from pathlib import Path
import yaml
import pandas as pd
import matplotlib.pyplot as plt

from model_fd import CaseConfig, clone_cfg, run_case, summarize_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-config', required=True)
    parser.add_argument('--convergence-config', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    cfg_yaml = yaml.safe_load(Path(args.convergence_config).read_text())
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    grid_rows = []
    for item in cfg_yaml['grid_cases']:
        nx = int(item['nx'])
        ny = int(item['ny'])
        cfg = clone_cfg(base, nx=nx, ny=ny)
        res = run_case(cfg)
        row = summarize_result(res)
        row['case'] = f'grid_{nx}x{ny}'
        grid_rows.append(row)
        print(f"grid {nx}x{ny} | depth={row['lesion_depth_mm']:.3f} mm | Tmax={row['peak_temperature_C']:.2f} C")
    grid_df = pd.DataFrame(grid_rows)
    grid_df.to_csv(outdir / 'grid_convergence.csv', index=False)

    dt_rows = []
    for dt in cfg_yaml['dt_values_s']:
        cfg = clone_cfg(base, dt_s=float(dt))
        res = run_case(cfg)
        row = summarize_result(res)
        row['case'] = f'dt_{float(dt):.3f}'
        dt_rows.append(row)
        print(f"dt {float(dt):.3f} s | depth={row['lesion_depth_mm']:.3f} mm | Tmax={row['peak_temperature_C']:.2f} C")
    dt_df = pd.DataFrame(dt_rows)
    dt_df.to_csv(outdir / 'dt_convergence.csv', index=False)

    fig, ax = plt.subplots(figsize=(7.2, 4.6), constrained_layout=True)
    ax.plot(grid_df['nx'], grid_df['lesion_depth_mm'], marker='o')
    ax.set_xlabel('nx')
    ax.set_ylabel('Lesion depth [mm]')
    ax.set_title('Grid convergence: lesion depth vs nx')
    fig.savefig(outdir / 'grid_convergence_depth.png', dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.6), constrained_layout=True)
    ax.plot(dt_df['dt_s'], dt_df['lesion_depth_mm'], marker='o')
    ax.set_xlabel('Time step dt [s]')
    ax.set_ylabel('Lesion depth [mm]')
    ax.set_title('Time-step convergence: lesion depth vs dt')
    fig.savefig(outdir / 'dt_convergence_depth.png', dpi=180)
    plt.close(fig)


if __name__ == '__main__':
    main()
