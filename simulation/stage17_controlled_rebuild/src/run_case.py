from __future__ import annotations

import argparse
from pathlib import Path

from controller import GenericTempLimitedController
from latency import LatencyConfig
from model_fd import CaseConfig, run_case_with_fields, plot_case, save_summary


def _peak_temperature_scalar(result: dict) -> float:
    if "peak_temperature_C" in result:
        return float(result["peak_temperature_C"])

    if "peak_T_C" in result:
        legacy_value = result["peak_T_C"]
        if hasattr(legacy_value, "max"):
            return float(legacy_value.max())
        return float(legacy_value)

    raise KeyError(
        "Result is missing both 'peak_temperature_C' and legacy 'peak_T_C' peak-temperature fields."
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--controller-config')
    parser.add_argument('--latency-config')
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    cfg = CaseConfig.from_yaml(args.config)
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
    result, fields = run_case_with_fields(cfg, controller=controller, latency=latency)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    plot_case(result, outdir / 'case_fields.png', fields=fields, cfg=cfg)
    save_summary(result, outdir / 'summary.yaml')
    print(f'Saved results to {outdir}')
    print(f"Lesion depth: {result['lesion_depth_mm']:.3f} mm")
    print(f"Lesion width: {result['lesion_width_mm']:.3f} mm")
    print(f"Lesion area: {result['lesion_area_mm2']:.4f} mm^2")
    print(f"Peak temperature: {_peak_temperature_scalar(result):.2f} C")
    print(f"Overheat area >=100C: {result['overheat_area_mm2']:.4f} mm^2")
    if 'requested_power_W' in result:
        print(f"Requested power: {result['requested_power_W']:.2f} W")
    if 'delivered_energy_J' in result:
        print(f"Delivered energy: {result['delivered_energy_J']:.4f} J")
    if 'mean_applied_power_W' in result:
        print(f"Mean applied power: {result['mean_applied_power_W']:.4f} W")
    if 'controller_enabled' in result:
        print(f"Controller enabled: {result['controller_enabled']}")
    if 'latency_enabled' in result:
        print(f"Latency enabled: {result['latency_enabled']}")
    if 'latency_duration_s' in result:
        print(f"Latency duration: {result['latency_duration_s']:.4f} s")


if __name__ == '__main__':
    main()
