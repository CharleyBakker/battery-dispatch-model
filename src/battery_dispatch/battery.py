from dataclasses import dataclass


@dataclass
class Battery:
    """A simple battery with power, capacity and efficiency limits."""

    capacity_kwh: float
    max_power_kw: float
    charge_efficiency: float = 0.95
    discharge_efficiency: float = 0.95
    soc_kwh: float = 0.0  # state of charge: current stored energy

    def charge(self, power_kw: float, hours: float = 1.0) -> float:
        """Charge from the grid. Returns the energy (kWh) drawn from the grid."""
        if power_kw < 0:
            raise ValueError("power_kw must be >= 0")
        grid_kwh = min(power_kw, self.max_power_kw) * hours
        stored_kwh = grid_kwh * self.charge_efficiency
        room_kwh = self.capacity_kwh - self.soc_kwh
        if stored_kwh > room_kwh:
            stored_kwh = room_kwh
            grid_kwh = stored_kwh / self.charge_efficiency
        self.soc_kwh += stored_kwh
        return grid_kwh

    def discharge(self, power_kw: float, hours: float = 1.0) -> float:
        """Discharge to the grid. Returns the energy (kWh) delivered to the grid."""
        if power_kw < 0:
            raise ValueError("power_kw must be >= 0")
        delivered_kwh = min(power_kw, self.max_power_kw) * hours
        drawn_kwh = delivered_kwh / self.discharge_efficiency
        if drawn_kwh > self.soc_kwh:
            drawn_kwh = self.soc_kwh
            delivered_kwh = drawn_kwh * self.discharge_efficiency
        self.soc_kwh -= drawn_kwh
        return delivered_kwh

    def __post_init__(self) -> None:
        if self.capacity_kwh <= 0 or self.max_power_kw <= 0:
            raise ValueError("capacity_kwh and max_power_kw must be > 0")
        if not (0 < self.charge_efficiency <= 1 and 0 < self.discharge_efficiency <= 1):
            raise ValueError("efficiencies must be between 0 (exclusive) and 1")
        if not (0 <= self.soc_kwh <= self.capacity_kwh):
            raise ValueError("soc_kwh must be between 0 and capacity_kwh")
