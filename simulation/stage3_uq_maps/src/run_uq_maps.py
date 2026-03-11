from __future__ import annotations

import argparse
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import yaml
import matplotlib.pyplot as plt
from scipy.stats import norm

from model_fd import CaseConfig, clone_cfg, rescale_ny, run_case, summarize_result


def lhs_normal(mean: float, sd: float, n: int, rng: np.random.Generator, lo: float | None = None, hi: float | None = None) -> np.ndarray:
    if sd <= 0:
        out = np.full(n, mean, dtype=float)
    else:
        u = (np.arange(n) + rng.random(n)) / n
        rng.shuffle(u)
        z = norm.ppf(u)
        out = mean + sd * z
    if lo is not None or hi is not None:
        lo = -np.inf if lo is None else lo
        hi = np.inf if hi is None else hi
        out = np.clip(out, lo, hi)
    return out


def make_samples(n: int, ins_mean: float, h_mean: float, cfg: dict, rng: np.random.Generator) -> Tuple[np.ndarray, np.ndarray]:
    ins_sd = float(cfg.get('insertion_sd_mm', 0.20))
    ins_lo = float(cfg.get('insertion_min_mm', 0.25))
    ins_hi = float(cfg.get('insertion_max_mm', 2.50))
    cooling_cv = float(cfg.get('cooling_cv', 0.15))
    h_sd = cooling_cv * h_mean
    h_lo = float(cfg.get('cooling_min_W_per_m2K', 300.0))
    h_hi = float(cfg.get('cooling_max_W_per_m2K', 4000.0))

    ins = lhs_normal(ins_mean, ins_sd, n, rng, lo=ins_lo, hi=ins_hi)
    h = lhs_normal(h_mean, h_sd, n, rng, lo=h_lo, hi=h_hi)
    return ins, h


def save_probability_panels(df: pd.DataFrame, protocol_name: str, value_col: str, title: str, outpath: Path) -> None:
    sub = df[df['name'] == protocol_name].copy()
    cooling_vals = sorted(sub['cooling_h_nominal_W_per_m2K'].unique())
    wall_vals = sorted(sub['wall_thickness_mm'].unique())
    ins_vals = sorted(sub['insertion_nominal_mm'].unique())

    fig, axes = plt.subplots(1, len(cooling_vals), figsize=(4.8 * len(cooling_vals), 4.4), constrained_layout=True)
    if len(cooling_vals) == 1:
        axes = [axes]

    vmin = float(sub[value_col].min())
    vmax = float(sub[value_col].max())
    if abs(vmax - vmin) < 1e-12:
        vmax = vmin + 1e-6

    im = None
    for ax, h in zip(axes, cooling_vals):
        cur = sub[sub['cooling_h_nominal_W_per_m2K'] == h]
        piv = cur.pivot_table(index='wall_thickness_mm', columns='insertion_nominal_mm', values=value_col, aggfunc='mean').reindex(index=wall_vals, columns=ins_vals)
        im = ax.imshow(piv.values, aspect='auto', origin='lower', vmin=vmin, vmax=vmax)
        ax.set_title(f'h = {h:.0f} W/m²K')
        ax.set_xlabel('Nominal insertion [mm]')
        ax.set_xticks(range(len(ins_vals)), labels=[f'{v:.2f}' for v in ins_vals])
        ax.set_yticks(range(len(wall_vals)), labels=[f'{v:.1f}' for v in wall_vals])
        ax.set_ylabel('Wall thickness [mm]')
        for iy in range(len(wall_vals)):
            for ix in range(len(ins_vals)):
                val = piv.values[iy, ix]
                if pd.notna(val):
                    ax.text(ix, iy, f'{val:.2f}', ha='center', va='center', fontsize=7)

    fig.suptitle(f'{protocol_name}: {title}', fontsize=13)
    if im is not None:
        cbar = fig.colorbar(im, ax=axes, shrink=0.84)
        cbar.set_label(value_col)
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-config', required=True)
    parser.add_argument('--protocols', required=True)
    parser.add_argument('--uq-config', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()

    base = CaseConfig.from_yaml(args.base_config)
    protocols = yaml.safe_load(Path(args.protocols).read_text())['protocols']
    uq_cfg = yaml.safe_load(Path(args.uq_config).read_text())

    wall_values = [float(v) for v in uq_cfg['wall_thickness_mm_values']]
    cooling_values = [float(v) for v in uq_cfg['cooling_h_W_per_m2K_values']]
    insertion_values = [float(v) for v in uq_cfg['insertion_depth_mm_values']]
    samples_per_cell = int(uq_cfg.get('samples_per_cell', 8))
    overheat_threshold_C = float(uq_cfg.get('overheat_threshold_C', 100.0))
    seed = int(uq_cfg.get('seed', 20260311))

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    rows = []
    for wall_mm in wall_values:
        for h_nom in cooling_values:
            for ins_nom in insertion_values:
                ins_samples, h_samples = make_samples(samples_per_cell, ins_nom, h_nom, uq_cfg, rng)
                for p in protocols:
                    cell_rows = []
                    for k in range(samples_per_cell):
                        cfg = clone_cfg(
                            base,
                            power_W=float(p['power_W']),
                            duration_s=float(p['duration_s']),
                            wall_thickness_mm=wall_mm,
                            cooling_h_W_per_m2K=float(h_samples[k]),
                            insertion_depth_mm=float(ins_samples[k]),
                            ny=rescale_ny(base, wall_mm),
                        )
                        res = run_case(cfg)
                        row = summarize_result(res)
                        row['name'] = p['name']
                        row['sample_id'] = k
                        row['wall_thickness_mm'] = wall_mm
                        row['cooling_h_nominal_W_per_m2K'] = h_nom
                        row['insertion_nominal_mm'] = ins_nom
                        row['cooling_h_sampled_W_per_m2K'] = float(h_samples[k])
                        row['insertion_sampled_mm'] = float(ins_samples[k])
                        row['overheat'] = bool(row['peak_temperature_C'] >= overheat_threshold_C or row['overheat_area_mm2'] > 0.0)
                        cell_rows.append(row)
                        rows.append(row)

                    cell_df = pd.DataFrame(cell_rows)
                    p_trans = float(cell_df['transmural'].mean())
                    p_over = float(cell_df['overheat'].mean())
                    q50 = float(cell_df['depth_fraction'].median())
                    print(
                        f"wall={wall_mm:.1f} | h_nom={h_nom:.0f} | ins_nom={ins_nom:.2f} | {p['name']} | "
                        f"Ptrans={p_trans:.2f} | Pover={p_over:.2f} | depth50={q50:.2f}"
                    )

    df = pd.DataFrame(rows)
    df.to_csv(outdir / 'uq_samples.csv', index=False)

    summary = (
        df.groupby(['name', 'wall_thickness_mm', 'cooling_h_nominal_W_per_m2K', 'insertion_nominal_mm'], as_index=False)
        .agg(
            transmural_probability=('transmural', 'mean'),
            overheat_probability=('overheat', 'mean'),
            depth_fraction_mean=('depth_fraction', 'mean'),
            depth_fraction_p10=('depth_fraction', lambda s: float(np.quantile(s, 0.10))),
            depth_fraction_p50=('depth_fraction', 'median'),
            depth_fraction_p90=('depth_fraction', lambda s: float(np.quantile(s, 0.90))),
            lesion_depth_mean_mm=('lesion_depth_mm', 'mean'),
            tmax_mean_C=('peak_temperature_C', 'mean'),
            tmax_p90_C=('peak_temperature_C', lambda s: float(np.quantile(s, 0.90))),
            n_samples=('sample_id', 'count'),
        )
    )
    summary.to_csv(outdir / 'uq_summary.csv', index=False)

    overview = (
        summary.groupby('name', as_index=False)
        .agg(
            transmural_probability_mean=('transmural_probability', 'mean'),
            transmural_probability_max=('transmural_probability', 'max'),
            overheat_probability_mean=('overheat_probability', 'mean'),
            overheat_probability_max=('overheat_probability', 'max'),
            depth_fraction_p50_mean=('depth_fraction_p50', 'mean'),
            depth_fraction_p50_max=('depth_fraction_p50', 'max'),
        )
    )
    overview.to_csv(outdir / 'uq_overview.csv', index=False)

    for protocol_name in summary['name'].unique():
        save_probability_panels(
            summary,
            protocol_name,
            'transmural_probability',
            'Transmural probability under uncertain contact/cooling',
            outdir / f'{protocol_name}_transmural_probability.png',
        )
        save_probability_panels(
            summary,
            protocol_name,
            'overheat_probability',
            'Overheat probability under uncertain contact/cooling',
            outdir / f'{protocol_name}_overheat_probability.png',
        )
        save_probability_panels(
            summary,
            protocol_name,
            'depth_fraction_p50',
            'Median depth fraction under uncertainty',
            outdir / f'{protocol_name}_depth_fraction_p50.png',
        )

    print('\nSaved UQ results to', outdir)


if __name__ == '__main__':
    main()
