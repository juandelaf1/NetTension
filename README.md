# NetTension

EU telecom network stress simulation validating 5/6 hypotheses on market dynamics.

[Full Case Study](https://juandelaf1.github.io/projects/net-tension)

## Overview

NetTension analyzes competitive dynamics in EU/Spain telecom markets under demand and revenue pressure scenarios. Built on public CNMC (and Eurostat) data, it evaluates six hypotheses about market concentration, pricing pressure, and infrastructure/network stress with explicit data provenance.

## Key Results

- **5/6 hypotheses** confirmed through data analysis (illustrative/simulation-based framing where applicable).
- **+127% traffic CAGR** vs **-0.4% revenue CAGR** (price/revenue compression signal).
- Public data sources (e.g., CNMC, Eurostat/European Commission) with traceable processing.
- **Interactive Streamlit dashboard** for exploration, supported by reproducible ETL outputs.

## Stack

Python · Pandas · DuckDB · Streamlit · SQL · Docker · CNMC/Eurostat data

## Reproducibility & Evidence

- **ETL / outputs:** reproducible pipeline producing processed datasets (e.g. Parquet/DuckDB) for analysis and dashboard use.
- **Versioned SQL:** auditable KPI/validation queries in [`sql/`](sql/) executed against `data/processed/net_tension.duckdb` (see [`sql/README.md`](sql/README.md)). Run via `python -m src.pipeline.export_duckdb`.
- **Data quality:** processed-data checks in `src/quality/data_quality.py` generate reports in [`reports/quality/`](reports/quality/) (also integrated at the end of the ETL when outputs are available). Example: `python -m src.quality.data_quality`.
- **Results & visualization registry:** exported KPI results in [`reports/results/`](reports/results/) and evidence/metadata for key Streamlit views in [`docs/visualizations/`](docs/visualizations/) (see [`docs/visualizations/README.md`](docs/visualizations/README.md)).

## Limitations

- Simulation/scenario outputs are illustrative, not predictive of market outcomes.
- Primarily based on Spanish telecom market data (CNMC) and selected macro sources.
- Does not model regulatory policy changes, mergers, or all real-world market effects.

---

*Full case study with hypothesis testing methodology and scenario definitions: [juandelaf1.github.io/projects/net-tension](https://juandelaf1.github.io/projects/net-tension)*
