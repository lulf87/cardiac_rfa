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
