from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


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


def rounded_box(ax, x: float, y: float, w: float, h: float, fc: str, ec: str = "#BFC7D5") -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=fc,
            edgecolor=ec,
            linewidth=1.0,
        )
    )


def arrow(ax, x0: float, y0: float, x1: float, y1: float, color: str = "#5C677D") -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.8,
            color=color,
        )
    )


def make_figure(outbase: Path) -> None:
    fig = plt.figure(figsize=(12.8, 6.7))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.03, 1.0], wspace=0.18)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    for ax in (ax0, ax1):
        ax.set_axis_off()

    # Panel (a): geometry/boundaries
    ax0.set_xlim(0, 10)
    ax0.set_ylim(0, 8)
    ax0.text(0.15, 7.72, "(a)", fontsize=12, fontweight="bold")
    ax0.text(0.65, 7.72, "Planar reduced 2D domain", fontsize=12, fontweight="bold")

    rounded_box(ax0, 0.55, 0.45, 8.7, 6.65, "#F7F8FB")
    ax0.add_patch(Rectangle((1.05, 2.35), 7.7, 3.25, facecolor="#EACFBE", edgecolor="none"))
    ax0.text(1.3, 3.95, "Myocardial wall", fontsize=11, fontweight="semibold")

    ax0.add_patch(Rectangle((1.05, 0.95), 7.7, 1.4, facecolor="#F2E7DD", edgecolor="none"))
    ax0.text(1.3, 1.55, "Bottom thermal buffer", fontsize=10)

    ax0.add_patch(Rectangle((4.35, 5.62), 1.1, 0.36, facecolor="#B9C4CE", edgecolor="#5C677D", linewidth=1.0))
    ax0.text(4.9, 6.2, "Electrode footprint", ha="center", fontsize=10)

    ax0.plot([1.05, 8.75], [5.6, 5.6], color="#5C677D", linewidth=1.2)
    for xpos in (1.55, 2.45, 3.35, 6.2, 7.1, 8.0):
        arrow(ax0, xpos, 6.25, xpos, 5.67, color="#6B9AC4")
    ax0.text(6.35, 6.45, "Effective top Robin cooling", fontsize=9.4, color="#476C8A")

    ax0.annotate(
        "",
        xy=(8.55, 2.35),
        xytext=(8.55, 5.6),
        arrowprops=dict(arrowstyle="<->", linewidth=1.4, color="#5C677D"),
    )
    ax0.text(8.72, 4.0, "Wall thickness", rotation=90, va="center", fontsize=9.2)

    ax0.annotate(
        "",
        xy=(8.1, 0.95),
        xytext=(8.1, 2.35),
        arrowprops=dict(arrowstyle="<->", linewidth=1.2, color="#5C677D"),
    )
    ax0.text(8.28, 1.63, "Buffer", rotation=90, va="center", fontsize=8.8)

    ax0.annotate(
        "",
        xy=(5.3, 5.6),
        xytext=(5.3, 4.6),
        arrowprops=dict(arrowstyle="<->", linewidth=1.3, color="#5C677D"),
    )
    ax0.text(5.48, 5.12, "Insertion depth surrogate", rotation=90, va="center", fontsize=8.8)

    ax0.text(0.92, 5.52, "Top boundary", fontsize=8.5, rotation=90, va="top")
    ax0.text(0.87, 2.6, "Insulated sides", fontsize=8.3, rotation=90, va="center")
    ax0.text(8.75, 0.63, "Insulated bottom", fontsize=8.3, ha="right")
    ax0.text(
        1.1,
        6.82,
        "No explicit blood subdomain in stage17;\n"
        "cooling enters through the top boundary profile.",
        fontsize=8.8,
        color="#485164",
        ha="left",
        va="top",
    )

    protocol_boxes = [
        (1.15, "Standard\n30 W / 30 s", "#2A9D8F"),
        (3.15, "HPSD\n50 W / 10 s", "#4C78A8"),
        (5.15, "Fixed\n90 W / 4 s", "#E76F51"),
        (7.15, "Temp-limited\n90 W / 4 s", "#6C5CE7"),
    ]
    for x, label, color in protocol_boxes:
        rounded_box(ax0, x, 0.18, 1.45, 0.44, color, ec=color)
        ax0.text(x + 0.725, 0.4, label, ha="center", va="center", fontsize=8.6, color="white")

    # Panel (b): algorithm/workflow
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.text(0.12, 9.52, "(b)", fontsize=12, fontweight="bold")
    ax1.text(0.62, 9.52, "Stage17 algorithm flow", fontsize=12, fontweight="bold")

    steps = [
        (1.15, 7.95, 7.0, 1.05, "#EEF3F8", "Unit-potential solve\n$\\nabla \\cdot (\\sigma \\nabla \\phi)=0$"),
        (
            1.15,
            6.18,
            7.0,
            1.12,
            "#EEF3F8",
            "Reduced RF source\n$q_{unit} \\rightarrow$ Gaussian regularization\n$\\rightarrow$ depth shift $\\rightarrow$ power/contact scaling",
        ),
        (
            1.15,
            4.38,
            7.0,
            1.15,
            "#EEF3F8",
            "Implicit bioheat step\nTop Robin cooling, insulated sides/bottom,\nperfusion term fixed at zero",
        ),
        (
            1.15,
            2.58,
            7.0,
            1.1,
            "#EEF3F8",
            "Arrhenius damage and latency\nDamage accumulation continues during\n8 s post-pulse thermal continuation",
        ),
        (
            1.15,
            0.78,
            7.0,
            1.08,
            "#EEF3F8",
            "Reported outputs\nDepth, width, area, depth fraction,\ndelivered energy, peak temperature, overheat area",
        ),
    ]

    for x, y, w, h, fc, label in steps:
        rounded_box(ax1, x, y, w, h, fc)
        ax1.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9.7)

    for y0, y1 in ((7.95, 7.3), (6.18, 5.54), (4.38, 3.74), (2.58, 1.93)):
        arrow(ax1, 4.65, y0, 4.65, y1)

    rounded_box(ax1, 8.45, 6.55, 1.2, 2.15, "#F4E8FF", ec="#D2B7F4")
    ax1.text(
        9.05,
        7.62,
        "Generic\ncontroller\n70/80 C\n0.05 s\nsample-hold",
        ha="center",
        va="center",
        fontsize=8.8,
        color="#4E3D73",
    )
    arrow(ax1, 8.4, 7.62, 8.16, 6.74, color="#6C5CE7")

    rounded_box(ax1, 8.45, 2.95, 1.2, 1.45, "#E7F4EA", ec="#A8C9B1")
    ax1.text(
        9.05,
        3.67,
        "Metrics\nfrom wall-only\nreporting mask",
        ha="center",
        va="center",
        fontsize=8.6,
        color="#36543C",
    )

    save_all(fig, outbase)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    make_figure(Path(args.outdir) / "fig1_stage17_geometry_workflow")


if __name__ == "__main__":
    main()
