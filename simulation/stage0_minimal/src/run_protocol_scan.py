from __future__ import annotations

import argparse
from pathlib import Path
import yaml
import pandas as pd
import matplotlib.pyplot as plt

from model_fd import CaseConfig, run_case, plot_case, save_summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-config', required=True)
    parser.add_argument('--protocols', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())['protocols']
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []

    for p in protocols:
        cfg = CaseConfig(**base.__dict__)
        cfg.power_W = float(p['power_W'])
        cfg.duration_s = float(p['duration_s'])
        res = run_case(cfg)
        case_dir = outdir / p['name']
        case_dir.mkdir(exist_ok=True)
        plot_case(res, case_dir / 'case_fields.png')
        save_summary(res, case_dir / 'summary.yaml')
        rows.append({
            'name': p['name'],
            'power_W': cfg.power_W,
            'duration_s': cfg.duration_s,
            'lesion_depth_mm': res['lesion_depth_mm'],
            'peak_temperature_C': float(res['peak_T_C'].max()),
            'overheat_area_mm2': res['overheat_area_mm2'],
            'transmural': res['transmural'],
        })

    df = pd.DataFrame(rows)
    df.to_csv(outdir / 'protocol_summary.csv', index=False)

    fig, ax = plt.subplots(figsize=(7, 4.2), constrained_layout=True)
    ax.scatter(df['peak_temperature_C'], df['lesion_depth_mm'])
    for _, r in df.iterrows():
        ax.annotate(r['name'], (r['peak_temperature_C'], r['lesion_depth_mm']), fontsize=8, xytext=(4, 4), textcoords='offset points')
    ax.set_xlabel('Peak temperature [°C]')
    ax.set_ylabel('Lesion depth [mm]')
    ax.set_title('Protocol comparison (stage-0 sandbox)')
    fig.savefig(outdir / 'protocol_comparison.png', dpi=180)
    plt.close(fig)
    print(df)


if __name__ == '__main__':
    main()
