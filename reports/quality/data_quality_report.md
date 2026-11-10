# Data Quality Report

- Generated (UTC): 2026-11-10T08:48:32.225308+00:00
- Processed dir: `C:\Users\JUAN\Desktop\Proyectos\NetTension\data\processed`
- Status: OK
- Summary: {'pass': 29, 'fail': 0, 'warn': 0, 'skip': 0}

| Check | Status | Detail |
|---|---|---|
| exists:fact_observed_agg | pass | found fact_observed_agg.parquet |
| exists:fact_eurostat_es | pass | found fact_eurostat_es.parquet |
| exists:kpi_hhi | pass | found kpi_hhi.parquet |
| exists:kpi_nsi | pass | found kpi_nsi.parquet |
| exists:kpi_elasticity | pass | found kpi_elasticity.parquet |
| exists:dim_time | pass | found dim_time.parquet |
| exists:dim_operator | pass | found dim_operator.parquet |
| exists:dim_service | pass | found dim_service.parquet |
| exists:dim_geography | pass | found dim_geography.parquet |
| exists:cnmc_mercados_clean | pass | found cnmc_mercados_clean.parquet |
| rows:kpi_hhi | pass | 83 rows |
| nulls:kpi_hhi | pass | no nulls in ['hhi'] |
| range:hhi | pass | min=1903.13, max=3537.77 (expected 0..10000) |
| coverage:kpi_hhi | pass | years 2005-2025 |
| rows:kpi_nsi | pass | 83 rows |
| positive:kpi_nsi | pass | non-negative in ['network_stress_index'] |
| coverage:kpi_nsi | pass | years inferred 2005-2025 |
| rows:kpi_elasticity | pass | 83 rows |
| positive:kpi_elasticity | pass | non-negative in ['revenue_per_line', 'traffic_per_line'] |
| coverage:kpi_elasticity | pass | years inferred 2005-2025 |
| rows:fact_observed_agg | pass | 83 rows |
| coverage:fact_observed_agg | pass | years 2005-2025 |
| positive:fact_observed_agg | pass | non-negative in ['revenue'] |
| rows:fact_eurostat_es | pass | 66 rows |
| coverage:fact_eurostat_es | pass | years 1960-2025 |
| rows:dim_time | pass | 83 rows |
| rows:dim_operator | pass | 32 rows |
| rows:dim_service | pass | 38 rows |
| rows:dim_geography | pass | 1 rows |
