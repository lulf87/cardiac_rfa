# V10 Results Outline

## 3.1 Stage17 comparator definition
- Introduce four protocols:
  - standard_30W_30s
  - hpsd_50W_10s
  - vhpsd_90W_4s_fixed
  - vhpsd_90W_4s_controlled
- State explicitly that the controlled 90W/4s comparator is generic temperature-limited, not catheter-specific.

## 3.2 Effect of post-pulse thermal latency
- Compare single-case 90W/4s fixed without vs with latency.
- Emphasize that latency materially increases depth and lesion area.

## 3.3 Deterministic four-way comparison at representative conditions
- Use protocol_summary.csv and the new stage17 deterministic figure.
- Main point:
  standard RF deepest, HPSD intermediate, fixed 90/4 shallowest-hotter, controlled 90/4 slightly cooler and slightly less deep than fixed 90/4.

## 3.4 Phase-prep maps with fixed vs controlled 90W/4s
- Use phase_prep_summary.csv.
- State that controlled 90/4 frequently reduces delivered energy and peak temperature.
- State that controller action is threshold-dependent and may be inactive in some cells.

## 3.5 Boundaries of interpretation
- Do not sell these maps as device-level prediction.
- Keep width and overheat-area as internal proxies.
