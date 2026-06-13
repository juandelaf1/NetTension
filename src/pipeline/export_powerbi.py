"""
NetTension — Export consolidated datasets for Power BI.

Creates:
  1. fact_observed_agg.parquet — Aggregated quarterly metrics (83 rows)
  2. fact_eurostat_es.parquet — Spain Eurostat data (66 rows)
  3. kpi_hhi_clean.parquet — HHI with classification (83 rows)
  4. dim_eu_context.parquet — European context data (21 indicators)
  5. dim_time.parquet — Time dimension (83 quarters)
  6. dim_operator.parquet — Operator reference table (31 operators)
  7. dim_service.parquet — Service/concept dimension
"""
import pandas as pd
import numpy as np
from pathlib import Path

PROC = Path(__file__).parents[2] / "data" / "processed"


def export_fact_observed():
    """Aggregate CNMC Mercados into quarterly fact table."""
    df = pd.read_parquet(PROC / "cnmc_mercados_clean.parquet")

    # Data traffic (KB, MB, GB or whatever units — relative index works)
    data_traffic = df.groupby("trimestre_dt").agg(
        data_traffic=("trafico_de_datos", "sum"),
    ).reset_index().sort_values("trimestre_dt")

    # Voice traffic
    voice = df[df["concepto"].str.contains("minutos", na=False, case=False)]
    voice_traffic = voice.groupby("trimestre_dt").agg(
        voice_traffic=("trafico", "sum"),
    ).reset_index().sort_values("trimestre_dt")

    # Revenue
    ing = df[df["concepto"] == "Ingresos"]
    revenue = ing.groupby("trimestre_dt").agg(
        revenue=("ingresos", "sum"),
    ).reset_index().sort_values("trimestre_dt")

    # Lines (total active lines per quarter)
    lines = df.groupby("trimestre_dt").agg(
        total_lines=("lineas_o_accesos", "sum"),
    ).reset_index().sort_values("trimestre_dt")

    # Merge
    result = data_traffic.merge(voice_traffic, on="trimestre_dt", how="outer")
    result = result.merge(revenue, on="trimestre_dt", how="outer")
    result = result.merge(lines, on="trimestre_dt", how="outer")
    result = result.fillna(0)

    # Derived KPIs
    result["data_traffic_index"] = (
        result["data_traffic"] / result["data_traffic"].iloc[0] * 100
        if result["data_traffic"].iloc[0] > 0 else 0
    )
    result["revenue_index"] = (
        result["revenue"] / result["revenue"].iloc[0] * 100
        if result["revenue"].iloc[0] > 0 else 0
    )
    result["nsi"] = np.where(
        result["total_lines"] > 0,
        result["data_traffic"] / result["total_lines"],
        0,
    )
    result["revenue_per_traffic"] = np.where(
        result["data_traffic"] > 0,
        result["revenue"] / result["data_traffic"],
        0,
    )
    result["revenue_per_line"] = np.where(
        result["total_lines"] > 0,
        result["revenue"] / result["total_lines"],
        0,
    )

    result["year"] = result["trimestre_dt"].dt.year
    result["quarter"] = result["trimestre_dt"].dt.quarter

    result.to_parquet(PROC / "fact_observed_agg.parquet", index=False)
    print(f"fact_observed_agg: {len(result)} rows, {len(result.columns)} cols")
    print(f"  Period: {result['trimestre_dt'].min()} -> {result['trimestre_dt'].max()}")
    return result


def export_eurostat_es():
    """Spain-specific Eurostat data."""
    pop = pd.read_parquet(PROC / "eurostat_demo_pjan_tidy.parquet")
    gdp = pd.read_parquet(PROC / "eurostat_nama_10_gdp_tidy.parquet")

    # Population: ES, age=TOTAL, sex=T
    pop_es = pop[
        (pop["geo"] == "ES")
        & (pop["age"] == "TOTAL")
        & (pop["sex"] == "T")
    ].copy()
    pop_es["year"] = pd.to_numeric(pop_es["time_period"], errors="coerce")
    pop_es = pop_es.dropna(subset=["year", "value_num"])
    pop_es = pop_es[["year", "value_num"]].rename(columns={"value_num": "population"})
    pop_es["year"] = pop_es["year"].astype(int)
    pop_es = pop_es.sort_values("year")

    # GDP: ES, na_item=B1G (GDP at market prices), unit=CP_MEUR (current prices)
    gdp_es = gdp[
        (gdp["geo"] == "ES")
        & (gdp["na_item"] == "B1G")
        & (gdp["unit"] == "CP_MEUR")
    ].copy()
    gdp_es["year"] = pd.to_numeric(gdp_es["time_period"], errors="coerce")
    gdp_es = gdp_es.dropna(subset=["year", "value_num"])
    gdp_es = gdp_es[["year", "value_num"]].rename(columns={"value_num": "gdp_meur"})
    gdp_es["year"] = gdp_es["year"].astype(int)
    gdp_es = gdp_es.sort_values("year")

    # Merge
    result = pop_es.merge(gdp_es, on="year", how="outer")
    result["gdp_per_capita"] = result["gdp_meur"] / result["population"] * 1_000_000

    result.to_parquet(PROC / "fact_eurostat_es.parquet", index=False)
    print(f"\nfact_eurostat_es: {len(result)} rows")
    print(f"  Years: {int(result['year'].min())} -> {int(result['year'].max())}")
    print(f"  Population 2025: {result[result['year']==2025]['population'].values[0]:.0f}")
    print(f"  GDP 2025: {result[result['year']==2025]['gdp_meur'].values[0]:.0f} Mn EUR")
    return result


def export_hhi():
    """Compute and export HHI with classification."""
    import sys
    sys.path.insert(0, str(Path(__file__).parents[1]))
    from loader.cnmc_loader import load_mercados
    from transform.data_cleaner import clean_mercados
    from transform.kpi_engine import hhi_quarterly

    df = clean_mercados(load_mercados())
    hhi_raw = hhi_quarterly(df)

    # Parse trimestre and add datetime
    hhi_raw["trimestre_dt"] = pd.to_datetime(
        hhi_raw["trimestre"].str.extract(r"(\d{4})T(\d)").apply(
            lambda r: f"{r[0]}-{int(r[1])*3-2:02d}-01", axis=1
        )
    )
    hhi_raw["year"] = hhi_raw["trimestre_dt"].dt.year

    hhi_raw["classification"] = pd.cut(
        hhi_raw["hhi"],
        bins=[0, 1000, 2500, 99999],
        labels=["Competitive", "Moderately Concentrated", "Highly Concentrated"],
    )

    hhi_raw.to_parquet(PROC / "kpi_hhi.parquet", index=False)
    print(f"\nkpi_hhi: {len(hhi_raw)} rows, range [{hhi_raw['hhi'].min():.0f}, {hhi_raw['hhi'].max():.0f}]")
    print(f"  First: HHI={hhi_raw['hhi'].iloc[0]:.0f} ({hhi_raw['classification'].iloc[0]}, {hhi_raw['trimestre'].iloc[0]})")
    print(f"  Last:  HHI={hhi_raw['hhi'].iloc[-1]:.0f} ({hhi_raw['classification'].iloc[-1]}, {hhi_raw['trimestre'].iloc[-1]})")


def export_eu_context():
    """Create a reference table with European context data from ETNO/GSMA."""
    context = pd.DataFrame([
        {"indicator": "EU Mobile Revenue (2023)", "value": 163, "unit": "Bn EUR",
         "source": "GSMA Mobile Economy Europe 2025"},
        {"indicator": "EU Operator CAPEX (2023)", "value": 57.9, "unit": "Bn EUR",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "EU CAPEX per capita", "value": 118, "unit": "EUR",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "USA CAPEX per capita", "value": 226, "unit": "EUR",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "Japan CAPEX per capita", "value": 188, "unit": "EUR",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "South Korea CAPEX per capita", "value": 173, "unit": "EUR",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "EU Mobile ARPU (2023)", "value": 14.8, "unit": "EUR/month",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "USA Mobile ARPU", "value": 41.7, "unit": "EUR/month",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "South Korea Mobile ARPU", "value": 26.0, "unit": "EUR/month",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "Japan Mobile ARPU", "value": 22.6, "unit": "EUR/month",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "EU 5G Adoption (2024)", "value": 30, "unit": "% of connections",
         "source": "GSMA Mobile Economy Europe 2025"},
        {"indicator": "EU 5G Adoption (2030 projected)", "value": 80, "unit": "% of connections",
         "source": "GSMA Mobile Economy Europe 2025"},
        {"indicator": "Mobile contribution to EU GDP", "value": 5.0, "unit": "%",
         "source": "GSMA Mobile Economy Europe 2025"},
        {"indicator": "Mobile contribution EU GDP value", "value": 1.1, "unit": "Tn EUR",
         "source": "GSMA Mobile Economy Europe 2025"},
        {"indicator": "EU Mobile Subscribers (2024)", "value": 520, "unit": "M",
         "source": "GSMA Mobile Economy Europe 2025"},
        {"indicator": "Mobile internet usage gap Europe", "value": 19, "unit": "%",
         "source": "GSMA Mobile Economy Europe 2025"},
        {"indicator": "EU 5G population coverage (2024)", "value": 94.3, "unit": "%",
         "source": "EU 5G Observatory 2025"},
        {"indicator": "Video share of internet traffic", "value": 65, "unit": "%",
         "source": "Sandvine GIPR 2024"},
        {"indicator": "Big 6 share of internet traffic", "value": 50, "unit": "%",
         "source": "Sandvine GIPR 2024"},
        {"indicator": "EU ROCE (2023)", "value": 5.9, "unit": "%",
         "source": "ETNO State of Digital Comms 2025"},
        {"indicator": "EU Revenue real growth (2023)", "value": -4.4, "unit": "%",
         "source": "ETNO State of Digital Comms 2025"},
    ])
    context.to_parquet(PROC / "dim_eu_context.parquet", index=False)
    print(f"\ndim_eu_context: {len(context)} indicators")

    # Also save as CSV for easy reference
    context.to_csv(PROC / "dim_eu_context.csv", index=False)


def export_dimensions():
    """Create dimension tables for Power BI star schema."""
    df = pd.read_parquet(PROC / "cnmc_mercados_clean.parquet")

    # Dim_Time: one row per quarter
    time_df = df[["trimestre_dt"]].drop_duplicates().sort_values("trimestre_dt").reset_index(drop=True)
    time_df["year"] = time_df["trimestre_dt"].dt.year
    time_df["quarter"] = time_df["trimestre_dt"].dt.quarter
    time_df["year_quarter"] = time_df["year"].astype(str) + " Q" + time_df["quarter"].astype(str)
    time_df["time_key"] = time_df["trimestre_dt"]
    time_df = time_df[["time_key", "trimestre_dt", "year", "quarter", "year_quarter"]]
    time_df.to_parquet(PROC / "dim_time.parquet", index=False)
    print(f"\ndim_time: {len(time_df)} quarters ({time_df['year'].min()}-{time_df['year'].max()})")

    # Dim_Operator: distinct operators with group classification
    operator_map = {
        "Telefónica de España": "Incumbent",
        "Telefónica Móviles España": "Incumbent",
        "Movistar": "Incumbent",
        "Vodafone España": "Competitor",
        "Vodafone": "Competitor",
        "Orange España": "Competitor",
        "Orange": "Competitor",
        "Orange España Comunicaciones Fijas": "Competitor",
        "Orange Spain": "Competitor",
        "MÁSMÓVIL": "Competitor",
        "MásMóvil": "Competitor",
        "Grupo MASMOVIL": "Competitor",
        "MASORANGE": "Competitor",
        "Yoigo": "Competitor",
        "Xfera Móviles": "Competitor",
        "Euskaltel": "Regional",
        "R Cable y Telecomunicaciones": "Regional",
        "R Cable": "Regional",
        "Telecable de Asturias": "Regional",
        "Telecable": "Regional",
        "Adam Internet": "Regional",
        "APDCAN": "Regional",
        "Grupo MásMóvil": "Competitor",
    }
    op_df = df[["operador"]].drop_duplicates().reset_index(drop=True)
    op_df["operator_group"] = op_df["operador"].map(operator_map).fillna("Other")
    op_df["is_incumbent"] = op_df["operator_group"] == "Incumbent"
    op_df = op_df.rename(columns={"operador": "operator_key"})
    op_df.to_parquet(PROC / "dim_operator.parquet", index=False)
    print(f"dim_operator: {len(op_df)} operators")

    # Dim_Service: distinct service/concept combos
    svc_df = df[["servicio", "concepto"]].drop_duplicates().reset_index(drop=True)
    svc_df["service_key"] = svc_df["servicio"] + " | " + svc_df["concepto"]
    svc_df["market_type"] = np.where(
        svc_df["servicio"].str.lower().str.contains("mayorista"), "Mayorista", "Minorista"
    )

    def categorize_concept(c):
        c = str(c).lower()
        if "voz" in c or "minuto" in c or "llamada" in c:
            return "Voice"
        elif "dato" in c or "internet" in c or "banda" in c:
            return "Data"
        elif "acceso" in c or "linea" in c or "bucle" in c:
            return "Access"
        elif "audiovisual" in c or "television" in c or "tv" in c:
            return "Audiovisual"
        elif "ingreso" in c or "cuota" in c or "abonado" in c:
            return "Revenue"
        elif "portabilidad" in c:
            return "Portability"
        else:
            return "Other"

    svc_df["category"] = svc_df["concepto"].apply(categorize_concept)
    svc_df = svc_df[["service_key", "servicio", "concepto", "market_type", "category"]]
    svc_df.to_parquet(PROC / "dim_service.parquet", index=False)
    print(f"dim_service: {len(svc_df)} service/concept combos")

    # Dim_Geography
    geo_df = pd.DataFrame([{
        "geography_key": "ES", "pais": "España", "geo_code": "ES", "region": "EU"
    }])
    geo_df.to_parquet(PROC / "dim_geography.parquet", index=False)
    print(f"dim_geography: {len(geo_df)} country")


if __name__ == "__main__":
    print("Exporting Power BI datasets...")
    export_fact_observed()
    export_eurostat_es()
    export_hhi()
    export_eu_context()
    export_dimensions()

    print("\n\nFiles ready for Power BI import (select all .parquet):")
    import os
    for f in sorted(Path(PROC).glob("*.parquet")):
        size_mb = os.path.getsize(f) / 1e6
        print(f"  {f.name}: {size_mb:.1f} MB")
    print(f"\nTotal: {len(list(Path(PROC).glob('*.parquet')))} files")
    print("\nImport all .parquet files at once using:")
    print("   Power BI → Get Data → Parquet → Select ALL files in data/processed/")
