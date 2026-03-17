from dataclasses import dataclass

@dataclass
class LatencyConfig:
    enabled: bool = False
    post_pulse_duration_s: float = 8.0
    record_dt_s: float = 0.05

def extra_latency_steps(duration_s: float, dt_s: float) -> int:
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    return max(0, int(round(duration_s / dt_s)))
