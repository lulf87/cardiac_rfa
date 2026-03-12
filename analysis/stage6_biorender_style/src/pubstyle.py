from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

SINGLE_COL_IN = 3.54
DOUBLE_COL_IN = 7.20

CANVAS = "#FBFAF7"
WHITE = "#FFFFFF"
TEXT = "#344054"
MUTED = "#667085"
SLATE = "#5F6F7B"
SLATE_DARK = "#44515B"
CHIP = "#EEF2F6"
GRID = "#D7DCE2"
BORDER = "#CBD5E1"
GOOD = "#DCEFE7"
GOOD_EDGE = "#8ABFA9"

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
    "standard_30W_30s": "#2A9D8F",
    "hpsd_50W_10s": "#8A7FB9",
    "vhpsd_90W_4s": "#E07A5F",
}
PROTOCOL_CHIPS = {
    "standard_30W_30s": "#DCEFE7",
    "hpsd_50W_10s": "#ECE8F6",
    "vhpsd_90W_4s": "#F8E2DA",
}
PROTOCOL_MARKERS = {
    "standard_30W_30s": "o",
    "hpsd_50W_10s": "s",
    "vhpsd_90W_4s": "^",
}
WALL_COLORS = {
    2.0: "#5BC0A7",
    3.0: "#95C65A",
    4.0: "#E9C46A",
    5.0: "#D69A6A",
    6.0: "#C76D5B",
}

TRANSMURAL_CMAP = LinearSegmentedColormap.from_list(
    "transmural_soft", ["#2E3A4B", "#6D7E95", "#77C8A3", "#F1C85C"]
)
OVERHEAT_CMAP = LinearSegmentedColormap.from_list(
    "overheat_soft", ["#231C2F", "#6F3B7F", "#DA6A6A", "#F4D4A2"]
)
DEPTH_CMAP = LinearSegmentedColormap.from_list(
    "depth_soft", ["#244C7A", "#6C7A89", "#B2AA8D", "#E2C86A", "#F4E56B"]
)

COOLING_TITLES = {
    800: "Weak cooling",
    1500: "Nominal cooling",
    2500: "Strong cooling",
}


def use_pub_style():
    plt.style.use("default")
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.titlesize": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "figure.titlesize": 10,
        "text.color": TEXT,
        "axes.labelcolor": TEXT,
        "axes.edgecolor": SLATE_DARK,
        "xtick.color": TEXT,
        "ytick.color": TEXT,
        "axes.linewidth": 0.9,
        "axes.facecolor": WHITE,
        "figure.facecolor": CANVAS,
        "savefig.facecolor": CANVAS,
        "savefig.transparent": False,
        "lines.linewidth": 2.0,
        "lines.markersize": 5.5,
        "savefig.dpi": 600,
        "figure.dpi": 170,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.color": GRID,
        "grid.alpha": 0.55,
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",
        "legend.frameon": True,
        "legend.fancybox": True,
        "legend.framealpha": 1.0,
        "legend.edgecolor": BORDER,
        "legend.facecolor": WHITE,
    })


def panel_label(ax, label):
    ax.text(-0.16, 1.06, label, transform=ax.transAxes, fontsize=11, fontweight="bold", color="black", va="bottom", ha="left")


def title_chip(ax, text, facecolor=SLATE, textcolor="white"):
    ax.set_title(text, pad=10, color=textcolor, bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.16", fc=facecolor, ec="none"))


def row_chip(ax, text, facecolor, x=-0.26):
    ax.annotate(text, xy=(x, 0.5), xycoords="axes fraction", rotation=90,
                va="center", ha="center", fontsize=8.6, fontweight="semibold",
                color=TEXT, bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.18", fc=facecolor, ec="none"))


def soft_legend(legend):
    if legend is None:
        return
    frame = legend.get_frame()
    frame.set_facecolor(WHITE)
    frame.set_edgecolor(BORDER)
    frame.set_linewidth(0.8)


def save_figure(fig, outbase):
    outbase = Path(outbase)
    outbase.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outbase.with_suffix('.png'), bbox_inches='tight')
    fig.savefig(outbase.with_suffix('.pdf'), bbox_inches='tight')
