import pandas as pd

def calculate_fair_share_impact(cagr_gap: float, ott_pct: float, capex_relief: float, traffic_adj: float) -> dict:
    adjusted_gap = cagr_gap + traffic_adj
    gap_closed = adjusted_gap * ott_pct
    capex_savings = 0.3 * capex_relief
    remaining = max(0, adjusted_gap - gap_closed)

    return {
        "gap_closed_pp": gap_closed * 100,
        "remaining_gap_pp": remaining * 100,
        "capex_savings_pct": capex_savings * 100,
        "adjusted_traffic_growth": 1 + traffic_adj,
        "total_gap_pp": adjusted_gap * 100,
    }

def calculate_network_stress_metrics(fact_df: pd.DataFrame) -> dict:
    latest = fact_df.iloc[-1]
    first = fact_df.iloc[0]
    
    return {
        "nsi_current": latest["nsi"],
        "nsi_growth": (latest["nsi"] / first["nsi"] - 1) if first["nsi"] > 0 else 0,
        "arpu_current": latest["revenue_per_line"],
        "arpu_decline": (latest["revenue_per_line"] / first["revenue_per_line"] - 1) if first["revenue_per_line"] > 0 else 0,
        "lines_current": latest["total_lines"],
    }