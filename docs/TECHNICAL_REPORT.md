# NetTension — Technical Report

> **Network Stress Simulation Framework for European Telecommunications**
>
> Prepared: June 2026 | Author: Juan de la Fuente
> Tags: `v0.1.0` · `v1.0.0` · `v1.1.0`
> Repository: [github.com/juandelaf1/NetTension](https://github.com/juandelaf1/NetTension)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Business Problem](#2-business-problem)
3. [Hypotheses and Results](#3-hypotheses-and-results)
4. [Architecture](#4-architecture)
5. [Technology Stack](#5-technology-stack)
6. [Data Model](#6-data-model)
7. [ETL Pipeline](#7-etl-pipeline)
8. [Streamlit Dashboard](#8-streamlit-dashboard)
9. [Data Governance](#9-data-governance)
10. [Testing and CI/CD](#10-testing-and-cicd)
11. [Deployment](#11-deployment)
12. [Strategic Opportunities](#12-strategic-opportunities)
13. [Limitations and Risks](#13-limitations-and-risks)

---

## 1. Executive Summary

**NetTension** is an interactive executive dashboard and data science project that analyzes the structural decoupling between exponential data traffic growth and flat/declining revenues in European telecommunications. Using 20 years of observed regulatory data from CNMC (Spain) and macroeconomic data from Eurostat, it tests 6 scientific hypotheses about the sector's sustainability.

**Development timeline:** ~8 intensive days (June 11–18, 2026)  
**Purpose:** Module II — Data Analysis & Visualization, ThePower Business School  
**Status:** v1.1.0 — Production-ready Streamlit dashboard with bilingual (ES/EN) support, Docker deployment, CI/CD, and Kaggle dataset publication.

### Key Findings

| Metric | Value |
|--------|-------|
| Data Traffic CAGR (2005–2025) | **+127% / year** |
| Revenue CAGR | **−0.4% / year** |
| Scissors Gap | **127.4 percentage points** |
| HHI (2005 → 2025) | **3,482 → 2,368** (−1,114 pts) |
| ARPU decline | **−83%** |
| Telecom GDP share | **3.2% → 2.0%** |

### Most Important Insight

**Hypothesis H2 (Market Concentration) was REFUTED.** HHI decreased by 1,114 points — more competition, not less — yet the Scissors Effect worsened. This proves the problem is a **structural utility model failure**, not a market power issue. Operators have exhausted survival mechanisms (OPEX reduction, asset monetization, network sharing). ROCE < WACC confirms infrastructure investment in Europe destroys shareholder value.

---

## 2. Business Problem

European telecommunications operators face an accelerating structural crisis:

- **Traffic explosion:** +127% CAGR in data traffic driven by video streaming, social media, cloud services, and IoT
- **Revenue stagnation:** −0.4% CAGR as ARPU has collapsed by 83% over 20 years
- **Investment gap:** ROCE (5.9%) has been below WACC (~8%) since 2018, meaning every euro invested in network infrastructure destroys economic value
- **Exhausted survival mechanisms:** Operators have survived through OPEX automation, copper-to-fiber migration, tower sales (sale & leaseback to Cellnex), and network sharing — all reaching physical limits
- **Regulatory crossroads:** The Fair Share debate (should OTT platforms contribute to network costs?) is central to EU digital policy

### Stakeholders

- European Commission (DG CONNECT)
- National Regulatory Authorities (CNMC, Ofcom, Arcep, BNetzA, AGCOM)
- Telecom operators (Telefónica, Vodafone, Orange, MasMovil, etc.)
- OTT platforms (Google, Meta, Netflix, Amazon, Apple, Microsoft)
- Investors and private equity
- Policy researchers and academics

### Key Questions Addressed

1. Is the Scissors Effect (traffic vs revenue divergence) real and measurable?
2. Is market concentration the cause, or is the problem structural?
3. Does data granularity matter? (CNMC microdata vs Eurostat aggregates)
4. Is Fair Share regulation a viable policy lever?
5. Can the Fair Share simulator quantify the investment gap?

---

## 3. Hypotheses and Results

Six falsifiable hypotheses were formulated and tested against observed data (2005–2025, Spain). Zero simulated or synthetic data was used.

| # | Hypothesis | Prediction | Method | Result |
|---|-----------|-----------|--------|--------|
| **H1** | **Scissors Effect** | Traffic CAGR >> Revenue CAGR, creating a widening gap | CAGR over 83 quarters (CNMC `trafico_de_datos`, `ingresos`) | ✅ **CONFIRMED** |
| **H2** | **Market Concentration** | HHI increases as operators consolidate | HHI per quarter using operator-level revenue | ❌ **REFUTED** (key finding) |
| **H3** | **Data Asymmetry** | Revenue per traffic unit collapses | Revenue_per_traffic and ARPU trend analysis | ✅ **CONFIRMED** |
| **H4** | **Network Stress** | Traffic per line grows faster than revenue per line | Network Stress Index = traffic / active lines | ✅ **CONFIRMED** |
| **H5** | **Macro Decline** | Telecom revenue share of GDP decreases | Revenue / GDP ratio (CNMC + Eurostat `nama_10_gdp`) | ✅ **CONFIRMED** |
| **H6** | **Infrastructure Elasticity** | Margin between transport cost and revenue compresses | Revenue_per_line vs traffic_per_line elasticity | ✅ **CONFIRMED** |

### H1 — Scissors Effect: CONFIRMED

| Metric | Value |
|--------|-------|
| Data Traffic CAGR | **+127% / year** (2005–2025) |
| Revenue CAGR | **−0.4% / year** |
| Scissors Gap | **127.4 percentage points** |
| Implication | Exponential divergence confirms structural business model stress |

### H2 — Market Concentration: REFUTED (unexpected finding)

| Metric | Value |
|--------|-------|
| HHI (2005) | **3,482** — Highly Concentrated |
| HHI (2025) | **2,368** — Moderately Concentrated |
| Change | **−1,114 points** (deconcentration) |
| Implication | **Competition increased** yet the Scissors Effect worsened. The problem is **structural, not monopolistic**. This is the foundational insight: neither monopoly nor competition resolves the traffic/revenue asymmetry. |

### H3 — Data Asymmetry: CONFIRMED

Revenue per data unit collapsed as usage exploded. The gap between what users pay and what they consume continues widening.

### H4 — Network Stress: CONFIRMED

Network Stress Index (traffic per active line) grew exponentially while ARPU declined, confirming unprecedented node saturation. The proprietary NSI metric reached 0.0810 in 2025, indicating maximum utilization relative to installed throughput.

### H5 — Macro Decline: CONFIRMED

Telecom revenue as a share of Spanish GDP decreased from 3.2% to 2.0% over 20 years, indicating the sector is shrinking relative to the broader economy.

### H6 — Infrastructure Elasticity: CONFIRMED

| Metric | Value |
|--------|-------|
| Revenue per line | **−83%** |
| Traffic per line | **+exponential** |
| Implication | Margin compression confirms the elasticity hypothesis. Operators cannot convert traffic growth into revenue growth. |

### Summary

```
H1  (Scissors Effect)        CONFIRMED    Traffic +127%/yr vs Revenue −0.4%/yr
H2  (Concentration)          REFUTED      HHI 3,482 → 2,368 (more competition)
H3  (Data Asymmetry)         CONFIRMED    Revenue per unit collapses
H4  (Network Stress)         CONFIRMED    Traffic per line diverges from ARPU
H5  (Macro Decline)          CONFIRMED    Telecom GDP share: 3.2% → 2.0%
H6  (Infrastructure Elastic) CONFIRMED    Margin compression confirmed
```

---

## 4. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER (raw)                        │
│  CNMC Mercados (5 CSVs)   │   Eurostat (2 TSV.GZ)            │
│  41,937 rows · 49 cols    │   3M+ rows · 8-9 cols            │
│  ETNO/GSMA/BEREC/Sandvine │   PDFs (5 reports)               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    ETL PIPELINE (Python)                      │
│                                                              │
│  ┌──────────┐   ┌──────────────┐   ┌──────────────────────┐ │
│  │ loader/  │──▶│ transform/   │──▶│  pipeline/            │ │
│  │ cnmc     │   │ data_cleaner │   │  etl_pipeline.py     │ │
│  │ eurostat │   │ kpi_engine   │   │  export_powerbi.py   │ │
│  └──────────┘   └──────────────┘   │  export_duckdb.py    │ │
│                                    └──┬───────────────────┘ │
│                        ┌──────────────┴──────────────┐       │
│                        ▼                             ▼       │
│               ┌────────────────┐          ┌────────────────┐ │
│               │ 14 .parquet    │          │ net_tension    │ │
│               │ (star schema)  │          │ .duckdb (SQL)  │ │
│               └────────────────┘          └────────────────┘ │
└──────────────────────────────────────┬───────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   DASHBOARD LAYER (Streamlit)                 │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Page 1: Market Overview  (Scissors Effect, KPIs)      │  │
│  │  Page 2: Network Stress   (NSI, HHI, Elasticity)       │  │
│  │  Page 3: European Context (EU vs USA vs Asia)          │  │
│  │  Page 4: Fair Share What-If (Scenario Simulator)       │  │
│  │  Page 5: Evolution & Strategy                          │  │
│  │  Page 6: About (Governance, Methodology)               │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                              │
│  ▼ Run: streamlit run streamlit_app/app.py                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Technology Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Language** | Python | 3.11 | ETL pipeline + dashboard |
| **Data Processing** | Pandas | 3.0 | Tabular transformations |
| **Numeric Computation** | NumPy | 2.4 | Vectorized KPI calculations |
| **SQL Engine** | DuckDB | 1.5+ | Embedded analytical SQL |
| **Dashboard** | Streamlit | 1.35+ | Interactive web app |
| **Charts** | streamlit-echarts (ECharts) | — | High-performance interactive charts |
| **Charts** | Plotly | 5.18+ | Animated scatter, bar charts |
| **Tables** | streamlit-aggrid (AG Grid) | — | Professional data tables |
| **Navigation** | streamlit-option-menu | — | Sidebar menu |
| **PDF Extraction** | PyMuPDF (fitz) | — | ETNO/GSMA/BEREC/Sandvine reports |
| **QR Code** | qrcode + Pillow | — | GitHub link QR |
| **Config** | PyYAML | — | `data/SOURCES.yaml` governance catalog |
| **Serialization** | Parquet | — | Columnar data storage |
| **Container** | Docker / Docker Compose | 27+ | ETL + dashboard containers |
| **CI/CD** | GitHub Actions | — | Lint + test + validate |
| **Cloud** | Streamlit Community Cloud | — | Public dashboard deployment |
| **Registry** | Docker Hub | — | `juandelaf/net-tension-etl` |
| **Testing** | pytest + pytest-cov | 7+ | Unit tests |
| **Linting** | black + flake8 + mypy | — | Code quality |
| **Packaging** | Hatchling / setuptools | — | Python package build |

### Dependencies

**ETL pipeline** (4 packages): `pandas`, `numpy`, `python-dotenv`, `duckdb`  
**Streamlit dashboard** (14 packages): adds `streamlit`, `plotly`, `streamlit-echarts`, `streamlit-aggrid`, `streamlit-option-menu`, `streamlit-antd-components`, `qrcode`, `pillow`, `openpyxl`, `pyyaml`  
**Test** (2 packages): `pytest`, `pytest-cov`

**Total:** ~18 unique packages (excluding Python standard library).

---

## 6. Data Model

### Star Schema

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

### Data Sources Inventory

| Source | Type | Rows | Coverage | Governance Layer |
|--------|------|------|----------|-----------------|
| CNMC Mercados (5 files) | Regulatory CSV | 41,937 | Spain, 2005T1–2025T4 | OBSERVED |
| CNMC Datos Generales | Regulatory CSV | 3,319 | Spain, 2005T1–2025T4 | OBSERVED |
| Eurostat demo_pjan | Statistical TSV.GZ | 1,171,170 | EU27+, 1960–2025 | OBSERVED |
| Eurostat nama_10_gdp | Statistical TSV.GZ | 1,861,806 | EU27+, 1975–2025 | OBSERVED |
| ETNO State of Digital Comms 2025 | Industry PDF | Extracted | Europe, 2015–2024 | OBSERVED |
| GSMA Mobile Economy Europe 2025 | Industry PDF | Extracted | Europe, 2023–2030 | OBSERVED |
| GSMA Mobile Economy Global 2026 | Industry PDF | Extracted | Global, 2024–2030 | OBSERVED |
| BEREC IP Interconnection 2025 | Regulatory PDF | Extracted | EU27, 2017–2023 | OBSERVED |
| Sandvine GIPR 2024 | Vendor PDF | Extracted | Global, 2024 | OBSERVED |

### Database Tables (DuckDB / Parquet)

| Table | Source | Rows | Description |
|-------|--------|------|-------------|
| `fact_observed_agg` | CNMC Mercados | 83 | Quarterly aggregated metrics |
| `fact_eurostat_es` | Eurostat | 66 | Spain GDP + population |
| `kpi_hhi` | CNMC Mercados | 83 | HHI per quarter |
| `kpi_nsi` | CNMC Mercados | 83 | Network Stress Index |
| `kpi_elasticity` | CNMC Mercados | 83 | Infrastructure Elasticity |
| `dim_time` | Generated | 83 | Quarter dimension |
| `dim_operator` | CNMC | 31 | Operator references |
| `dim_service` | CNMC | varies | Service/concept combinations |
| `dim_geography` | Generated | 1 | Country dimension |
| `dim_eu_context` | PDF reports | 21 | EU benchmark indicators |
| `cnmc_mercados_clean` | CNMC | ~42K | Full cleaned data |
| `cnmc_datos_generales_clean` | CNMC | ~3.3K | Full cleaned datos generales |
| `eurostat_demo_pjan_tidy` | Eurostat | ~1.17M | Population data |
| `eurostat_nama_10_gdp_tidy` | Eurostat | ~1.86M | GDP data |

---

## 7. ETL Pipeline

The pipeline is executed by `python -m src.pipeline.etl_pipeline` and runs in **4 sequential layers**.

### Layer 1: CNMC Mercados Loader

| File | Rows | Period |
|------|------|--------|
| `cnmc_mercados_2005_2009.csv` | 7,809 | 2005–2009 |
| `cnmc_mercados_2010_2014.csv` | 10,397 | 2010–2014 |
| `cnmc_mercados_2015_2019.csv` | 10,807 | 2015–2019 |
| `cnmc_mercados_2020_2024.csv` | 10,900 | 2020–2024 |
| `cnmc_mercados_2025T1_2025T4.csv` | 2,024 | 2025 |
| **Total** | **41,937** | **2005–2025** |

All 5 files share an identical 49-column schema and are auto-concatenated.

### Layer 2: CNMC Datos Generales Loader

Single-file loader (3,319 rows, 14 columns) covering revenue by operator, employees, and bundled services. ISO-8859-1 encoded with semicolon delimiter.

### Layer 3: Eurostat Loader

Parses SDMX-TSV compact format (dimensions as rows, years as columns) into tidy (long) DataFrames:

- `demo_pjan`: Population by age/sex/country → 1.17M rows
- `nama_10_gdp`: GDP by country/indicator → 1.86M rows

### Layer 4: KPI Computation

All KPIs computed by `src/transform/kpi_engine.py`:

- `hhi_quarterly()`: Herfindahl-Hirschman Index
- `network_stress_index()`: Traffic per active line
- `infrastructure_elasticity_margin()`: Revenue per traffic unit
- `traffic_vs_revenue_cagr()`: Scissors Gap
- `macro_contribution_ratio()`: Telecom revenue / GDP
- `digital_density_margin()`: Active lines / population

### Post-Pipeline Exports

1. **Parquet export** (`export_powerbi.py`): 7 fact/dimension tables + star schema
2. **DuckDB export** (`export_duckdb.py`): SQL database with 6 validation queries
3. **PDF extraction** (`extract_pdf_data.py`): Key metrics from 5 industry reports
4. **Data quality audit** (`data_audit.py`): Row counts, nulls, period coverage
5. **Data profiling** (`data_profile.py`): Concept discovery, traffic decomposition

---

## 8. Streamlit Dashboard

### Pages

| Page | File | Key Visualizations |
|------|------|-------------------|
| Market Overview | `views/market_overview.py` | Scissors Effect line chart, 4 KPI cards with sparklines |
| Network Stress | `views/network_stress.py` | HHI with concentration bands, animated NSI vs ARPU scatter |
| European Context | `views/european_context.py` | EU vs World CAPEX/ARPU bars, 5G adoption gauge |
| Fair Share | `views/fair_share.py` | 3-simulator interactive dashboard, dual donut, gauges |
| Evolution & Strategy | `views/evolution_strategy.py` | 4-tab strategic roadmap (Quick Wins, Models, Roadmap, Monetization) |
| About | `views/about.py` | Data governance register, bias disclosure, QR code |

### Features (24 implemented)

1. Bilingual UI (ES/EN) with instant switching via sidebar radio button
2. 6 narrative-driven dashboard pages
3. Scissors Effect visualization (traffic index vs revenue index, ECharts)
4. 4 KPI cards with sparklines, delta indicators, and color-coded borders
5. HHI concentration analysis with regulatory threshold bands (DOJ/FTC)
6. Network Stress Index (NSI) proprietary logarithmic metric
7. Animated scatter plot (NSI vs ARPU by year, Plotly)
8. EU vs World comparison (CAPEX/ARPU normalized to EU=100%)
9. 5G adoption gauge (ECharts)
10. Fair Share policy simulator with 3 adjustable parameters
11. Before/after scenario gauges (ECharts)
12. OTT traffic composition dual concentric donut
13. 3-scenario comparison table (Baseline / OTT only / OTT + CAPEX)
14. Evolution & Strategy roadmap with 4 tabs
15. 7 new hypotheses (H7-H10) proposed
16. Data governance register with filterable AG Grid table
17. 7 documented biases with severity and mitigation
18. Click-to-learn popups on all 12 charts
19. CSV download per page
20. Dark corporate theme with custom CSS (306 lines)
21. Sidebar filters (year range, simulation parameters)
22. QR code linking to GitHub repository
23. Multi-engine chart rendering (ECharts + Plotly)
24. Docker + Streamlit Cloud deployment ready

### Component Architecture

```
streamlit_app/
├── app.py                  ─── Entry point, navigation, i18n init
├── views/                  ─── Page render functions
│   ├── market_overview.py  ─── Scissors Effect, KPIs
│   ├── network_stress.py   ─── HHI, NSI, Elasticity
│   ├── european_context.py ─── EU benchmarks
│   ├── fair_share.py       ─── What-If simulator
│   ├── evolution_strategy.py ── Strategic roadmap
│   └── about.py            ─── Governance, biases
├── components/             ─── Reusable UI components
│   ├── charts.py           ─── ECharts + Plotly with corporate template
│   ├── kpi_card.py         ─── KPI card renderer
│   ├── filters.py          ─── Sidebar filters and sliders
│   ├── tables.py           ─── AG Grid table renderer
│   └── explain_popup.py    ─── Educational popups (12 charts)
├── utils/                  ─── Data logic
│   ├── data_loader.py      ─── Cached data loading (DuckDB/Parquet)
│   ├── calculations.py     ─── Fair Share and NSI business logic
│   ├── export.py           ─── CSV download helper
│   └── i18n.py             ─── ES/EN translations (410+ lines)
└── assets/style.css        ─── Corporate dark theme
```

---

## 9. Data Governance

### 4-Tier Classification (DEC-007)

| Layer | Description | Example | Confidence |
|-------|------------|---------|------------|
| `OBSERVED` | Directly from official source | CNMC revenue, Eurostat GDP | HIGH |
| `ESTIMATED` | Derived from observed variables | HHI, CAGR, NSI | MEDIUM–HIGH |
| `POLICY_MODEL` | Scenario under regulatory assumptions | Fair Share impact | LOW |
| `CONSTANT` | Fixed documented parameters | HHI thresholds (1000/2500) | HIGH |

### Governance Metadata per Variable (DEC-008)

Each variable in the model is documented with:
- `Governance_Layer`
- `Confidence_Level` (HIGH / MEDIUM / LOW)
- `Review_Date` and `Review_Owner`
- `Source_Type` (PUBLIC_REGULATOR / PUBLIC_STATISTICAL / INDUSTRY_ASSOCIATION / DERIVED / SCENARIO_MODEL / FIXED_PARAMETER)
- `Reproducible` (TRUE / PARTIAL)
- `Documentation_Reference` (file path or URL)

Full catalog in `data/SOURCES.yaml` (428 lines).

### Documented Biases

| Bias | Severity | Mitigation |
|------|----------|------------|
| Survivorship bias (operators who left market) | High | Include historical operators in `dim_operator` with `active=False` |
| CNMC methodology changes (2005 vs 2025) | High | Document changes in SOURCES.yaml per period |
| Reverse causality (investment → traffic) | Medium | Granger causality test with lags |
| COVID contamination (2020 Q2–Q3) | Medium | Dummy variable + robustness test without 2020 |
| Spain-only as EU proxy | Low | Next phase: multi-country expansion |

---

## 10. Testing and CI/CD

### Unit Tests

**`tests/test_kpi_engine.py`** — 7 tests covering:
- Perfect monopoly (HHI = 10,000)
- Equal market split (HHI = 3,333)
- Empty DataFrame handling
- NaN value filtering
- Multi-quarter HHI computation
- CAGR formula validation
- HHI classification boundaries

Run via:
```bash
pytest tests/ -v
```

### CI Pipeline (`.github/workflows/ci.yml`)

3 parallel jobs on push to master/develop and PR to master:

1. **lint**: `black --check src/ streamlit_app/ tests/` + `flake8 src/ streamlit_app/ tests/`
2. **validate-data**: YAML syntax check on `data/SOURCES.yaml`
3. **test**: `pytest tests/ -v --cov=src/ --cov-report=term-missing`

### Docker Build-Time Validation

The Dockerfile runs pytest during build:
```dockerfile
RUN python -m pytest tests/ -v
```

---

## 11. Deployment

### Local Development

```bash
# Clone
git clone https://github.com/juandelaf1/NetTension.git
cd NetTension

# ETL
pip install -r requirements-prod.txt
python -m src.pipeline.etl_pipeline

# Dashboard
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

### Docker

```bash
# Build and run both services
docker compose up --build

# Individual containers
docker build -t net-tension-etl -f Dockerfile .
docker build -t net-tension-dashboard -f Dockerfile.dashboard .
```

### Streamlit Cloud

Deploy directly from GitHub — set the main file path to `streamlit_app/app.py` with `streamlit_app/requirements.txt` as the dependency file.

---

## 12. Strategic Opportunities

### Academic Publication Potential

| Paper | Target Journal | Quartile | Estimated Acceptance |
|-------|---------------|----------|---------------------|
| Scissors Effect in Telecom | Telecommunications Policy | Q1 | 60% |
| H2 Refutation: Structural Problem | Journal of Regulatory Economics | Q1 | 30% |
| Network Stress Index as Synthetic Indicator | IEEE Access | Q2 | 80% |
| Fair Share Elasticity Model | Information Economics & Policy | Q1 | 40% |
| Data Asymmetry: CNMC Micro vs Eurostat Macro | Statistical Journal of the IAOS | Q2 | 50% |
| Dashboard for Policy Makers | Data & Policy | Q2 | 60% |

### Monetization Potential

| Stream | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Consulting (reports) | €15K | €40K | €80K |
| SaaS (NRA licenses) | €0 | €30K | €120K |
| API (developers) | €0 | €5K | €20K |
| Fair Share Calculator | €0 | €0 (lead gen) | €10K (premium) |
| **Total** | **€15K** | **€75K** | **€230K** |

### Consulting Opportunities

| Client | Service | Value Range |
|--------|---------|-------------|
| CNMC / NRA | Extension to more years/markets | €15–30K |
| Telefónica | Competitor benchmarking | €10–20K |
| ETNO / Connect Europe | Fair Share report with own data | €25–50K |
| European Commission (DG CONNECT) | EU network stress study | €50–100K |
| Private equity investors | TELCO market due diligence | €5–15K |
| Consultancies (BCG, McKinsey) | Input for TELCO projects | €3–10K/license |

### 6-Month Roadmap

| Month | Milestone | Owner |
|-------|-----------|-------|
| M1 | Quick Wins (H7–H10 regression, elasticity, voice-data substitution) | Data Scientist |
| M1 | Stable CI/CD, Docker tests | Engineer |
| M2 | Predictive traffic model (Prophet) | Data Scientist |
| M2 | Fair Share Simulator v2 (non-linear) | Economist |
| M3 | Streamlit v2 (multi-country) | Full Stack |
| M3 | First paper: Scissors Effect | Academic |
| M4 | Landing page + Fair Share Calculator | Product |
| M5 | CNMC/ETNO meetings | Consultant |
| M6 | Release v2.0: multi-country + predictive | All |

---

## 13. Limitations and Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Single-country scope (Spain only) | High | Expand to Italy, Portugal, Greece in v2.0 |
| No formal statistical p-values | Medium | Add regression testing with HC3 robust errors |
| CNMC methodology change ~2012 in data traffic | High | Documented in SOURCES.yaml, separate pre/post analysis |
| Fair Share model is intentionally linear | Medium | Documented as POLICY_MODEL, not OBSERVED |
| No direct CAPEX data per operator | Medium | Proxy from ETNO/GSMA benchmarks |
| Sandvine data has proprietary methodology | Medium | Marked as `confidence: MEDIUM`, `reproducible: PARTIAL` |
| Rapid development (~8 days) limits depth | Medium | Expand with structured research phase |
| No external peer review | Medium | Public Kaggle dataset + open source invites review |

---

## References

- README: `README.md`
- Data Sources Catalog: `data/SOURCES.yaml`
- Data Model Specification: `docs/DATA_MODEL.md`
- EDA Summary: `reports/EDA_SUMMARY.md`
- Presentation Script: `docs/PRESENTATION.md`
- Strategic Report: `docs/STRATEGIC_REPORT.md`
- Roadmap: `ROADMAP.md`
