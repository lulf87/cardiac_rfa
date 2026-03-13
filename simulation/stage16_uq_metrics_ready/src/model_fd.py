from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Iterable

import numpy as np
from scipy import sparse
from scipy.ndimage import gaussian_filter
from scipy.sparse.linalg import factorized, spsolve
import yaml
import matplotlib.pyplot as plt

R_GAS = 8.314462618  # J/(mol K)


@dataclass
class CaseConfig:
    # Geometry
    width_mm: float = 18.0
    wall_thickness_mm: float = 4.0
    bottom_buffer_mm: float = 4.0
    nx: int = 281
    ny: int = 141
    electrode_width_mm: float = 2.0

    # Protocol
    power_W: float = 50.0
    duration_s: float = 10.0
    dt_s: float = 0.05

    # Tissue / thermal parameters
    t_init_C: float = 37.0
    t_blood_C: float = 37.0
    sigma_S_per_m: float = 0.6
    k_W_per_mK: float = 0.55
    rho_kg_per_m3: float = 1050.0
    c_J_per_kgK: float = 3600.0
    perfusion_W_per_m3K: float = 0.0
    cooling_h_W_per_m2K: float = 1500.0

    # Source regularization / scaling
    power_per_depth_scale_W_per_m_per_W: float = 6.8
    source_smoothing_mm: float = 0.20

    # Contact surrogate (deterministic placeholder for next stage)
    insertion_depth_mm: float = 1.0
    reference_insertion_mm: float = 1.0
    contact_power_gain_per_mm: float = 0.16
    contact_h_reduction_per_mm: float = 0.35
    min_contact_h_scale: float = 0.50
    max_contact_h_scale: float = 1.40
    source_shift_per_mm_insertion: float = 0.25

    # Damage model
    arrhenius_A_1_per_s: float = 7.39e39
    arrhenius_Ea_J_per_mol: float = 2.577e5
    lesion_omega_threshold: float = 1.0

    @staticmethod
    def from_yaml(path: str | Path) -> "CaseConfig":
        raw = yaml.safe_load(Path(path).read_text())
        data: Dict[str, Any] = {}
        for key, value in raw.items():
            if key in {"nx", "ny"}:
                data[key] = int(value)
            else:
                data[key] = float(value)
        return CaseConfig(**data)

    @property
    def domain_depth_mm(self) -> float:
        return self.wall_thickness_mm + self.bottom_buffer_mm



def physical_wall_mask(y: np.ndarray, cfg: CaseConfig) -> np.ndarray:
    return y <= (cfg.wall_thickness_mm * 1e-3 + 1e-12)


def clone_cfg(cfg: CaseConfig, **kwargs: float | int) -> CaseConfig:
    data = dict(cfg.__dict__)
    data.update(kwargs)
    return CaseConfig(**data)


def rescale_ny(base_cfg: CaseConfig, wall_thickness_mm: float) -> int:
    old_total = base_cfg.wall_thickness_mm + base_cfg.bottom_buffer_mm
    new_total = wall_thickness_mm + base_cfg.bottom_buffer_mm
    ratio = new_total / old_total
    ny = int(round((base_cfg.ny - 1) * ratio)) + 1
    return max(41, ny)


def make_grid(cfg: CaseConfig):
    x = np.linspace(-0.5 * cfg.width_mm * 1e-3, 0.5 * cfg.width_mm * 1e-3, cfg.nx)
    y = np.linspace(0.0, cfg.domain_depth_mm * 1e-3, cfg.ny)
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

            # Laplace with insulated sides and insulated non-electrode top.
            diag = 0.0

            # x-direction
            if i == 0:
                add(p, idx(i + 1, j, nx), 2.0 / dx**2)
                diag -= 2.0 / dx**2
            elif i == nx - 1:
                add(p, idx(i - 1, j, nx), 2.0 / dx**2)
                diag -= 2.0 / dx**2
            else:
                add(p, idx(i - 1, j, nx), 1.0 / dx**2)
                add(p, idx(i + 1, j, nx), 1.0 / dx**2)
                diag -= 2.0 / dx**2

            # y-direction
            if j == 0:
                add(p, idx(i, j + 1, nx), 2.0 / dy**2)
                diag -= 2.0 / dy**2
            else:
                add(p, idx(i, j - 1, nx), 1.0 / dy**2)
                add(p, idx(i, j + 1, nx), 1.0 / dy**2)
                diag -= 2.0 / dy**2

            add(p, p, diag)

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


def shift_source_in_depth(q_reg: np.ndarray, shift_m: float, y: np.ndarray) -> np.ndarray:
    if abs(shift_m) < 1e-12:
        return q_reg.copy()
    ny, nx = q_reg.shape
    out = np.zeros_like(q_reg)
    for i in range(nx):
        out[:, i] = np.interp(y - shift_m, y, q_reg[:, i], left=q_reg[0, i], right=0.0)
    return out


def regularize_and_scale_heat_source(q_unit: np.ndarray, cfg: CaseConfig, x: np.ndarray, y: np.ndarray, dx: float, dy: float) -> np.ndarray:
    if cfg.source_smoothing_mm > 0.0:
        sigma_x = (cfg.source_smoothing_mm * 1e-3) / dx
        sigma_y = (cfg.source_smoothing_mm * 1e-3) / dy
        q_reg = gaussian_filter(q_unit, sigma=(sigma_y, sigma_x), mode="nearest")
    else:
        q_reg = q_unit.copy()

    insertion_delta = cfg.insertion_depth_mm - cfg.reference_insertion_mm
    shift_m = cfg.source_shift_per_mm_insertion * cfg.insertion_depth_mm * 1e-3
    q_reg = shift_source_in_depth(q_reg, shift_m=shift_m, y=y)

    total_per_depth = float(np.sum(q_reg) * dx * dy)
    if total_per_depth <= 0.0:
        raise ValueError("Regularized source has non-positive integral.")

    contact_scale = max(0.5, 1.0 + cfg.contact_power_gain_per_mm * insertion_delta)
    q = cfg.power_per_depth_scale_W_per_m_per_W * cfg.power_W * contact_scale * q_reg / total_per_depth
    return q


def top_h_profile(cfg: CaseConfig, x: np.ndarray) -> np.ndarray:
    h_top = np.full_like(x, cfg.cooling_h_W_per_m2K, dtype=float)
    elec = electrode_mask(x, cfg)
    insertion_delta = cfg.insertion_depth_mm - cfg.reference_insertion_mm
    scale = 1.0 - cfg.contact_h_reduction_per_mm * insertion_delta
    scale = float(np.clip(scale, cfg.min_contact_h_scale, cfg.max_contact_h_scale))
    h_top[elec] = cfg.cooling_h_W_per_m2K * scale
    return h_top


def assemble_heat_stepper(cfg: CaseConfig):
    x, y, dx, dy = make_grid(cfg)
    nx, ny = cfg.nx, cfg.ny
    N = nx * ny
    rows, cols, vals = [], [], []
    rhs_bc = np.zeros(N)

    rho_c_dt = cfg.rho_kg_per_m3 * cfg.c_J_per_kgK / cfg.dt_s
    perf = cfg.perfusion_W_per_m3K
    k = cfg.k_W_per_mK
    Tb = cfg.t_blood_C
    h_top = top_h_profile(cfg, x)

    def add(r: int, c: int, v: float) -> None:
        rows.append(r)
        cols.append(c)
        vals.append(v)

    for j in range(ny):
        for i in range(nx):
            p = idx(i, j, nx)
            h = float(h_top[i]) if j == 0 else 0.0
            diag = rho_c_dt + perf
            rhs_extra = perf * Tb

            # x-direction (insulated side boundaries)
            if i == 0:
                add(p, idx(i + 1, j, nx), -2.0 * k / dx**2)
                diag += 2.0 * k / dx**2
            elif i == nx - 1:
                add(p, idx(i - 1, j, nx), -2.0 * k / dx**2)
                diag += 2.0 * k / dx**2
            else:
                add(p, idx(i - 1, j, nx), -k / dx**2)
                add(p, idx(i + 1, j, nx), -k / dx**2)
                diag += 2.0 * k / dx**2

            # y-direction
            if j == 0:
                # Robin: k dT/dy = h (T - Tb)
                add(p, idx(i, j + 1, nx), -2.0 * k / dy**2)
                diag += 2.0 * k / dy**2 + 2.0 * h / dy
                rhs_extra += 2.0 * h / dy * Tb
            elif j == ny - 1:
                # insulated bottom
                add(p, idx(i, j - 1, nx), -2.0 * k / dy**2)
                diag += 2.0 * k / dy**2
            else:
                add(p, idx(i, j - 1, nx), -k / dy**2)
                add(p, idx(i, j + 1, nx), -k / dy**2)
                diag += 2.0 * k / dy**2

            add(p, p, diag)
            rhs_bc[p] = rhs_extra

    A = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N))
    solve = factorized(A.tocsc())
    return x, y, solve, rhs_bc



def interpolate_lesion_depth_mm(
    omega: np.ndarray,
    y_m: np.ndarray,
    threshold: float,
    centerline: int,
    wall_thickness_mm: float,
) -> float:
    wall_m = wall_thickness_mm * 1e-3
    valid = y_m <= wall_m + 1e-12
    y_use = y_m[valid]
    line = omega[valid, centerline]

    if len(y_use) == 0:
        return 0.0

    # Already transmural inside the physical wall.
    if line[-1] >= threshold:
        return wall_thickness_mm

    above = np.where(line >= threshold)[0]
    if len(above) == 0:
        return 0.0

    j = int(above.max())
    if j >= len(y_use) - 1:
        return min(wall_thickness_mm, 1e3 * float(y_use[j]))

    om0 = float(line[j])
    om1 = float(line[j + 1])
    y0 = float(y_use[j])
    y1 = float(y_use[j + 1])
    if om0 == om1:
        y_star = y0
    else:
        alpha = (threshold - om0) / (om1 - om0)
        alpha = float(np.clip(alpha, 0.0, 1.0))
        y_star = y0 + alpha * (y1 - y0)
    return min(wall_thickness_mm, 1e3 * y_star)




def _interp_crossing_x_mm(line: np.ndarray, x_mm: np.ndarray, threshold: float, i0: int, i1: int) -> float:
    v0 = float(line[i0])
    v1 = float(line[i1])
    x0 = float(x_mm[i0])
    x1 = float(x_mm[i1])
    if abs(v1 - v0) < 1e-15:
        return x0
    alpha = (threshold - v0) / (v1 - v0)
    alpha = float(np.clip(alpha, 0.0, 1.0))
    return x0 + alpha * (x1 - x0)


def compute_max_lesion_width_mm(omega: np.ndarray, x_m: np.ndarray, y_m: np.ndarray, threshold: float, wall_thickness_mm: float) -> float:
    x_mm = x_m * 1e3
    y_mm = y_m * 1e3
    width_max = 0.0
    valid_rows = np.where(y_mm <= wall_thickness_mm + 1e-12)[0]
    center = len(x_mm) // 2
    for j in valid_rows:
        line = omega[j, :]
        above = np.where(line >= threshold)[0]
        if len(above) == 0:
            continue
        left = int(above.min())
        right = int(above.max())
        # keep the central connected lesion branch if multiple islands occur
        if not (left <= center <= right):
            # choose component closest to center
            comps = []
            start = above[0]
            prev = above[0]
            for idx in above[1:]:
                if idx == prev + 1:
                    prev = idx
                else:
                    comps.append((start, prev))
                    start = idx
                    prev = idx
            comps.append((start, prev))
            left, right = min(comps, key=lambda ab: abs((ab[0] + ab[1]) / 2 - center))
        x_left = float(x_mm[left])
        x_right = float(x_mm[right])
        if left > 0:
            x_left = _interp_crossing_x_mm(line, x_mm, threshold, left - 1, left)
        if right < len(x_mm) - 1:
            x_right = _interp_crossing_x_mm(line, x_mm, threshold, right, right + 1)
        width_max = max(width_max, x_right - x_left)
    return float(max(width_max, 0.0))


def compute_lesion_area_mm2(lesion_mask: np.ndarray, dx: float, dy: float) -> float:
    return float(lesion_mask.sum() * dx * dy * 1e6)


def run_case(cfg: CaseConfig) -> Dict[str, Any]:
    x, y, dx, dy = make_grid(cfg)
    _, _, phi = solve_unit_potential(cfg)
    q_unit = compute_unit_heat(phi, cfg, dx, dy)
    q = regularize_and_scale_heat_source(q_unit, cfg, x, y, dx, dy)

    _, _, solve_heat, rhs_bc = assemble_heat_stepper(cfg)
    T = np.full((cfg.ny, cfg.nx), cfg.t_init_C, dtype=float)
    omega = np.zeros_like(T)
    peak_T = T.copy()
    steps = int(np.ceil(cfg.duration_s / cfg.dt_s))
    rho_c_dt = cfg.rho_kg_per_m3 * cfg.c_J_per_kgK / cfg.dt_s
    wall_mask_1d = physical_wall_mask(y, cfg)
    wall_mask_2d = np.repeat(wall_mask_1d[:, None], cfg.nx, axis=1)

    for _ in range(steps):
        rhs = rho_c_dt * T.ravel() + q.ravel() + rhs_bc
        T_new = solve_heat(rhs).reshape(cfg.ny, cfg.nx)
        temp_K = T_new + 273.15
        d_omega = cfg.arrhenius_A_1_per_s * np.exp(-cfg.arrhenius_Ea_J_per_mol / (R_GAS * temp_K)) * cfg.dt_s
        omega += d_omega * wall_mask_2d
        peak_T = np.maximum(peak_T, T_new)
        T = T_new

    omega_report = np.where(wall_mask_2d, omega, 0.0)
    peak_T_report = np.where(wall_mask_2d, peak_T, cfg.t_init_C)
    lesion_mask = omega_report >= cfg.lesion_omega_threshold
    centerline = cfg.nx // 2
    lesion_depth_mm = interpolate_lesion_depth_mm(
        omega_report,
        y,
        cfg.lesion_omega_threshold,
        centerline,
        cfg.wall_thickness_mm,
    )
    lesion_width_mm = compute_max_lesion_width_mm(
        omega_report, x, y, cfg.lesion_omega_threshold, cfg.wall_thickness_mm
    )
    lesion_area_mm2 = compute_lesion_area_mm2(lesion_mask, dx, dy)
    transmural = lesion_depth_mm >= cfg.wall_thickness_mm - 1e-6
    overheat_area_mm2 = float((peak_T_report >= 100.0).sum() * dx * dy * 1e6)

    return {
        "x_m": x,
        "y_m": y,
        "phi": phi,
        "q_unit": q_unit,
        "q": q,
        "peak_T_C": peak_T_report,
        "omega": omega_report,
        "lesion_mask": lesion_mask,
        "lesion_depth_mm": float(lesion_depth_mm),
        "lesion_width_mm": float(lesion_width_mm),
        "lesion_area_mm2": float(lesion_area_mm2),
        "depth_to_width_ratio": float(lesion_depth_mm / lesion_width_mm) if lesion_width_mm > 1e-12 else float("nan"),
        "transmural": bool(transmural),
        "overheat_area_mm2": overheat_area_mm2,
        "cfg": cfg,
    }


def summarize_result(result: Dict[str, Any]) -> Dict[str, Any]:
    cfg: CaseConfig = result["cfg"]
    return {
        "power_W": float(cfg.power_W),
        "duration_s": float(cfg.duration_s),
        "wall_thickness_mm": float(cfg.wall_thickness_mm),
        "bottom_buffer_mm": float(cfg.bottom_buffer_mm),
        "cooling_h_W_per_m2K": float(cfg.cooling_h_W_per_m2K),
        "insertion_depth_mm": float(cfg.insertion_depth_mm),
        "nx": int(cfg.nx),
        "ny": int(cfg.ny),
        "dt_s": float(cfg.dt_s),
        "source_smoothing_mm": float(cfg.source_smoothing_mm),
        "lesion_depth_mm": float(result["lesion_depth_mm"]),
        "lesion_width_mm": float(result["lesion_width_mm"]),
        "lesion_area_mm2": float(result["lesion_area_mm2"]),
        "depth_to_width_ratio": float(result["depth_to_width_ratio"]),
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

    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.4), constrained_layout=True)

    im0 = axes[0].imshow(phi, extent=[x.min(), x.max(), y.max(), y.min()], aspect='auto')
    axes[0].set_title('Unit potential')
    axes[0].set_xlabel('x [mm]')
    axes[0].set_ylabel('depth [mm]')
    fig.colorbar(im0, ax=axes[0], shrink=0.8)

    im1 = axes[1].imshow(peak_T, extent=[x.min(), x.max(), y.max(), y.min()], aspect='auto')
    axes[1].axhline(cfg.wall_thickness_mm, linestyle='--', linewidth=1)
    axes[1].set_title('Peak temperature [°C]')
    axes[1].set_xlabel('x [mm]')
    axes[1].set_ylabel('depth [mm]')
    fig.colorbar(im1, ax=axes[1], shrink=0.8)

    log_omega = np.log10(np.clip(omega, 1e-8, None))
    im2 = axes[2].imshow(log_omega, extent=[x.min(), x.max(), y.max(), y.min()], aspect='auto')
    axes[2].axhline(cfg.wall_thickness_mm, linestyle='--', linewidth=1)
    axes[2].set_title('log10 Arrhenius Ω')
    axes[2].set_xlabel('x [mm]')
    axes[2].set_ylabel('depth [mm]')
    fig.colorbar(im2, ax=axes[2], shrink=0.8)

    fig.suptitle(
        f'{cfg.power_W:.0f} W / {cfg.duration_s:.0f} s | wall={cfg.wall_thickness_mm:.1f} mm | ' 
        f'insert={cfg.insertion_depth_mm:.2f} mm | depth={depth:.2f} mm | width={result["lesion_width_mm"]:.2f} mm',
        fontsize=13,
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
    fig, ax = plt.subplots(figsize=(7.4, 3.8), constrained_layout=True)
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
