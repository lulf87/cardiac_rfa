from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class GenericTempLimitedController:
    enabled: bool = False
    sensor_location: str = "surface_adjacent"
    target_temperature_C: float = 55.0
    ceiling_temperature_C: float = 65.0
    max_power_W: float = 90.0
    min_power_W: float = 5.0
    ramp_down_gain_W_per_C: float = 15.0
    sample_period_s: float = 0.05

    @staticmethod
    def from_yaml(path: str | Path) -> "GenericTempLimitedController":
        raw = yaml.safe_load(Path(path).read_text()) or {}
        raw.pop("notes", None)
        raw.pop("controller_name", None)

        data: dict[str, object] = {}
        for key, value in raw.items():
            if key == "enabled":
                data[key] = bool(value)
            elif key == "sensor_location":
                data[key] = str(value)
            else:
                data[key] = float(value)

        controller = GenericTempLimitedController(**data)
        controller.validate()
        return controller

    def validate(self) -> None:
        if self.sensor_location != "surface_adjacent":
            raise ValueError(
                "Only sensor_location: surface_adjacent is supported in stage17 minimal controller mode."
            )
        if self.sample_period_s <= 0.0:
            raise ValueError("controller sample_period_s must be positive")
        if self.max_power_W < 0.0 or self.min_power_W < 0.0:
            raise ValueError("controller power bounds must be non-negative")
        if self.max_power_W < self.min_power_W:
            raise ValueError("controller max_power_W must be >= min_power_W")
        if self.ceiling_temperature_C < self.target_temperature_C:
            raise ValueError("controller ceiling_temperature_C must be >= target_temperature_C")

    def compute_power(self, measured_temp_C: float, requested_power_W: float) -> float:
        requested_power_W = float(requested_power_W)
        if not self.enabled:
            return requested_power_W

        self.validate()

        upper = min(requested_power_W, self.max_power_W)
        lower = min(self.min_power_W, upper)

        if measured_temp_C <= self.target_temperature_C:
            return upper

        if measured_temp_C >= self.ceiling_temperature_C:
            return lower

        reduction = self.ramp_down_gain_W_per_C * (measured_temp_C - self.target_temperature_C)
        proposed = requested_power_W - reduction
        proposed = min(proposed, upper)
        proposed = max(proposed, lower)
        return proposed
