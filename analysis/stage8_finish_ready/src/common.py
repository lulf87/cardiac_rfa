
from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple
import yaml
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "styles" / "cardiac_biorender_light.mplstyle"
PALETTE_YAML = ROOT / "styles" / "palette.yaml"

PROTOCOL_ORDER = ["standard_30W_30s", "hpsd_50W_10s", "vhpsd_90W_4s"]
PROTOCOL_DISPLAY = {
    "standard_30W_30s": "Standard",
    "hpsd_50W_10s": "HPSD",
    "vhpsd_90W_4s": "vHPSD",
}
PROTOCOL_SHORT = {
    "standard_30W_30s": "Standard",
    "hpsd_50W_10s": "HPSD",
    "vhpsd_90W_4s": "vHPSD",
}
PROTOCOL_MARKER = {
    "standard_30W_30s": "o",
    "hpsd_50W_10s": "s",
    "vhpsd_90W_4s": "^",
}
PROTOCOL_LINESTYLE = {
    "standard_30W_30s": "-",
    "hpsd_50W_10s": "-",
    "vhpsd_90W_4s": "-",
}


def load_palette() -> Dict:
    return yaml.safe_load(PALETTE_YAML.read_text())


def apply_style() -> Dict:
    plt.style.use(str(STYLE))
    pal = load_palette()
    plt.rcParams.update({
        "figure.facecolor": pal["background"],
        "axes.facecolor": pal["axes_face"],
        "axes.edgecolor": pal["spine"],
        "axes.labelcolor": pal["text"],
        "xtick.color": pal["text"],
        "ytick.color": pal["text"],
        "text.color": pal["text"],
        "grid.color": pal["grid"],
        "axes.titlepad": 10,
    })
    return pal


def protocol_color(pal: Dict, key: str) -> str:
    return pal["protocol"][key]


def wall_color(pal: Dict, wall_mm: float) -> str:
    return pal["wall"][f"{float(wall_mm):.1f}"]


def wall_label_color(pal: Dict, wall_mm: float) -> str:
    return pal["wall_label"][f"{float(wall_mm):.1f}"]


def add_chip(ax, text: str, fontsize: int = 11) -> None:
    pal = load_palette()
    ax.text(
        0.5, 1.06, text,
        transform=ax.transAxes,
        ha="center", va="bottom",
        fontsize=fontsize,
        color=pal["chip_text"],
        bbox=dict(
            boxstyle="round,pad=0.28,rounding_size=0.18",
            fc=pal["chip"], ec="none"
        ),
    )


def add_row_label(fig, x: float, y: float, text: str, fc: str, rotation: int = 90, fontsize: int = 11):
    fig.text(
        x, y, text,
        ha="center", va="center",
        rotation=rotation,
        fontsize=fontsize, weight="semibold",
        bbox=dict(boxstyle="round,pad=0.26,rounding_size=0.18", fc=fc, ec="none")
    )


def save_pdf_png(fig, outbase: Path, png_dpi: int = 600, tiff_dpi: int = 600) -> None:
    outbase.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outbase.with_suffix(".pdf"), bbox_inches="tight", facecolor=fig.get_facecolor())
    fig.savefig(outbase.with_suffix(".png"), dpi=png_dpi, bbox_inches="tight", facecolor=fig.get_facecolor())
    fig.savefig(outbase.with_suffix(".tiff"), dpi=tiff_dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor(), pil_kwargs={"compression": "tiff_lzw"})


def panel_label(ax, label: str):
    ax.text(-0.14, 1.09, label, transform=ax.transAxes, fontsize=16, fontweight="bold", ha="left", va="bottom")


def force_white_grid(ax, alpha: float = 0.55):
    ax.grid(True, color="white", alpha=alpha, linewidth=1.2)


def final_size_note() -> str:
    return "Exported as PDF + PNG (600 dpi preview). Use PDF for submission when possible."
