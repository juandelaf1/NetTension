"""
NetTension — Export consolidated datasets to DuckDB.

Creates net_tension.duckdb with all processed parquet files as SQL tables.
Power BI can connect via DuckDB ODBC driver for SQL-based queries.
"""
import duckdb
from pathlib import Path

PROC = Path(__file__).parents[2] / "data" / "processed"
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


def export_to_duckdb():
    """Load all parquet files into DuckDB database."""
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = duckdb.connect(str(DB_PATH))

    for table_name, parquet_path in PARQUET_TABLES.items():
        if parquet_path.exists():
            con.execute(f"""
                CREATE TABLE {table_name} AS
                SELECT * FROM read_parquet('{parquet_path.as_posix()}')
            """)
            row_count = con.execute(f"SELECT count(*) FROM {table_name}").fetchone()[0]
            print(f"  {table_name}: {row_count} rows")

    print(f"\nDatabase: {DB_PATH}")

    return con


def run_validation_queries(con):
    """Demonstrate SQL analytics capabilities on the DuckDB database."""
    queries = {
        "Scissors Effect (H1)": """
            SELECT year, quarter,
                   data_traffic_index, revenue_index,
                   (data_traffic_index - revenue_index) AS scissors_gap
            FROM fact_observed_agg
            WHERE year IN (2005, 2010, 2015, 2020, 2025)
            ORDER BY year, quarter
        """,
        "HHI Trend (H2)": """
            SELECT year,
                   round(avg(hhi), 0)::INT AS avg_hhi,
                   classification
            FROM kpi_hhi
            WHERE year IN (2005, 2010, 2015, 2020, 2025)
            GROUP BY year, classification
            ORDER BY year
        """,
        "NSI vs ARPU (H4)": """
            SELECT year, quarter,
                   round(nsi, 0)::INT AS nsi,
                   round(revenue_per_line, 2) AS revenue_per_line
            FROM fact_observed_agg
            WHERE year IN (2005, 2010, 2015, 2020, 2025)
            ORDER BY year, quarter
        """,
        "Macro Context (H5)": """
            SELECT f.year, f.population, f.gdp_meur,
                   round(f.gdp_per_capita, 0)::INT AS gdp_per_capita,
                   round(o.revenue / (f.gdp_meur * 1e6) * 100, 2) AS telecom_gdp_share
            FROM fact_eurostat_es f
            JOIN (
                SELECT year, avg(revenue) AS revenue
                FROM fact_observed_agg
                GROUP BY year
            ) o ON f.year = o.year
            WHERE f.year IN (2005, 2010, 2015, 2020, 2025)
            ORDER BY f.year
        """,
        "Operator Count by Group": """
            SELECT operator_group, count(*) AS num_operators
            FROM dim_operator
            GROUP BY operator_group
            ORDER BY num_operators DESC
        """,
        "Service Categories": """
            SELECT category, market_type, count(*) AS num_services
            FROM dim_service
            GROUP BY category, market_type
            ORDER BY category, market_type
        """,
    }

    print("\n=== VALIDATION QUERIES ===")
    for name, sql in queries.items():
        print(f"\n--- {name} ---")
        result = con.execute(sql)
        print(result.fetchdf().to_string(index=False))


if __name__ == "__main__":
    print("Exporting to DuckDB...")
    con = export_to_duckdb()
    run_validation_queries(con)
    con.close()
