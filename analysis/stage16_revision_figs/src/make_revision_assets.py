
from __future__ import annotations
import argparse
from pathlib import Path
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yaml

PROTOCOL_ORDER = ['standard_30W_30s', 'hpsd_50W_10s', 'vhpsd_90W_4s']
PROTOCOL_LABELS = {
    'standard_30W_30s': 'Standard 30 W / 30 s',
    'hpsd_50W_10s': 'HPSD 50 W / 10 s',
    'vhpsd_90W_4s': 'vHPSD 90 W / 4 s',
}
COLORS = {
    'standard_30W_30s': '#2A9D8F',
    'hpsd_50W_10s': '#5B5F97',
    'vhpsd_90W_4s': '#E76F51',
}
MARKERS = {
    'standard_30W_30s': 'o',
    'hpsd_50W_10s': 's',
    'vhpsd_90W_4s': '^',
}

def save_all(fig: plt.Figure, outbase: Path) -> None:
    outbase.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outbase.with_suffix('.pdf'))
    fig.savefig(outbase.with_suffix('.png'), dpi=300)
    fig.savefig(outbase.with_suffix('.tiff'), dpi=600, pil_kwargs={'compression':'tiff_lzw'})
    plt.close(fig)


def make_fig3(phase_df: pd.DataFrame, outbase: Path) -> None:
    phase_df = phase_df.copy()
    fig, axes = plt.subplots(2, 3, figsize=(12.5, 7.0), constrained_layout=True)
    panels = [
        ('wall_thickness_mm', 'lesion_depth_mm', 'Wall thickness [mm]', 'Lesion depth [mm]', '(a) Depth vs wall thickness'),
        ('wall_thickness_mm', 'lesion_width_mm', 'Wall thickness [mm]', 'Maximum lesion width [mm]', '(b) Width vs wall thickness'),
        ('wall_thickness_mm', 'lesion_area_mm2', 'Wall thickness [mm]', 'Lesion area [mm²]', '(c) Area vs wall thickness'),
        ('insertion_depth_mm', 'peak_temperature_C', 'Insertion depth [mm]', 'Peak temperature [°C]', '(d) Peak temperature vs insertion'),
        ('cooling_h_W_per_m2K', 'depth_fraction', 'Cooling coefficient h [W m$^{-2}$ K$^{-1}$]', 'Depth fraction [-]', '(e) Depth fraction vs cooling'),
        ('cooling_h_W_per_m2K', 'depth_to_width_ratio', 'Cooling coefficient h [W m$^{-2}$ K$^{-1}$]', 'Depth-to-width ratio [-]', '(f) Depth-to-width ratio vs cooling'),
    ]

    # representative slices matching manuscript narrative
    wall_slice = phase_df[(phase_df['cooling_h_W_per_m2K'] == 1500.0) & (phase_df['insertion_depth_mm'] == 1.0)]
    ins_slice = phase_df[(phase_df['wall_thickness_mm'] == 4.0) & (phase_df['cooling_h_W_per_m2K'] == 1500.0)]
    cool_slice = phase_df[(phase_df['wall_thickness_mm'] == 4.0) & (phase_df['insertion_depth_mm'] == 1.0)]
    slices = [wall_slice, wall_slice, wall_slice, ins_slice, cool_slice, cool_slice]

    for ax, (xcol, ycol, xlabel, ylabel, title), sub in zip(axes.flat, panels, slices):
        for name in PROTOCOL_ORDER:
            g = sub[sub['name'] == name].sort_values(xcol)
            if len(g) == 0:
                continue
            ax.plot(g[xcol], g[ycol], marker=MARKERS[name], color=COLORS[name], label=PROTOCOL_LABELS[name])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc='left', fontweight='bold')
        if ycol == 'depth_fraction':
            ax.set_ylim(0, 1.05)
    handles, labels = axes[0,0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=3, loc='lower center', bbox_to_anchor=(0.5, -0.02), frameon=False)
    save_all(fig, outbase)


def make_table2(baseline_yaml: Path, uq_yaml: Path, uq_df: pd.DataFrame, outdir: Path) -> None:
    base = yaml.safe_load(Path(baseline_yaml).read_text())
    uq = yaml.safe_load(Path(uq_yaml).read_text())
    rows = [
        ('Deterministic baseline grid', f"{int(base['nx'])} × {int(base['ny'])}"),
        ('Time step Δt', f"{float(base['dt_s']):.3f} s"),
        ('Wall thickness levels', ', '.join(str(v) for v in uq['wall_thickness_mm_values'])),
        ('Nominal cooling levels h', ', '.join(str(v) for v in uq['cooling_h_W_per_m2K_values'])),
        ('Nominal insertion levels', ', '.join(str(v) for v in uq['insertion_depth_mm_values'])),
        ('UQ samples per cell', str(int(uq['samples_per_cell']))),
        ('Insertion distribution', f"Truncated normal, mean = nominal, sd = {uq['insertion_sd_mm']:.2f} mm"),
        ('Insertion support', f"[{uq['insertion_min_mm']:.2f}, {uq['insertion_max_mm']:.2f}] mm"),
        ('Cooling distribution', f"Truncated normal, mean = nominal, CV = {uq['cooling_cv']:.2f}"),
        ('Cooling support', f"[{uq['cooling_min_W_per_m2K']:.0f}, {uq['cooling_max_W_per_m2K']:.0f}] W m^-2 K^-1"),
        ('Probability interval', '95% Wilson score interval'),
        ('Overheat proxy threshold', f"Tmax ≥ {uq['overheat_threshold_C']:.0f} °C or non-zero area above 100 °C"),
    ]
    df = pd.DataFrame(rows, columns=['Item', 'Value'])
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir/'table2_uncertainty_solver_settings.csv', index=False)
    # markdown
    md = ['| Item | Value |', '|---|---|']
    md += [f"| {r[0]} | {r[1]} |" for r in rows]
    (outdir/'table2_uncertainty_solver_settings.md').write_text('\n'.join(md))


def make_figS3(uq_df: pd.DataFrame, outbase: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), constrained_layout=True)
    for ax, prob_col, lo_col, hi_col, title in [
        (axes[0], 'transmural_probability', 'transmural_probability_ci_low', 'transmural_probability_ci_high', '(a) Transmural probability CI half-width'),
        (axes[1], 'overheat_probability', 'overheat_probability_ci_low', 'overheat_probability_ci_high', '(b) Overheat probability CI half-width'),
    ]:
        half = 0.5 * (uq_df[hi_col] - uq_df[lo_col])
        ax.hist(half, bins=12, color='#6C757D', edgecolor='white')
        ax.set_xlabel('CI half-width [-]')
        ax.set_ylabel('Cell count')
        ax.set_title(title, loc='left', fontweight='bold')
    save_all(fig, outbase)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase-csv', required=True)
    parser.add_argument('--uq-csv', required=True)
    parser.add_argument('--baseline-yaml', required=True)
    parser.add_argument('--uq-yaml', required=True)
    parser.add_argument('--outdir', required=True)
    args = parser.parse_args()
    plt.style.use(str(Path(__file__).resolve().parents[1] / 'styles' / 'revision_light.mplstyle'))
    outdir = Path(args.outdir)
    phase_df = pd.read_csv(args.phase_csv)
    uq_df = pd.read_csv(args.uq_csv)
    make_fig3(phase_df, outdir / 'fig3_deterministic_summary_v2')
    make_table2(Path(args.baseline_yaml), Path(args.uq_yaml), uq_df, outdir)
    make_figS3(uq_df, outdir / 'figS3_probability_ci_halfwidths')

if __name__ == '__main__':
    main()
