from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class LatencyConfig:
    enabled: bool = False
    post_pulse_duration_s: float = 8.0
    record_dt_s: float = 0.05

    @staticmethod
    def from_yaml(path: str | Path) -> "LatencyConfig":
        raw = yaml.safe_load(Path(path).read_text()) or {}
        raw.pop("notes", None)

        data: dict[str, object] = {}
        for key, value in raw.items():
            if key == "enabled":
                data[key] = bool(value)
            else:
                data[key] = float(value)

        latency = LatencyConfig(**data)
        latency.validate()
        return latency

    def validate(self) -> None:
        if self.post_pulse_duration_s < 0.0:
            raise ValueError("latency post_pulse_duration_s must be non-negative")
        if self.record_dt_s <= 0.0:
            raise ValueError("latency record_dt_s must be positive")


def extra_latency_steps(duration_s: float, dt_s: float) -> int:
    if dt_s <= 0:
        raise ValueError("dt_s must be positive")
    return max(0, int(round(duration_s / dt_s)))
