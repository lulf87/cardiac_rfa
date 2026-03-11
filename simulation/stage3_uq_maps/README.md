# Stage 3: uncertainty-aware RFCA maps

This stage keeps the stabilized deterministic model from Stage 2 and adds a first uncertainty layer so the outputs become **probability maps** rather than single deterministic lesion contours.

## What is new

1. **Uncertain contact and cooling**
   - `insertion_depth_mm` is sampled around each nominal setting.
   - `cooling_h_W_per_m2K` is sampled around each nominal setting.
   - Sampling uses a lightweight Latin-hypercube style normal draw with clipping.

2. **Probability outputs**
   - transmural probability
   - overheat probability
   - median / p10 / p90 depth fraction

3. **Two run modes**
   - `run_uq_fast.sh`: smaller run for quick local testing
   - `run_uq_paper.sh`: denser run intended for figure-quality maps

## Important limitation

In this reduced model, the heat source is normalized after the potential solve. That means **bulk electrical conductivity is not yet an active uncertainty driver** in the current UQ stage. Do not claim conductivity UQ until a later calibration stage where power control is tied more directly to the electrical model.

## Recommended order

```bash
cd ~/Projects/cardiac_rfa/simulation/stage3_uq_maps
bash run_all.sh          # deterministic checks
bash run_phase_prep.sh   # deterministic phase boundaries
bash run_uq_fast.sh      # first probability maps
```

If the fast run looks good, then run:

```bash
bash run_uq_paper.sh
```

## Expected outputs

Fast run:
- `outputs/uq_fast/uq_summary.csv`
- `outputs/uq_fast/uq_overview.csv`
- `outputs/uq_fast/*_transmural_probability.png`
- `outputs/uq_fast/*_overheat_probability.png`
- `outputs/uq_fast/*_depth_fraction_p50.png`

Paper run:
- same file set under `outputs/uq_paper/`

## What success looks like

You should see:
- standard protocol: largest transmural-probability region
- HPSD: intermediate region, with a boundary in thin wall / higher contact settings
- vHPSD: low transmural probability overall, but rising overheat probability at high insertion and weak cooling

If that pattern appears, the model is ready for manuscript-style figures and literature-derived validation.
