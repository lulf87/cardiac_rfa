from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yaml

from controller import GenericTempLimitedController
from latency import LatencyConfig
from model_fd import CaseConfig, clone_cfg, plot_case, run_case_with_fields, save_summary, summarize_result


def make_protocol_comparison(df: pd.DataFrame, outpath: str | Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.0), constrained_layout=True)
    x = range(len(df))
    labels = df["name"].tolist()

    panels = [
        ("lesion_depth_mm", "Lesion depth [mm]"),
        ("peak_temperature_C", "Peak temperature [C]"),
        ("overheat_area_mm2", "Overheat area [mm^2]"),
    ]

    for ax, (col, ylabel) in zip(axes, panels):
        ax.bar(x, df[col], color="#4C78A8")
        ax.set_xticks(list(x), labels=labels, rotation=20, ha="right")
        ax.set_ylabel(ylabel)
        ax.set_title(col)

    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", required=True)
    parser.add_argument("--protocols", required=True)
    parser.add_argument("--controller-config")
    parser.add_argument("--latency-config")
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())["protocols"]
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
        )
        result, fields = run_case_with_fields(
            cfg,
            controller=controller if use_controller else None,
            latency=latency,
        )

        case_dir = outdir / str(p["name"])
        case_dir.mkdir(parents=True, exist_ok=True)
        plot_case(result, case_dir / "case_fields.png", fields=fields, cfg=cfg)
        save_summary(result, case_dir / "summary.yaml")

        row = summarize_result(result)
        row["name"] = str(p["name"])
        row["use_controller"] = use_controller
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(outdir / "protocol_summary.csv", index=False)
    make_protocol_comparison(df, outdir / "protocol_comparison.png")

    display_cols = [
        "name",
        "power_W",
        "duration_s",
        "lesion_depth_mm",
        "peak_temperature_C",
        "overheat_area_mm2",
        "transmural",
    ]
    optional_cols = [
        "requested_power_W",
        "delivered_energy_J",
        "mean_applied_power_W",
        "controller_enabled",
        "latency_enabled",
        "latency_duration_s",
    ]
    display_cols.extend([col for col in optional_cols if col in df.columns])
    print(df[display_cols])


if __name__ == "__main__":
    main()
