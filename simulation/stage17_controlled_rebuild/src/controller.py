from dataclasses import dataclass

@dataclass
class GenericTempLimitedController:
    enabled: bool = False
    target_temperature_C: float = 55.0
    ceiling_temperature_C: float = 65.0
    max_power_W: float = 90.0
    min_power_W: float = 5.0
    ramp_down_gain_W_per_C: float = 15.0

    def compute_power(self, measured_temp_C: float, requested_power_W: float) -> float:
        if not self.enabled:
            return requested_power_W

        if measured_temp_C <= self.target_temperature_C:
            return min(requested_power_W, self.max_power_W)

        reduction = self.ramp_down_gain_W_per_C * (measured_temp_C - self.target_temperature_C)
        proposed = requested_power_W - reduction
        proposed = min(proposed, self.max_power_W)
        proposed = max(proposed, self.min_power_W)
        return proposed
