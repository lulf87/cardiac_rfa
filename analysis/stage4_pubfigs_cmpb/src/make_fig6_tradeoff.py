
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pubstyle import use_pub_style, save_figure, panel_label, DOUBLE_COL_IN, PROTOCOL_COLORS, PROTOCOL_MARKERS, PROTOCOL_SHORT

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uq-summary-csv", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    use_pub_style()
    df = pd.read_csv(args.uq_summary_csv)
    hvals = sorted(df["cooling_h_nominal_W_per_m2K"].unique())
    wall_levels = sorted(df["wall_thickness_mm"].unique())
    wall_palette = {2.0:"#1b9e77", 3.0:"#66a61e", 4.0:"#e6ab02", 6.0:"#d95f02"}
    # if 5 mm present in paper version, auto-extend
    if 5.0 in wall_levels:
        wall_palette[5.0] = "#a6761d"

    fig, axs = plt.subplots(1, len(hvals), figsize=(DOUBLE_COL_IN, 2.7), constrained_layout=True, sharex=True, sharey=True)
    if len(hvals) == 1:
        axs = [axs]

    for i, h in enumerate(hvals):
        ax = axs[i]
        sub = df[df["cooling_h_nominal_W_per_m2K"] == h]
        for _, row in sub.iterrows():
            ax.scatter(
                row["transmural_probability"], row["overheat_probability"],
                s=18 + 28*row["insertion_nominal_mm"],
                marker=PROTOCOL_MARKERS[row["name"]],
                c=wall_palette.get(row["wall_thickness_mm"], "#666666"),
                edgecolors="black", linewidths=0.3, alpha=0.9
            )
        ax.set_title(f"h = {int(h)} W/m²K")
        ax.set_xlabel("Transmural probability")
        if i == 0:
            ax.set_ylabel("Overheat probability")
        ax.set_xlim(-0.03, 1.03)
        ax.set_ylim(-0.03, 1.03)
        ax.grid(alpha=0.18)

    protocol_handles = [
        Line2D([0], [0], marker=PROTOCOL_MARKERS[n], color="w", markerfacecolor="0.6",
               markeredgecolor="black", markersize=6, label=PROTOCOL_SHORT[n])
        for n in ["standard_30W_30s", "hpsd_50W_10s", "vhpsd_90W_4s"]
    ]
    wall_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=wall_palette[w],
               markeredgecolor="black", markersize=6, label=f"{w:.0f} mm")
        for w in sorted(wall_palette.keys())
    ]
    axs[-1].legend(handles=protocol_handles + wall_handles, frameon=False, loc="center left",
                   bbox_to_anchor=(1.02, 0.5), title="Markers: protocol\nColors: wall thickness")
    save_figure(fig, Path(args.outdir)/"fig7_tradeoff_scatter")

if __name__ == "__main__":
    main()
