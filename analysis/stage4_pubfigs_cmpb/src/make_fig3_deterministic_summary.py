
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from pubstyle import use_pub_style, save_figure, panel_label, DOUBLE_COL_IN, PROTOCOL_COLORS, PROTOCOL_LABELS, PROTOCOL_SHORT
from common import read_csv, protocol_order

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase-prep-csv", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    use_pub_style()
    df = read_csv(args.phase_prep_csv)
    order = protocol_order()

    fig, axs = plt.subplots(2, 2, figsize=(DOUBLE_COL_IN, 5.2), constrained_layout=True)

    # (a) wall sweep at nominal h=1500, ins=1.0
    ax = axs[0,0]
    sub = df[(df["cooling_h_W_per_m2K"] == 1500) & (df["insertion_depth_mm"] == 1.0)]
    for name in order:
        s = sub[sub["name"] == name].sort_values("wall_thickness_mm")
        ax.plot(s["wall_thickness_mm"], s["depth_fraction"], marker="o",
                color=PROTOCOL_COLORS[name], label=PROTOCOL_SHORT[name])
    ax.set_xlabel("Wall thickness [mm]")
    ax.set_ylabel("Depth fraction [-]")
    ax.set_ylim(0, 1.08)
    ax.set_title("Nominal cooling and contact")
    ax.legend(frameon=False, ncol=1, loc="upper right")
    panel_label(ax, "(a)")

    # (b) insertion sweep at thin wall and nominal cooling
    ax = axs[0,1]
    sub = df[(df["wall_thickness_mm"] == 2.0) & (df["cooling_h_W_per_m2K"] == 1500)]
    for name in order:
        s = sub[sub["name"] == name].sort_values("insertion_depth_mm")
        ax.plot(s["insertion_depth_mm"], s["depth_fraction"], marker="o",
                color=PROTOCOL_COLORS[name], label=PROTOCOL_SHORT[name])
    ax.set_xlabel("Nominal insertion [mm]")
    ax.set_ylabel("Depth fraction [-]")
    ax.set_ylim(0, 1.08)
    ax.set_title("Thin wall, nominal cooling")
    panel_label(ax, "(b)")

    # (c) cooling sweep at 4 mm wall and higher contact
    ax = axs[1,0]
    sub = df[(df["wall_thickness_mm"] == 4.0) & (df["insertion_depth_mm"] == 1.5)]
    for name in order:
        s = sub[sub["name"] == name].sort_values("cooling_h_W_per_m2K")
        ax.plot(s["cooling_h_W_per_m2K"], s["depth_fraction"], marker="o",
                color=PROTOCOL_COLORS[name], label=PROTOCOL_SHORT[name])
    ax.set_xlabel("Cooling coefficient h [W/m²K]")
    ax.set_ylabel("Depth fraction [-]")
    ax.set_ylim(0, 1.0)
    ax.set_title("Moderate-thickness wall, elevated contact")
    panel_label(ax, "(c)")

    # (d) temperature rise at thin wall and nominal cooling
    ax = axs[1,1]
    sub = df[(df["wall_thickness_mm"] == 2.0) & (df["cooling_h_W_per_m2K"] == 1500)]
    for name in order:
        s = sub[sub["name"] == name].sort_values("insertion_depth_mm")
        ax.plot(s["insertion_depth_mm"], s["peak_temperature_C"], marker="o",
                color=PROTOCOL_COLORS[name], label=PROTOCOL_SHORT[name])
    ax.axhline(100.0, color="0.35", ls="--", lw=1.0)
    ax.text(0.02, 0.96, "100°C threshold", transform=ax.transAxes, va="top", ha="left", fontsize=7.5, color="0.3")
    ax.set_xlabel("Nominal insertion [mm]")
    ax.set_ylabel("Peak temperature [°C]")
    ax.set_title("Thin wall, nominal cooling")
    panel_label(ax, "(d)")

    save_figure(fig, Path(args.outdir)/"fig3_deterministic_summary")

if __name__ == "__main__":
    main()
