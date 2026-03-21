from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Provenance note:
# The panel structure and selected-point highlighting are adapted from the
# legacy `analysis/stage7_freeze_final/src/make_figures.py::fig4_verification`
# layout. This script is stage17-native in its data path: it reads current
# stage17 convergence CSVs and recomputes relative errors from the exported raw
# metrics because the current CSV schema does not include legacy `*_relerr_pct`
# columns.


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


def relative_error_pct(series: pd.Series) -> pd.Series:
    reference = float(series.iloc[-1])
    if reference == 0.0:
        return pd.Series(np.nan, index=series.index)
    return (series.astype(float) - reference).abs() / abs(reference) * 100.0


def prepare_grid_df(grid_df: pd.DataFrame) -> pd.DataFrame:
    df = grid_df.copy()
    df["grid_cells"] = df["nx"].astype(int) * df["ny"].astype(int)
    df = df.sort_values(["grid_cells", "nx", "ny"]).reset_index(drop=True)
    df["x_label"] = df["nx"].astype(int).astype(str) + "x" + df["ny"].astype(int).astype(str)
    df["depth_relerr_pct"] = relative_error_pct(df["lesion_depth_mm"])
    df["temp_relerr_pct"] = relative_error_pct(df["peak_temperature_C"])
    return df


def prepare_dt_df(dt_df: pd.DataFrame) -> pd.DataFrame:
    df = dt_df.copy()
    df = df.sort_values("dt_s", ascending=False).reset_index(drop=True)
    df["x_label"] = df["dt_s"].map(lambda value: f"{float(value):.3f}")
    df["depth_relerr_pct"] = relative_error_pct(df["lesion_depth_mm"])
    df["temp_relerr_pct"] = relative_error_pct(df["peak_temperature_C"])
    return df


def grid_selection_index(df: pd.DataFrame) -> int | None:
    selected = df[(df["nx"].astype(int) == 281) & (df["ny"].astype(int) == 141)]
    if selected.empty:
        return None
    return int(selected.index[0])


def dt_selection_index(df: pd.DataFrame) -> int | None:
    selected = df[np.isclose(df["dt_s"].astype(float), 0.05)]
    if selected.empty:
        return None
    return int(selected.index[0])


def highlight_selected(ax: plt.Axes, x_idx: int, y_depth: float, y_temp: float, label: str) -> None:
    depth_color = "#486E9B"
    temp_color = "#E38A1A"
    ax.scatter(
        [x_idx],
        [y_depth],
        s=130,
        facecolors="none",
        edgecolors=depth_color,
        linewidths=1.8,
        zorder=5,
    )
    ax.scatter(
        [x_idx],
        [y_temp],
        s=150,
        facecolors="none",
        edgecolors=temp_color,
        linewidths=1.8,
        marker="s",
        zorder=5,
    )
    ax.annotate(
        label,
        (x_idx, max(y_depth, y_temp)),
        xytext=(10, 10),
        textcoords="offset points",
        fontsize=8,
        color="#333333",
    )


def make_figure(grid_df: pd.DataFrame, dt_df: pd.DataFrame, outbase: Path) -> None:
    depth_color = "#486E9B"
    temp_color = "#E38A1A"

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.8))

    x = np.arange(len(grid_df))
    ax = axes[0]
    ax.plot(x, grid_df["depth_relerr_pct"], color=depth_color, marker="o", linewidth=2.2, label="Lesion depth")
    ax.plot(x, grid_df["temp_relerr_pct"], color=temp_color, marker="s", linewidth=2.2, label="Peak temperature")
    ax.set_xticks(x)
    ax.set_xticklabels(grid_df["x_label"])
    ax.set_xlabel("Grid [nx x ny]")
    ax.set_ylabel("Relative error to finest solution [%]")
    ax.set_title("(a) Grid refinement", loc="left", fontweight="bold")
    ax.margins(x=0.06)
    selected_grid_idx = grid_selection_index(grid_df)
    if selected_grid_idx is not None:
        highlight_selected(
            ax,
            selected_grid_idx,
            float(grid_df.loc[selected_grid_idx, "depth_relerr_pct"]),
            float(grid_df.loc[selected_grid_idx, "temp_relerr_pct"]),
            "selected grid",
        )

    x = np.arange(len(dt_df))
    ax = axes[1]
    ax.plot(x, dt_df["depth_relerr_pct"], color=depth_color, marker="o", linewidth=2.2, label="Lesion depth")
    ax.plot(x, dt_df["temp_relerr_pct"], color=temp_color, marker="s", linewidth=2.2, label="Peak temperature")
    ax.set_xticks(x)
    ax.set_xticklabels(dt_df["x_label"])
    ax.set_xlabel("dt [s]")
    ax.set_ylabel("Relative error to finest solution [%]")
    ax.set_title("(b) Time-step refinement", loc="left", fontweight="bold")
    ax.margins(x=0.06)
    selected_dt_idx = dt_selection_index(dt_df)
    if selected_dt_idx is not None:
        highlight_selected(
            ax,
            selected_dt_idx,
            float(dt_df.loc[selected_dt_idx, "depth_relerr_pct"]),
            float(dt_df.loc[selected_dt_idx, "temp_relerr_pct"]),
            "selected dt",
        )

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.subplots_adjust(bottom=0.22, wspace=0.25)
    save_all(fig, outbase)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid-csv", required=True)
    parser.add_argument("--dt-csv", required=True)
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    plt.style.use(str(Path(__file__).resolve().parents[1] / "styles" / "revision_light.mplstyle"))
    grid_df = prepare_grid_df(pd.read_csv(args.grid_csv))
    dt_df = prepare_dt_df(pd.read_csv(args.dt_csv))
    make_figure(grid_df, dt_df, Path(args.outdir) / "fig4_stage17_verification")


if __name__ == "__main__":
    main()
