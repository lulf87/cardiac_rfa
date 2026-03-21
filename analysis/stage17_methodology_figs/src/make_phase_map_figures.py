from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, TwoSlopeNorm
import numpy as np
import pandas as pd

COOLING_ORDER = [800.0, 1500.0, 2500.0]
PROTOCOL_ORDER = ["vhpsd_90W_4s_fixed", "vhpsd_90W_4s_controlled"]
PROTOCOL_LABELS = {
    "vhpsd_90W_4s_fixed": "90 W / 4 s fixed",
    "vhpsd_90W_4s_controlled": "90 W / 4 s temperature-limited",
}
COOLING_LABELS = {
    800.0: "h = 800 W m$^{-2}$ K$^{-1}$",
    1500.0: "h = 1500 W m$^{-2}$ K$^{-1}$",
    2500.0: "h = 2500 W m$^{-2}$ K$^{-1}$",
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


def text_color(value: float, cmap, norm) -> str:
    r, g, b, _ = cmap(norm(value))
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "white" if luminance < 0.45 else "black"


def draw_heatmap(ax, matrix, walls, insertions, cmap, norm, fmt: str) -> None:
    ax.imshow(
        matrix,
        origin="lower",
        aspect="auto",
        cmap=cmap,
        norm=norm,
        extent=[insertions[0] - 0.25, insertions[-1] + 0.25, walls[0] - 0.5, walls[-1] + 0.5],
    )
    ax.set_xticks(insertions)
    ax.set_yticks(walls)
    ax.grid(color="white", linewidth=1.0, alpha=0.45)
    for wall_idx, wall in enumerate(walls):
        for ins_idx, insertion in enumerate(insertions):
            value = matrix[wall_idx, ins_idx]
            if np.isnan(value):
                continue
            label = format(value, fmt)
            if label == "-0.0":
                label = "0.0"
            if label == "-0":
                label = "0"
            ax.text(
                insertion,
                wall,
                label,
                ha="center",
                va="center",
                fontsize=8.5,
                color=text_color(value, cmap, norm),
            )


def make_protocol_maps(
    df: pd.DataFrame,
    value_col: str,
    outbase: Path,
    colorbar_label: str,
    cmap: str,
    fmt: str,
) -> None:
    walls = sorted(df["wall_thickness_mm"].unique())
    insertions = sorted(df["insertion_depth_mm"].unique())
    vmin = float(df[value_col].min())
    vmax = float(df[value_col].max())
    norm = Normalize(vmin=vmin, vmax=vmax)

    fig = plt.figure(figsize=(11.4, 6.6))
    gs = fig.add_gridspec(
        2,
        4,
        width_ratios=[1.0, 1.0, 1.0, 0.08],
        left=0.11,
        right=0.95,
        top=0.88,
        bottom=0.12,
        hspace=0.18,
        wspace=0.14,
    )
    last_image = None
    for row, protocol in enumerate(PROTOCOL_ORDER):
        for col, cooling_h in enumerate(COOLING_ORDER):
            ax = fig.add_subplot(gs[row, col])
            matrix = build_matrix(
                df,
                cooling_h=cooling_h,
                protocol=protocol,
                value_col=value_col,
                walls=walls,
                insertions=insertions,
            )
            draw_heatmap(ax, matrix, walls, insertions, plt.get_cmap(cmap), norm, fmt)
            if row == 0:
                ax.set_title(COOLING_LABELS[cooling_h], fontsize=10.2, pad=10)
            if row == len(PROTOCOL_ORDER) - 1:
                ax.set_xlabel("Insertion depth [mm]")
            else:
                ax.set_xticklabels([])
            if col == 0:
                ax.set_ylabel("Wall thickness [mm]")
            else:
                ax.set_yticklabels([])
            last_image = ax.images[0]
        y_center = 0.69 if row == 0 else 0.30
        fig.text(
            0.045,
            y_center,
            PROTOCOL_LABELS[protocol],
            rotation=90,
            va="center",
            ha="center",
            fontsize=10,
            fontweight="semibold",
        )

    cax = fig.add_subplot(gs[:, 3])
    cbar = fig.colorbar(last_image, cax=cax)
    cbar.set_label(colorbar_label)
    save_all(fig, outbase)


def make_difference_maps(df: pd.DataFrame, outbase: Path) -> None:
    walls = sorted(df["wall_thickness_mm"].unique())
    insertions = sorted(df["insertion_depth_mm"].unique())
    fixed = df[df["name"] == "vhpsd_90W_4s_fixed"].copy()
    controlled = df[df["name"] == "vhpsd_90W_4s_controlled"].copy()
    join_cols = ["wall_thickness_mm", "cooling_h_W_per_m2K", "insertion_depth_mm"]
    merged = controlled.merge(
        fixed,
        on=join_cols,
        suffixes=("_controlled", "_fixed"),
        validate="one_to_one",
    )
    merged["delta_energy_J"] = merged["delivered_energy_J_controlled"] - merged["delivered_energy_J_fixed"]
    merged["delta_peak_temperature_C"] = (
        merged["peak_temperature_C_controlled"] - merged["peak_temperature_C_fixed"]
    )

    metrics = [
        ("delta_energy_J", "Controlled - fixed energy [J]", ".0f"),
        ("delta_peak_temperature_C", "Controlled - fixed peak temperature [°C]", ".1f"),
    ]

    fig = plt.figure(figsize=(11.8, 6.2))
    gs = fig.add_gridspec(
        2,
        4,
        width_ratios=[1.0, 1.0, 1.0, 0.08],
        left=0.11,
        right=0.95,
        top=0.88,
        bottom=0.12,
        hspace=0.22,
        wspace=0.14,
    )
    row_centers = [0.69, 0.28]
    for row, (metric, colorbar_label, fmt) in enumerate(metrics):
        vmax = float(np.max(np.abs(merged[metric])))
        norm = TwoSlopeNorm(vmin=-vmax, vcenter=0.0, vmax=vmax)
        last_image = None
        for col, cooling_h in enumerate(COOLING_ORDER):
            ax = fig.add_subplot(gs[row, col])
            matrix = build_matrix(merged, cooling_h=cooling_h, protocol=None, value_col=metric, walls=walls, insertions=insertions)
            draw_heatmap(ax, matrix, walls, insertions, plt.get_cmap("RdBu_r"), norm, fmt)
            if row == 0:
                ax.set_title(COOLING_LABELS[cooling_h], fontsize=10.2, pad=10)
            if row == len(metrics) - 1:
                ax.set_xlabel("Insertion depth [mm]")
            else:
                ax.set_xticklabels([])
            if col == 0:
                ax.set_ylabel("Wall thickness [mm]")
            else:
                ax.set_yticklabels([])
            last_image = ax.images[0]
        fig.text(
            0.045,
            row_centers[row],
            colorbar_label,
            rotation=90,
            va="center",
            ha="center",
            fontsize=10,
            fontweight="semibold",
        )
        cax = fig.add_subplot(gs[row, 3])
        cbar = fig.colorbar(last_image, cax=cax)
        cbar.set_label(colorbar_label)
    save_all(fig, outbase)


def build_matrix(
    df: pd.DataFrame,
    cooling_h: float,
    protocol: str | None,
    value_col: str,
    walls: list[float],
    insertions: list[float],
) -> np.ndarray:
    sub = df[df["cooling_h_W_per_m2K"] == cooling_h]
    if protocol is not None:
        sub = sub[sub["name"] == protocol]
    pivot = sub.pivot(
        index="wall_thickness_mm",
        columns="insertion_depth_mm",
        values=value_col,
    ).reindex(index=walls, columns=insertions)
    return pivot.to_numpy(float)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-csv", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    plt.style.use(str(Path(__file__).resolve().parents[1] / "styles" / "revision_light.mplstyle"))
    phase_df = pd.read_csv(args.phase_csv)
    outdir = Path(args.outdir)
    make_protocol_maps(
        phase_df[phase_df["name"].isin(PROTOCOL_ORDER)],
        value_col="depth_fraction",
        outbase=outdir / "fig5_depth_fraction_fixed_vs_controlled",
        colorbar_label="Depth fraction [-]",
        cmap="viridis",
        fmt=".2f",
    )
    make_protocol_maps(
        phase_df[phase_df["name"].isin(PROTOCOL_ORDER)],
        value_col="peak_temperature_C",
        outbase=outdir / "fig6_peak_temperature_fixed_vs_controlled",
        colorbar_label="Peak temperature [°C]",
        cmap="viridis",
        fmt=".1f",
    )
    make_difference_maps(
        phase_df[phase_df["name"].isin(PROTOCOL_ORDER)],
        outdir / "fig7_controlled_minus_fixed_maps",
    )


if __name__ == "__main__":
    main()
