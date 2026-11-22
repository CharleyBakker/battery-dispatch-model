import pytest

from battery_dispatch.battery import Battery
from battery_dispatch.dispatch import threshold_dispatch


def test_profit_with_clear_price_spread():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    result = threshold_dispatch(
        battery, prices_eur_per_mwh=[20, 20, 100, 100], low=30, high=90
    )
    assert result.profit_eur == pytest.approx(7.025)
    assert result.final_soc_kwh == pytest.approx(0)


def test_flat_prices_do_nothing():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    result = threshold_dispatch(battery, [50, 50, 50], low=30, high=90)
    assert result.profit_eur == 0
    assert result.actions_kwh == [0.0, 0.0, 0.0]


def test_input_battery_is_not_modified():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    threshold_dispatch(battery, [20, 100], low=30, high=90)
    assert battery.soc_kwh == 0

def test_low_above_high_raises():
    battery = Battery(capacity_kwh=100, max_power_kw=50)
    with pytest.raises(ValueError):
        threshold_dispatch(battery, [20, 100], low=90, high=30)