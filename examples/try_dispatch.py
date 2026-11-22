from battery_dispatch.battery import Battery
from battery_dispatch.dispatch import threshold_dispatch

prices = [20, 20, 100, 100]  # €/MWh per uur
battery = Battery(capacity_kwh=100, max_power_kw=50)
result = threshold_dispatch(battery, prices, low=30, high=90)

for hour, (price, action) in enumerate(zip(prices, result.actions_kwh)):
    print(f"Uur {hour}: prijs {price} €/MWh, actie {action:.1f} kWh")
print(f"Winst: €{result.profit_eur:.3f}")