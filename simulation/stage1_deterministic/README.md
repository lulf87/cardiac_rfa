# cardiac_rfa / simulation / stage1_deterministic

这是第二步：从 stage0 的“能跑通”升级到“能写 Methods/Results 骨架”的确定性版本。

这一步包含 4 个模块：
1. 单病例基线运行
2. 三协议比较
3. 壁厚 × 协议扫描
4. 冷却 × 协议扫描
5. 网格 / 时间步收敛测试

## 目录
- `src/model_fd.py`：2D 有限差分最小电-热-损伤模型
- `src/run_case.py`：单病例运行
- `src/run_protocol_scan.py`：三协议比较
- `src/run_wall_protocol_scan.py`：壁厚与协议扫描
- `src/run_cooling_protocol_scan.py`：冷却与协议扫描
- `src/run_convergence.py`：收敛性测试
- `configs/*.yaml`：参数文件
- `run_all.sh`：一键运行

## 本地运行
```bash
cd cardiac_rfa/simulation/stage1_deterministic
bash run_all.sh
```

## 建议输出目录
运行后会生成：
- `outputs/baseline_50W_10s_4mm/`
- `outputs/protocol_scan/`
- `outputs/wall_protocol_scan/`
- `outputs/cooling_protocol_scan/`
- `outputs/convergence/`

## 这一阶段的定位
这一阶段仍然是“确定性论文骨架”，不是最终投稿版本。
它的任务是先产出：
- 4 张候选主图
- 3 个 CSV 结果表
- 1 组收敛性结果

## 你应该先关注什么
1. 三协议的 lesion depth 排序是否稳定
2. 随壁厚增加，depth fraction 是否下降
3. 冷却增强时，peak T 和 lesion depth 是否下降
4. 网格/时间步进一步加密后，结果变化是否足够小
