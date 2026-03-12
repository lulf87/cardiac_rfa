from pathlib import Path
import pandas as pd


def read_csv(path):
    return pd.read_csv(Path(path))


def protocol_order():
    return ["standard_30W_30s", "hpsd_50W_10s", "vhpsd_90W_4s"]


def prob_show_label(val, eps=1e-9):
    return (val > 0.0 + eps) and (val < 1.0 - eps)
