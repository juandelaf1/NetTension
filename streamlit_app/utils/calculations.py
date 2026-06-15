import pandas as pd
import numpy as np

def calculate_cagr(start_val: float, end_val: float, periods: int) -> float:
    if start_val <= 0 or end_val <= 0 or periods <= 0:
        return 0.0
    return (end_val / start_val) ** (1 / periods) - 1

def calculate_fair_share_impact(cagr_gap: float, ott_pct: float, capex_relief: float, traffic_adj: float) -> dict:
    """Calculate Fair Share what-if scenario impact."""
    gap_closed = cagr_gap * ott_pct
    capex_savings = 0.3 * capex_relief  # simplified
    adjusted_growth = 1 + traffic_adj
    
    return {
        "gap_closed_pp": gap_closed * 100,
        "remaining_gap_pp": (cagr_gap - gap_closed) * 100,
        "capex_savings_pct": capex_savings * 100,
        "adjusted_traffic_growth": adjusted_growth,
    }

def calculate_hhi_stats(hhi_df: pd.DataFrame) -> dict:
    return {
        "current": hhi_df["hhi"].iloc[-1],
        "min": hhi_df["hhi"].min(),
        "max": hhi_df["hhi"].max(),
        "avg": hhi_df["hhi"].mean(),
        "trend": "decreasing" if hhi_df["hhi"].iloc[-1] < hhi_df["hhi"].iloc[0] else "increasing",
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