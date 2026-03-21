#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import yaml
from docx import Document


DEFAULT_PROTOCOLS = Path("simulation/stage17_controlled_rebuild/configs/protocols_stage17_fourway.yaml")
DEFAULT_DOCX = Path("papers/V13/CMBBE_RF_ablation_reduced_model_main.docx")
DEFAULT_OUTDIR = Path("tmp/table_exports")


def read_docx_table1(docx_path: Path) -> list[dict[str, str]]:
    doc = Document(docx_path)
    table = doc.tables[0]
    header = [cell.text.strip() for cell in table.rows[0].cells]
    rows = []
    for row in table.rows[1:]:
        values = [cell.text.strip() for cell in row.cells]
        rows.append(dict(zip(header, values)))
    return rows


def format_number(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.3f}".rstrip("0").rstrip(".")


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "| protocol_key | manuscript_protocol_label | power_W | duration_s | computed_max_energy_J | manuscript_energy_display | manuscript_energy_display_status | manuscript_role | manuscript_role_status |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {protocol_key} | {manuscript_protocol_label} | {power_W} | {duration_s} | {computed_max_energy_J} | {manuscript_energy_display} | {manuscript_energy_display_status} | {manuscript_role} | {manuscript_role_status} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocols", default=str(DEFAULT_PROTOCOLS))
    parser.add_argument("--docx", default=str(DEFAULT_DOCX))
    parser.add_argument("--outdir", default=str(DEFAULT_OUTDIR))
    args = parser.parse_args()

    protocols_yaml = yaml.safe_load(Path(args.protocols).read_text())
    protocols = protocols_yaml["protocols"]
    table1_docx = read_docx_table1(Path(args.docx))

    rows: list[dict[str, str]] = []
    for idx, proto in enumerate(protocols):
        manuscript_row = table1_docx[idx] if idx < len(table1_docx) else {}
        power_w = float(proto["power_W"])
        duration_s = float(proto["duration_s"])
        computed_energy_j = power_w * duration_s
        use_controller = bool(proto.get("use_controller", False))

        if use_controller:
            manuscript_energy_display = manuscript_row.get("Nominal energy (J)", "MANUAL")
            manuscript_energy_display_status = "MANUAL"
            manuscript_energy_display_source = f"{args.docx} :: Table 1"
        else:
            manuscript_energy_display = format_number(computed_energy_j)
            manuscript_energy_display_status = "AUTO"
            manuscript_energy_display_source = args.protocols

        rows.append(
            {
                "protocol_key": str(proto["name"]),
                "use_controller": str(use_controller),
                "power_W": format_number(power_w),
                "power_W_status": "AUTO",
                "power_W_source": args.protocols,
                "duration_s": format_number(duration_s),
                "duration_s_status": "AUTO",
                "duration_s_source": args.protocols,
                "computed_max_energy_J": format_number(computed_energy_j),
                "computed_max_energy_J_status": "AUTO",
                "computed_max_energy_J_source": args.protocols,
                "manuscript_protocol_label": manuscript_row.get("Protocol", "MANUAL"),
                "manuscript_protocol_label_status": "MANUAL",
                "manuscript_protocol_label_source": f"{args.docx} :: Table 1",
                "manuscript_energy_display": manuscript_energy_display,
                "manuscript_energy_display_status": manuscript_energy_display_status,
                "manuscript_energy_display_source": manuscript_energy_display_source,
                "manuscript_role": manuscript_row.get("Role in comparison", "MANUAL"),
                "manuscript_role_status": "MANUAL",
                "manuscript_role_source": f"{args.docx} :: Table 1",
            }
        )

    outdir = Path(args.outdir)
    csv_path = outdir / "table1_stage17_protocols.csv"
    md_path = outdir / "table1_stage17_protocols.md"
    fieldnames = list(rows[0].keys()) if rows else []
    write_csv(csv_path, rows, fieldnames)
    write_md(md_path, rows)
    print(f"Saved {csv_path}")
    print(f"Saved {md_path}")


if __name__ == "__main__":
    main()
