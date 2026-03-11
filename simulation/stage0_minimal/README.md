# cardiac_rfa / simulation / stage0_minimal

这是第一步的最小可运行版本，只做三件事：
1. 单个基线病例（50 W / 10 s / 4 mm）
2. 三种协议比较（30/30, 50/10, 90/4）
3. 输出图像和 CSV

## 目录
- `src/model_fd.py`：2D 最小有限差分模型
- `src/run_case.py`：运行单个病例
- `src/run_protocol_scan.py`：运行三协议比较
- `configs/baseline_50W_10s_4mm.yaml`：基线配置
- `configs/protocols.yaml`：协议配置
- `requirements.txt`：依赖
- `run_all.sh`：一键运行

## 本地运行
```bash
cd cardiac_rfa/simulation/stage0_minimal
bash run_all.sh
```

运行结束后会生成：
- `outputs/baseline_50W_10s_4mm/`
- `outputs/protocol_scan_stage0/`

## 手动运行
```bash
cd cardiac_rfa/simulation/stage0_minimal
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
python src/run_case.py --config configs/baseline_50W_10s_4mm.yaml --outdir outputs/baseline_50W_10s_4mm
python src/run_protocol_scan.py --base-config configs/baseline_50W_10s_4mm.yaml --protocols configs/protocols.yaml --outdir outputs/protocol_scan_stage0
```
