
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from common import apply_style, add_chip, panel_label, save_pdf_png, protocol_color, PROTOCOL_ORDER, PROTOCOL_DISPLAY, load_palette


def arrow(fig_ax, x0, y0, x1, y1, color, lw=1.8, ms=12):
    fig_ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=ms, lw=lw, color=color))


def rounded_box(ax, xy, wh, fc, ec='none', rs=0.03, alpha=1.0):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.012,rounding_size={rs}", fc=fc, ec=ec, lw=1.0, alpha=alpha)
    ax.add_patch(patch)
    return patch


def make_fig1(outbase: Path):
    pal = apply_style()
    fig = plt.figure(figsize=(11.8, 5.8))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0], wspace=0.18)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    # ----- Panel a: geometry and conditions -----
    ax0.set_xlim(0, 10)
    ax0.set_ylim(0, 8)
    ax0.axis("off")
    panel_label(ax0, "(a)")
    add_chip(ax0, "2D reduced electro-thermal model")

    # Domains
    blood_fc = "#DDEAF5"
    tissue_fc = "#EACFBE"
    buffer_fc = "#F2E7DD"
    electrode_fc = "#B9C4CE"

    rounded_box(ax0, (0.6, 0.4), (8.6, 6.8), fc=pal["axes_face"], ec=pal["grid"], rs=0.04)
    ax0.add_patch(Rectangle((1.0, 5.8), 7.8, 1.0, fc=blood_fc, ec='none'))
    ax0.text(1.2, 6.23, "Blood pool / cooling boundary", fontsize=10)

    ax0.add_patch(Rectangle((1.0, 3.0), 7.8, 2.8, fc=tissue_fc, ec='none'))
    ax0.text(1.2, 4.4, "Myocardial wall", fontsize=11, fontweight='semibold')

    ax0.add_patch(Rectangle((1.0, 1.1), 7.8, 1.9, fc=buffer_fc, ec='none'))
    ax0.text(1.2, 2.05, "Thermal buffer", fontsize=10)

    # Electrode
    ax0.add_patch(Rectangle((4.3, 6.25), 1.4, 0.75, fc=electrode_fc, ec=pal["spine"], lw=1.3))
    ax0.text(5.0, 7.15, "Electrode", ha="center", fontsize=10)
    # insertion
    ax0.plot([5.0, 5.0], [6.25, 5.2], color=pal["spine"], lw=1.6)
    ax0.annotate("", xy=(5.35, 5.2), xytext=(5.35, 6.25), arrowprops=dict(arrowstyle='<->', color=pal["spine"], lw=1.4))
    ax0.text(5.52, 5.72, "Insertion depth", fontsize=9, rotation=90, va="center")

    # wall thickness
    ax0.annotate("", xy=(8.55, 3.0), xytext=(8.55, 5.8), arrowprops=dict(arrowstyle='<->', color=pal["spine"], lw=1.4))
    ax0.text(8.72, 4.4, "Wall thickness", fontsize=9, rotation=90, va="center")

    # bottom buffer
    ax0.annotate("", xy=(8.15, 1.1), xytext=(8.15, 3.0), arrowprops=dict(arrowstyle='<->', color=pal["spine"], lw=1.2))
    ax0.text(8.32, 2.02, "Bottom buffer", fontsize=8.7, rotation=90, va="center")

    # Top cooling arrows
    for xx in np.linspace(2.0, 8.0, 5):
        ax0.annotate("", xy=(xx, 5.85), xytext=(xx, 6.55), arrowprops=dict(arrowstyle='-|>', color="#7AA9D6", lw=1.2))
    ax0.text(6.95, 6.55, "Convective cooling  h", fontsize=9.5, color="#537DA7")

    # side/bottom insulation
    ax0.plot([1.0, 1.0], [1.1, 5.8], color=pal["spine"], lw=1.4, alpha=0.8)
    ax0.plot([8.8, 8.8], [1.1, 5.8], color=pal["spine"], lw=1.4, alpha=0.8)
    ax0.plot([1.0, 8.8], [1.1, 1.1], color=pal["spine"], lw=1.4, alpha=0.8)
    ax0.text(0.83, 5.85, "Insulated", fontsize=8.5, rotation=90, va="top")
    ax0.text(8.95, 5.85, "Insulated", fontsize=8.5, rotation=90, va="top")
    ax0.text(8.7, 0.82, "Insulated", fontsize=8.5, ha="right")

    # Protocol chips
    y0 = 0.55
    xstarts = [1.2, 3.75, 6.15]
    for xs, key in zip(xstarts, PROTOCOL_ORDER):
        rounded_box(ax0, (xs, y0), (1.8, 0.36), fc=protocol_color(pal, key), rs=0.08)
        ax0.text(xs + 0.9, y0 + 0.18, PROTOCOL_DISPLAY[key], ha='center', va='center', fontsize=9.5, color='white')
    ax0.text(5.0, 0.15, "Protocols compared: 30 W / 30 s, 50 W / 10 s, 90 W / 4 s", ha='center', fontsize=9.3)

    # ----- Panel b: workflow -----
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis("off")
    panel_label(ax1, "(b)")
    add_chip(ax1, "Simulation workflow and outputs")

    box_fc = "#EEF3F8"
    box_ec = pal["grid"]
    step_y = [8.2, 6.3, 4.4, 2.5]
    labels = [
        "Electrical subproblem\n∇·(σ∇φ)=0  →  Joule heating q",
        "Transient bioheat\nρc ∂T/∂t = ∇·(k∇T)+q−ω_b ρ_b c_b(T−T_b)",
        "Arrhenius damage\nΩ(t)=∫ A exp(−E_a/RT) dt",
        "Summary metrics\nDepth, depth fraction, transmurality,\noverheat area, probability maps",
    ]
    for y, lab in zip(step_y, labels):
        rounded_box(ax1, (1.2, y), (7.0, 1.2), fc=box_fc, ec=box_ec, rs=0.06)
        ax1.text(4.7, y + 0.6, lab, ha="center", va="center", fontsize=10.3)
    for y0, y1 in zip(step_y[:-1], step_y[1:]):
        arrow(ax1, 4.7, y0, 4.7, y1 + 1.2, pal["chip"])

    # Inputs / uncertain factors
    rounded_box(ax1, (0.4, 6.0), (0.55, 2.6), fc=pal["protocol_light"]["standard_30W_30s"], rs=0.08)
    ax1.text(0.675, 7.3, "Inputs", rotation=90, ha="center", va="center", fontsize=10.2, fontweight="semibold")
    rounded_box(ax1, (8.55, 5.8), (1.0, 2.7), fc=pal["protocol_light"]["vhpsd_90W_4s"], rs=0.08)
    ax1.text(9.05, 7.15, "Uncertain\ncontact,\ncooling", ha="center", va="center", fontsize=9.3)

    # Small output icons
    rounded_box(ax1, (8.35, 2.15), (1.25, 0.7), fc=pal["protocol_light"]["hpsd_50W_10s"], rs=0.08)
    ax1.text(8.975, 2.5, "Fig. 5–7", ha="center", va="center", fontsize=9.4)
    ax1.text(8.95, 1.72, "Deterministic +\nprobabilistic outputs", ha="center", va="top", fontsize=8.8)

    save_pdf_png(fig, outbase)
    plt.close(fig)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", type=Path, required=True)
    args = p.parse_args()
    make_fig1(args.outdir / "fig1_model_workflow")


if __name__ == "__main__":
    main()
