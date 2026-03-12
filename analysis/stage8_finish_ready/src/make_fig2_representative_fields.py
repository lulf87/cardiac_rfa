
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt

from common import apply_style, add_chip, panel_label, save_pdf_png, protocol_color, PROTOCOL_ORDER, PROTOCOL_DISPLAY, PROTOCOL_MARKER, load_palette


def import_stage3(stage3_root: Path):
    src = stage3_root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from model_fd import CaseConfig, clone_cfg, run_case
    return CaseConfig, clone_cfg, run_case


def make_fig2(stage3_root: Path, baseline_yaml: Path, protocols_yaml: Path, outbase: Path,
              wall_mm: float = 4.0, h_W_m2K: float = 1500.0, insertion_mm: float = 1.0):
    pal = apply_style()
    CaseConfig, clone_cfg, run_case = import_stage3(stage3_root)

    base_cfg = CaseConfig.from_yaml(baseline_yaml)
    proto_raw = yaml.safe_load(protocols_yaml.read_text())
    if isinstance(proto_raw, dict) and "protocols" in proto_raw:
        proto = {item["name"]: item for item in proto_raw["protocols"]}
    else:
        proto = proto_raw

    results = {}
    for key in PROTOCOL_ORDER:
        cfg = clone_cfg(
            base_cfg,
            power_W=float(proto[key]["power_W"]),
            duration_s=float(proto[key]["duration_s"]),
            wall_thickness_mm=float(wall_mm),
            cooling_h_W_per_m2K=float(h_W_m2K),
            insertion_depth_mm=float(insertion_mm),
        )
        results[key] = run_case(cfg)

    fig = plt.figure(figsize=(11.8, 6.6))
    gs = fig.add_gridspec(2, 3, hspace=0.18, wspace=0.12)

    # Shared scales
    tmin, tmax = 37.0, max(float(np.max(results[k]["peak_T_C"])) for k in PROTOCOL_ORDER)
    tmax = max(100.0, np.ceil(tmax/5)*5)
    omin, omax = -4.0, 2.0

    ims = {}
    for c, key in enumerate(PROTOCOL_ORDER):
        res = results[key]
        x = res["x_m"] * 1e3
        y = res["y_m"] * 1e3
        extent = [x.min(), x.max(), y.max(), y.min()]

        axT = fig.add_subplot(gs[0, c])
        axO = fig.add_subplot(gs[1, c], sharex=axT)

        if c == 0:
            panel_label(axT, "(a)")
            panel_label(axO, "(b)")

        # temperature
        imT = axT.imshow(res["peak_T_C"], extent=extent, aspect="auto", vmin=tmin, vmax=tmax, cmap="inferno")
        axT.contour(x, y, res["omega"], levels=[1.0], colors=["#5CE1E6"], linewidths=1.6)
        axT.axhline(0.0, lw=1.0, color=pal["spine"], alpha=0.8)
        axT.axhline(wall_mm, ls="--", lw=1.0, color=pal["spine"], alpha=0.8)
        axT.grid(False)
        ew = res["cfg"].electrode_width_mm / 2
        axT.add_patch(plt.Rectangle((-ew, -0.10), 2*ew, 0.12, fc="#B9C4CE", ec=pal["spine"], lw=0.8, clip_on=False))
        add_chip(axT, PROTOCOL_DISPLAY[key])
        axT.set_title("")  # chip only
        if c == 0:
            axT.set_ylabel("Depth [mm]")
        axT.set_xticks([])
        axT.set_ylim(y.max(), 0)
        axT.set_xlim(x.min(), x.max())
        axT.text(0.02, 0.93, f"depth = {res['lesion_depth_mm']:.2f} mm", transform=axT.transAxes,
                 fontsize=9.2, bbox=dict(boxstyle="round,pad=0.2", fc=(1,1,1,0.82), ec="none"))

        # damage
        log_omega = np.log10(np.clip(res["omega"], 1e-6, None))
        imO = axO.imshow(log_omega, extent=extent, aspect="auto", vmin=omin, vmax=omax, cmap="viridis")
        axO.contour(x, y, res["omega"], levels=[1.0], colors=["#F6E27A"], linewidths=1.6)
        axO.axhline(0.0, lw=1.0, color=pal["spine"], alpha=0.8)
        axO.axhline(wall_mm, ls="--", lw=1.0, color=pal["spine"], alpha=0.8)
        axO.grid(False)
        axO.add_patch(plt.Rectangle((-ew, -0.10), 2*ew, 0.12, fc="#B9C4CE", ec=pal["spine"], lw=0.8, clip_on=False))
        if c == 0:
            axO.set_ylabel("Depth [mm]")
        axO.set_xlabel("Lateral position [mm]")
        axO.set_ylim(y.max(), 0)
        axO.set_xlim(x.min(), x.max())
        ims["T"] = imT
        ims["O"] = imO

    caxT = fig.add_axes([0.92, 0.56, 0.018, 0.28])
    cbT = fig.colorbar(ims["T"], cax=caxT)
    cbT.set_label("Temperature [°C]")

    caxO = fig.add_axes([0.92, 0.14, 0.018, 0.28])
    cbO = fig.colorbar(ims["O"], cax=caxO)
    cbO.set_label("log10(Arrhenius Ω)")

    fig.text(0.5, 0.98, f"Representative case: wall={wall_mm:.1f} mm, h={h_W_m2K:.0f} W/m²K, insertion={insertion_mm:.2f} mm",
             ha="center", va="top", fontsize=11.5, color=pal["text"])
    fig.text(0.014, 0.77, "Ω = 1 contour", rotation=90, va="center", ha="center", fontsize=9.5, color="#5CE1E6")
    fig.text(0.014, 0.33, "Ω = 1 contour", rotation=90, va="center", ha="center", fontsize=9.5, color="#F6E27A")

    save_pdf_png(fig, outbase)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage3-root", type=Path, required=True, help="Path to simulation/stage3_uq_maps")
    ap.add_argument("--baseline-yaml", type=Path, required=True)
    ap.add_argument("--protocols-yaml", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--wall-mm", type=float, default=4.0)
    ap.add_argument("--cooling-h", type=float, default=1500.0)
    ap.add_argument("--insertion-mm", type=float, default=1.0)
    args = ap.parse_args()
    make_fig2(args.stage3_root, args.baseline_yaml, args.protocols_yaml,
              args.outdir / "fig2_representative_fields",
              wall_mm=args.wall_mm, h_W_m2K=args.cooling_h, insertion_mm=args.insertion_mm)


if __name__ == "__main__":
    main()
