import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path
from typing import Optional

_src = Path(__file__).resolve().parent
_project_root = _src.parents[2]
DB_PATH = _project_root / "data" / "processed" / "net_tension.duckdb"
if not DB_PATH.exists():
    DB_PATH = Path.cwd() / "data" / "processed" / "net_tension.duckdb"

PARQUET_DIR = _project_root / "data" / "processed"
PARQUET_DIR.mkdir(parents=True, exist_ok=True)

@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH), read_only=True)


def _parquet_path(name: str) -> Path:
    return PARQUET_DIR / f"{name}.parquet"


def _load_parquet(name: str) -> Optional[pd.DataFrame]:
    path = _parquet_path(name)
    if not path.exists():
        return None
    try:
        con = duckdb.connect()
        return con.execute(f"SELECT * FROM read_parquet('{path.as_posix()}')").df()
    except Exception:
        return None


def _save_parquet(name: str, df: pd.DataFrame) -> None:
    path = _parquet_path(name)
    try:
        con = duckdb.connect()
        con.register("tmp_df", df)
        con.execute(f"COPY tmp_df TO '{path.as_posix()}' (FORMAT PARQUET)")
    except Exception:
        pass


def _load_table(name: str, query: str) -> pd.DataFrame:
    df = _load_parquet(name)
    if df is not None:
        return df
    df = get_connection().execute(query).df()
    _save_parquet(name, df)
    return df

@st.cache_data(ttl=3600)
def load_fact_observed() -> pd.DataFrame:
    return _load_table("fact_observed_agg", "SELECT * FROM fact_observed_agg ORDER BY trimestre_dt")

@st.cache_data(ttl=3600)
def load_hhi() -> pd.DataFrame:
    return _load_table("kpi_hhi", "SELECT * FROM kpi_hhi ORDER BY trimestre_dt")

@st.cache_data(ttl=3600)
def load_eu_context() -> pd.DataFrame:
    return _load_table("dim_eu_context", "SELECT * FROM dim_eu_context")

@st.cache_data(ttl=3600)
def load_sources() -> pd.DataFrame:
    import yaml
    sources_path = Path(__file__).parents[2] / "data" / "SOURCES.yaml"
    with open(sources_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    rows = []
    for key, value in data.items():
        if key == "future_sources":
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict):
                    sub_value["source_name"] = sub_key
                    sub_value["governance_layer"] = "FUTURE"
                    rows.append(sub_value)
        elif isinstance(value, dict) and "governance_layer" in value:
            value["source_name"] = key
            rows.append(value)
    return pd.DataFrame(rows)

@st.cache_data
def get_kpis() -> dict:
    fact = load_fact_observed()
    hhi = load_hhi()

    def _safe_first(df, col, year):
        vals = df[df["year"] == year][col].values
        return vals[0] if len(vals) > 0 else None

    def _safe_last(df, col, year):
        vals = df[df["year"] == year][col].values
        return vals[-1] if len(vals) > 0 else None

    def _safe_mean(df, col, year=None):
        if year is not None:
            vals = df[df["year"] == year][col]
        else:
            vals = df[col]
        return vals.mean() if len(vals) > 0 else 0

    years = sorted(fact["year"].unique())
    start_year = years[0]
    end_year = years[-1]
    periods = end_year - start_year

    traffic_start = _safe_first(fact, "data_traffic", start_year)
    traffic_end = _safe_last(fact, "data_traffic", end_year)
    rev_start = _safe_first(fact, "revenue", start_year)
    rev_end = _safe_last(fact, "revenue", end_year)

    traffic_cagr = (traffic_end / traffic_start) ** (1 / periods) - 1 if (traffic_start and traffic_end and traffic_start > 0) else 0
    rev_cagr = (rev_end / rev_start) ** (1 / periods) - 1 if (rev_start and rev_end and rev_start > 0) else 0

    hhi_2005 = _safe_mean(hhi, "hhi", start_year)
    hhi_end = _safe_mean(hhi, "hhi", end_year)

    return {
        "traffic_cagr": traffic_cagr,
        "rev_cagr": rev_cagr,
        "cagr_gap": traffic_cagr - rev_cagr,
        "avg_nsi": _safe_mean(fact, "nsi"),
        "avg_arpu": _safe_mean(fact, "revenue_per_line"),
        "hhi_2005": hhi_2005,
        "hhi_2025": hhi_end,
        "hhi_delta": hhi_end - hhi_2005,
    }


def filter_by_year(df: pd.DataFrame, year_range: tuple) -> pd.DataFrame:
    yr_min, yr_max = year_range
    return df[(df["year"] >= yr_min) & (df["year"] <= yr_max)]
