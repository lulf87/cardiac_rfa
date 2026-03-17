# Stage17 Decision Log

## 2026-03-17
- stage16 is frozen as the baseline.
- stage17 starts from a clean copy of stage16 code/configs, excluding outputs and venv.
- no device-specific QDOT claim will be made.
- 90 W / 4 s will later be handled as:
  1. generic fixed-power comparator
  2. generic temperature-limited comparator
- lesion depth / depth fraction are primary outputs.
- width and overheating are secondary proxies unless stronger evidence is added.

## 2026-03-17 (controller selection)
- Selected provisional controller for stage17 scans:
  configs/controller_selected_stage17.yaml
- Rationale:
  - soft and mid produced no effective throttling
  - hard produced modest throttling without collapsing lesion depth to zero
  - latency loop behaved plausibly in fixed and controlled 90W/4s single-case tests

## 2026-03-17 (four-way protocol scan)
- Four-way protocol scan completed successfully with:
  - standard_30W_30s
  - hpsd_50W_10s
  - vhpsd_90W_4s_fixed
  - vhpsd_90W_4s_controlled
- All protocols used latency_enabled.yaml.
- Only vhpsd_90W_4s_controlled used controller_selected_stage17.yaml.
- Controlled 90W/4s produced lower delivered energy and lower peak temperature than fixed 90W/4s, with only a modest depth reduction.
- Next step: extend wall / cooling / contact scans before touching phase_prep.
