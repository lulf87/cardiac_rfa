#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

PALETTE = {
    'background': '#f6f4ef',
    'grid': '#c8ced6',
    'axis': '#42526e',
    'chip': '#73879a',
    'reported': '#b9c3cf',
    'standard': '#2aa198',
    'hpsd': '#8f80c9',
    'vhpsd': '#e07b58',
}
MARKERS = {
    'standard_30W_30s': 'o',
    'hpsd_50W_10s': 's',
    'vhpsd_90W_4s': '^',
}
COLORS = {
    'standard_30W_30s': PALETTE['standard'],
    'hpsd_50W_10s': PALETTE['hpsd'],
    'vhpsd_90W_4s': PALETTE['vhpsd'],
}
DISPLAY = {
    'standard_30W_30s': 'Standard',
    'hpsd_50W_10s': 'HPSD',
    'vhpsd_90W_4s': 'vHPSD',
}
ORDER = ['standard_30W_30s', 'hpsd_50W_10s', 'vhpsd_90W_4s']


def style_axes(ax):
    ax.set_facecolor(PALETTE['background'])
    ax.grid(True, color=PALETTE['grid'], lw=0.8, alpha=0.6)
    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
    for side in ['left', 'bottom']:
        ax.spines[side].set_color(PALETTE['axis'])
        ax.spines[side].set_linewidth(1.2)
    ax.tick_params(colors=PALETTE['axis'], labelsize=10)
    ax.xaxis.label.set_color(PALETTE['axis'])
    ax.yaxis.label.set_color(PALETTE['axis'])
    ax.title.set_color(PALETTE['axis'])


def chip(ax, text):
    ax.text(
        0.5, 1.06, text, transform=ax.transAxes,
        ha='center', va='bottom', fontsize=11, color='white',
        bbox=dict(boxstyle='round,pad=0.28,rounding_size=0.12',
                  facecolor=PALETTE['chip'], edgecolor='none')
    )


def build_fig(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 5.8), facecolor=PALETTE['background'])

    # (a) depth agreement scatter
    ax = axes[0]
    style_axes(ax)
    maxv = max(df['reported_depth_mm'].max(), df['simulated_depth_mm'].max()) * 1.1
    ax.plot([0, maxv], [0, maxv], ls='--', color=PALETTE['chip'], lw=1.6)
    for _, row in df.iterrows():
        p = row['protocol_key']
        ax.scatter(row['reported_depth_mm'], row['simulated_depth_mm'], s=120,
                   marker=MARKERS[p], facecolor=COLORS[p], edgecolor='black', linewidth=1.2, zorder=3)
    ax.set_xlim(0, maxv)
    ax.set_ylim(0, maxv)
    ax.set_xlabel('Reported lesion depth [mm]', fontsize=11)
    ax.set_ylabel('Simulated lesion depth [mm]', fontsize=11)
    ax.text(-0.14, 1.08, '(a)', transform=ax.transAxes, fontsize=18, fontweight='bold', color=PALETTE['axis'])
    chip(ax, 'Depth agreement')
    handles = [
        Line2D([0], [0], marker=MARKERS[p], color='none', markerfacecolor=COLORS[p],
               markeredgecolor='black', markersize=10, label=DISPLAY[p]) for p in ORDER
    ]
    leg = ax.legend(handles=handles, title='Protocol', loc='lower right', frameon=True)
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_edgecolor('#b4bcc6')
    leg.get_title().set_color(PALETTE['axis'])
    for t in leg.get_texts():
        t.set_color(PALETTE['axis'])

    # (b) protocol-level trend
    ax = axes[1]
    style_axes(ax)
    grp = df.groupby('protocol_key', as_index=False)[['reported_depth_mm', 'simulated_depth_mm']].mean()
    grp['sort'] = grp['protocol_key'].map({k: i for i, k in enumerate(ORDER)})
    grp = grp.sort_values('sort')
    x = range(len(grp))
    width = 0.35
    ax.bar([i - width/2 for i in x], grp['reported_depth_mm'], width=width,
           color=PALETTE['reported'], edgecolor='black', linewidth=1.2, label='Reported mean')
    ax.bar([i + width/2 for i in x], grp['simulated_depth_mm'], width=width,
           color=[COLORS[p] for p in grp['protocol_key']], edgecolor='black', linewidth=1.2, label='Simulated mean')
    ax.set_xticks(list(x))
    ax.set_xticklabels([DISPLAY[p] for p in grp['protocol_key']], fontsize=11)
    ax.set_ylabel('Mean lesion depth [mm]', fontsize=11)
    ax.text(-0.14, 1.08, '(b)', transform=ax.transAxes, fontsize=18, fontweight='bold', color=PALETTE['axis'])
    chip(ax, 'Protocol-level trend')
    leg = ax.legend(loc='upper right', frameon=True)
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_edgecolor('#b4bcc6')
    for t in leg.get_texts():
        t.set_color(PALETTE['axis'])

    fig.tight_layout()
    return fig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True)
    ap.add_argument('--outbase', required=True)
    args = ap.parse_args()
    df = pd.read_csv(args.csv)
    required = {'source_id', 'protocol_key', 'reported_depth_mm', 'simulated_depth_mm'}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f'Missing columns: {sorted(missing)}')
    fig = build_fig(df)
    outbase = Path(args.outbase)
    outbase.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(outbase) + '.pdf', bbox_inches='tight')
    fig.savefig(str(outbase) + '.png', dpi=300, bbox_inches='tight')
    fig.savefig(str(outbase) + '.tiff', dpi=600, bbox_inches='tight', pil_kwargs={'compression': 'tiff_lzw'})
    print(f'Saved {outbase}.pdf/.png/.tiff')


if __name__ == '__main__':
    main()
