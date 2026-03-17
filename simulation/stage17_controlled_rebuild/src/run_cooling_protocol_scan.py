from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml

from controller import GenericTempLimitedController
from latency import LatencyConfig
from model_fd import CaseConfig, clone_cfg, line_plot, run_case, summarize_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", required=True)
    parser.add_argument("--protocols", required=True)
    parser.add_argument("--cooling-scan", required=True)
    parser.add_argument("--controller-config")
    parser.add_argument("--latency-config")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())["protocols"]
    cooling_cfg = yaml.safe_load(Path(args.cooling_scan).read_text())
    cooling_values = [float(v) for v in cooling_cfg["cooling_h_W_per_m2K_values"]]

    controller = (
        GenericTempLimitedController.from_yaml(args.controller_config)
        if args.controller_config
        else None
    )
    latency = (
        LatencyConfig.from_yaml(args.latency_config)
        if args.latency_config
        else None
    )

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    for h in cooling_values:
        for p in protocols:
            use_controller = bool(p.get("use_controller", False))
            if use_controller and controller is None:
                raise ValueError(
                    f"Protocol '{p['name']}' requested use_controller: true but no --controller-config was provided."
                )

            cfg = clone_cfg(
                base,
                power_W=float(p["power_W"]),
                duration_s=float(p["duration_s"]),
                cooling_h_W_per_m2K=h,
            )
            result = run_case(
                cfg,
                controller=controller if use_controller else None,
                latency=latency,
            )
            row = summarize_result(result)
            row["name"] = str(p["name"])
            row["use_controller"] = use_controller
            rows.append(row)
            print(
                f"h={h:.0f} | {p['name']} | "
                f"depth={row['lesion_depth_mm']:.3f} mm | "
                f"Tmax={row['peak_temperature_C']:.2f} C | "
                f"transmural={row['transmural']}"
            )

    df = pd.DataFrame(rows)
    df.to_csv(outdir / "cooling_protocol_summary.csv", index=False)

    line_plot(
        df,
        x_col="cooling_h_W_per_m2K",
        y_col="lesion_depth_mm",
        group_col="name",
        title="Cooling vs lesion depth",
        xlabel="Cooling coefficient h [W m^-2 K^-1]",
        ylabel="Lesion depth [mm]",
        outpath=outdir / "cooling_vs_depth.png",
    )
    line_plot(
        df,
        x_col="cooling_h_W_per_m2K",
        y_col="peak_temperature_C",
        group_col="name",
        title="Cooling vs peak temperature",
        xlabel="Cooling coefficient h [W m^-2 K^-1]",
        ylabel="Peak temperature [C]",
        outpath=outdir / "cooling_vs_peakT.png",
    )
    print("\nSaved cooling scan results to", outdir)


if __name__ == "__main__":
    main()
