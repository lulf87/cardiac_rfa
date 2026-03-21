from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROTOCOL_ORDER = [
    "standard_30W_30s",
    "hpsd_50W_10s",
    "vhpsd_90W_4s_fixed",
    "vhpsd_90W_4s_controlled",
]

PROTOCOL_LABELS = {
    "standard_30W_30s": "Standard 30 W / 30 s",
    "hpsd_50W_10s": "HPSD 50 W / 10 s",
    "vhpsd_90W_4s_fixed": "90 W / 4 s fixed",
    "vhpsd_90W_4s_controlled": "90 W / 4 s temperature-limited",
}

COLORS = {
    "standard_30W_30s": "#2A9D8F",
    "hpsd_50W_10s": "#4C78A8",
    "vhpsd_90W_4s_fixed": "#E76F51",
    "vhpsd_90W_4s_controlled": "#6C5CE7",
}

MARKERS = {
    "standard_30W_30s": "o",
    "hpsd_50W_10s": "s",
    "vhpsd_90W_4s_fixed": "^",
    "vhpsd_90W_4s_controlled": "D",
}


def save_all(fig: plt.Figure, outbase: Path) -> None:
    outbase.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outbase.with_suffix(".pdf"))
    fig.savefig(outbase.with_suffix(".png"), dpi=300)
    fig.savefig(
        outbase.with_suffix(".tiff"),
        dpi=600,
        pil_kwargs={"compression": "tiff_lzw"},
    )
    plt.close(fig)


def make_figure(phase_df: pd.DataFrame, outbase: Path) -> None:
    fig = plt.figure(figsize=(13.4, 8.0))
    gs = fig.add_gridspec(3, 3, height_ratios=[1.0, 1.0, 0.18], hspace=0.34, wspace=0.18)
    axes = [
        [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2])],
        [fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1]), fig.add_subplot(gs[1, 2])],
    ]
    legend_ax = fig.add_subplot(gs[2, :])
    legend_ax.axis("off")

    wall_slice = phase_df[
        (phase_df["cooling_h_W_per_m2K"] == 1500.0)
        & (phase_df["insertion_depth_mm"] == 1.0)
    ].copy()
    ins_slice = phase_df[
        (phase_df["wall_thickness_mm"] == 4.0)
        & (phase_df["cooling_h_W_per_m2K"] == 1500.0)
    ].copy()
    cool_slice = phase_df[
        (phase_df["wall_thickness_mm"] == 4.0)
        & (phase_df["insertion_depth_mm"] == 1.0)
    ].copy()

    panels = [
        (
            axes[0][0],
            wall_slice,
            "wall_thickness_mm",
            "lesion_depth_mm",
            "Wall thickness [mm]",
            "Lesion depth [mm]",
            "(a) Depth vs wall thickness",
        ),
        (
            axes[0][1],
            wall_slice,
            "wall_thickness_mm",
            "lesion_width_mm",
            "Wall thickness [mm]",
            "Maximum lesion width [mm]",
            "(b) Width vs wall thickness",
        ),
        (
            axes[0][2],
            wall_slice,
            "wall_thickness_mm",
            "lesion_area_mm2",
            "Wall thickness [mm]",
            "Lesion area [mm²]",
            "(c) Area vs wall thickness",
        ),
        (
            axes[1][0],
            ins_slice,
            "insertion_depth_mm",
            "peak_temperature_C",
            "Insertion depth [mm]",
            "Peak temperature [°C]",
            "(d) Peak temperature vs insertion",
        ),
        (
            axes[1][1],
            cool_slice,
            "cooling_h_W_per_m2K",
            "depth_fraction",
            "Cooling coefficient h [W m$^{-2}$ K$^{-1}$]",
            "Depth fraction [-]",
            "(e) Depth fraction vs cooling",
        ),
        (
            axes[1][2],
            cool_slice,
            "cooling_h_W_per_m2K",
            "delivered_energy_J",
            "Cooling coefficient h [W m$^{-2}$ K$^{-1}$]",
            "Delivered energy [J]",
            "(f) Delivered energy vs cooling",
        ),
    ]

    for ax, sub, xcol, ycol, xlabel, ylabel, title in panels:
        for name in PROTOCOL_ORDER:
            g = sub[sub["name"] == name].sort_values(xcol)
            if g.empty:
                continue
            ax.plot(
                g[xcol],
                g[ycol],
                marker=MARKERS[name],
                color=COLORS[name],
                linewidth=2.0,
                markersize=6.0,
                label=PROTOCOL_LABELS[name],
            )
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc="left", fontweight="bold")
        ax.margins(x=0.05)
        if ycol == "depth_fraction":
            ax.set_ylim(0.0, 1.05)

    handles, labels = axes[0][0].get_legend_handles_labels()
    legend_ax.legend(
        handles,
        labels,
        ncol=4,
        loc="center",
        frameon=False,
    )
    save_all(fig, outbase)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-csv", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    phase_df = pd.read_csv(args.phase_csv)
    outdir = Path(args.outdir)
    make_figure(phase_df, outdir / "fig_stage17_deterministic_fourway")


if __name__ == "__main__":
    main()
