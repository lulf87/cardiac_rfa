from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import yaml

from controller import GenericTempLimitedController
from latency import LatencyConfig
from model_fd import CaseConfig, bool_heatmap, clone_cfg, line_plot, run_case, summarize_result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", required=True)
    parser.add_argument("--protocols", required=True)
    parser.add_argument("--contact-scan", required=True)
    parser.add_argument("--controller-config")
    parser.add_argument("--latency-config")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())["protocols"]
    contact_cfg = yaml.safe_load(Path(args.contact_scan).read_text())
    insertion_values = [float(v) for v in contact_cfg["insertion_depth_mm_values"]]

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
    for ins in insertion_values:
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
                insertion_depth_mm=ins,
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
                f"ins={ins:.2f} | {p['name']} | "
                f"depth={row['lesion_depth_mm']:.3f} mm | "
                f"Tmax={row['peak_temperature_C']:.2f} C | "
                f"transmural={row['transmural']}"
            )

    df = pd.DataFrame(rows)
    df["transmural_int"] = df["transmural"].astype(int)
    df.to_csv(outdir / "contact_protocol_summary.csv", index=False)

    protocol_names = [str(p["name"]) for p in protocols]
    bool_heatmap(
        df,
        x_values=insertion_values,
        y_values=protocol_names,
        x_col="insertion_depth_mm",
        y_col="name",
        value_col="transmural_int",
        title="Transmurality across insertion depth",
        xlabel="Insertion depth [mm]",
        ylabel="Protocol",
        outpath=outdir / "contact_transmurality_map.png",
    )
    line_plot(
        df,
        x_col="insertion_depth_mm",
        y_col="lesion_depth_mm",
        group_col="name",
        title="Insertion depth vs lesion depth",
        xlabel="Insertion depth [mm]",
        ylabel="Lesion depth [mm]",
        outpath=outdir / "contact_vs_depth.png",
    )
    line_plot(
        df,
        x_col="insertion_depth_mm",
        y_col="peak_temperature_C",
        group_col="name",
        title="Insertion depth vs peak temperature",
        xlabel="Insertion depth [mm]",
        ylabel="Peak temperature [C]",
        outpath=outdir / "contact_vs_peakT.png",
    )
    print("\nSaved contact scan results to", outdir)


if __name__ == "__main__":
    main()
