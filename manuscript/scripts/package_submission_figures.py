#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import csv
import shutil

MAIN_ORDER = [f'fig{i}' for i in range(1,9)]
SUPP_ORDER = ['figS1', 'figS2']
EXTS = ['.pdf', '.png', '.tiff']


def copy_one(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--project-root', required=True)
    ap.add_argument('--main-dir', required=True)
    ap.add_argument('--supp-dir', required=True)
    ap.add_argument('--captions', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()

    project_root = Path(args.project_root).resolve()
    main_dir = Path(args.main_dir).resolve()
    supp_dir = Path(args.supp_dir).resolve()
    captions = Path(args.captions).resolve()
    outdir = Path(args.outdir).resolve()

    for sub in ['main_pdf', 'main_tiff', 'main_png_preview', 'supp_pdf', 'supp_tiff', 'supp_png_preview']:
        (outdir / sub).mkdir(parents=True, exist_ok=True)

    manifest = []

    def process(prefixes, src_dir, pdf_sub, tiff_sub, png_sub, group):
        files = {p.name: p for p in src_dir.iterdir() if p.is_file()}
        for prefix in prefixes:
            matched = sorted([name for name in files if name.startswith(prefix + '_') or name == prefix + '.pdf' or name == prefix + '.png' or name == prefix + '.tiff'])
            for name in matched:
                src = files[name]
                ext = src.suffix.lower()
                if ext == '.pdf':
                    dst = outdir / pdf_sub / name
                elif ext == '.tiff':
                    dst = outdir / tiff_sub / name
                elif ext == '.png':
                    dst = outdir / png_sub / name
                else:
                    continue
                copy_one(src, dst)
                manifest.append({'group': group, 'figure_prefix': prefix, 'filename': name, 'ext': ext, 'path': str(dst.relative_to(project_root))})

    if main_dir.exists():
        process(MAIN_ORDER, main_dir, 'main_pdf', 'main_tiff', 'main_png_preview', 'main')
    if supp_dir.exists():
        process(SUPP_ORDER, supp_dir, 'supp_pdf', 'supp_tiff', 'supp_png_preview', 'supplement')

    copy_one(captions, outdir / 'figure_captions_v3.md')
    manifest_path = outdir / 'figure_manifest.csv'
    with manifest_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['group', 'figure_prefix', 'filename', 'ext', 'path'])
        writer.writeheader()
        writer.writerows(manifest)

    print(f'Created submission package at: {outdir}')


if __name__ == '__main__':
    main()
