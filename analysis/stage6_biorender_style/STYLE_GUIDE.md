# Unified figure system

## Overall principle
- Use a **BioRender-like visual hierarchy** for conceptual structure: muted slate headers, rounded chips, warm off-white canvas, compact labels.
- Use a **journal-clean plotting style** for quantitative panels: white axes, thin spines, external legends, shared colorbars, restrained annotation.

## Typography
- Sans-serif throughout (`DejaVu Sans`, close to Arial/Helvetica)
- Panel letter: 11 pt bold
- Axis title: 9 pt
- Tick labels: 8 pt
- Figure strip/header chip: 8.5 pt semibold

## Palette
- Slate header: `#5F6F7B`
- Text: `#344054`
- Warm canvas: `#FBFAF7`
- Light chip fill: `#EEF2F6`
- Standard: `#2A9D8F`
- HPSD: `#8A7FB9`
- vHPSD: `#E07A5F`
- Thin/medium/thick wall tones: mint → olive → gold → terra-cotta

## Figure-specific rules
- Figure 3: line plots, no filled background, one external legend.
- Figure 4: linear percent error scale, no log-style presentation.
- Figure 5/6/S1: column chips for cooling, row chips for protocols, annotate only transitional probabilities.
- Figure 7: fixed marker size, protocol by marker shape, wall thickness by color, favorable zone highlighted with a soft rounded box.

## Export
- PNG for drafting
- PDF for manuscript submission
- 600 dpi for raster export
