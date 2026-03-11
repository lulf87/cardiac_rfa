# Stage 2: phase-ready deterministic RFCA model

This stage fixes the main reporting issue found in Stage 1.5 and prepares the project for deterministic phase-diagram generation.

## What changed

1. **Physical wall vs thermal buffer separation**
   - `bottom_buffer_mm` is now treated as a **thermal buffer only**.
   - Arrhenius damage is accumulated and reported **only inside the physical myocardial wall**.
   - Reported lesion depth is clipped to `wall_thickness_mm`, so `depth_fraction` cannot exceed 1.0.

2. **Same stabilized heat boundaries**
   - Side and bottom boundaries remain zero-flux.
   - Top boundary remains convective.

3. **Phase-prep sweep**
   - Added `run_phase_prep.py` and `configs/phase_prep.yaml`.
   - This performs a deterministic scan over wall thickness, cooling, contact surrogate, and protocol.

## Basic run

```bash
cd ~/Projects/cardiac_rfa/simulation/stage2_phase_ready
bash run_all.sh
```

## Phase-prep run

```bash
cd ~/Projects/cardiac_rfa/simulation/stage2_phase_ready
bash run_phase_prep.sh
```

## Expected outputs

- `outputs/protocol_scan/protocol_summary.csv`
- `outputs/wall_protocol_scan/wall_protocol_summary.csv`
- `outputs/contact_protocol_scan/contact_protocol_summary.csv`
- `outputs/convergence/grid_convergence.csv`
- `outputs/phase_prep/phase_prep_summary.csv`

## Interpretation target

This stage should give you:

- stable protocol ordering
- valid lesion-depth fractions (`<= 1.0`)
- mixed success/failure regions for thin-wall, low-cooling, high-contact cases
- deterministic maps that are ready to become uncertainty maps in the next stage
