from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Iterable

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import factorized, spsolve
import yaml
import matplotlib.pyplot as plt

R_GAS = 8.314462618  # J/(mol K)


@dataclass
class CaseConfig:
    width_mm: float = 12.0
    wall_thickness_mm: float = 4.0
    nx: int = 241
    ny: int = 121
    electrode_width_mm: float = 2.0
    power_W: float = 50.0
    duration_s: float = 10.0
    dt_s: float = 0.05
    t_init_C: float = 37.0
    t_blood_C: float = 37.0
    sigma_S_per_m: float = 0.6
    k_W_per_mK: float = 0.55
    rho_kg_per_m3: float = 1050.0
    c_J_per_kgK: float = 3600.0
    perfusion_W_per_m3K: float = 0.0
    cooling_h_W_per_m2K: float = 1500.0
    q_scale_W_per_m3_per_W: float = 3.0
    arrhenius_A_1_per_s: float = 7.39e39
    arrhenius_Ea_J_per_mol: float = 2.577e5
    lesion_omega_threshold: float = 1.0

    @staticmethod
    def from_yaml(path: str | Path) -> "CaseConfig":
        raw = yaml.safe_load(Path(path).read_text())
        data = {}
        for key, value in raw.items():
            if key in {"nx", "ny"}:
                data[key] = int(value)
            else:
                data[key] = float(value)
        return CaseConfig(**data)


def clone_cfg(cfg: CaseConfig, **kwargs: float | int) -> CaseConfig:
    data = dict(cfg.__dict__)
    data.update(kwargs)
    return CaseConfig(**data)


def rescale_ny(base_cfg: CaseConfig, wall_thickness_mm: float) -> int:
    ratio = wall_thickness_mm / base_cfg.wall_thickness_mm
    ny = int(round((base_cfg.ny - 1) * ratio)) + 1
    return max(21, ny)


def make_grid(cfg: CaseConfig):
    x = np.linspace(-0.5 * cfg.width_mm * 1e-3, 0.5 * cfg.width_mm * 1e-3, cfg.nx)
    y = np.linspace(0.0, cfg.wall_thickness_mm * 1e-3, cfg.ny)
    dx = x[1] - x[0]
    dy = y[1] - y[0]
    return x, y, dx, dy


def idx(i: int, j: int, nx: int) -> int:
    return j * nx + i


def electrode_mask(x: np.ndarray, cfg: CaseConfig) -> np.ndarray:
    ew = cfg.electrode_width_mm * 1e-3
    return np.abs(x) <= 0.5 * ew


def assemble_potential_system(cfg: CaseConfig):
    x, y, dx, dy = make_grid(cfg)
    nx, ny = cfg.nx, cfg.ny
    N = nx * ny
    rows, cols, vals = [], [], []
    b = np.zeros(N)
    elec = electrode_mask(x, cfg)

    def add(r: int, c: int, v: float) -> None:
        rows.append(r)
        cols.append(c)
        vals.append(v)

    for j in range(ny):
        for i in range(nx):
            p = idx(i, j, nx)

            if j == ny - 1:
                add(p, p, 1.0)
                b[p] = 0.0
                continue

            if j == 0 and elec[i]:
                add(p, p, 1.0)
                b[p] = 1.0
                continue

            cx = 2.0 / dx**2 if (i == 0 or i == nx - 1) else 1.0 / dx**2
            cy = 2.0 / dy**2 if (j == 0) else 1.0 / dy**2
            center = -(cx + cy + 1.0 / dx**2 + 1.0 / dy**2)

            if i == 0:
                add(p, idx(i + 1, j, nx), 2.0 / dx**2)
            elif i == nx - 1:
                add(p, idx(i - 1, j, nx), 2.0 / dx**2)
            else:
                add(p, idx(i - 1, j, nx), 1.0 / dx**2)
                add(p, idx(i + 1, j, nx), 1.0 / dx**2)

            if j == 0:
                add(p, idx(i, j + 1, nx), 2.0 / dy**2)
            else:
                add(p, idx(i, j - 1, nx), 1.0 / dy**2)
                add(p, idx(i, j + 1, nx), 1.0 / dy**2)

            add(p, p, center)

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))
    return x, y, A, b


def solve_unit_potential(cfg: CaseConfig):
    x, y, A, b = assemble_potential_system(cfg)
    phi = spsolve(A, b).reshape(cfg.ny, cfg.nx)
    return x, y, phi


def compute_unit_heat(phi: np.ndarray, cfg: CaseConfig, dx: float, dy: float) -> np.ndarray:
    dphi_dy, dphi_dx = np.gradient(phi, dy, dx)
    q_unit = cfg.sigma_S_per_m * (dphi_dx**2 + dphi_dy**2)
    return q_unit


def assemble_heat_stepper(cfg: CaseConfig):
    x, y, dx, dy = make_grid(cfg)
    nx, ny = cfg.nx, cfg.ny
    N = nx * ny
    rows, cols, vals = [], [], []
    rhs_bc = np.zeros(N)
    rho_c_dt = cfg.rho_kg_per_m3 * cfg.c_J_per_kgK / cfg.dt_s
    perf = cfg.perfusion_W_per_m3K
    k = cfg.k_W_per_mK
    h = cfg.cooling_h_W_per_m2K
    Tb = cfg.t_blood_C

    def add(r: int, c: int, v: float) -> None:
        rows.append(r)
        cols.append(c)
        vals.append(v)

    for j in range(ny):
        for i in range(nx):
            p = idx(i, j, nx)

            if i == 0 or i == nx - 1 or j == ny - 1:
                add(p, p, 1.0)
                rhs_bc[p] = Tb
                continue

            if j == 0:
                add(p, p, rho_c_dt + 2.0 * k / dy**2 + 2.0 * h / dy + perf)
                add(p, idx(i, j + 1, nx), -2.0 * k / dy**2)
                add(p, idx(i - 1, j, nx), -k / dx**2)
                add(p, idx(i + 1, j, nx), -k / dx**2)
                add(p, p, 2.0 * k / dx**2)
                rhs_bc[p] = (2.0 * h / dy + perf) * Tb
                continue

            add(p, p, rho_c_dt + 2.0 * k / dx**2 + 2.0 * k / dy**2 + perf)
            add(p, idx(i - 1, j, nx), -k / dx**2)
            add(p, idx(i + 1, j, nx), -k / dx**2)
            add(p, idx(i, j - 1, nx), -k / dy**2)
            add(p, idx(i, j + 1, nx), -k / dy**2)
            rhs_bc[p] = perf * Tb

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))
    solve = factorized(A.tocsc())
    return x, y, solve, rhs_bc


def run_case(cfg: CaseConfig) -> Dict[str, Any]:
    x, y, dx, dy = make_grid(cfg)
    _, _, phi = solve_unit_potential(cfg)
    q_unit = compute_unit_heat(phi, cfg, dx, dy)
    q = cfg.q_scale_W_per_m3_per_W * cfg.power_W * q_unit

    _, _, solve_heat, rhs_bc = assemble_heat_stepper(cfg)
    T = np.full((cfg.ny, cfg.nx), cfg.t_init_C, dtype=float)
    omega = np.zeros_like(T)
    peak_T = T.copy()
    steps = int(np.ceil(cfg.duration_s / cfg.dt_s))
    rho_c_dt = cfg.rho_kg_per_m3 * cfg.c_J_per_kgK / cfg.dt_s

    for _ in range(steps):
        rhs = rho_c_dt * T.ravel() + q.ravel() + rhs_bc
        for j in range(cfg.ny):
            rhs[idx(0, j, cfg.nx)] = cfg.t_blood_C
            rhs[idx(cfg.nx - 1, j, cfg.nx)] = cfg.t_blood_C
        for i in range(cfg.nx):
            rhs[idx(i, cfg.ny - 1, cfg.nx)] = cfg.t_blood_C
        T_new = solve_heat(rhs).reshape(cfg.ny, cfg.nx)
        T_new[:, 0] = cfg.t_blood_C
        T_new[:, -1] = cfg.t_blood_C
        T_new[-1, :] = cfg.t_blood_C

        temp_K = T_new + 273.15
        omega += cfg.arrhenius_A_1_per_s * np.exp(-cfg.arrhenius_Ea_J_per_mol / (R_GAS * temp_K)) * cfg.dt_s
        peak_T = np.maximum(peak_T, T_new)
        T = T_new

    lesion_mask = omega >= cfg.lesion_omega_threshold
    centerline = cfg.nx // 2
    lesion_depth_mm = 0.0
    if lesion_mask[:, centerline].any():
        lesion_depth_mm = 1e3 * y[np.where(lesion_mask[:, centerline])[0].max()]

    transmural = lesion_depth_mm >= cfg.wall_thickness_mm - 1e-6
    overheat_area_mm2 = (peak_T >= 100.0).sum() * dx * dy * 1e6

    return {
        "x_m": x,
        "y_m": y,
        "phi": phi,
        "q_unit": q_unit,
        "q": q,
        "peak_T_C": peak_T,
        "omega": omega,
        "lesion_mask": lesion_mask,
        "lesion_depth_mm": lesion_depth_mm,
        "transmural": bool(transmural),
        "overheat_area_mm2": float(overheat_area_mm2),
        "cfg": cfg,
    }


def summarize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    cfg: CaseConfig = result["cfg"]
    return {
        "power_W": float(cfg.power_W),
        "duration_s": float(cfg.duration_s),
        "wall_thickness_mm": float(cfg.wall_thickness_mm),
        "cooling_h_W_per_m2K": float(cfg.cooling_h_W_per_m2K),
        "nx": int(cfg.nx),
        "ny": int(cfg.ny),
        "dt_s": float(cfg.dt_s),
        "lesion_depth_mm": float(result["lesion_depth_mm"]),
        "depth_fraction": float(result["lesion_depth_mm"] / cfg.wall_thickness_mm),
        "transmural": bool(result["transmural"]),
        "overheat_area_mm2": float(result["overheat_area_mm2"]),
        "peak_temperature_C": float(np.max(result["peak_T_C"])),
    }


def plot_case(result: Dict[str, Any], outpath: str | Path) -> None:
    x = result["x_m"] * 1e3
    y = result["y_m"] * 1e3
    cfg: CaseConfig = result["cfg"]
    phi = result["phi"]
    peak_T = result["peak_T_C"]
    omega = result["omega"]
    depth = result["lesion_depth_mm"]

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.2), constrained_layout=True)

    im0 = axes[0].imshow(phi, extent=[x.min(), x.max(), y.max(), y.min()], aspect='auto')
    axes[0].set_title('Unit potential')
    axes[0].set_xlabel('x [mm]')
    axes[0].set_ylabel('depth [mm]')
    fig.colorbar(im0, ax=axes[0], shrink=0.8)

    im1 = axes[1].imshow(peak_T, extent=[x.min(), x.max(), y.max(), y.min()], aspect='auto')
    axes[1].set_title('Peak temperature [°C]')
    axes[1].set_xlabel('x [mm]')
    axes[1].set_ylabel('depth [mm]')
    fig.colorbar(im1, ax=axes[1], shrink=0.8)

    log_omega = np.log10(np.clip(omega, 1e-8, None))
    im2 = axes[2].imshow(log_omega, extent=[x.min(), x.max(), y.max(), y.min()], aspect='auto')
    axes[2].set_title('log10 Arrhenius Ω')
    axes[2].set_xlabel('x [mm]')
    axes[2].set_ylabel('depth [mm]')
    fig.colorbar(im2, ax=axes[2], shrink=0.8)

    fig.suptitle(
        f'{cfg.power_W:.0f} W / {cfg.duration_s:.0f} s | wall={cfg.wall_thickness_mm:.1f} mm | depth={depth:.2f} mm',
        fontsize=14,
    )
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def save_summary(result: Dict[str, Any], outpath: str | Path) -> None:
    Path(outpath).write_text(yaml.safe_dump(summarize_result(result), sort_keys=False))


def line_plot(df, x_col: str, y_col: str, group_col: str, title: str, xlabel: str, ylabel: str, outpath: str | Path):
    fig, ax = plt.subplots(figsize=(7.2, 4.6), constrained_layout=True)
    for name, g in df.groupby(group_col):
        g = g.sort_values(x_col)
        ax.plot(g[x_col], g[y_col], marker='o', label=name)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(frameon=False)
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def bool_heatmap(df, x_values: Iterable[float], y_values: Iterable[str], x_col: str, y_col: str, value_col: str, title: str, xlabel: str, ylabel: str, outpath: str | Path):
    x_vals = list(x_values)
    y_vals = list(y_values)
    mat = np.zeros((len(y_vals), len(x_vals)), dtype=float)
    for iy, yv in enumerate(y_vals):
        for ix, xv in enumerate(x_vals):
            row = df[(df[y_col] == yv) & (df[x_col] == xv)]
            if len(row):
                mat[iy, ix] = float(row.iloc[0][value_col])
    fig, ax = plt.subplots(figsize=(7.2, 3.6), constrained_layout=True)
    im = ax.imshow(mat, aspect='auto', origin='lower')
    ax.set_xticks(range(len(x_vals)), labels=[str(v) for v in x_vals])
    ax.set_yticks(range(len(y_vals)), labels=list(y_vals))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    for iy in range(len(y_vals)):
        for ix in range(len(x_vals)):
            ax.text(ix, iy, f'{mat[iy, ix]:.0f}', ha='center', va='center', fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.85)
    fig.savefig(outpath, dpi=180)
    plt.close(fig)
