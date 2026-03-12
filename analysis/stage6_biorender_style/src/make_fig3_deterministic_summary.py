import argparse
from pathlib import Path
import matplotlib.pyplot as plt
from pubstyle import use_pub_style, save_figure, panel_label, DOUBLE_COL_IN, PROTOCOL_COLORS, PROTOCOL_SHORT, title_chip, soft_legend
from common import read_csv, protocol_order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--phase-prep-csv', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()

    use_pub_style()
    df = read_csv(args.phase_prep_csv)
    order = protocol_order()

    fig, axs = plt.subplots(2, 2, figsize=(DOUBLE_COL_IN, 5.15), constrained_layout=True)
    handles = []

    ax = axs[0, 0]
    sub = df[(df['cooling_h_W_per_m2K'] == 1500) & (df['insertion_depth_mm'] == 1.0)]
    for name in order:
        s = sub[sub['name'] == name].sort_values('wall_thickness_mm')
        line, = ax.plot(s['wall_thickness_mm'], s['depth_fraction'], marker='o', color=PROTOCOL_COLORS[name], label=PROTOCOL_SHORT[name])
        handles.append(line)
    ax.set_xlabel('Wall thickness [mm]')
    ax.set_ylabel('Depth fraction [-]')
    ax.set_ylim(0, 1.08)
    title_chip(ax, 'Nominal contact, nominal cooling')
    ax.grid(axis='y')
    panel_label(ax, '(a)')

    ax = axs[0, 1]
    sub = df[(df['wall_thickness_mm'] == 2.0) & (df['cooling_h_W_per_m2K'] == 1500)]
    for name in order:
        s = sub[sub['name'] == name].sort_values('insertion_depth_mm')
        ax.plot(s['insertion_depth_mm'], s['depth_fraction'], marker='o', color=PROTOCOL_COLORS[name])
    ax.set_xlabel('Nominal insertion [mm]')
    ax.set_ylabel('Depth fraction [-]')
    ax.set_ylim(0, 1.08)
    title_chip(ax, 'Thin wall, nominal cooling')
    ax.grid(axis='y')
    panel_label(ax, '(b)')

    ax = axs[1, 0]
    sub = df[(df['wall_thickness_mm'] == 4.0) & (df['insertion_depth_mm'] == 1.5)]
    for name in order:
        s = sub[sub['name'] == name].sort_values('cooling_h_W_per_m2K')
        ax.plot(s['cooling_h_W_per_m2K'], s['depth_fraction'], marker='o', color=PROTOCOL_COLORS[name])
    ax.set_xlabel('Cooling coefficient h [W m$^{-2}$ K$^{-1}$]')
    ax.set_ylabel('Depth fraction [-]')
    ax.set_ylim(0, 1.0)
    title_chip(ax, 'Moderate-thickness wall, elevated contact')
    ax.grid(axis='y')
    panel_label(ax, '(c)')

    ax = axs[1, 1]
    sub = df[(df['wall_thickness_mm'] == 2.0) & (df['cooling_h_W_per_m2K'] == 1500)]
    for name in order:
        s = sub[sub['name'] == name].sort_values('insertion_depth_mm')
        ax.plot(s['insertion_depth_mm'], s['peak_temperature_C'], marker='o', color=PROTOCOL_COLORS[name])
    ax.axhline(100.0, color='#6B7280', ls='--', lw=1.1)
    ax.text(0.02, 0.96, '100°C threshold', transform=ax.transAxes, va='top', ha='left', fontsize=7.5, color='#555')
    ax.set_xlabel('Nominal insertion [mm]')
    ax.set_ylabel('Peak temperature [°C]')
    title_chip(ax, 'Thin wall, nominal cooling')
    ax.grid(axis='y')
    panel_label(ax, '(d)')

    leg = fig.legend(handles=handles, labels=[PROTOCOL_SHORT[n] for n in order], loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.01), columnspacing=1.4, handlelength=2.2)
    soft_legend(leg)
    save_figure(fig, Path(args.outdir) / 'fig3_deterministic_summary')

if __name__ == '__main__':
    main()
