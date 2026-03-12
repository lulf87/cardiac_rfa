import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from pubstyle import use_pub_style, save_figure, panel_label, DOUBLE_COL_IN, title_chip, soft_legend, PROTOCOL_COLORS


def rel_error_percent(series):
    ref = series.iloc[-1]
    return (series - ref).abs() / abs(ref) * 100.0 if abs(ref) > 1e-12 else series * 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--grid-csv', required=True)
    ap.add_argument('--dt-csv', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    use_pub_style()
    grid = pd.read_csv(args.grid_csv).sort_values(['nx','ny'])
    dt = pd.read_csv(args.dt_csv).sort_values('dt_s', ascending=False)

    fig, axs = plt.subplots(1, 2, figsize=(DOUBLE_COL_IN, 2.95), constrained_layout=True)

    ax = axs[0]
    xg = [f"{n}×{m}" for n, m in zip(grid['nx'], grid['ny'])]
    e_depth = rel_error_percent(grid['lesion_depth_mm'])
    e_temp = rel_error_percent(grid['peak_temperature_C'])
    ax.plot(xg, e_depth, marker='o', color='#4C78A8', label='Lesion depth')
    ax.plot(xg, e_temp, marker='s', color='#F58518', label='Peak temperature')
    ax.set_xlabel('Grid')
    ax.set_ylabel('Relative error to finest solution [%]')
    ax.set_ylim(0, max(e_depth.max(), e_temp.max())*1.15)
    ax.grid(axis='y')
    title_chip(ax, 'Grid refinement')
    panel_label(ax, '(a)')
    leg = ax.legend(loc='upper right')
    soft_legend(leg)

    ax = axs[1]
    xd = [f"{v:.3f}" for v in dt['dt_s']]
    e_depth = rel_error_percent(dt['lesion_depth_mm'])
    e_temp = rel_error_percent(dt['peak_temperature_C'])
    ax.plot(xd, e_depth, marker='o', color='#4C78A8', label='Lesion depth')
    ax.plot(xd, e_temp, marker='s', color='#F58518', label='Peak temperature')
    ax.set_xlabel('Δt [s]')
    ax.set_ylabel('Relative error to finest solution [%]')
    ax.set_ylim(0, max(e_depth.max(), e_temp.max())*1.15)
    ax.grid(axis='y')
    title_chip(ax, 'Time-step refinement')
    panel_label(ax, '(b)')
    leg = ax.legend(loc='upper right')
    soft_legend(leg)

    save_figure(fig, Path(args.outdir) / 'fig4_verification')

if __name__ == '__main__':
    main()
