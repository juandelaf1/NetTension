# NetTension

Traceable analysis of traffic/revenue dynamics and network-stress hypotheses in the telecom context (Spain/EU), with a reproducible ETL pipeline, versioned SQL checks, data-quality reports, and an interactive Streamlit dashboard.

[Full Case Study (portfolio)](https://juandelaf1.github.io/projects/net-tension)

## Purpose
Evaluate predefined hypotheses on telecom market dynamics (e.g. traffic vs revenue pressure, concentration, stress indicators) using public data with explicit provenance, reproducible processing, and inspectable outputs.

## Overview
NetTension analyzes public CNMC (and selected Eurostat) data through an ETL and KPI workflow. Results are exposed as processed datasets, SQL query outputs, quality reports, and a Streamlit application for interactive exploration.

## Key results (from project analysis)
- **5/6 hypotheses** confirmed in the project analysis (with documented methodology/assumptions in case study).
- **+127% traffic CAGR** vs **-0.4% revenue CAGR** observed in the analyzed series (illustrative of pressure/compression dynamics).
- Outputs are backed by reproducible artifacts (processed data, SQL results, quality reports).

> Scenario/simulation-style interpretations are **illustrative**, not predictive.

## Stack
- **Language/analysis:** Python, Pandas
- **Data/queries:** DuckDB, SQL (`sql/`)
- **Visualization:** Streamlit (`streamlit_app/`)
- **Packaging/ops:** Docker (ETL image), GitHub Actions CI
- **Data sources:** Public CNMC/Eurostat datasets (attribution applies)

## How to run / validate

### Prerequisites
- Python 3.10+ (CI uses 3.11)
- Source data available as expected by the pipeline/config (see `data/SOURCES.yaml` and project docs)

### Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements-prod.txt
pip install -r requirements-test.txt  # optional, for tests
```

### Run
```bash
# ETL (generates processed outputs; may run quality checks when outputs are available)
python -m src.pipeline.etl_pipeline

# Export DuckDB + execute versioned SQL and produce result artifacts
python -m src.pipeline.export_duckdb

# Data quality report (explicit)
python -m src.quality.data_quality

# Streamlit dashboard
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

### Validate
```bash
python -m pytest tests/ -q
```

## Repository structure (high level)
- `src/` — ETL, loaders, transforms, KPI engine, quality checks, pipeline/export utilities
- `sql/` — versioned KPI/validation SQL queries (auditable)
- `streamlit_app/` — Streamlit dashboard
- `data/` — data configuration/sources metadata (e.g. `SOURCES.yaml`); raw/processed data handling per project setup
- `reports/quality/` — data quality reports
- `reports/results/` — exported SQL/KPI result tables
- `docs/visualizations/` — visualization/results registry and capture guidance
- `tests/` — automated tests (e.g. KPI engine)
- `.github/workflows/ci.yml` — CI (lint/checks, data YAML validation, tests)

## Reproducibility & evidence
- **Versioned SQL:** `sql/` executed against `data/processed/net_tension.duckdb` (see `sql/README.md`).
- **Data quality:** `src/quality/data_quality.py` → `reports/quality/data_quality_report.(json|md)`.
- **Results:** exported KPI outputs in `reports/results/`.
- **Visualization registry:** `docs/visualizations/` (includes capture guide/log template for reproducible Streamlit evidence).

## Limitations
- Scenario/simulation outputs are **illustrative, not predictive** of market outcomes.
- Primarily focused on Spanish telecom market data (CNMC) plus selected macro sources.
- Does not model regulatory policy changes, mergers, or all real-world market effects.
- Data availability/coverage depends on source datasets and local pipeline inputs.

## Status, license & attribution
- **Status:** portfolio/analysis project with reproducible pipeline artifacts and dashboard; not presented as a production market-prediction system.
- **License:** no explicit `LICENSE` file is present in this repository at the time of writing. Code/data usage should respect original source terms.
- **Data attribution:** CNMC and Eurostat (and any other sources referenced in `data/SOURCES.yaml`/docs) retain their original licenses and attribution requirements.

## Documentation
- Technical case study: [docs/case-study.md](docs/case-study.md)
- Visualization evidence registry: [docs/visualizations/README.md](docs/visualizations/README.md)
- Portfolio case study: https://juandelaf1.github.io/projects/net-tension
