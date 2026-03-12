
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from pubstyle import use_pub_style, save_figure, panel_label, DOUBLE_COL_IN

def rel_error_percent(series):
    ref = series.iloc[-1]
    return (series - ref).abs() / abs(ref) * 100.0 if abs(ref) > 1e-12 else series * 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid-csv", required=True)
    ap.add_argument("--dt-csv", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    use_pub_style()
    grid = pd.read_csv(args.grid_csv).sort_values(["nx","ny"])
    dt = pd.read_csv(args.dt_csv).sort_values("dt_s", ascending=False)

    fig, axs = plt.subplots(1, 2, figsize=(DOUBLE_COL_IN, 2.8), constrained_layout=True)

    ax = axs[0]
    xg = [f"{n}×{m}" for n, m in zip(grid["nx"], grid["ny"])]
    ax.plot(xg, rel_error_percent(grid["lesion_depth_mm"]), marker="o", label="Lesion depth")
    ax.plot(xg, rel_error_percent(grid["peak_temperature_C"]), marker="s", label="Peak temperature")
    ax.set_title("Grid refinement")
    ax.set_xlabel("Grid")
    ax.set_ylabel("Relative error to finest solution [%]")
    ax.set_yscale("log")
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    panel_label(ax, "(a)")

    ax = axs[1]
    xd = [f"{v:.3f}" for v in dt["dt_s"]]
    ax.plot(xd, rel_error_percent(dt["lesion_depth_mm"]), marker="o", label="Lesion depth")
    ax.plot(xd, rel_error_percent(dt["peak_temperature_C"]), marker="s", label="Peak temperature")
    ax.set_title("Time-step refinement")
    ax.set_xlabel("Δt [s]")
    ax.set_ylabel("Relative error to finest solution [%]")
    ax.set_yscale("log")
    ax.legend(frameon=False, fontsize=7, loc="upper right")
    panel_label(ax, "(b)")

    save_figure(fig, Path(args.outdir)/"fig4_verification")

if __name__ == "__main__":
    main()
