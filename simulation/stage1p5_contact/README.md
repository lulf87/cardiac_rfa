# Stage 1.5: stabilized deterministic RFCA model

这一步是从 Stage 1 的“能跑通”升级到“更能当论文底座”的版本。

## 这次改了什么
1. **热边界条件修正**：左右和底部改为零通量，不再固定 37°C；顶部保留 Robin 对流冷却。
2. **几何缓冲区加大**：宽度扩大到 18 mm，并加入 `bottom_buffer_mm`，减少侧边/底边对病灶深度的污染。
3. **加入接触代理变量入口**：以 `insertion_depth_mm` 作为低/中/高接触 surrogate，当前通过局部冷却修正与热源轻度放大/下移实现。
4. **保留 Stage 1 的完整确定性扫描**：协议、壁厚、冷却、收敛性都还在。

## 目录
- `src/model_fd.py`：2D 有限差分电-热-损伤模型
- `src/run_case.py`：单病例基线
- `src/run_protocol_scan.py`：协议扫描
- `src/run_wall_protocol_scan.py`：壁厚 × 协议扫描
- `src/run_cooling_protocol_scan.py`：冷却 × 协议扫描
- `src/run_contact_scan.py`：接触代理变量 × 协议扫描
- `src/run_convergence.py`：网格 / 时间步收敛

## 本地运行
```bash
cd cardiac_rfa/simulation/stage1p5_contact
bash run_all.sh
```

## 建议先看的结果
- `outputs/protocol_scan/protocol_summary.csv`
- `outputs/wall_protocol_scan/wall_protocol_summary.csv`
- `outputs/cooling_protocol_scan/cooling_protocol_summary.csv`
- `outputs/contact_protocol_scan/contact_protocol_summary.csv`
- `outputs/convergence/grid_convergence.csv`
- `outputs/convergence/dt_convergence.csv`

## 这一阶段的定位
这仍然不是最终投稿版，但已经比 Stage 1 更适合做：
- Methods 中的边界条件说明
- Results 中的 deterministic trend 图
- 下一步不确定性传播前的“模型底座”
