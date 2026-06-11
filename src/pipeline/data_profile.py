"""
NetTension — Data Profile

Detailed profiling of cleaned data for analysis planning.
"""
import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(__file__).parents[2] / "data" / "processed"

df = pd.read_parquet(PROCESSED_DIR / "cnmc_mercados_clean.parquet")

print("UNIQUE CONCEPTS (repr):")
for c in sorted(df["concepto"].dropna().unique()):
    print(f"  {repr(c)}")

print("\nTRAFFIC CONCEPT SEARCH:")
for pat in ["fico", "datos", "minutos", "mensajes"]:
    mask = df["concepto"].str.contains(pat, na=False, case=False)
    print(f"  '{pat}': {mask.sum()} rows")
    if mask.any():
        for c in df.loc[mask, "concepto"].unique():
            print(f"    -> {repr(c)}")

print("\nSERVICES (all):")
for s in sorted(df["servicio"].dropna().unique()):
    print(f"  {repr(s)}")

print("\nTRAFFIC BY SERVICE (concepts matching 'Tráfico'):")
idx = df["concepto"].str.contains("Tráfico", na=False)
traffic = df[idx].copy()
print(f"  Total rows: {len(traffic)}")
print(f"  Non-null trafico: {traffic['trafico'].notna().sum()}")

print("\n  Group by servicio + concepto:")
for (svc, conc), grp in traffic.groupby(["servicio", "concepto"]):
    nn = grp["trafico"].notna().sum()
    mean_v = grp["trafico"].mean()
    total = grp["trafico"].sum()
    print(f"  [{svc}] [{conc}]: rows={len(grp)}, nonnull={nn}, mean={mean_v:.1f}, total={total:.0f}")

print("\nTRAFFIC OVER TIME (data, not minutes):")
data_traf = traffic[traffic["concepto"].str.contains("datos", na=False, case=False)]
if not data_traf.empty:
    data_traf["year"] = data_traf["trimestre_dt"].dt.year
    by_year = data_traf.groupby("year").agg(
        traffic=("trafico", "sum"),
        rows=("trafico", "count"),
    )
    for yr, row in by_year.iterrows():
        print(f"  {int(yr)}: traffic={row['traffic']:.0f}")
else:
    print("  No data traffic found with 'datos' pattern")
    print(f"  All unique concepts: {sorted(traffic['concepto'].unique())}")

print("\nVOICE TRAFFIC OVER TIME:")
voice_traf = traffic[traffic["concepto"].str.contains("minutos", na=False, case=False)]
if not voice_traf.empty:
    voice_traf["year"] = voice_traf["trimestre_dt"].dt.year
    by_year = voice_traf.groupby("year").agg(
        traffic=("trafico", "sum"),
        rows=("trafico", "count"),
    )
    for yr, row in by_year.iterrows():
        print(f"  {int(yr)}: traffic={row['traffic']:.0f} (minutos)")

# Check units
print("\nTRAFFIC UNITS:")
print(traffic["unidades"].value_counts(dropna=False))

print("\nDATA TRAFFIC (trafico_de_datos):")
datos = df[df["trafico_de_datos"].notna()]
if not datos.empty:
    print(f"  Rows: {len(datos)}")
    datos["year"] = datos["trimestre_dt"].dt.year
    by_year = datos.groupby("year").agg(
        traffic=("trafico_de_datos", "sum"),
    )
    for yr, row in by_year.iterrows():
        print(f"  {int(yr)}: traffic_de_datos={row['traffic']:.0f}")
else:
    print("  No data")

# Revenue profile
print("\nREVENUE INGRESOS (by service):")
ing = df[df["concepto"] == "Ingresos"]
for svc, grp in ing.groupby("servicio"):
    nn = grp["ingresos"].notna().sum()
    total = grp["ingresos"].sum()
    print(f"  {svc}: rows={len(grp)}, nonnull={nn}, total={total:.0f}")

print("\nREVENUE INGRESOS_POR_OPERADOR (by service):")
for svc, grp in ing.groupby("servicio"):
    nn = grp["ingresos_por_operador"].notna().sum()
    total = grp["ingresos_por_operador"].sum()
    print(f"  {svc}: rows={len(grp)}, nonnull={nn}, total={total:.0f}")

# Units
print("\nUNITS FOR INGRESOS:")
print(ing["unidades"].value_counts(dropna=False))
