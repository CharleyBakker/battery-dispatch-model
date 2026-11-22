from dataclasses import dataclass


@dataclass
class Battery:
    """Een eenvoudige batterij met vermogens-, capaciteits- en rendementsgrenzen."""

    capacity_kwh: float
    max_power_kw: float
    charge_efficiency: float = 0.95
    discharge_efficiency: float = 0.95
    soc_kwh: float = 0.0  # state of charge: huidige lading

    def charge(self, power_kw: float, hours: float = 1.0) -> float:
        """Laad op vanaf het net. Geeft de energie (kWh) terug die het net leverde."""
        if power_kw < 0:
            raise ValueError("power_kw moet >= 0 zijn")
        grid_kwh = min(power_kw, self.max_power_kw) * hours
        stored_kwh = grid_kwh * self.charge_efficiency
        room_kwh = self.capacity_kwh - self.soc_kwh
        if stored_kwh > room_kwh:
            stored_kwh = room_kwh
            grid_kwh = stored_kwh / self.charge_efficiency
        self.soc_kwh += stored_kwh
        return grid_kwh

    def discharge(self, power_kw: float, hours: float = 1.0) -> float:
        """Ontlaad naar het net. Geeft de geleverde energie (kWh) terug."""
        if power_kw < 0:
            raise ValueError("power_kw moet >= 0 zijn")
        delivered_kwh = min(power_kw, self.max_power_kw) * hours
        drawn_kwh = delivered_kwh / self.discharge_efficiency
        if drawn_kwh > self.soc_kwh:
            drawn_kwh = self.soc_kwh
            delivered_kwh = drawn_kwh * self.discharge_efficiency
        self.soc_kwh -= drawn_kwh
        return delivered_kwh

    def __post_init__(self) -> None:
    if self.capacity_kwh <= 0 or self.max_power_kw <= 0:
        raise ValueError("capacity_kwh en max_power_kw moeten > 0 zijn")
    if not (0 < self.charge_efficiency <= 1 and 0 < self.discharge_efficiency <= 1):
        raise ValueError("rendementen moeten tussen 0 (excl.) en 1 liggen")
    if not (0 <= self.soc_kwh <= self.capacity_kwh):
        raise ValueError("soc_kwh moet tussen 0 en capacity_kwh liggen")

    def test_full_cycle_round_trip_efficiency():
        battery = Battery(capacity_kwh=100, max_power_kw=50)
        battery.charge(power_kw=10, hours=1)
        delivered_kwh = battery.discharge(power_kw=10, hours=1)
        assert delivered_kwh == pytest.approx(10 * 0.95 * 0.95)
        assert battery.soc_kwh == pytest.approx(0)
