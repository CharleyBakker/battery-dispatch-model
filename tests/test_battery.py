import pytest

from battery_dispatch.battery import Battery


def test_charge_stores_energy_with_losses():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    grid_kwh = battery.charge(power_kw=50, hours=1)
    assert grid_kwh == pytest.approx(50)
    assert battery.soc_kwh == pytest.approx(47.5)


def test_charge_limited_by_capacity():
    battery = Battery(capacity_kwh=10, max_power_kw=50)
    battery.charge(power_kw=50, hours=1)
    assert battery.soc_kwh == pytest.approx(10)


def test_charge_limited_by_max_power():
    battery = Battery(capacity_kwh=100, max_power_kw=20)
    grid_kwh = battery.charge(power_kw=50, hours=1)
    assert grid_kwh == pytest.approx(20)


def test_discharge_limited_by_soc():
    battery = Battery(capacity_kwh=100, max_power_kw=50, soc_kwh=10)
    delivered_kwh = battery.discharge(power_kw=50, hours=1)
    assert delivered_kwh == pytest.approx(9.5)
    assert battery.soc_kwh == pytest.approx(0)


def test_negative_power_raises():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    with pytest.raises(ValueError):
        battery.charge(power_kw=-5)
