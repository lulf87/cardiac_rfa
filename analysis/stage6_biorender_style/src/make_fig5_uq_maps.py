import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from pubstyle import (
    use_pub_style, save_figure, DOUBLE_COL_IN, PROTOCOL_SHORT, PROTOCOL_CHIPS,
    title_chip, row_chip, TRANSMURAL_CMAP, OVERHEAT_CMAP, DEPTH_CMAP,
    COOLING_TITLES
)
from common import protocol_order, prob_show_label


def text_color_for_value(val, cmap, norm):
    r, g, b, _ = cmap(norm(val))
    luminance = 0.2126*r + 0.7152*g + 0.0722*b
    return 'white' if luminance < 0.52 else 'black'


def draw_map(ax, sub, value_col, x_vals, y_vals, cmap, annotate='transition', vmin=0, vmax=1):
    pivot = sub.pivot(index='wall_thickness_mm', columns='insertion_nominal_mm', values=value_col).reindex(index=y_vals, columns=x_vals)
    arr = pivot.values
    norm = Normalize(vmin=vmin, vmax=vmax)
    im = ax.imshow(arr, origin='lower', aspect='auto', cmap=cmap, norm=norm, interpolation='nearest',
                   extent=[x_vals[0]-0.25, x_vals[-1]+0.25, y_vals[0]-0.5, y_vals[-1]+0.5])
    ax.set_xticks(x_vals)
    ax.set_yticks(y_vals)
    xedges = [x_vals[0]-0.25] + [0.5*(x_vals[i]+x_vals[i+1]) for i in range(len(x_vals)-1)] + [x_vals[-1]+0.25]
    yedges = [y_vals[0]-0.5] + [0.5*(y_vals[i]+y_vals[i+1]) for i in range(len(y_vals)-1)] + [y_vals[-1]+0.5]
    for xe in xedges:
        ax.axvline(xe, color='white', lw=0.8, alpha=0.55, zorder=3)
    for ye in yedges:
        ax.axhline(ye, color='white', lw=0.8, alpha=0.55, zorder=3)
    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):
            val = arr[i, j]
            if np.isnan(val):
                continue
            show = annotate == 'all' or (annotate == 'transition' and prob_show_label(val))
            if show:
                ax.text(x, y, f'{val:.2f}', ha='center', va='center', fontsize=7.1, color=text_color_for_value(val, cmap, norm))
    return im


def make_map_figure(df, row_names, col_hvals, value_col, cmap, cbar_label, outbase, annotate='transition'):
    x_vals = sorted(df['insertion_nominal_mm'].unique())
    y_vals = sorted(df['wall_thickness_mm'].unique())
    fig, axs = plt.subplots(len(row_names), len(col_hvals), figsize=(DOUBLE_COL_IN, 5.75), constrained_layout=True, sharex=True, sharey=True)
    axs = np.atleast_2d(axs)
    for r, name in enumerate(row_names):
        for c, h in enumerate(col_hvals):
            ax = axs[r, c]
            sub = df[(df['name'] == name) & (df['cooling_h_nominal_W_per_m2K'] == h)]
            im = draw_map(ax, sub, value_col, x_vals, y_vals, cmap, annotate=annotate)
            ax.set_facecolor('white')
            if r == 0:
                ttl = COOLING_TITLES.get(int(h), f'h = {int(h)}') + f'\n{int(h)} W/m²K'
                title_chip(ax, ttl)
            if c != 0:
                ax.tick_params(labelleft=False)
            if r != len(row_names)-1:
                ax.tick_params(labelbottom=False)
        row_chip(axs[r,0], PROTOCOL_SHORT[name], PROTOCOL_CHIPS[name])
    fig.supxlabel('Nominal insertion [mm]')
    fig.supylabel('Wall thickness [mm]')
    cbar = fig.colorbar(im, ax=axs.ravel().tolist(), fraction=0.022, pad=0.02)
    cbar.set_label(cbar_label)
    save_figure(fig, outbase)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--uq-summary-csv', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    use_pub_style()
    df = pd.read_csv(args.uq_summary_csv)
    outdir = Path(args.outdir)
    hvals = sorted(df['cooling_h_nominal_W_per_m2K'].unique())

    make_map_figure(df, protocol_order(), hvals, 'transmural_probability', TRANSMURAL_CMAP, 'Transmural probability', outdir/'fig5_transmural_probability_maps', annotate='transition')
    over_df = df[df['name'].isin(['hpsd_50W_10s','vhpsd_90W_4s'])].copy()
    make_map_figure(over_df, ['hpsd_50W_10s','vhpsd_90W_4s'], hvals, 'overheat_probability', OVERHEAT_CMAP, 'Overheat probability', outdir/'fig6_overheat_probability_maps', annotate='transition')
    make_map_figure(df, protocol_order(), hvals, 'depth_fraction_p50', DEPTH_CMAP, 'Median depth fraction', outdir/'figS1_depth_fraction_p50_maps', annotate='all')

if __name__ == '__main__':
    main()
