
# Stage 7 polishing patch

这个补丁只改 `analysis/` 层的绘图，不需要重跑仿真。

## 目录建议

把本目录解压到：

```text
~/Projects/cardiac_rfa/analysis/stage7_polishing_patch
```

## 直接用示例数据跑

```bash
cd ~/Projects/cardiac_rfa/analysis/stage7_polishing_patch
bash run_make_figures.sh
```

## 用你自己的 stage3 输出跑

```bash
cd ~/Projects/cardiac_rfa/analysis/stage7_polishing_patch

PHASE_CSV=../../simulation/stage3_uq_maps/outputs/phase_prep/phase_prep_summary.csv \
GRID_CSV=../../simulation/stage3_uq_maps/outputs/convergence/grid_convergence.csv \
DT_CSV=../../simulation/stage3_uq_maps/outputs/convergence/dt_convergence.csv \
UQ_CSV=../../simulation/stage3_uq_maps/outputs/uq_fast/uq_summary.csv \
OUTDIR=example_outputs \
bash run_make_figures.sh
```

## 本补丁做了什么

- Figure 3：共享图例下移，避免和 panel chip 冲突
- Figure 4：加了 selected grid / selected Δt 标记
- Figure 5：只标注 0<p<1 的过渡单元
- Figure 6：保留 HPSD / vHPSD 两行，并补充 Standard 未过热的说明
- Figure 7：主图改为 `median depth fraction` vs `overheat probability`
- Supplement：保留 `Ptrans` vs `Pover` 和 `depth_fraction_p50` heatmap

## 主要输出

- `fig3_deterministic_summary`
- `fig4_verification`
- `fig5_transmural_probability_maps`
- `fig6_overheat_probability_maps`
- `fig7_tradeoff_depthrisk`
- `figS1_depth_fraction_p50_maps`
- `figS2_tradeoff_ptrans_pover`
