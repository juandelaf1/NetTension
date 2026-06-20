# NetTension — Data Model Specification

Star-schema data model powering the Streamlit dashboard. All data is processed by the Python ETL pipeline (`src/pipeline/etl_pipeline.py`) and persisted as compressed Parquet files + DuckDB SQL database.

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                             │
│  CNMC Mercados (5 CSVs, 41,937 rows)                       │
│  CNMC Datos Generales (1 CSV, 3,319 rows)                  │
│  Eurostat demo_pjan (TSV.GZ, 1.17M rows)                   │
│  Eurostat nama_10_gdp (TSV.GZ, 1.86M rows)                 │
│  ETNO/GSMA/BEREC/Sandvine PDFs (extracted)                 │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                    ETL PIPELINE (Python)                     │
│  Loaders → Cleaners → KPI Engine → Export                   │
│  Output: 14 Parquet files + net_tension.duckdb              │
└──────────────────────────┬─────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────┐
│                  STREAMLIT DASHBOARD                         │
│  data_loader.py (cached via DuckDB/Parquet)                 │
│  → 6 interactive pages (ECharts + Plotly + AG Grid)        │
└────────────────────────────────────────────────────────────┘
```

All Parquet files are in `data/processed/`. The dashboard loads them through `streamlit_app/utils/data_loader.py` using DuckDB's native Parquet scanning or `pandas.read_parquet()`.

---

## Star Schema

```
dim_time ───── fact_observed_agg ───── dim_operator
                │
 dim_geography ─┤
                │
 dim_service ───┘

 fact_eurostat_es ───── dim_time (via year)
 kpi_hhi ────────────── dim_time (via trimestre_dt)
 kpi_nsi
 kpi_elasticity
```

---

## Table Definitions

### Fact Tables

**fact_observed_agg** — Quarterly aggregated CNMC market metrics (83 rows)

| Column | Type | Description |
|--------|------|-------------|
| trimestre_dt | Date | Quarter start (2005-01-01) |
| total_revenue | Float | Total revenue (Mn EUR) |
| total_data_traffic | Float | Total data traffic |
| total_voice_traffic | Float | Total voice traffic (minutes) |
| total_lines | Float | Total active lines |
| traffic_per_line | Float | Data traffic per active line (NSI) |
| revenue_per_line | Float | Revenue per active line |
| revenue_per_traffic | Float | Revenue per data unit |

**fact_eurostat_es** — Spain macroeconomic indicators (66 rows)

| Column | Type | Description |
|--------|------|-------------|
| year | Int | 2005–2025 |
| population | Float | Spain population count |
| gdp_meur | Float | GDP (million EUR, current prices) |
| gdp_per_capita | Float | GDP per capita (EUR) |

### Dimension Tables

**dim_time** — Calendar quarter dimension (83 rows)

| Column | Type | Description |
|--------|------|-------------|
| time_key | Date | First day of quarter |
| year | Int | 2005–2025 |
| quarter | Int | 1–4 |
| year_quarter | String | "2005 Q1" |

**dim_operator** — Telecom operators in Spain (31 operators)

| Column | Type | Description |
|--------|------|-------------|
| operator_key | String | Operator name |
| operator_group | String | Incumbent, Competitor, Wholesale, Regional, Other |
| is_incumbent | Boolean | True if Telefónica/Movistar |

**dim_service** — Service/concept combinations

| Column | Type | Description |
|--------|------|-------------|
| service_key | String | servicio + concepto |
| servicio | String | Retail, Wholesale, etc. |
| concepto | String | Metric name (Ingresos, Traffic, etc.) |
| market_type | String | Minorista / Mayorista |
| category | String | Voice, Data, Access, Audiovisual |

**dim_geography** — Country dimension

| Column | Type | Description |
|--------|------|-------------|
| geography_key | String | Country code (ES) |
| pais | String | Country name |
| geo_code | String | Eurostat code (ES) |

**dim_eu_context** — European benchmark indicators (21 indicators)

| Column | Type | Description |
|--------|------|-------------|
| indicator | String | Metric name (ARPU, CAPEX per capita, etc.) |
| value | Float | Metric value |
| unit | String | EUR, %, etc. |
| source | String | ETNO, GSMA, BEREC, etc. |
| geography | String | Country or region |

### KPI Tables

**kpi_hhi** — Herfindahl-Hirschman Index per quarter (83 rows)

| Column | Type | Description |
|--------|------|-------------|
| trimestre_dt | Date | Quarter |
| hhi | Float | HHI value (0–10000) |
| classification | String | Competitive / Moderate / Concentrated |

**kpi_nsi** — Network Stress Index per quarter (83 rows)

| Column | Type | Description |
|--------|------|-------------|
| trimestre_dt | Date | Quarter |
| nsi | Float | Traffic per active line |

**kpi_elasticity** — Infrastructure Elasticity Margin per quarter (83 rows)

| Column | Type | Description |
|--------|------|-------------|
| trimestre_dt | Date | Quarter |
| revenue_per_traffic | Float | Revenue per data unit |
| revenue_per_line | Float | Revenue per active line |
| traffic_per_line | Float | Traffic per active line |

---

## Key Performance Indicators

All KPIs are pre-computed by `src/transform/kpi_engine.py` during the ETL pipeline run, then stored as Parquet for the dashboard to consume.

| KPI | Formula | Source | Interpretation |
|-----|---------|--------|----------------|
| **HHI** | `Σ(market_share_i)² × 10000` | CNMC Mercados | Concentration: <1000 competitive, 1000–2500 moderate, >2500 concentrated |
| **NSI** | `total_traffic / active_lines` | CNMC Mercados | Network congestion pressure |
| **Infrastructure Elasticity** | `revenue_per_line / traffic_per_line` | CNMC Mercados | Business model sustainability (margin compression) |
| **CAGR** | `(Vₜ/V₀)^(1/t) − 1` | CNMC Mercados | Growth rate over period |
| **CAGR Gap** | `CAGR_traffic − CAGR_revenue` | Derived | Scissors Effect divergence (127.4pp) |
| **Macro Contribution** | `telecom_revenue / GDP` | CNMC + Eurostat | Sector weight in economy |
| **Digital Density** | `active_lines / population × 100` | CNMC + Eurostat | Real per-capita penetration |

---

## Data Governance Layers

Per DEC-007 and DEC-008 compliance (see `data/SOURCES.yaml` for full catalog):

| Layer | Description | Example Variables |
|-------|------------|-------------------|
| `OBSERVED` | Directly from official source | CNMC revenue, Eurostat GDP |
| `ESTIMATED` | Derived from observed data | HHI, CAGR, NSI, Elasticity |
| `POLICY_MODEL` | Scenario under regulatory assumptions | Fair Share impact, CAPEX relief |
| `CONSTANT` | Fixed documented thresholds | HHI threshold (2500), GDP deflator (2%) |

Every variable is documented with: Governance_Layer, Confidence_Level (HIGH/MEDIUM/LOW), Review_Date, Review_Owner, Source_Type, Reproducible (TRUE/PARTIAL), and Documentation_Reference.

---

## Storage

### Parquet files (default)
14 compressed, columnar files in `data/processed/`. Loaded by the dashboard with zero SQL setup:

```python
import pandas as pd
df = pd.read_parquet("data/processed/fact_observed_agg.parquet")
```

### DuckDB SQL database (optional)
`data/processed/net_tension.duckdb` bundles all tables into a portable SQL database with 6 validation queries. Generated by `src/pipeline/export_duckdb.py`.

```python
import duckdb
con = duckdb.connect("data/processed/net_tension.duckdb")
con.sql("SELECT * FROM fact_observed_agg").df()
```

### CSV export (Power BI compatibility)
8 CSV files in `data/csv/` for direct import into external tools. Generated by `src/pipeline/export_powerbi.py`.

### Source data
Raw CSVs (CNMC), TSV.GZ (Eurostat), and PDFs (ETNO, GSMA, BEREC, Sandvine) in `data/raw/`. See `data/SOURCES.yaml` for download links and license information.

---

## Loading in the Dashboard

The Streamlit dashboard (`streamlit_app/`) loads data via `streamlit_app/utils/data_loader.py`:

- DuckDB connection is cached with `@st.cache_resource`
- DataFrame queries are cached with `@st.cache_data(ttl=3600)`
- Falls back to parquet directly if DuckDB is unavailable (Cloud deployment)

```python
# From streamlit_app/utils/data_loader.py
@st.cache_resource
def get_connection():
    return duckdb.connect(str(DB_PATH))

@st.cache_data(ttl=3600)
def load_fact_observed():
    return _load_table("fact_observed_agg")
```
