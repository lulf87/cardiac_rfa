
import argparse
import os
import re
from typing import Dict, List

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import yaml

PROTOCOL_ORDER = ["standard_30W_30s", "hpsd_50W_10s", "vhpsd_90W_4s"]
PROTOCOL_LABEL = {
    "standard_30W_30s": "Standard",
    "hpsd_50W_10s": "HPSD",
    "vhpsd_90W_4s": "vHPSD",
}
PROTOCOL_MARKER = {
    "standard_30W_30s": "o",
    "hpsd_50W_10s": "s",
    "vhpsd_90W_4s": "^",
}
COOLING_LABEL = {
    800.0: "Weak cooling\n800 W/m²K",
    1500.0: "Nominal cooling\n1500 W/m²K",
    2500.0: "Strong cooling\n2500 W/m²K",
}
WALL_ORDER = [2.0, 3.0, 4.0, 6.0]
INSERTION_ORDER = [0.5, 1.0, 1.5, 2.0]


def load_palette(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def apply_style(style_path: str) -> None:
    plt.style.use(style_path)
    mpl.rcParams.update({
        "figure.facecolor": PALETTE["background"],
        "axes.facecolor": PALETTE["axes_face"],
        "axes.edgecolor": PALETTE["spine"],
        "axes.labelcolor": PALETTE["text"],
        "xtick.color": PALETTE["text"],
        "ytick.color": PALETTE["text"],
        "grid.color": PALETTE["grid"],
        "grid.alpha": 0.45,
        "legend.facecolor": PALETTE["axes_face"],
        "legend.edgecolor": "#B8C0CC",
        "text.color": PALETTE["text"],
        "axes.titlecolor": PALETTE["text"],
    })
    mpl.rcParams["pdf.fonttype"] = 42
    mpl.rcParams["ps.fonttype"] = 42


def chip(ax, text, x=0.5, y=1.04, fs=11, ha="center"):
    ax.text(
        x, y, text, transform=ax.transAxes, ha=ha, va="bottom",
        fontsize=fs, color="white",
        bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.14",
                  fc=PALETTE["chip"], ec="none")
    )


def protocol_tag(fig, ax, text, fc):
    bb = ax.get_position()
    x = bb.x0 - 0.032
    y = (bb.y0 + bb.y1) / 2
    fig.text(
        x, y, text, rotation=90, ha="center", va="center",
        fontsize=11, color=PALETTE["text"], weight="semibold",
        bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.14", fc=fc, ec="none")
    )


def panel_label(ax, label):
    ax.text(-0.16, 1.10, label, transform=ax.transAxes,
            fontsize=16, fontweight="bold", color="black")


def save(fig, outbase):
    fig.savefig(outbase + ".png", dpi=300, bbox_inches="tight")
    fig.savefig(outbase + ".pdf", bbox_inches="tight")
    plt.close(fig)


def _parse_grid_label(row):
    if "grid_label" in row and pd.notna(row["grid_label"]):
        return str(row["grid_label"])
    if "case" in row and isinstance(row["case"], str) and row["case"].startswith("grid_"):
        return row["case"].replace("grid_", "").replace("x", "×")
    if {"nx", "ny"}.issubset(row.index):
        return f"{int(row['nx'])}×{int(row['ny'])}"
    raise ValueError("Could not infer grid label.")


def _parse_dt_label(row):
    if "dt_s" in row:
        return float(row["dt_s"])
    if "case" in row and isinstance(row["case"], str) and row["case"].startswith("dt_"):
        return float(row["case"].replace("dt_", ""))
    raise ValueError("Could not infer dt value.")


def load_convergence(path: str, kind: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if kind == "grid":
        labels, keys = [], []
        for _, row in df.iterrows():
            labels.append(_parse_grid_label(row))
            m = re.match(r"(\d+)×(\d+)", labels[-1])
            keys.append(int(m.group(1)) * int(m.group(2)) if m else len(keys))
        df = df.copy()
        df["x_label"] = labels
        df["sort_key"] = keys
    else:
        vals = []
        for _, row in df.iterrows():
            vals.append(_parse_dt_label(row))
        df = df.copy()
        df["x_label"] = vals
        df["sort_key"] = [-v for v in vals]  # 0.1, 0.05, 0.025

    df = df.sort_values("sort_key").reset_index(drop=True)
    depth_fine = df["lesion_depth_mm"].iloc[-1]
    temp_fine = df["peak_temperature_C"].iloc[-1]
    df["depth_relerr_pct"] = 100.0 * np.abs(df["lesion_depth_mm"] - depth_fine) / max(depth_fine, 1e-9)
    df["temp_relerr_pct"] = 100.0 * np.abs(df["peak_temperature_C"] - temp_fine) / max(temp_fine, 1e-9)
    return df


def fig3_deterministic(phase_df: pd.DataFrame, outdir: str):
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.2), facecolor=PALETTE["background"])
    colors = PALETTE["protocol"]

    # (a) nominal contact + nominal cooling
    ax = axes[0, 0]
    sub = phase_df[(phase_df["cooling_h_W_per_m2K"] == 1500.0) & (phase_df["insertion_depth_mm"] == 1.0)]
    for name in PROTOCOL_ORDER:
        s = sub[sub["name"] == name].sort_values("wall_thickness_mm")
        ax.plot(s["wall_thickness_mm"], s["depth_fraction"], marker="o", color=colors[name], label=PROTOCOL_LABEL[name])
    ax.set_xlabel("Wall thickness [mm]")
    ax.set_ylabel("Depth fraction [-]")
    ax.set_ylim(0, 1.08)
    chip(ax, "Nominal contact, nominal cooling")
    panel_label(ax, "(a)")

    # (b) thin wall nominal cooling
    ax = axes[0, 1]
    sub = phase_df[(phase_df["cooling_h_W_per_m2K"] == 1500.0) & (phase_df["wall_thickness_mm"] == 2.0)]
    for name in PROTOCOL_ORDER:
        s = sub[sub["name"] == name].sort_values("insertion_depth_mm")
        ax.plot(s["insertion_depth_mm"], s["depth_fraction"], marker="o", color=colors[name])
    ax.set_xlabel("Nominal insertion [mm]")
    ax.set_ylabel("Depth fraction [-]")
    ax.set_ylim(0, 1.08)
    chip(ax, "Thin wall, nominal cooling")
    panel_label(ax, "(b)")

    # (c) moderate-thickness wall, elevated contact
    ax = axes[1, 0]
    sub = phase_df[(phase_df["wall_thickness_mm"] == 4.0) & (phase_df["insertion_depth_mm"] == 1.5)]
    for name in PROTOCOL_ORDER:
        s = sub[sub["name"] == name].sort_values("cooling_h_W_per_m2K")
        ax.plot(s["cooling_h_W_per_m2K"], s["depth_fraction"], marker="o", color=colors[name])
    ax.set_xlabel("Cooling coefficient h [W m$^{-2}$ K$^{-1}$]")
    ax.set_ylabel("Depth fraction [-]")
    ax.set_ylim(0, 1.0)
    chip(ax, "Moderate-thickness wall, elevated contact")
    panel_label(ax, "(c)")

    # (d) thin wall nominal cooling peak temp
    ax = axes[1, 1]
    sub = phase_df[(phase_df["cooling_h_W_per_m2K"] == 1500.0) & (phase_df["wall_thickness_mm"] == 2.0)]
    for name in PROTOCOL_ORDER:
        s = sub[sub["name"] == name].sort_values("insertion_depth_mm")
        ax.plot(s["insertion_depth_mm"], s["peak_temperature_C"], marker="o", color=colors[name])
    ax.axhline(100.0, ls="--", lw=1.5, color="#6B7280")
    ax.text(0.02, 0.92, "100°C threshold", transform=ax.transAxes, color="#555555", fontsize=11)
    ax.set_xlabel("Nominal insertion [mm]")
    ax.set_ylabel("Peak temperature [°C]")
    chip(ax, "Thin wall, nominal cooling")
    panel_label(ax, "(d)")

    handles = [
        Line2D([0], [0], color=colors[n], marker="o", lw=2.5, markersize=8, label=PROTOCOL_LABEL[n])
        for n in PROTOCOL_ORDER
    ]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=True,
               bbox_to_anchor=(0.5, -0.01), columnspacing=1.2)
    fig.subplots_adjust(top=0.93, bottom=0.12, wspace=0.20, hspace=0.40)
    save(fig, os.path.join(outdir, "fig3_deterministic_summary"))


def fig4_verification(grid_df: pd.DataFrame, dt_df: pd.DataFrame, outdir: str):
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6), facecolor=PALETTE["background"])
    selected_c = "#4B6E97"
    temp_c = "#F08A1F"

    ax = axes[0]
    x = np.arange(len(grid_df))
    ax.plot(x, grid_df["depth_relerr_pct"], color=selected_c, marker="o", lw=2.8, label="Lesion depth")
    ax.plot(x, grid_df["temp_relerr_pct"], color=temp_c, marker="s", lw=2.8, label="Peak temperature")
    ax.set_xticks(x, grid_df["x_label"])
    ax.set_ylabel("Relative error to finest solution [%]")
    ax.set_xlabel("Grid")
    chip(ax, "Grid refinement")
    panel_label(ax, "(a)")
    # selected grid = middle
    if len(x) >= 2:
        sx = 1
        ax.scatter([sx], [grid_df["depth_relerr_pct"].iloc[sx]], s=140, facecolors="none", edgecolors=selected_c, linewidths=2.0, zorder=5)
        ax.scatter([sx], [grid_df["temp_relerr_pct"].iloc[sx]], s=160, facecolors="none", edgecolors=temp_c, linewidths=2.0, marker="s", zorder=5)
        ax.annotate("selected grid", (sx, max(grid_df["depth_relerr_pct"].iloc[sx], grid_df["temp_relerr_pct"].iloc[sx])),
                    xytext=(12, 12), textcoords="offset points", fontsize=10, color=PALETTE["text"])

    ax = axes[1]
    x = np.arange(len(dt_df))
    labels = [f"{v:.3f}" for v in dt_df["x_label"]]
    ax.plot(x, dt_df["depth_relerr_pct"], color=selected_c, marker="o", lw=2.8, label="Lesion depth")
    ax.plot(x, dt_df["temp_relerr_pct"], color=temp_c, marker="s", lw=2.8, label="Peak temperature")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Relative error to finest solution [%]")
    ax.set_xlabel("Δt [s]")
    chip(ax, "Time-step refinement")
    panel_label(ax, "(b)")
    if len(x) >= 2:
        sx = 1
        ax.scatter([sx], [dt_df["depth_relerr_pct"].iloc[sx]], s=140, facecolors="none", edgecolors=selected_c, linewidths=2.0, zorder=5)
        ax.scatter([sx], [dt_df["temp_relerr_pct"].iloc[sx]], s=160, facecolors="none", edgecolors=temp_c, linewidths=2.0, marker="s", zorder=5)
        ax.annotate("selected Δt", (sx, max(dt_df["depth_relerr_pct"].iloc[sx], dt_df["temp_relerr_pct"].iloc[sx])),
                    xytext=(12, 12), textcoords="offset points", fontsize=10, color=PALETTE["text"])

    handles = [
        Line2D([0], [0], color=selected_c, marker="o", lw=2.8, label="Lesion depth"),
        Line2D([0], [0], color=temp_c, marker="s", lw=2.8, label="Peak temperature"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=True, bbox_to_anchor=(0.5, -0.02))
    fig.subplots_adjust(top=0.88, bottom=0.20, wspace=0.25)
    save(fig, os.path.join(outdir, "fig4_verification"))


def draw_matrix(fig, axes, df, value_col, cmap, cbar_label, outbase, protocols, annotate_mode="transition", omit_note=None):
    vmin, vmax = 0.0, 1.0
    cols = sorted(df["cooling_h_nominal_W_per_m2K"].unique())
    rows = protocols
    first_img = None
    for i, protocol in enumerate(rows):
        for j, h in enumerate(cols):
            ax = axes[i, j]
            sub = df[(df["name"] == protocol) & (df["cooling_h_nominal_W_per_m2K"] == h)]
            mat = np.full((len(WALL_ORDER), len(INSERTION_ORDER)), np.nan)
            for wi, wall in enumerate(WALL_ORDER):
                for ii, ins in enumerate(INSERTION_ORDER):
                    s = sub[(sub["wall_thickness_mm"] == wall) & (sub["insertion_nominal_mm"] == ins)]
                    if len(s):
                        mat[wi, ii] = float(s[value_col].iloc[0])
            img = ax.imshow(mat, origin="lower", aspect="auto", vmin=vmin, vmax=vmax, cmap=cmap,
                            extent=[INSERTION_ORDER[0]-0.25, INSERTION_ORDER[-1]+0.25, WALL_ORDER[0]-0.5, WALL_ORDER[-1]+0.5])
            if first_img is None:
                first_img = img
            ax.set_xticks(INSERTION_ORDER)
            ax.set_yticks(WALL_ORDER)
            ax.grid(color="white", linewidth=1.25, alpha=0.55)
            ax.set_axisbelow(False)
            if i < len(rows)-1:
                ax.set_xticklabels([])
            else:
                ax.set_xlabel("Nominal insertion [mm]")
            if j > 0:
                ax.set_yticklabels([])

            if i == 0:
                chip(ax, COOLING_LABEL[float(h)], y=1.05)

            # annotate selected cells
            for wi, wall in enumerate(WALL_ORDER):
                for ii, ins in enumerate(INSERTION_ORDER):
                    val = mat[wi, ii]
                    if np.isnan(val):
                        continue
                    show = False
                    if annotate_mode == "transition":
                        show = (val > 0) and (val < 1)
                    elif annotate_mode == "all":
                        show = True
                    elif annotate_mode == "nonzero":
                        show = val > 0
                    if show:
                        color = "white" if val < 0.45 else "black"
                        ax.text(ins, wall, f"{val:.2f}", ha="center", va="center", fontsize=11, color=color)

    for i, protocol in enumerate(rows):
        protocol_tag(fig, axes[i, 0], PROTOCOL_LABEL[protocol], PALETTE["protocol_light"][protocol])

    fig.text(0.04, 0.50, "Wall thickness [mm]", rotation=90, va="center", ha="center",
             fontsize=13, color=PALETTE["text"])
    cbar = fig.colorbar(first_img, ax=axes.ravel().tolist(), fraction=0.03, pad=0.02)
    cbar.set_label(cbar_label)
    if omit_note:
        fig.text(0.12, 0.02, omit_note, fontsize=10.5, color=PALETTE["text"])
    fig.subplots_adjust(left=0.12, right=0.92, top=0.92, bottom=0.10, wspace=0.08, hspace=0.10)
    save(fig, outbase)


def fig5_transmural(uq_df: pd.DataFrame, outdir: str):
    fig, axes = plt.subplots(3, 3, figsize=(10.5, 8.2), facecolor=PALETTE["background"], sharex=True, sharey=True)
    draw_matrix(fig, axes, uq_df, "transmural_probability", PALETTE["cmap_prob"],
                "Transmural probability",
                os.path.join(outdir, "fig5_transmural_probability_maps"),
                protocols=PROTOCOL_ORDER, annotate_mode="transition")


def fig6_overheat(uq_df: pd.DataFrame, outdir: str):
    sub = uq_df[uq_df["name"].isin(["hpsd_50W_10s", "vhpsd_90W_4s"])].copy()
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 6.4), facecolor=PALETTE["background"], sharex=True, sharey=True)
    draw_matrix(fig, axes, sub, "overheat_probability", PALETTE["cmap_overheat"],
                "Overheat probability",
                os.path.join(outdir, "fig6_overheat_probability_maps"),
                protocols=["hpsd_50W_10s", "vhpsd_90W_4s"],
                annotate_mode="transition",
                omit_note="Standard protocol omitted because overheating was not observed in the scanned conditions.")


def fig7_tradeoff_depthrisk(uq_df: pd.DataFrame, outdir: str):
    coolings = sorted(uq_df["cooling_h_nominal_W_per_m2K"].unique())
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.4), facecolor=PALETTE["background"], sharex=True, sharey=True)
    for j, h in enumerate(coolings):
        ax = axes[j]
        chip(ax, COOLING_LABEL[float(h)], y=1.05)
        ax.axvspan(0.80, 1.02, ymin=0.0, ymax=0.23, color="#BDE5D2", alpha=0.40, zorder=0)
        ax.text(0.93, 0.14, "favorable\nzone", ha="center", va="center", fontsize=11, color="#4F6E5E",
                transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.25,rounding_size=0.12",
                                                  fc="#BDE5D2", ec="#7AB894", lw=1.5, alpha=0.65))
        sub = uq_df[uq_df["cooling_h_nominal_W_per_m2K"] == h]
        for protocol in PROTOCOL_ORDER:
            ss = sub[sub["name"] == protocol]
            for wall in WALL_ORDER:
                s = ss[ss["wall_thickness_mm"] == wall]
                if len(s) == 0:
                    continue
                ax.scatter(
                    s["depth_fraction_p50"], s["overheat_probability"],
                    s=160, marker=PROTOCOL_MARKER[protocol],
                    facecolor=PALETTE["wall"][f"{wall:.1f}"], edgecolor="black",
                    linewidth=1.0, alpha=0.95
                )
        ax.set_xlim(-0.02, 1.03)
        ax.set_ylim(-0.02, 1.05)
        ax.set_xlabel("Median depth fraction")
        if j == 0:
            ax.set_ylabel("Overheat probability")
    protocol_handles = [
        Line2D([0], [0], marker=PROTOCOL_MARKER[p], markersize=12, lw=0,
               markerfacecolor="#D7DCE3", markeredgecolor="black", markeredgewidth=1.2,
               label=PROTOCOL_LABEL[p]) for p in PROTOCOL_ORDER
    ]
    wall_handles = [
        Line2D([0], [0], marker="o", markersize=11, lw=0,
               markerfacecolor=PALETTE["wall"][f"{w:.1f}"], markeredgecolor="black",
               label=f"{int(w)} mm") for w in WALL_ORDER
    ]
    leg1 = fig.legend(handles=protocol_handles, title="Protocol", loc="center left",
                      bbox_to_anchor=(0.98, 0.70), frameon=True)
    leg2 = fig.legend(handles=wall_handles, title="Wall thickness", loc="center left",
                      bbox_to_anchor=(0.98, 0.28), frameon=True)
    fig.add_artist(leg1)
    fig.subplots_adjust(left=0.08, right=0.86, top=0.90, bottom=0.16, wspace=0.18)
    save(fig, os.path.join(outdir, "fig7_tradeoff_depthrisk"))

    # supplementary ptrans-vs-pover scatter
    fig, axes = plt.subplots(1, 3, figsize=(12.2, 4.4), facecolor=PALETTE["background"], sharex=True, sharey=True)
    for j, h in enumerate(coolings):
        ax = axes[j]
        chip(ax, COOLING_LABEL[float(h)], y=1.05)
        sub = uq_df[uq_df["cooling_h_nominal_W_per_m2K"] == h]
        for protocol in PROTOCOL_ORDER:
            ss = sub[sub["name"] == protocol]
            for wall in WALL_ORDER:
                s = ss[ss["wall_thickness_mm"] == wall]
                if len(s) == 0:
                    continue
                ax.scatter(
                    s["transmural_probability"], s["overheat_probability"],
                    s=140, marker=PROTOCOL_MARKER[protocol],
                    facecolor=PALETTE["wall"][f"{wall:.1f}"], edgecolor="black",
                    linewidth=1.0, alpha=0.95
                )
        ax.set_xlim(-0.02, 1.03); ax.set_ylim(-0.02, 1.05)
        ax.set_xlabel("Transmural probability")
        if j == 0:
            ax.set_ylabel("Overheat probability")
    fig.legend(handles=protocol_handles, title="Protocol", loc="center left",
               bbox_to_anchor=(0.98, 0.70), frameon=True)
    fig.legend(handles=wall_handles, title="Wall thickness", loc="center left",
               bbox_to_anchor=(0.98, 0.28), frameon=True)
    fig.subplots_adjust(left=0.08, right=0.86, top=0.90, bottom=0.16, wspace=0.18)
    save(fig, os.path.join(outdir, "figS2_tradeoff_ptrans_pover"))


def figS1_depth(uq_df: pd.DataFrame, outdir: str):
    fig, axes = plt.subplots(3, 3, figsize=(10.5, 8.2), facecolor=PALETTE["background"], sharex=True, sharey=True)
    draw_matrix(fig, axes, uq_df, "depth_fraction_p50", PALETTE["cmap_depth"],
                "Median depth fraction",
                os.path.join(outdir, "figS1_depth_fraction_p50_maps"),
                protocols=PROTOCOL_ORDER, annotate_mode="all")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase-csv", required=True)
    parser.add_argument("--grid-csv", required=True)
    parser.add_argument("--dt-csv", required=True)
    parser.add_argument("--uq-csv", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--style", required=True)
    parser.add_argument("--palette", required=True)
    args = parser.parse_args()

    global PALETTE
    PALETTE = load_palette(args.palette)
    apply_style(args.style)
    os.makedirs(args.outdir, exist_ok=True)

    phase_df = pd.read_csv(args.phase_csv)
    grid_df = load_convergence(args.grid_csv, kind="grid")
    dt_df = load_convergence(args.dt_csv, kind="dt")
    uq_df = pd.read_csv(args.uq_csv)

    fig3_deterministic(phase_df, args.outdir)
    fig4_verification(grid_df, dt_df, args.outdir)
    fig5_transmural(uq_df, args.outdir)
    fig6_overheat(uq_df, args.outdir)
    fig7_tradeoff_depthrisk(uq_df, args.outdir)
    figS1_depth(uq_df, args.outdir)

    print(f"Saved polished figures to {args.outdir}")


if __name__ == "__main__":
    main()
