import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch
import pandas as pd
from pubstyle import use_pub_style, save_figure, DOUBLE_COL_IN, PROTOCOL_MARKERS, PROTOCOL_SHORT, WALL_COLORS, soft_legend, title_chip, COOLING_TITLES, GOOD, GOOD_EDGE
from common import protocol_order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--uq-summary-csv', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    use_pub_style()
    df = pd.read_csv(args.uq_summary_csv)
    hvals = sorted(df['cooling_h_nominal_W_per_m2K'].unique())
    wall_levels = sorted(df['wall_thickness_mm'].unique())

    fig, axs = plt.subplots(1, 4, figsize=(DOUBLE_COL_IN, 2.95), constrained_layout=True, sharey=True, gridspec_kw={'width_ratios':[1,1,1,0.8]})
    plot_axes = axs[:3]
    leg_ax = axs[3]
    leg_ax.axis('off')

    for i, h in enumerate(hvals):
        ax = plot_axes[i]
        sub = df[df['cooling_h_nominal_W_per_m2K'] == h]
        patch = FancyBboxPatch((0.77, -0.01), 0.24, 0.24, boxstyle='round,pad=0.02,rounding_size=0.03',
                               linewidth=0.9, edgecolor=GOOD_EDGE, facecolor=GOOD, alpha=0.95, zorder=0,
                               transform=ax.transData)
        ax.add_patch(patch)
        ax.text(0.785, 0.075, 'favorable\nzone', fontsize=7.0, color='#496A5A')
        for _, row in sub.iterrows():
            ax.scatter(row['transmural_probability'], row['overheat_probability'], s=52,
                       marker=PROTOCOL_MARKERS[row['name']], c=WALL_COLORS[float(row['wall_thickness_mm'])],
                       edgecolors='black', linewidths=0.42, alpha=0.96, zorder=3)
        title_chip(ax, COOLING_TITLES.get(int(h), f'h={int(h)}') + f'\n{int(h)} W/m²K')
        ax.set_xlabel('Transmural probability')
        if i == 0:
            ax.set_ylabel('Overheat probability')
        else:
            ax.tick_params(labelleft=False)
        ax.set_xlim(-0.03, 1.03)
        ax.set_ylim(-0.03, 1.03)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True)

    protocol_handles = [Line2D([0],[0], marker=PROTOCOL_MARKERS[n], color='black', linestyle='None', markerfacecolor='#BFC6CF', markeredgecolor='black', markersize=6.8, label=PROTOCOL_SHORT[n]) for n in protocol_order()]
    wall_handles = [Line2D([0],[0], marker='o', color='black', linestyle='None', markerfacecolor=WALL_COLORS[w], markeredgecolor='black', markersize=6.8, label=f'{int(w)} mm') for w in wall_levels]
    leg1 = leg_ax.legend(handles=protocol_handles, title='Protocol', loc='upper left')
    soft_legend(leg1)
    leg_ax.add_artist(leg1)
    leg2 = leg_ax.legend(handles=wall_handles, title='Wall thickness', loc='lower left')
    soft_legend(leg2)

    save_figure(fig, Path(args.outdir) / 'fig7_tradeoff_scatter')

if __name__ == '__main__':
    main()
