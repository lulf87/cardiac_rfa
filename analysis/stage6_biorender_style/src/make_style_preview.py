import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from pubstyle import use_pub_style, save_figure, DOUBLE_COL_IN, PROTOCOL_COLORS, WALL_COLORS, SLATE, PROTOCOL_CHIPS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()
    use_pub_style()
    fig, ax = plt.subplots(figsize=(DOUBLE_COL_IN*0.72, 1.7), constrained_layout=True)
    ax.axis('off')
    ax.text(0.02, 0.88, 'Unified palette preview', fontsize=10, fontweight='bold', transform=ax.transAxes)
    ax.text(0.02, 0.72, 'Protocol colors', fontsize=8.5, color=SLATE, transform=ax.transAxes)
    xs = [0.02, 0.22, 0.42]
    labels = ['Standard', 'HPSD', 'vHPSD']
    keys = ['standard_30W_30s','hpsd_50W_10s','vhpsd_90W_4s']
    for x, lab, key in zip(xs, labels, keys):
        ax.add_patch(plt.Rectangle((x, 0.50), 0.14, 0.12, transform=ax.transAxes, facecolor=PROTOCOL_COLORS[key], edgecolor='none'))
        ax.text(x+0.07, 0.40, lab, ha='center', va='top', fontsize=8.3, transform=ax.transAxes)
        ax.add_patch(plt.Rectangle((x, 0.22), 0.14, 0.08, transform=ax.transAxes, facecolor=PROTOCOL_CHIPS[key], edgecolor='none'))
    ax.text(0.62, 0.72, 'Wall colors', fontsize=8.5, color=SLATE, transform=ax.transAxes)
    x = 0.62
    for i, (wall, color) in enumerate(WALL_COLORS.items()):
        ax.add_patch(plt.Circle((x + i*0.07, 0.56), 0.025, transform=ax.transAxes, facecolor=color, edgecolor='black', lw=0.4))
        ax.text(x + i*0.07, 0.40, f'{int(wall)}', ha='center', va='top', fontsize=7.8, transform=ax.transAxes)
    save_figure(fig, Path(args.outdir) / 'style_preview_palette')


if __name__ == '__main__':
    main()
