import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path
import os

_src = Path(__file__).resolve().parent
# Walk up from utils/ to find project root (contains data/processed/)
_project_root = _src.parents[2]  # streamlit_app/utils -> streamlit_app -> project
DB_PATH = _project_root / "data" / "processed" / "net_tension.duckdb"
# Fallback: try cwd (for when streamlit is run from project root)
if not DB_PATH.exists():
    DB_PATH = Path.cwd() / "data" / "processed" / "net_tension.duckdb"

@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH), read_only=True)

@st.cache_data(ttl=3600)
def load_fact_observed() -> pd.DataFrame:
    con = get_connection()
    return con.execute("SELECT * FROM fact_observed_agg ORDER BY trimestre_dt").df()

@st.cache_data(ttl=3600)
def load_hhi() -> pd.DataFrame:
    con = get_connection()
    return con.execute("SELECT * FROM kpi_hhi ORDER BY trimestre_dt").df()

@st.cache_data(ttl=3600)
def load_eu_context() -> pd.DataFrame:
    con = get_connection()
    return con.execute("SELECT * FROM dim_eu_context").df()

@st.cache_data(ttl=3600)
def load_dim_operator() -> pd.DataFrame:
    con = get_connection()
    return con.execute("SELECT * FROM dim_operator").df()

@st.cache_data(ttl=3600)
def load_dim_service() -> pd.DataFrame:
    con = get_connection()
    return con.execute("SELECT * FROM dim_service").df()

@st.cache_data(ttl=3600)
def load_sources() -> pd.DataFrame:
    import yaml
    sources_path = Path(__file__).parents[3] / "data" / "SOURCES.yaml"
    with open(sources_path) as f:
        data = yaml.safe_load(f)
    rows = []
    for layer, vars in data.items():
        for var in vars:
            var["governance_layer"] = layer
            rows.append(var)
    return pd.DataFrame(rows)

@st.cache_data
def get_kpis() -> dict:
    fact = load_fact_observed()
    hhi = load_hhi()
    
    traffic_start = fact[fact["year"]==2005]["data_traffic"].values[0]
    traffic_end = fact[fact["year"]==2025]["data_traffic"].values[-1]
    rev_start = fact[fact["year"]==2005]["revenue"].values[0]
    rev_end = fact[fact["year"]==2025]["revenue"].values[-1]
    
    periods = 20
    traffic_cagr = (traffic_end / traffic_start) ** (1/periods) - 1 if traffic_start else 0
    rev_cagr = (rev_end / rev_start) ** (1/periods) - 1 if rev_start else 0
    
    return {
        "traffic_cagr": traffic_cagr,
        "rev_cagr": rev_cagr,
        "cagr_gap": traffic_cagr - rev_cagr,
        "avg_nsi": fact["nsi"].mean(),
        "avg_arpu": fact["revenue_per_line"].mean(),
        "hhi_2005": hhi[hhi["year"]==2005]["hhi"].mean(),
        "hhi_2025": hhi[hhi["year"]==2025]["hhi"].mean(),
        "hhi_delta": hhi[hhi["year"]==2025]["hhi"].mean() - hhi[hhi["year"]==2005]["hhi"].mean(),
    }

def filter_by_year(df: pd.DataFrame, year_range: tuple) -> pd.DataFrame:
    yr_min, yr_max = year_range
    return df[(df["year"] >= yr_min) & (df["year"] <= yr_max)]