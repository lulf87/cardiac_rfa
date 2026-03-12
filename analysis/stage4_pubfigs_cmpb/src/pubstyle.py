
from pathlib import Path
import matplotlib.pyplot as plt

SINGLE_COL_IN = 3.54   # ~90 mm
DOUBLE_COL_IN = 7.20   # ~183 mm

PROTOCOL_LABELS = {
    "standard_30W_30s": "Standard 30 W / 30 s",
    "hpsd_50W_10s": "HPSD 50 W / 10 s",
    "vhpsd_90W_4s": "vHPSD 90 W / 4 s",
}
PROTOCOL_SHORT = {
    "standard_30W_30s": "Standard",
    "hpsd_50W_10s": "HPSD",
    "vhpsd_90W_4s": "vHPSD",
}
PROTOCOL_COLORS = {
    "standard_30W_30s": "#1b9e77",
    "hpsd_50W_10s": "#7570b3",
    "vhpsd_90W_4s": "#d95f02",
}
PROTOCOL_MARKERS = {
    "standard_30W_30s": "o",
    "hpsd_50W_10s": "s",
    "vhpsd_90W_4s": "^",
}

def use_pub_style():
    plt.rcParams.update({
        "font.size": 8.5,
        "axes.titlesize": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 10,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.6,
        "lines.markersize": 4.5,
        "savefig.dpi": 600,
        "figure.dpi": 160,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })

def panel_label(ax, label):
    ax.text(
        -0.16, 1.04, label, transform=ax.transAxes,
        fontsize=10, fontweight="bold", va="bottom", ha="left"
    )

def save_figure(fig, outbase):
    outbase = Path(outbase)
    outbase.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outbase.with_suffix(".png"), bbox_inches="tight")
    fig.savefig(outbase.with_suffix(".pdf"), bbox_inches="tight")
