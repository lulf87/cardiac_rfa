
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from common import apply_style, add_chip, panel_label, save_pdf_png, protocol_color, PROTOCOL_ORDER, PROTOCOL_DISPLAY, PROTOCOL_MARKER


TEMPLATE_COLUMNS = [
    "source_id",
    "protocol_key",
    "reported_depth_mm",
    "simulated_depth_mm",
    "reported_width_mm",
    "simulated_width_mm",
    "notes",
]


def ensure_template(csv_path: Path):
    if csv_path.exists():
        try:
            df = pd.read_csv(csv_path)
            return df
        except Exception:
            pass
    df = pd.DataFrame(columns=TEMPLATE_COLUMNS)
    df.to_csv(csv_path, index=False)
    return df


def make_placeholder(outbase: Path):
    pal = apply_style()
    fig, ax = plt.subplots(figsize=(8.8, 3.8))
    ax.axis("off")
    panel_label(ax, "(a)")
    add_chip(ax, "Literature benchmark template required")
    msg = (
        "Populate benchmark_points.csv with literature-derived lesion depths\n"
        "before generating Figure 8.\n\n"
        "Required columns:\n"
        "source_id, protocol_key, reported_depth_mm, simulated_depth_mm\n"
        "Optional columns: reported_width_mm, simulated_width_mm, notes"
    )
    ax.text(0.5, 0.47, msg, ha="center", va="center", fontsize=12)
    save_pdf_png(fig, outbase)
    plt.close(fig)


def make_fig8(df: pd.DataFrame, outbase: Path):
    pal = apply_style()
    fig = plt.figure(figsize=(10.5, 4.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.95], wspace=0.22)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    panel_label(ax0, "(a)")
    panel_label(ax1, "(b)")
    add_chip(ax0, "Depth agreement")
    add_chip(ax1, "Protocol-level trend")

    valid = df.dropna(subset=["reported_depth_mm", "simulated_depth_mm", "protocol_key"]).copy()
    if valid.empty:
        make_placeholder(outbase)
        return

    # Scatter
    x = valid["reported_depth_mm"].to_numpy(float)
    y = valid["simulated_depth_mm"].to_numpy(float)
    lo = 0
    hi = max(np.max(x), np.max(y)) * 1.1
    ax0.plot([lo, hi], [lo, hi], ls="--", lw=1.3, color="#7D8795")
    for _, row in valid.iterrows():
        key = row["protocol_key"]
        ax0.scatter(row["reported_depth_mm"], row["simulated_depth_mm"],
                    s=90, marker=PROTOCOL_MARKER.get(key, "o"),
                    facecolor=protocol_color(pal, key), edgecolor="black", linewidth=1.0, zorder=3)
        if isinstance(row.get("source_id"), str) and row["source_id"]:
            ax0.annotate(row["source_id"], (row["reported_depth_mm"], row["simulated_depth_mm"]),
                         textcoords="offset points", xytext=(4, 3), fontsize=8.5)
    ax0.set_xlabel("Reported lesion depth [mm]")
    ax0.set_ylabel("Simulated lesion depth [mm]")
    ax0.set_xlim(lo, hi)
    ax0.set_ylim(lo, hi)
    ax0.set_aspect("equal", adjustable="box")

    # grouped means by protocol
    g = valid.groupby("protocol_key", sort=False)[["reported_depth_mm", "simulated_depth_mm"]].mean().reindex(PROTOCOL_ORDER)
    xx = np.arange(len(g))
    w = 0.36
    ax1.bar(xx - w/2, g["reported_depth_mm"], width=w, color="#CFD8E3", edgecolor="black", label="Reported mean")
    ax1.bar(xx + w/2, g["simulated_depth_mm"], width=w, color=[protocol_color(pal, k) for k in g.index], edgecolor="black", label="Simulated mean")
    ax1.set_xticks(xx, [PROTOCOL_DISPLAY[k] for k in g.index], rotation=0)
    ax1.set_ylabel("Mean lesion depth [mm]")
    ax1.legend(loc="upper right")

    # shared legend for markers
    handles = []
    labels = []
    for key in PROTOCOL_ORDER:
        handles.append(plt.Line2D([], [], marker=PROTOCOL_MARKER[key], linestyle="None",
                                  markerfacecolor=protocol_color(pal, key), markeredgecolor="black", markersize=8))
        labels.append(PROTOCOL_DISPLAY[key])
    ax0.legend(handles, labels, loc="lower right", title="Protocol")
    save_pdf_png(fig, outbase)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark-csv", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    args = ap.parse_args()
    df = ensure_template(args.benchmark_csv)
    if df.empty:
        make_placeholder(args.outdir / "fig8_literature_benchmark")
    else:
        make_fig8(df, args.outdir / "fig8_literature_benchmark")


if __name__ == "__main__":
    main()
