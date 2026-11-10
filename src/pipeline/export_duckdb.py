"""
NetTension — Export consolidated datasets to DuckDB.

Creates net_tension.duckdb with all processed parquet files as SQL tables.
Versioned KPI/validation queries live in `sql/` (see sql/README.md).
"""

from pathlib import Path

import duckdb

ROOT = Path(__file__).parents[2]
PROC = ROOT / "data" / "processed"
SQL_DIR = ROOT / "sql"
RESULTS_DIR = ROOT / "reports" / "results"
DB_PATH = PROC / "net_tension.duckdb"

PARQUET_TABLES = {
    "fact_observed_agg": PROC / "fact_observed_agg.parquet",
    "fact_eurostat_es": PROC / "fact_eurostat_es.parquet",
    "kpi_hhi": PROC / "kpi_hhi.parquet",
    "kpi_nsi": PROC / "kpi_nsi.parquet",
    "kpi_elasticity": PROC / "kpi_elasticity.parquet",
    "dim_time": PROC / "dim_time.parquet",
    "dim_operator": PROC / "dim_operator.parquet",
    "dim_service": PROC / "dim_service.parquet",
    "dim_geography": PROC / "dim_geography.parquet",
    "dim_eu_context": PROC / "dim_eu_context.parquet",
    "cnmc_mercados_clean": PROC / "cnmc_mercados_clean.parquet",
    "cnmc_datos_generales_clean": PROC / "cnmc_datos_generales_clean.parquet",
    "eurostat_demo_pjan_tidy": PROC / "eurostat_demo_pjan_tidy.parquet",
    "eurostat_nama_10_gdp_tidy": PROC / "eurostat_nama_10_gdp_tidy.parquet",
}

# Ordered, versioned validation queries (files in sql/)
VALIDATION_QUERIES = [
    ("Scissors Effect (H1)", SQL_DIR / "01_scissors_effect_h1.sql"),
    ("HHI Trend (H2)", SQL_DIR / "02_hhi_trend_h2.sql"),
    ("NSI vs ARPU (H4)", SQL_DIR / "03_nsi_vs_arpu_h4.sql"),
    ("Macro Context (H5)", SQL_DIR / "04_macro_context_h5.sql"),
    ("Operator Count by Group", SQL_DIR / "05_operator_groups.sql"),
    ("Service Categories", SQL_DIR / "06_service_categories.sql"),
]


def load_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def export_to_duckdb(db_path: Path = DB_PATH):
    """Load all parquet files into DuckDB database."""
    db_path = Path(db_path)
    if db_path.exists():
        db_path.unlink()

    con = duckdb.connect(str(db_path))

    for table_name, parquet_path in PARQUET_TABLES.items():
        if parquet_path.exists():
            con.execute(
                f"""
                CREATE TABLE {table_name} AS
                SELECT * FROM read_parquet('{parquet_path.as_posix()}')
                """
            )
            row_count = con.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
            print(f"  {table_name}: {row_count} rows")

    print(f"\nDatabase: {db_path}")

    return con


def run_validation_queries(con, queries=None, save_dir: Path | None = None):
    """Execute versioned SQL validation queries, print results, and optionally save outputs."""
    queries = VALIDATION_QUERIES if queries is None else queries
    if save_dir is not None:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
    print("\n=== VALIDATION QUERIES ===")
    for name, sql_ref in queries:
        sql = load_sql(sql_ref) if isinstance(sql_ref, Path) else str(sql_ref)
        print(f"\n--- {name} ---")
        rel = con.execute(sql)
        df = rel.fetchdf()
        print(df.to_string(index=False))
        if save_dir is not None and isinstance(sql_ref, Path):
            out = save_dir / f"{sql_ref.stem}.csv"
            df.to_csv(out, index=False)
            print(f"  -> saved: {out}")


if __name__ == "__main__":
    print("Exporting to DuckDB...")
    con = export_to_duckdb()
    run_validation_queries(con, save_dir=RESULTS_DIR)
    con.close()
    print(f"\nResults saved to: {RESULTS_DIR}")
