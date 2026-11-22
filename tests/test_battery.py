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


def test_full_cycle_round_trip_efficiency():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    battery.charge(power_kw=10, hours=1)
    delivered_kwh = battery.discharge(power_kw=10, hours=1)
    assert delivered_kwh == pytest.approx(10 * 0.95 * 0.95)
    assert battery.soc_kwh == pytest.approx(0)


def test_charge_with_quarter_hour_step():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    grid_kwh = battery.charge(power_kw=40, hours=0.25)
    assert grid_kwh == pytest.approx(10)
    assert battery.soc_kwh == pytest.approx(9.5)


def test_discharge_limited_by_max_power():
    battery = Battery(capacity_kwh=100, max_power_kw=20, soc_kwh=80)
    delivered_kwh = battery.discharge(power_kw=50, hours=1)
    assert delivered_kwh == pytest.approx(20)
    assert battery.soc_kwh == pytest.approx(80 - 20 / 0.95)


def test_negative_discharge_power_raises():
    battery = Battery(capacity_kwh=100, max_power_kw=50, soc_kwh=10)
    with pytest.raises(ValueError):
        battery.discharge(power_kw=-5)


def test_invalid_capacity_raises():
    with pytest.raises(ValueError):
        Battery(capacity_kwh=-5, max_power_kw=50)