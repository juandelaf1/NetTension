# SQL (KPI y validación)

Consultas versionadas y auditables ejecutadas sobre `data/processed/net_tension.duckdb` (tablas cargadas desde los parquets del pipeline).

| Archivo | Hipótesis/Propósito | Inputs principales |
|---|---|---|
| `01_scissors_effect_h1.sql` | H1 Scissors Effect (tráfico vs ingresos) | `fact_observed_agg` |
| `02_hhi_trend_h2.sql` | H2 Concentración de mercado (HHI) | `kpi_hhi` |
| `03_nsi_vs_arpu_h4.sql` | H4 Network Stress (NSI vs revenue/line) | `fact_observed_agg` |
| `04_macro_context_h5.sql` | H5 Peso macro telecom/GDP | `fact_eurostat_es`, `fact_observed_agg` |
| `05_operator_groups.sql` | Resumen dimensión operadores | `dim_operator` |
| `06_service_categories.sql` | Resumen dimensión servicios | `dim_service` |

**Ejecución:** `python -m src.pipeline.export_duckdb` (carga parquets en DuckDB y ejecuta estas consultas) o mediante las utilidades del pipeline. Las consultas están alineadas con las definiciones de KPIs/hipótesis documentadas en el proyecto.
