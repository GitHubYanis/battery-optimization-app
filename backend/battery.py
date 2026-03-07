
def build_optimize_result(load, prices, battery):
    total_cost_before = sum(load[h] * prices[h] for h in range(24))

    charge_kw, discharge_kw, soc_kwh = _optimize_battery_schedule(prices, battery)

    total_cost_after = sum(
        (load[h] - discharge_kw[h] + charge_kw[h]) * prices[h]
        for h in range(24)
    )

    savings = total_cost_before - total_cost_after
    
    top_3_hours = _find_top_three_savings_hours(load, prices, charge_kw, discharge_kw)

    if top_3_hours:
        parts = [f"heure {h} ({savings_h:.3f}$)" for h, savings_h in top_3_hours]
        explanation = f"Les 3 heures avec le plus d'économies sont : {', '.join(parts)}."
    else:
        explanation = "Aucune décharge effectuée — la batterie n'a pas pu générer d'économies."

    return {
        "charge_kw": charge_kw,
        "discharge_kw": discharge_kw,
        "soc_kwh": soc_kwh,
        "total_cost_before": round(total_cost_before, 2),
        "total_cost_after": round(total_cost_after, 2),
        "savings": round(savings, 2),
        "explanation": explanation
    }


def _optimize_battery_schedule(prices, battery):
    price_median = sorted(prices)[12]

    charge_kw = [0.0] * 24
    discharge_kw = [0.0] * 24
    soc_kwh = [0.0] * 24

    soc = battery.initial_soc_kwh

    for h in range(24):
        price = prices[h]

        if price < price_median:
            # Heure cheap, on essaie de charger
            max_charge = min(
                battery.max_charge_kw,
                (battery.capacity_kwh - soc) / battery.efficiency
            )
            charge = max(0.0, max_charge)
            soc = soc + charge * battery.efficiency
            charge_kw[h] = round(charge, 2)
        elif price > price_median:
            # Heure chère, on essaie de décharger
            max_discharge = min(
                battery.max_discharge_kw,
                soc * battery.efficiency
            )
            discharge = max(0.0, max_discharge)
            soc = soc - discharge / battery.efficiency
            discharge_kw[h] = round(discharge, 2)

        soc = max(0.0, min(battery.capacity_kwh, soc)) # on s'assure que SoC entre 0 et capacity
        soc_kwh[h] = round(soc, 2)

    return charge_kw, discharge_kw, soc_kwh

def _find_top_three_savings_hours(load, prices, charge_kw, discharge_kw):
    savings_per_hour = []
    for h in range(24):
        cost_before = load[h] * prices[h]
        cost_after = (load[h] - discharge_kw[h] + charge_kw[h]) * prices[h]
        savings = cost_before - cost_after
        savings_per_hour.append((h, savings))

    # Trier les économies en ordre décroissant puis prendre les 3 premières
    return sorted(savings_per_hour, key=lambda x: x[1], reverse=True)[:3]

def build_optimize_result(load, prices, battery):
    total_cost_before = sum(load[h] * prices[h] for h in range(24))

    charge_kw, discharge_kw, soc_kwh = _optimize_battery_schedule(prices, battery)

    total_cost_after = sum(
        (load[h] - discharge_kw[h] + charge_kw[h]) * prices[h]
        for h in range(24)
    )

    savings = total_cost_before - total_cost_after

    top_3_hours = _find_top_three_savings_hours(load, prices, charge_kw, discharge_kw)

    if top_3_hours:
        parts = [f"heure {h} ({s:.3f}$)" for h, s in top_3_hours]
        explanation = f"Les 3 heures avec le plus d'économies sont : {', '.join(parts)}."
    else:
        explanation = "Aucune décharge effectuée — la batterie n'a pas pu générer d'économies."

    return {
        "charge_kw": charge_kw,
        "discharge_kw": discharge_kw,
        "soc_kwh": soc_kwh,
        "total_cost_before": round(total_cost_before, 2),
        "total_cost_after": round(total_cost_after, 2),
        "savings": round(savings, 2),
        "explanation": explanation
    }


def build_charts(load, prices, result):
    hours = list(range(24))

    load_chart = {
        "data": [
            {"x": hours, "y": load, "type": "scatter", "mode": "lines", "name": "Charge originale (kW)"},
            {
                "x": hours,
                "y": [load[h] - result["discharge_kw"][h] + result["charge_kw"][h] for h in range(24)],
                "type": "scatter", "mode": "lines", "name": "Charge nette (kW)",
            }
        ],
        "layout": {
            "title": {"text": "Consommation du réseau (kW)", "font": {"size": 14}},
            "xaxis": {"title": {"text": "Heure (0-23)"}, "tickmode": "linear", "tick0": 0, "dtick": 2},
            "yaxis": {"title": {"text": "Consommation (kW)"}},
            "width": 360, "height": 288,
            "legend": {"x": 0, "y": 1, "xanchor": "left", "yanchor": "top", "font": {"size": 10}},
            "margin": {"r": 10, "t": 40, "b": 40, "l": 40},
        }
    }

    dispatch_chart = {
        "data": [
            {"x": hours, "y": result["charge_kw"], "type": "bar", "name": "Charge (kW)", "marker": {"color": "#2ecc71"}},
            {"x": hours, "y": [-d for d in result["discharge_kw"]], "type": "bar", "name": "Décharge (kW)", "marker": {"color": "#e74c3c"}},
            {"x": hours, "y": prices, "type": "scatter", "mode": "lines", "name": "Prix ($/kWh)", "yaxis": "y2", "line": {"color": "#3498db", "dash": "dot"}},
        ],
        "layout": {
            "title": {"text": "Dispatch de la batterie", "font": {"size": 16}},
            "xaxis": {"title": {"text": "Heure (0-23)"}, "tickmode": "linear", "tick0": 0, "dtick": 2},
            "yaxis": {"title": {"text": "Puissance (kW)"}},
            "yaxis2": {
                "title": {"text": "Prix ($/kWh)"},
                "overlaying": "y", 
                "side": "right", 
                "range": [0, 0.5], 
                "fixedrange": True
            },
            "barmode": "relative",
            "width": 360, "height": 288,
            "margin": {"r": 40, "t": 40, "b": 40, "l": 40},
            "legend": {
                "x": 0.04,
                "y": 0.98,
                "xanchor": "left",
                "yanchor": "top",
                "font": {"size": 9},
            }
        }
    }

    soc_chart = {
        "data": [
            {
                "x": hours, "y": result["soc_kwh"],
                "type": "scatter", "mode": "lines+markers",
                "name": "SoC (kWh)", "fill": "tozeroy",
            }
        ],
        "layout": {
            "title": {"text": "État de charge de la batterie (kWh)", "font": {"size": 14}},
            "xaxis": {"title": {"text": "Heure (0-23)"}, "tickmode": "linear", "tick0": 0, "dtick": 2},
            "yaxis": {"title": {"text": "État de charge (kWh)"}},
            "width": 360, "height": 288,
            "legend": {"x": 0, "y": 1, "xanchor": "left", "yanchor": "top", "font": {"size": 10}},
            "margin": {"r": 10, "t": 40, "b": 40, "l": 40},
        }
    }

    return {"load_chart": load_chart, "dispatch_chart": dispatch_chart, "soc_chart": soc_chart}
