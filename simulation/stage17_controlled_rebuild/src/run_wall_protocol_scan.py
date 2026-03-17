from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml

from controller import GenericTempLimitedController
from latency import LatencyConfig
from model_fd import (
    CaseConfig,
    bool_heatmap,
    clone_cfg,
    line_plot,
    rescale_ny,
    run_case,
    summarize_result,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", required=True)
    parser.add_argument("--protocols", required=True)
    parser.add_argument("--wall-scan", required=True)
    parser.add_argument("--controller-config")
    parser.add_argument("--latency-config")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())["protocols"]
    wall_cfg = yaml.safe_load(Path(args.wall_scan).read_text())
    wall_values = [float(v) for v in wall_cfg["wall_thickness_mm_values"]]

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
    for wall_mm in wall_values:
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
                wall_thickness_mm=wall_mm,
                ny=rescale_ny(base, wall_mm),
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
                f"wall={wall_mm:.1f} | {p['name']} | "
                f"depth={row['lesion_depth_mm']:.3f} mm | "
                f"frac={row['depth_fraction']:.3f} | "
                f"Tmax={row['peak_temperature_C']:.2f} C | "
                f"transmural={row['transmural']}"
            )

    df = pd.DataFrame(rows)
    df["transmural_int"] = df["transmural"].astype(int)
    df.to_csv(outdir / "wall_protocol_summary.csv", index=False)

    protocol_names = [str(p["name"]) for p in protocols]
    bool_heatmap(
        df,
        x_values=wall_values,
        y_values=protocol_names,
        x_col="wall_thickness_mm",
        y_col="name",
        value_col="transmural_int",
        title="Transmurality across wall thickness",
        xlabel="Wall thickness [mm]",
        ylabel="Protocol",
        outpath=outdir / "wall_transmurality_map.png",
    )
    line_plot(
        df,
        x_col="wall_thickness_mm",
        y_col="lesion_depth_mm",
        group_col="name",
        title="Wall thickness vs lesion depth",
        xlabel="Wall thickness [mm]",
        ylabel="Lesion depth [mm]",
        outpath=outdir / "wall_vs_depth.png",
    )
    line_plot(
        df,
        x_col="wall_thickness_mm",
        y_col="depth_fraction",
        group_col="name",
        title="Wall thickness vs depth fraction",
        xlabel="Wall thickness [mm]",
        ylabel="Depth fraction [-]",
        outpath=outdir / "wall_vs_depth_fraction.png",
    )
    print("\nSaved wall scan results to", outdir)


if __name__ == "__main__":
    main()
