"""
NetTension — Master ETL Pipeline

Orchestrates all data loading, cleaning, and KPI computation.
Output: processed parquet files ready for Power BI.

Layer 1: CNMC Mercados (union 5 files + clean)
Layer 2: CNMC Datos Generales
Layer 3: Eurostat (population + GDP)
Layer 4: KPIs (HHI, NSI, CAGR, Elasticity Margin)
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).parents[1]
sys.path.insert(0, str(SRC_DIR))

from loader.cnmc_loader import load_mercados
from loader.datos_generales_loader import load_datos_generales
from loader.eurostat_loader import load_demo_pjan, load_nama_gdp
from transform.data_cleaner import clean_mercados, clean_datos_generales
from transform.kpi_engine import (
    hhi_quarterly,
    network_stress_index,
    infrastructure_elasticity_margin,
    traffic_vs_revenue_cagr,
)

PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"


def run_pipeline():
    print("=" * 60)
    print("NetTension — ETL Pipeline")
    print("=" * 60)

    # Layer 1: CNMC Mercados
    print("\n--- Layer 1: CNMC Mercados ---")
    mercados_raw = load_mercados()
    mercados_clean = clean_mercados(mercados_raw)
    print(f"  Clean: {len(mercados_clean)} rows, {len(mercados_clean.columns)} cols")
    print(f"  Period: {mercados_clean['trimestre'].min()} -> {mercados_clean['trimestre'].max()}")
    print(f"  Operators: {sorted(mercados_clean['operador'].dropna().unique())}")
    print(f"  Services: {sorted(mercados_clean['servicio'].dropna().unique())}")
    print(f"  Concepts: {sorted(mercados_clean['concepto'].dropna().unique())}")

    # Layer 2: CNMC Datos Generales
    print("\n--- Layer 2: CNMC Datos Generales ---")
    generales_raw = load_datos_generales()
    generales_clean = clean_datos_generales(generales_raw)
    print(f"  Clean: {len(generales_clean)} rows, {len(generales_clean.columns)} cols")
    print(f"  Period: {generales_clean['trimestre'].min()} -> {generales_clean['trimestre'].max()}")

    # Layer 3: Eurostat
    print("\n--- Layer 3: Eurostat ---")
    pop = load_demo_pjan()
    gdp = load_nama_gdp()
    print(f"  Population: {len(pop)} rows")
    print(f"  GDP: {len(gdp)} rows")

    # Layer 4: KPIs from Mercados
    print("\n--- Layer 4: KPI Computation ---")
    hhi = hhi_quarterly(mercados_clean, value_col="ingresos_por_operador")
    print(f"  HHI computed: {len(hhi)} quarters")
    print(f"  HHI range: [{hhi['hhi'].min():.0f}, {hhi['hhi'].max():.0f}]")

    nsi = network_stress_index(mercados_clean)
    print(f"  NSI computed: {len(nsi)} quarters")

    elasticity = infrastructure_elasticity_margin(mercados_clean)
    print(f"  Elasticity computed: {len(elasticity)} quarters")

    cagr_result = traffic_vs_revenue_cagr(mercados_clean)
    print(f"  CAGR: Traffic={cagr_result['traffic_cagr']}%, Revenue={cagr_result['revenue_cagr']}%, Gap={cagr_result['gap_pp']}pp")

    # Save everything
    print("\n--- Saving processed data ---")
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    mercados_clean.to_parquet(PROCESSED_DIR / "cnmc_mercados_clean.parquet", index=False)
    generales_clean.to_parquet(PROCESSED_DIR / "cnmc_datos_generales_clean.parquet", index=False)
    pop.to_parquet(PROCESSED_DIR / "eurostat_demo_pjan_tidy.parquet", index=False)
    gdp.to_parquet(PROCESSED_DIR / "eurostat_nama_10_gdp_tidy.parquet", index=False)
    hhi.to_parquet(PROCESSED_DIR / "kpi_hhi.parquet", index=False)
    nsi.to_parquet(PROCESSED_DIR / "kpi_nsi.parquet", index=False)
    elasticity.to_parquet(PROCESSED_DIR / "kpi_elasticity.parquet", index=False)

    print(f"\n  All files saved to: {PROCESSED_DIR}")
    return mercados_clean, generales_clean, pop, gdp, hhi, nsi, elasticity


if __name__ == "__main__":
    run_pipeline()
