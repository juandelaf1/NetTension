"""
NetTension — KPI Engine

Calculates all strategic KPIs from cleaned data.

KPIs:
  - HHI (Herfindahl-Hirschman Index) quarterly
  - Network Stress Index (traffic per active line)
  - Infrastructure Elasticity Margin
  - Macro Contribution Ratio (telecom revenue / GDP)
  - Digital Density Margin (lines per 100 inhabitants)
  - Traffic CAGR vs Revenue CAGR
"""

import pandas as pd
import numpy as np


def hhi_quarterly(
    df: pd.DataFrame,
    value_col: str = "ingresos_por_operador",
    group_col: str = "operador",
    time_col: str = "trimestre",
) -> pd.DataFrame:
    """Calculate Herfindahl-Hirschman Index per quarter.

    Uses ingresos_por_operador (operator-level revenue) for accuracy.
    Filters to rows where value_col > 0 and operator is not null.

    HHI = sum(cuota_i^2) * 10000

    <1000 → competitive
    1000–2500 → moderately concentrated
    >2500 → highly concentrated
    """
    mask = (df[value_col] > 0) & df[group_col].notna()
    op_rev = df[mask].groupby([time_col, group_col])[value_col].sum().reset_index()
    totals = op_rev.groupby(time_col)[value_col].sum().rename("total")
    shares = op_rev.merge(totals, on=time_col)
    shares["cuota"] = shares[value_col] / shares["total"]
    hhi = shares.groupby(time_col).apply(
        lambda g: (g["cuota"] ** 2).sum() * 10000,
        include_groups=False,
    )
    result = hhi.reset_index(name="hhi")
    return result[result["hhi"] > 0]


def network_stress_index(
    df: pd.DataFrame,
    traffic_col: str = "trafico",
    lines_col: str = "lineas_o_accesos",
    time_col: str = "trimestre",
) -> pd.DataFrame:
    """Network Stress Index = total traffic / total active lines per period.

    Higher values indicate more pressure on the network infrastructure.
    """
    agg = df.groupby(time_col).agg({traffic_col: "sum", lines_col: "sum"}).reset_index()
    agg["network_stress_index"] = agg[traffic_col] / agg[lines_col]
    return agg[[time_col, "network_stress_index"]]


def infrastructure_elasticity_margin(
    df: pd.DataFrame,
    revenue_col: str = "ingresos",
    traffic_col: str = "trafico",
    lines_col: str = "lineas_o_accesos",
    time_col: str = "trimestre",
) -> pd.DataFrame:
    """Infrastructure Elasticity Margin = cost per TB / avg revenue per line.

    Approximates unit cost structure deterioration over time.

    revenue_per_line = total revenue / total lines
    traffic_per_line = total traffic / total lines

    Higher traffic per line with flat revenue per line → margin compression.
    """
    agg = (
        df.groupby(time_col)
        .agg({revenue_col: "sum", traffic_col: "sum", lines_col: "sum"})
        .reset_index()
    )
    agg["revenue_per_line"] = agg[revenue_col] / agg[lines_col]
    agg["traffic_per_line"] = agg[traffic_col] / agg[lines_col]
    agg["revenue_per_traffic_unit"] = agg[revenue_col] / agg[traffic_col]
    return agg[[time_col, "revenue_per_line", "traffic_per_line", "revenue_per_traffic_unit"]]


def macro_contribution_ratio(
    telecom_revenue: pd.DataFrame,
    gdp: pd.DataFrame,
    time_col: str = "year",
    revenue_col: str = "ingresos",
    gdp_col: str = "value_num",
) -> pd.DataFrame:
    """Macro Contribution Ratio = total telecom revenue / GDP.

    Measures the weight of the telecom sector in the economy.
    """
    annual_revenue = telecom_revenue.groupby(time_col)[revenue_col].sum().reset_index()
    merged = annual_revenue.merge(gdp, on=time_col, how="left")
    merged["macro_contribution_ratio"] = merged[revenue_col] / merged[gdp_col]
    return merged[[time_col, "macro_contribution_ratio"]]


def digital_density_margin(
    lines: pd.DataFrame,
    population: pd.DataFrame,
    time_col: str = "year",
    lines_col: str = "lineas_o_accesos",
    pop_col: str = "value_num",
) -> pd.DataFrame:
    """Digital Density Margin = active lines / population * 100.

    Penetration rate per 100 inhabitants.
    """
    annual_lines = lines.groupby(time_col)[lines_col].sum().reset_index()
    merged = annual_lines.merge(population, on=time_col, how="left")
    merged["digital_density"] = merged[lines_col] / merged[pop_col] * 100
    return merged[[time_col, "digital_density"]]


def cagr(series: pd.Series) -> float:
    """Compound Annual Growth Rate over a time series."""
    if len(series) < 2:
        return np.nan
    start = series.iloc[0]
    end = series.iloc[-1]
    n = len(series) - 1
    if start <= 0 or end <= 0:
        return np.nan
    return (end / start) ** (1 / n) - 1


def traffic_vs_revenue_cagr(
    df: pd.DataFrame,
    traffic_col: str = "trafico",
    revenue_col: str = "ingresos",
    time_col: str = "trimestre",
) -> dict:
    """Compare CAGR of traffic vs revenue — the 'scissors effect'."""
    agg = df.groupby(time_col).agg({traffic_col: "sum", revenue_col: "sum"}).reset_index()
    traffic_cagr = cagr(agg[traffic_col])
    revenue_cagr = cagr(agg[revenue_col])
    return {
        "traffic_cagr": round(traffic_cagr * 100, 2),
        "revenue_cagr": round(revenue_cagr * 100, 2),
        "gap_pp": round((traffic_cagr - revenue_cagr) * 100, 2),
    }


if __name__ == "__main__":
    # Test with synthetic data
    np.random.seed(42)
    test = pd.DataFrame({
        "trimestre": ["2020T1"] * 3 + ["2020T2"] * 3,
        "operador": ["A", "B", "C"] * 2,
        "ingresos": np.random.uniform(100, 500, 6),
        "trafico": np.random.uniform(1000, 5000, 6),
        "lineas_o_accesos": np.random.uniform(100, 300, 6),
    })
    print("HHI:\n", hhi_quarterly(test))
    print("NSI:\n", network_stress_index(test))
    print("CAGR:", traffic_vs_revenue_cagr(test))
