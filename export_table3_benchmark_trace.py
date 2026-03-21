#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from docx import Document
import pandas as pd


DEFAULT_DOCX = Path("papers/V13/CMBBE_RF_ablation_reduced_model_main.docx")
DEFAULT_CURRENT_BENCHMARK = Path("analysis/stage8_finish_ready/example_data/benchmark_points.csv")
DEFAULT_DUPLICATE_CURRENT_BENCHMARK = Path("manuscript/example_data/benchmark_points_v2.csv")
DEFAULT_HISTORICAL_WIDTHS = Path("papers/V7/tables/source_csv/benchmark_points_v3.csv")
DEFAULT_OUTDIR = Path("tmp/table_exports")


PROTOCOL_KEY_MAP = {
    "Standard RF": "standard_30W_30s",
    "HPSD": "hpsd_50W_10s",
    "90 W / 4 s fixed-power reference": "vhpsd_90W_4s",
}


def read_docx_table3(docx_path: Path) -> list[dict[str, str]]:
    doc = Document(docx_path)
    table = doc.tables[2]
    header = [cell.text.strip() for cell in table.rows[0].cells]
    rows = []
    for row in table.rows[1:]:
        values = [cell.text.strip() for cell in row.cells]
        rows.append(dict(zip(header, values)))
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "| protocol_key | reported_depth_mm | reported_depth_status | simulated_depth_mm | simulated_depth_status | reported_width_mm | reported_width_status | simulated_width_mm | simulated_width_status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {protocol_key} | {reported_depth_mm} | {reported_depth_status} | {simulated_depth_mm} | {simulated_depth_status} | {reported_width_mm} | {reported_width_status} | {simulated_width_mm} | {simulated_width_status} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines))


def matches_or_not_found(value: str, series_value: float | int | None) -> bool:
    if series_value is None or pd.isna(series_value):
        return False
    value_text = str(value).strip()
    if "." in value_text:
        decimals = len(value_text.split(".", 1)[1])
        tolerance = 0.5 * (10 ** (-decimals)) + 1e-12
    else:
        tolerance = 0.5 + 1e-12
    return abs(float(value) - float(series_value)) <= tolerance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docx", default=str(DEFAULT_DOCX))
    parser.add_argument("--current-benchmark", default=str(DEFAULT_CURRENT_BENCHMARK))
    parser.add_argument("--current-benchmark-duplicate", default=str(DEFAULT_DUPLICATE_CURRENT_BENCHMARK))
    parser.add_argument("--historical-widths", default=str(DEFAULT_HISTORICAL_WIDTHS))
    parser.add_argument("--outdir", default=str(DEFAULT_OUTDIR))
    args = parser.parse_args()

    docx_rows = read_docx_table3(Path(args.docx))
    current_df = pd.read_csv(args.current_benchmark)
    duplicate_df = pd.read_csv(args.current_benchmark_duplicate)
    historical_df = pd.read_csv(args.historical_widths)

    rows: list[dict[str, str]] = []
    for docx_row in docx_rows:
        protocol_display = docx_row["Protocol"]
        protocol_key = PROTOCOL_KEY_MAP[protocol_display]
        current_row = current_df[current_df["protocol_key"] == protocol_key].iloc[0]
        duplicate_row = duplicate_df[duplicate_df["protocol_key"] == protocol_key].iloc[0]
        historical_row = historical_df[historical_df["protocol_key"] == protocol_key].iloc[0]

        current_source = args.current_benchmark
        duplicate_note = f"duplicate current benchmark: {args.current_benchmark_duplicate}"
        historical_source = (
            f"{args.historical_widths}; identical duplicates at "
            "papers/V6/tables/source_csv/benchmark_points_v3.csv and "
            "papers/V7/tables/main/table3_literature_benchmark_points.csv"
        )

        reported_depth_status = "AUTO" if matches_or_not_found(docx_row["Reported depth (mm)"], current_row["reported_depth_mm"]) else "MANUAL"
        simulated_depth_status = "AUTO" if matches_or_not_found(docx_row["Simulated depth (mm)"], current_row["simulated_depth_mm"]) else "MANUAL"
        reported_width_status = "AUTO" if matches_or_not_found(docx_row["Reported width (mm)"], current_row["reported_width_mm"]) else "MANUAL"
        simulated_width_status = "HISTORICAL_TRACE" if matches_or_not_found(docx_row["Simulated width (mm)"], historical_row["simulated_width_mm"]) else "MANUAL"

        rows.append(
            {
                "manuscript_source_label": docx_row["Source / matched point"],
                "manuscript_source_label_status": "MANUAL",
                "manuscript_source_label_source": f"{args.docx} :: Table 3",
                "manuscript_protocol_label": protocol_display,
                "manuscript_protocol_label_status": "MANUAL",
                "manuscript_protocol_label_source": f"{args.docx} :: Table 3",
                "protocol_key": protocol_key,
                "reported_depth_mm": docx_row["Reported depth (mm)"],
                "reported_depth_status": reported_depth_status,
                "reported_depth_source_file": current_source if reported_depth_status == "AUTO" else f"MANUAL :: {args.docx} :: Table 3",
                "simulated_depth_mm": docx_row["Simulated depth (mm)"],
                "simulated_depth_status": simulated_depth_status,
                "simulated_depth_source_file": current_source if simulated_depth_status == "AUTO" else f"MANUAL :: {args.docx} :: Table 3",
                "reported_width_mm": docx_row["Reported width (mm)"],
                "reported_width_status": reported_width_status,
                "reported_width_source_file": current_source if reported_width_status == "AUTO" else f"MANUAL :: {args.docx} :: Table 3",
                "simulated_width_mm": docx_row["Simulated width (mm)"],
                "simulated_width_status": simulated_width_status,
                "simulated_width_source_file": historical_source if simulated_width_status == "HISTORICAL_TRACE" else f"MANUAL :: {args.docx} :: Table 3",
                "notes": duplicate_note,
            }
        )

    outdir = Path(args.outdir)
    csv_path = outdir / "table3_benchmark_trace.csv"
    md_path = outdir / "table3_benchmark_trace.md"
    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(csv_path, rows, fieldnames)
    write_md(md_path, rows)
    print(f"Saved {csv_path}")
    print(f"Saved {md_path}")


if __name__ == "__main__":
    main()
