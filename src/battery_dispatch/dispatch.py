from dataclasses import dataclass, replace

from battery_dispatch.battery import Battery


@dataclass
class DispatchResult:
    actions_kwh: list[
        float
    ]  # positief = laden uit het net, negatief = ontladen naar het net
    profit_eur: float
    final_soc_kwh: float


def threshold_dispatch(
    battery: Battery,
    prices_eur_per_mwh: list[float],
    low: float,
    high: float,
    hours_per_step: float = 1.0,
) -> DispatchResult:
    """Baseline strategy: charge at full power when the price is <= low,
    discharge at full power when the price is >= high.

    The strategy is greedy: it does not look ahead at future prices.

    Args:
        battery: Battery to simulate. It is copied, so the input is not changed.
        prices_eur_per_mwh: Price per time step in EUR/MWh.
        low: Charging threshold in EUR/MWh.
        high: Discharging threshold in EUR/MWh. Must be larger than `low`.
        hours_per_step: Length of each time step in hours. Must be > 0.

    Returns:
        DispatchResult with, per step, the energy exchanged with the grid in kWh
        (positive = charging, negative = discharging), the total profit in EUR
        and the final state of charge in kWh.
    """
    if low >= high:
        raise ValueError("low must be smaller than high")
    if hours_per_step <= 0:
        raise ValueError("hours_per_step must be > 0")

    battery = replace(battery)
    profit_eur = 0.0
    actions_kwh: list[float] = []

    for price in prices_eur_per_mwh:
        if price <= low:
            grid_kwh = battery.charge(battery.max_power_kw, hours_per_step)
            profit_eur -= grid_kwh / 1000 * price
            actions_kwh.append(grid_kwh)
        elif price >= high:
            delivered_kwh = battery.discharge(battery.max_power_kw, hours_per_step)
            profit_eur += delivered_kwh / 1000 * price
            actions_kwh.append(-delivered_kwh)
        else:
            actions_kwh.append(0.0)

    return DispatchResult(actions_kwh, profit_eur, battery.soc_kwh)
