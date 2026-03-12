
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from pubstyle import use_pub_style, save_figure, panel_label, DOUBLE_COL_IN, PROTOCOL_SHORT
from common import protocol_order

def draw_map(ax, sub, value_col, x_vals, y_vals, cmap, annotate_mode="transition"):
    pivot = sub.pivot(index="wall_thickness_mm", columns="insertion_nominal_mm", values=value_col).reindex(index=y_vals, columns=x_vals)
    arr = pivot.values
    im = ax.imshow(arr, origin="lower", aspect="auto", cmap=cmap, norm=Normalize(vmin=0, vmax=1),
                   extent=[x_vals[0]-0.25, x_vals[-1]+0.25, y_vals[0]-0.5, y_vals[-1]+0.5])
    ax.set_xticks(x_vals)
    ax.set_yticks(y_vals)
    # light cell borders
    for x in np.arange(len(x_vals)+1):
        xpos = (x_vals[0]-0.25) + x*0.5
    # annotate only intermediate values by default
    for i, y in enumerate(y_vals):
        for j, x in enumerate(x_vals):
            val = arr[i, j]
            if np.isnan(val):
                continue
            show = False
            if annotate_mode == "all":
                show = True
            elif annotate_mode == "transition":
                show = (val > 0.0 + 1e-9) and (val < 1.0 - 1e-9)
            if show:
                txt_color = "white" if val < 0.45 else "black"
                ax.text(x, y, f"{val:.2f}", ha="center", va="center", fontsize=7.2, color=txt_color)
    return im

def make_grid_figure(df, names, value_col, row_names, col_hvals, outbase, cbar_label, cmap="viridis"):
    x_vals = sorted(df["insertion_nominal_mm"].unique())
    y_vals = sorted(df["wall_thickness_mm"].unique())
    fig, axs = plt.subplots(len(row_names), len(col_hvals), figsize=(DOUBLE_COL_IN, 0.95*len(row_names)+3.2), constrained_layout=True)
    if len(row_names) == 1:
        axs = np.array([axs])
    if len(col_hvals) == 1:
        axs = axs[:, None]
    for r, name in enumerate(row_names):
        for c, h in enumerate(col_hvals):
            ax = axs[r, c]
            sub = df[(df["name"] == name) & (df["cooling_h_nominal_W_per_m2K"] == h)]
            im = draw_map(ax, sub, value_col, x_vals, y_vals, cmap=cmap, annotate_mode="transition")
            if r == 0:
                ax.set_title(f"h = {int(h)} W/m²K")
            if c == 0:
                ax.set_ylabel(f"{PROTOCOL_SHORT[name]}\nWall thickness [mm]")
            else:
                ax.set_ylabel("")
            if r == len(row_names)-1:
                ax.set_xlabel("Nominal insertion [mm]")
            else:
                ax.set_xlabel("")
    cbar = fig.colorbar(im, ax=axs.ravel().tolist(), fraction=0.018, pad=0.02)
    cbar.set_label(cbar_label)
    save_figure(fig, outbase)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uq-summary-csv", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    use_pub_style()
    df = pd.read_csv(args.uq_summary_csv)
    col_hvals = sorted(df["cooling_h_nominal_W_per_m2K"].unique())
    outdir = Path(args.outdir)

    # Full transmural probability map across protocols
    make_grid_figure(
        df=df,
        names=protocol_order(),
        value_col="transmural_probability",
        row_names=protocol_order(),
        col_hvals=col_hvals,
        outbase=outdir/"fig5_transmural_probability_maps",
        cbar_label="Transmural probability",
        cmap="viridis"
    )

    # Overheat probability - omit Standard from main figure because it is identically zero in current dataset
    make_grid_figure(
        df=df,
        names=["hpsd_50W_10s", "vhpsd_90W_4s"],
        value_col="overheat_probability",
        row_names=["hpsd_50W_10s", "vhpsd_90W_4s"],
        col_hvals=col_hvals,
        outbase=outdir/"fig6_overheat_probability_maps",
        cbar_label="Overheat probability",
        cmap="magma"
    )

    # Supplemental map: median depth fraction
    make_grid_figure(
        df=df,
        names=protocol_order(),
        value_col="depth_fraction_p50",
        row_names=protocol_order(),
        col_hvals=col_hvals,
        outbase=outdir/"figS1_depth_fraction_p50_maps",
        cbar_label="Median depth fraction",
        cmap="cividis"
    )

if __name__ == "__main__":
    main()
