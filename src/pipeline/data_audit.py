"""
NetTension — Data Quality Audit

Runs after ETL pipeline to verify data integrity,
profile key variables, and identify issues.
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"


def audit_mercados():
    print("=" * 60)
    print("AUDIT: CNMC Mercados")
    print("=" * 60)

    df = pd.read_parquet(PROCESSED_DIR / "cnmc_mercados_clean.parquet")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Period: {df['trimestre'].min()} -> {df['trimestre'].max()}")

    # Traffic by concept
    print("\n--- Traffic Concepts ---")
    traffic_rows = df[df["concepto"].str.contains("Tráfico", na=False, case=False)]
    summary = traffic_rows.groupby("concepto").agg(
        rows=("trafico", "count"),
        non_null=("trafico", lambda x: x.notna().sum()),
        mean=("trafico", "mean"),
    )
    print(summary.to_string())

    # Revenue concepts
    print("\n--- Revenue ---")
    ing = df[df["concepto"] == "Ingresos"]
    print(f"Ingresos rows: {len(ing)}, non-null: {ing['ingresos'].notna().sum()}")

    # Traffic over time (aggregate)
    print("\n--- Annual Traffic (sum, all concepts) ---")
    df["year"] = df["trimestre_dt"].dt.year
    annual = df.groupby("year").agg(
        traffic_sum=("trafico", "sum"),
        traffic_n=("trafico", "count"),
        revenue_sum=("ingresos", "sum"),
        revenue_n=("ingresos", "count"),
    )
    for yr, row in annual.iterrows():
        print(f"  {int(yr)}: traffic={row['traffic_sum']:.0f} (n={int(row['traffic_n'])}), revenue={row['revenue_sum']:.0f} (n={int(row['revenue_n'])})")

    return df


def audit_generales():
    print("\n" + "=" * 60)
    print("AUDIT: CNMC Datos Generales")
    print("=" * 60)

    df = pd.read_parquet(PROCESSED_DIR / "cnmc_datos_generales_clean.parquet")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Period: {df['trimestre'].min()} -> {df['trimestre'].max()}")
    print(f"Operators: {sorted(df['operador'].dropna().unique())}")
    print(f"Concepts: {sorted(df['concepto'].dropna().unique())}")

    # Revenue over time
    ing = df[df["concepto"] == "Ingresos"]
    print(f"\nIngresos rows: {len(ing)}")
    if not ing.empty:
        print(f"Non-null ingresos: {ing['ingresos_por_operador'].notna().sum()}")
        print(f"Sample:\n{ing.head(10).to_string()}")


def audit_eurostat():
    print("\n" + "=" * 60)
    print("AUDIT: Eurostat")
    print("=" * 60)

    pop = pd.read_parquet(PROCESSED_DIR / "eurostat_demo_pjan_tidy.parquet")
    gdp = pd.read_parquet(PROCESSED_DIR / "eurostat_nama_10_gdp_tidy.parquet")

    print(f"Population: {len(pop):,} rows, cols: {list(pop.columns)}")
    print(f"  Years: {pop['time_period'].min()} -> {pop['time_period'].max()}")
    print(f"  GEOs: {sorted(pop[pop['geo'].str.len() == 2]['geo'].unique())}")

    print(f"\nGDP: {len(gdp):,} rows, cols: {list(gdp.columns)}")
    print(f"  Years: {gdp['time_period'].min()} -> {gdp['time_period'].max()}")
    print(f"  GEOs: {sorted(gdp[gdp['geo'].str.len() == 2]['geo'].unique())}")


def check_cagr():
    """Check why CAGR was 0.57% — likely wrong."""
    print("\n" + "=" * 60)
    print("CAGR DIAGNOSTIC")
    print("=" * 60)

    df = pd.read_parquet(PROCESSED_DIR / "cnmc_mercados_clean.parquet")

    # Total traffic per trimestre
    agg = df.groupby("trimestre").agg(
        traffic=("trafico", "sum"),
        revenue=("ingresos", "sum"),
    ).reset_index()

    # Sort by trimestre (string sort is correct for T1..T4 within year)
    agg = agg.sort_values("trimestre")
    print(f"Traffic series: {len(agg)} periods")
    print(f"  First: {agg.iloc[0]['trimestre']} = {agg.iloc[0]['traffic']:.0f}")
    print(f"  Last:  {agg.iloc[-1]['trimestre']} = {agg.iloc[-1]['traffic']:.0f}")
    print(f"  Growth factor: {agg.iloc[-1]['traffic'] / agg.iloc[0]['traffic']:.2f}x")

    # Check if traffic data is spread across multiple concepts that shouldn't be summed
    print("\n--- Traffic by service over time ---")
    df["year"] = df["trimestre_dt"].dt.year
    traffic_df = df[df["concepto"].str.contains("Tráfico", na=False, case=False)]
    by_svc = traffic_df.groupby(["year", "servicio"]).agg(
        traffic=("trafico", "sum")
    ).reset_index()
    for yr in sorted(by_svc["year"].unique())[::5]:
        subset = by_svc[by_svc["year"] == yr].sort_values("traffic", ascending=False)
        print(f"  {int(yr)}:")
        for _, r in subset.iterrows():
            print(f"    {r['servicio'][:40]}: {r['traffic']:.0f}")


if __name__ == "__main__":
    audit_mercados()
    audit_generales()
    audit_eurostat()
    check_cagr()
