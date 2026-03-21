#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import yaml
from docx import Document


DEFAULT_BASELINE = Path("simulation/stage17_controlled_rebuild/configs/baseline_90W_4s_4mm.yaml")
DEFAULT_PROTOCOLS = Path("simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml")
DEFAULT_CONTROLLER = Path("simulation/stage17_controlled_rebuild/configs/controller_selected_stage17.yaml")
DEFAULT_LATENCY = Path("simulation/stage17_controlled_rebuild/configs/latency_enabled.yaml")
DEFAULT_PHASE = Path("simulation/stage17_controlled_rebuild/configs/phase_prep_stage17_fourway.yaml")
DEFAULT_DOCX = Path("papers/V13/CMBBE_RF_ablation_reduced_model_main.docx")
DEFAULT_OUTDIR = Path("tmp/table_exports")


def read_docx_table2(docx_path: Path) -> dict[str, str]:
    doc = Document(docx_path)
    table = doc.tables[1]
    data: dict[str, str] = {}
    for row in table.rows[1:]:
        cells = [cell.text.strip() for cell in row.cells]
        if len(cells) >= 2:
            data[cells[0]] = cells[1]
    return data


def format_number(value: float, decimals: int = 1) -> str:
    fmt = f"{{value:.{decimals}f}}"
    return fmt.format(value=value)


def join_float_list(values: list[float], suffix: str) -> str:
    return ", ".join(format_number(float(v), 1) for v in values) + f" {suffix}"


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "| Item | exported_value | status | source_file | manuscript_value | matches_manuscript |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {item} | {exported_value} | {status} | {source_file} | {manuscript_value} | {matches_manuscript} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines))


def add_row(rows: list[dict[str, str]], item: str, exported_value: str, status: str, source_file: str, manuscript_map: dict[str, str], notes: str = "") -> None:
    manuscript_value = manuscript_map.get(item, "NOT FOUND")
    matches = "YES" if manuscript_value == exported_value else "NO"
    rows.append(
        {
            "item": item,
            "exported_value": exported_value,
            "status": status,
            "source_file": source_file,
            "manuscript_value": manuscript_value,
            "matches_manuscript": matches,
            "notes": notes,
        }
    )


def protocol_display_from_config(protocol: dict[str, object], protocol_rows: list[dict[str, object]]) -> str:
    power = int(float(protocol["power_W"]))
    duration = int(float(protocol["duration_s"]))
    use_controller = bool(protocol.get("use_controller", False))
    same_pair = [
        row
        for row in protocol_rows
        if int(float(row["power_W"])) == power and int(float(row["duration_s"])) == duration
    ]
    if use_controller:
        return f"{power} W / {duration} s temperature-limited"
    if len(same_pair) > 1:
        return f"{power} W / {duration} s fixed"
    return f"{power} W / {duration} s"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", default=str(DEFAULT_BASELINE))
    parser.add_argument("--protocols", default=str(DEFAULT_PROTOCOLS))
    parser.add_argument("--controller", default=str(DEFAULT_CONTROLLER))
    parser.add_argument("--latency", default=str(DEFAULT_LATENCY))
    parser.add_argument("--phase", default=str(DEFAULT_PHASE))
    parser.add_argument("--docx", default=str(DEFAULT_DOCX))
    parser.add_argument("--outdir", default=str(DEFAULT_OUTDIR))
    args = parser.parse_args()

    baseline = yaml.safe_load(Path(args.baseline).read_text())
    protocols = yaml.safe_load(Path(args.protocols).read_text())["protocols"]
    controller = yaml.safe_load(Path(args.controller).read_text())
    latency = yaml.safe_load(Path(args.latency).read_text())
    phase = yaml.safe_load(Path(args.phase).read_text())
    docx_table = read_docx_table2(Path(args.docx))

    rows: list[dict[str, str]] = []
    add_row(
        rows,
        "Deterministic production grid",
        f"{int(baseline['nx'])} x {int(baseline['ny'])}",
        "AUTO",
        args.baseline,
        docx_table,
    )
    add_row(
        rows,
        "Time step",
        f"{float(baseline['dt_s']):.2f} s",
        "AUTO",
        args.baseline,
        docx_table,
    )
    add_row(
        rows,
        "Wall thickness levels",
        join_float_list(list(phase["wall_thickness_mm_values"]), "mm"),
        "AUTO",
        args.phase,
        docx_table,
    )
    add_row(
        rows,
        "Nominal cooling coefficients",
        ", ".join(str(int(float(v))) for v in phase["cooling_h_W_per_m2K_values"]) + " W m^-2 K^-1",
        "AUTO",
        args.phase,
        docx_table,
    )
    add_row(
        rows,
        "Nominal insertion levels",
        join_float_list(list(phase["insertion_depth_mm_values"]), "mm"),
        "AUTO",
        args.phase,
        docx_table,
    )
    comparator_set = ", ".join(protocol_display_from_config(protocol, protocols) for protocol in protocols)
    add_row(
        rows,
        "Comparator set",
        comparator_set,
        "AUTO",
        args.protocols,
        docx_table,
    )
    add_row(
        rows,
        "Controller sensor",
        "MANUAL",
        "MANUAL",
        f"{args.docx} :: Table 2; supporting config {args.controller}",
        docx_table,
        notes="Exact manuscript phrase is not stored verbatim in the controller config.",
    )
    add_row(
        rows,
        "Controller target / ceiling",
        f"{float(controller['target_temperature_C']):.0f} °C / {float(controller['ceiling_temperature_C']):.0f} °C",
        "AUTO",
        args.controller,
        docx_table,
    )
    add_row(
        rows,
        "Controller sample period",
        f"{float(controller['sample_period_s']):.2f} s",
        "AUTO",
        args.controller,
        docx_table,
    )
    add_row(
        rows,
        "Post-pulse latency window",
        f"{float(latency['post_pulse_duration_s']):.1f} s",
        "AUTO",
        args.latency,
        docx_table,
    )
    phase_grid_size = (
        f"{len(phase['wall_thickness_mm_values'])} x "
        f"{len(phase['cooling_h_W_per_m2K_values'])} x "
        f"{len(phase['insertion_depth_mm_values'])} x "
        f"{len(protocols)} = "
        f"{len(phase['wall_thickness_mm_values']) * len(phase['cooling_h_W_per_m2K_values']) * len(phase['insertion_depth_mm_values']) * len(protocols)} protocol-cell evaluations"
    )
    add_row(
        rows,
        "Phase-preparation grid size",
        phase_grid_size,
        "AUTO",
        f"{args.phase}; {args.protocols}",
        docx_table,
    )
    add_row(
        rows,
        "Primary interpretive outputs",
        "MANUAL",
        "MANUAL",
        f"{args.docx} :: Table 2",
        docx_table,
        notes="Current wording is manuscript-curated rather than stored verbatim in config files.",
    )
    add_row(
        rows,
        "Secondary internal proxies",
        "MANUAL",
        "MANUAL",
        f"{args.docx} :: Table 2",
        docx_table,
        notes="Current wording is manuscript-curated rather than stored verbatim in config files.",
    )
    add_row(
        rows,
        "Calibration status",
        "MANUAL",
        "MANUAL",
        f"{args.docx} :: Table 2",
        docx_table,
        notes="Narrative limitation statement; supporting context exists in config files and audit notes but not as a canonical exported value.",
    )
    add_row(
        rows,
        "Supplementary UQ status",
        "MANUAL",
        "MANUAL",
        f"{args.docx} :: Table 2",
        docx_table,
        notes="Narrative scope statement; not stored as a config value.",
    )

    outdir = Path(args.outdir)
    csv_path = outdir / "table2_stage17_controls.csv"
    md_path = outdir / "table2_stage17_controls.md"
    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(csv_path, rows, fieldnames)
    write_md(md_path, rows)
    print(f"Saved {csv_path}")
    print(f"Saved {md_path}")


if __name__ == "__main__":
    main()
